import asyncio
import json
import os
import redis.asyncio as aioredis
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
import httpx
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

scheduler = AsyncIOScheduler()
redis_client = None


async def init_redis():
    global redis_client
    redis_url = os.getenv("REDIS_URL", "redis://localhost:6379")
    redis_client = await aioredis.from_url(redis_url)
    logger.info("Redis connected")


async def poll_flight(icao24: str, flight_id: str):
    """Poll a single flight from OpenSky Network."""
    async with httpx.AsyncClient(timeout=10.0) as client:
        try:
            resp = await client.get(
                "https://opensky-network.org/api/states/all",
                params={"icao24": icao24},
                auth=(os.getenv("OPENSKY_USER", ""), os.getenv("OPENSKY_PASS", "")),
            )
            if resp.status_code != 200:
                return

            states = resp.json().get("states") or []
            if not states:
                return

            current = states[0]
            last_key = f"flight_state:{flight_id}"
            last_raw = await redis_client.get(last_key)

            current_state = {
                "on_ground": current[8],
                "velocity": current[9],
                "callsign": (current[1] or "").strip(),
                "last_update": current[4],
            }

            if last_raw:
                last_state = json.loads(last_raw)
                await compare_and_emit(flight_id, last_state, current_state)

            await redis_client.setex(last_key, 3600, json.dumps(current_state))
        except Exception as e:
            logger.error(f"Error polling flight {flight_id}: {e}")


async def compare_and_emit(flight_id: str, last_state: dict, current_state: dict):
    """Compare states and emit disruption event if changed."""
    last_callsign = last_state.get("callsign", "")
    current_callsign = current_state.get("callsign", "")

    if last_callsign != current_callsign:
        await emit_disruption(flight_id, "DELAY", 0)
        logger.info(
            f"Flight {flight_id} state changed: {last_callsign} -> {current_callsign}"
        )


async def emit_disruption(flight_id: str, disruption_type: str, delay_minutes: int):
    """Publish a disruption event to Redis Streams."""
    await redis_client.xadd(
        "disruptions",
        {
            "flight_id": flight_id,
            "type": disruption_type,
            "delay_minutes": str(delay_minutes),
            "detected_at": str(int(asyncio.get_event_loop().time())),
        },
    )
    logger.info(f"Disruption emitted for flight {flight_id}: {disruption_type}")


async def disruption_consumer():
    """Consumer for disruption events."""
    try:
        await redis_client.xgroup_create(
            "disruptions", "workers", id="0", mkstream=True
        )
    except Exception:
        pass

    while True:
        try:
            events = await redis_client.xreadgroup(
                "workers",
                "worker-1",
                {"disruptions": ">"},
                count=10,
                block=5000,
            )
            for stream, messages in events or []:
                for msg_id, data in messages:
                    logger.info(f"Processing disruption: {data}")
                    await redis_client.xack("disruptions", "workers", msg_id)
        except Exception as e:
            logger.error(f"Consumer error: {e}")
            await asyncio.sleep(1)


async def register_flight_jobs():
    """Register polling jobs for all active monitored flights."""
    from sqlalchemy import select
    from app.database import async_session_maker
    from models.models import MonitoredFlight

    async with async_session_maker() as session:
        result = await session.execute(
            select(MonitoredFlight).where(MonitoredFlight.status == "SCHEDULED")
        )
        flights = result.scalars().all()

        for f in flights:
            scheduler.add_job(
                poll_flight,
                IntervalTrigger(seconds=60),
                args=[f.icao24, str(f.id)],
                id=f"poll_{f.id}",
                replace_existing=True,
            )
            logger.info(f"Registered polling job for flight {f.flight_no}")


async def main():
    await init_redis()

    scheduler.add_job(
        register_flight_jobs,
        "interval",
        seconds=300,
        id="register_jobs",
    )
    scheduler.start()

    await disruption_consumer()


if __name__ == "__main__":
    asyncio.run(main())

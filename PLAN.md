# PLAN.md — Reroute: Flight Compensation Recovery Agent

> **One-liner:** The first travel agent that acts before the bags stop moving — auto-rebooks flights and files compensation claims the moment disruption hits.

---

## 🎯 Vision

Frequent flyers lose more to disruption than just money — they lose time. Existing claims services show up *after* the damage. Reroute shows up *before* the gate agent finishes the first announcement. By combining real-time monitoring, intelligent rebooking, and automated compensation filing, Reroute turns flight disruption from a crisis into a handled event.

---

## 🧩 Problem

- Airlines are legally required to compensate passengers for qualifying delays, but reject most first-attempt claims
- Existing claims companies take 35% and only engage post-disruption
- Frequent flyers spend 1+ hours on hold rebooking — time more valuable than the missed payout
- No fully integrated solution exists that combines monitoring + rebooking + proactive claims filing

---

## 💡 Solution: Reroute

A real-time flight disruption management platform that:

1. **Monitors** flights using public airline data feeds
2. **Detects** disruptions the moment they occur
3. **Rebooks** instantly based on stored preferences (seat, loyalty program, connection risk)
4. **Files claims** automatically by checking compensation eligibility and assembling documentation
5. **Learns** from outcome data to sharpen which claims succeed by airline, route, and disruption type

---

## 🏗️ Value Ladder

| Tier | Offer | Price | Purpose |
|---|---|---|---|
| Lead Magnet | Travel Compensation Calculator | Free | Acquire & qualify leads |
| Frontend | Basic Monitoring & Alerts | $29/month | Build habit, capture early adopters |
| Core | Auto Rebooking + Claims Filing | $29/month + 25% of successful claims | Primary revenue driver |
| Enterprise | Corporate Travel Desk Integration | $10–$30/user/month + 25% commission | Scale with B2B |

---

## 🗺️ Execution Roadmap

### Phase 1 — MVP (Weeks 1–4): Monitoring + Alerts
- [ ] Connect to OpenSky Network free API for real-time ADS-B flight state data
- [ ] Build disruption detection engine (cancellations, delays, gate changes)
- [ ] Implement user onboarding: store flight itineraries, seat & loyalty preferences
- [ ] Send real-time alerts via email (Resend free tier) and WebSocket (FastAPI + Redis Pub/Sub)
- [ ] Launch **Free Compensation Calculator** as lead magnet on Vercel
- [ ] Deploy to 50–100 beta users (frequent flyer communities, travel subreddits)

### Phase 2 — Rebooking Engine (Weeks 5–10)
- [ ] Build Playwright headless scraper for Google Flights alternatives (zero API cost)
- [ ] Build preference-ranking algorithm: loyalty tier, seat type, connection risk score
- [ ] Implement 1-click rebooking confirmation flow via email / web app
- [ ] A/B test rebooking suggestion UX with PostHog (self-hosted, free)
- [ ] Launch **$29/month** monitoring tier

### Phase 3 — Claims Engine (Weeks 11–20)
- [ ] Map EC 261/2004 compensation rules for EU carriers as JSON rulesets
- [ ] Build modular claims logic (each airline = one JSON row in DB — no code deploy needed)
- [ ] Auto-assemble PDF claim packages using WeasyPrint + Jinja2 templates
- [ ] Integrate e-signature using self-hosted DocuSeal (open source, MIT license)
- [ ] Train scikit-learn classifier on claim outcomes; nightly retrain via APScheduler
- [ ] Launch **Core tier**: $29/month + 25% commission on successful claims

### Phase 4 — B2B Expansion (Months 6–12)
- [ ] Build corporate dashboard: disruption cost visibility, route risk analytics
- [ ] Integrate with Expensify public API and open webhook standards for T&E tools
- [ ] Develop predictive risk scoring: flag high-disruption routes before booking
- [ ] Launch **Enterprise pricing**: $10–$30/user/month + 25% commission
- [ ] Partner with corporate travel management companies (TMCs)

---

## 💰 Revenue Model

| Stream | Structure | Notes |
|---|---|---|
| Individual Subscription | $29/month | Flat monthly fee |
| Corporate Subscription | $10–$30/user/month | Volume-based pricing |
| Claims Commission | 25% of successful payouts | Aligned incentive — paid only on wins |
| Predictive Risk Data | Premium add-on | For corporate travel desks |

**Target ARR Range:** $1M–$10M (per IdeaBrowser analysis, Exceptional opportunity score: 9/10)

---

## 🌍 Go-To-Market Strategy

### Early Adopters
- Frequent flyer forums (FlyerTalk, Reddit r/churning, r/travel)
- LinkedIn targeting: road warriors, sales executives, management consultants
- Travel influencer partnerships for free tool promotion

### Distribution Channels
1. **SEO / Content** — Target high-intent keywords (e.g., "EasyJet flight delay compensation" — 9.9K monthly volume, +1578% growth)
2. **Free Calculator** — Viral acquisition tool; captures email for nurture
3. **B2B Direct Sales** — Target corporate travel managers at mid-size companies
4. **TMC Partnerships** — White-label or integration deals with travel management companies

### Competitive Moat
- Speed of action (pre-disruption vs. post-disruption)
- Outcome learning loop (claims data → smarter filing)
- Loyalty program awareness (rebooking doesn't blow miles status)
- Switching cost from stored preferences and claim history

---

## ⚙️ Full System Architecture

```
┌────────────────────────────────────────────────────────────────────────────┐
│                          DATA INGESTION LAYER                              │
│                                                                            │
│  OpenSky Network REST API ──┐                                              │
│  ADS-B Exchange (free)     ─┼──► Ingestion Worker (Python + APScheduler)  │
│  Airline HTML scraper      ─┘    polls every 60s per monitored flight      │
└────────────────────────────────────────┬───────────────────────────────────┘
                                         │  raw state events
                                         ▼
┌────────────────────────────────────────────────────────────────────────────┐
│                        EVENT PROCESSING LAYER                              │
│                                                                            │
│  Redis Streams ◄── DisruptionEvent {flight_id, type, delay_min, ts}        │
│       │                                                                    │
│       ▼  (consumer groups — each service reads independently)              │
│  ┌─────────────┐   ┌──────────────────┐   ┌─────────────────────────┐     │
│  │  Rebooking  │   │  Claims Engine   │   │  Notification Service   │     │
│  │  Worker     │   │  Worker          │   │  Worker                 │     │
│  └──────┬──────┘   └────────┬─────────┘   └──────────┬──────────────┘     │
└─────────┼────────────────────┼──────────────────────  ┼ ──────────────────┘
          │                    │                         │
          ▼                    ▼                         ▼
  ┌───────────────┐  ┌──────────────────┐   ┌───────────────────────┐
  │  Playwright   │  │  JSON Ruleset    │   │  Resend (email)       │
  │  (Google      │  │  Eligibility     │   │  pywebpush (web push) │
  │  Flights)     │  │  Check           │   │  FastAPI WebSocket    │
  │               │  │  WeasyPrint PDF  │   └───────────────────────┘
  │  Preference   │  │  DocuSeal sign   │
  │  Ranker algo  │  │  Outcome → DB    │
  └───────────────┘  └──────────────────┘
          │                    │
          └──────────┬─────────┘
                     ▼
          ┌─────────────────────┐
          │     PostgreSQL      │
          │  (single source of  │
          │   truth + JSONB     │
          │   ruleset store)    │
          └─────────────────────┘
                     │
                     ▼
          ┌─────────────────────┐
          │  scikit-learn ML    │
          │  nightly retrain    │
          │  (claim predictor)  │
          └─────────────────────┘
                     │
                     ▼
┌────────────────────────────────────────────────────────────────────────────┐
│                      FRONTEND LAYER                                        │
│  Next.js 14 App Router + Tailwind CSS (deployed on Vercel free tier)       │
│  - Dashboard (WebSocket live alerts)                                       │
│  - Onboarding / preferences                                                │
│  - Claims tracker                                                          │
│  - Free compensation calculator (SSR for SEO)                             │
└────────────────────────────────────────────────────────────────────────────┘
```

---

## 🛠️ Deep Tech Stack — Every Layer Explained

### 1. Runtime & Language: Python 3.12 + FastAPI

**Why Python over Node.js or Go:**
Python has the most mature ecosystems for all three of Reroute's core non-trivial concerns — async I/O workers, data scraping, and ML training. The same language handles the polling scheduler (APScheduler), the claims eligibility engine (pure Python logic), the ML retraining pipeline (scikit-learn), and the API server (FastAPI). A solo founder avoids context-switching between runtimes.

**Why FastAPI over Flask or Django:**
FastAPI is built on `asyncio` and Starlette. The system runs tens to hundreds of concurrent polling jobs — one per monitored flight — and must handle WebSocket connections for real-time alerts. Flask is synchronous (WSGI) and serialises requests; under polling load it becomes a bottleneck. Django's ORM, admin, and template layers add overhead with zero benefit here — there is no CMS, no traditional form-posting. FastAPI also generates OpenAPI docs automatically from type hints, keeping API documentation always in sync without extra tooling.

```
fastapi==0.111.0
uvicorn[standard]==0.29.0   # ASGI server, MIT license
pydantic==2.7.0             # request/response validation, MIT license
```

**Cost:** $0 — MIT license, open source.

---

### 2. Data Ingestion: OpenSky Network API + ADS-B Exchange

**Why OpenSky Network:**
OpenSky is a non-profit, community-driven ADS-B receiver network providing a completely free REST API. It exposes real-time aircraft state vectors (position, ground speed, altitude, on-ground flag, squawk code) for all ICAO-registered aircraft globally. The free anonymous tier allows polling every 10 seconds; a free registered account reduces that to 5 seconds. No credit card, no commercial agreement required.

**Endpoints used:**
- `GET /states/all?icao24={icao24}` — current state for one aircraft
- `GET /flights/aircraft?icao24={icao24}&begin={unix}&end={unix}` — historical flight trail, used as evidence in claims
- `GET /flights/departure?airport={icao_airport}&begin={unix}&end={unix}` — all departures from an airport in a window (used for bulk disruption scanning)

**Why ADS-B Exchange as a fallback:**
ADS-B Exchange is fully unfiltered (unlike FlightAware, which scrubs military/private flights) and exposes a public JSON endpoint. It requires no API key. It is used as a secondary source when OpenSky state data is stale or missing.

**Polling architecture (APScheduler):**
Each monitored flight gets an independent async job that fires every 60 seconds. The job fetches the current state, compares it to the last known state stored in Redis, and emits a `DisruptionEvent` to Redis Streams if state has changed materially (delay increased by > 15 minutes, flight moved to cancelled, gate changed).

```python
# workers/poller.py
import httpx
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import redis.asyncio as aioredis

scheduler = AsyncIOScheduler()
redis_client = aioredis.from_url("redis://localhost:6379")

async def poll_flight(icao24: str, flight_id: str):
    async with httpx.AsyncClient(timeout=10.0) as client:
        resp = await client.get(
            "https://opensky-network.org/api/states/all",
            params={"icao24": icao24},
            auth=("username", "password")   # free registered account
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
    }

    if last_raw:
        last_state = json.loads(last_raw)
        await compare_and_emit(flight_id, last_state, current_state)

    await redis_client.setex(last_key, 3600, json.dumps(current_state))

# Register one job per active monitored flight on startup
async def register_flight_jobs():
    flights = await db.fetch_all("SELECT id, icao24 FROM monitored_flights
                                  WHERE status = 'SCHEDULED'")
    for f in flights:
        scheduler.add_job(
            poll_flight, "interval", seconds=60,
            args=[f["icao24"], str(f["id"])],
            id=f"poll_{f['id']}", replace_existing=True
        )
```

**Cost:** $0 — OpenSky free tier. APScheduler is MIT licensed. httpx is BSD licensed.

---

### 3. Message Bus: Redis Streams + Pub/Sub (self-hosted)

**Why Redis Streams over Kafka or RabbitMQ:**
Kafka is operationally heavy — it requires a ZooKeeper ensemble or KRaft cluster, brokers, and topic management. At Reroute's early scale (hundreds of flights, not millions of events/second), Kafka is pure overhead. RabbitMQ is simpler but lacks the persistent, replayable log that Redis Streams provides. Redis Streams is an append-only log with native consumer group support. Each downstream service (rebooking, claims, notifications) maintains its own read cursor and can process at its own pace with at-least-once delivery guarantees.

Redis also doubles as the application cache (flight state snapshots, session tokens, rate-limit counters) — one service handles both concerns.

```python
# workers/disruption_detector.py
import redis.asyncio as aioredis
import json

r = aioredis.from_url("redis://localhost:6379")

async def emit_disruption(flight_id: str, disruption_type: str,
                           delay_minutes: int):
    """Publish a disruption event to Redis Streams."""
    await r.xadd("disruptions", {
        "flight_id": flight_id,
        "type": disruption_type,          # "DELAY" | "CANCEL" | "DIVERT"
        "delay_minutes": str(delay_minutes),
        "detected_at": str(int(time.time()))
    })

# --- Consumer (e.g., rebooking worker) ---
async def start_rebooking_consumer():
    # Create consumer group once
    try:
        await r.xgroup_create("disruptions", "rebooking-workers",
                               id="0", mkstream=True)
    except Exception:
        pass  # group already exists

    while True:
        events = await r.xreadgroup(
            "rebooking-workers", "worker-1",
            {"disruptions": ">"},
            count=10, block=5000
        )
        for stream, messages in (events or []):
            for msg_id, data in messages:
                await handle_rebooking(data)
                await r.xack("disruptions", "rebooking-workers", msg_id)
```

**Redis Pub/Sub** is used for the real-time WebSocket notification path — a lighter fan-out channel where the notifications worker publishes alert payloads keyed per user (`alerts:{user_id}`), and FastAPI WebSocket handlers subscribe and forward to open browser connections.

**Cost:** $0 — Redis is BSD licensed. `redis-py` is MIT licensed.

---

### 4. Primary Database: PostgreSQL 16 (self-hosted via Docker)

**Why PostgreSQL over SQLite or MySQL:**
PostgreSQL handles both OLTP (users, claims, preferences) and lightweight OLAP (claim success rates by carrier/route for ML training) without requiring a separate analytics database at this scale. The `JSONB` column type stores carrier-specific compensation rulesets with full index support — enabling the modular claims engine without a schema migration every time a new carrier is added. PostgreSQL's `asyncpg` driver provides a fully async connection pool that integrates with FastAPI natively.

**Schema (key tables):**

```sql
-- Core user identity
CREATE TABLE users (
    id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email       TEXT UNIQUE NOT NULL,
    created_at  TIMESTAMPTZ DEFAULT now()
);

-- Stored travel preferences per user
CREATE TABLE flight_preferences (
    user_id         UUID PRIMARY KEY REFERENCES users(id) ON DELETE CASCADE,
    loyalty_program TEXT,       -- e.g. "BA Executive Club", "Miles&More"
    seat_preference TEXT,       -- "AISLE" | "WINDOW" | "EXIT_ROW"
    alliance        TEXT,       -- "ONEWORLD" | "STAR" | "SKYTEAM"
    max_connections INT DEFAULT 1,
    updated_at      TIMESTAMPTZ DEFAULT now()
);

-- One row per flight being actively monitored for a user
CREATE TABLE monitored_flights (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id         UUID REFERENCES users(id) ON DELETE CASCADE,
    flight_no       TEXT NOT NULL,        -- "BA234"
    icao24          TEXT,                 -- aircraft hex ID for OpenSky
    dep_airport     CHAR(4) NOT NULL,     -- ICAO code e.g. "EGLL"
    arr_airport     CHAR(4) NOT NULL,
    scheduled_dep   TIMESTAMPTZ NOT NULL,
    status          TEXT DEFAULT 'SCHEDULED',  -- SCHEDULED|DELAYED|CANCELLED|LANDED
    created_at      TIMESTAMPTZ DEFAULT now()
);

-- Immutable log of every disruption event detected
CREATE TABLE disruptions (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    flight_id       UUID REFERENCES monitored_flights(id),
    type            TEXT NOT NULL,    -- "DELAY" | "CANCEL" | "DIVERT"
    delay_minutes   INT,
    cause           TEXT,             -- populated when known: "WEATHER" | "ATC" etc.
    detected_at     TIMESTAMPTZ DEFAULT now(),
    raw_state       JSONB             -- full OpenSky state snapshot (evidence payload)
);

-- Compensation claims lifecycle
CREATE TABLE claims (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    disruption_id   UUID REFERENCES disruptions(id),
    user_id         UUID REFERENCES users(id),
    carrier         CHAR(2) NOT NULL,
    regulation      TEXT NOT NULL,    -- "EC261" | "UK261" | "DOT"
    amount_eur      NUMERIC(8,2),
    status          TEXT DEFAULT 'DRAFT',
        -- DRAFT | SUBMITTED | ACCEPTED | REJECTED | APPEALED | PAID
    submitted_at    TIMESTAMPTZ,
    resolved_at     TIMESTAMPTZ,
    outcome_notes   JSONB,            -- airline's rejection reason, for ML training
    doc_url         TEXT              -- signed PDF URL from DocuSeal
);

-- Carrier compensation rules stored as JSONB — no code deploy to add a carrier
CREATE TABLE carrier_rules (
    carrier_iata    CHAR(2) PRIMARY KEY,
    regulation      TEXT NOT NULL,
    rules           JSONB NOT NULL,
    updated_at      TIMESTAMPTZ DEFAULT now()
);

-- Indexes
CREATE INDEX ON monitored_flights (user_id, status);
CREATE INDEX ON disruptions (flight_id, detected_at DESC);
CREATE INDEX ON claims (user_id, status);
CREATE INDEX ON claims (carrier, status);   -- for ML training queries
CREATE INDEX ON carrier_rules USING GIN (rules);  -- JSONB index
```

**ORM:** SQLAlchemy 2.0 async with `asyncpg` driver. Alembic for schema migrations.

```
sqlalchemy==2.0.30     # MIT license
asyncpg==0.29.0        # BSD license — async PostgreSQL driver
alembic==1.13.1        # MIT license — schema migrations
```

**Cost:** $0 — PostgreSQL is open source. All Python libraries are MIT/BSD.

---

### 5. Rebooking Engine: Playwright (Headless Browser Automation)

**Why Playwright instead of a paid GDS or NDC API:**
GDS APIs (Amadeus, Sabre, Travelport) require commercial agreements or charge per search. Duffel has a free developer sandbox but charges per live booking. At MVP scale, the fastest zero-cost path to real alternative flight inventory is programmatic scraping of Google Flights, which aggregates live seat availability from all carriers in one place.

**Why Playwright over Selenium or BeautifulSoup:**
Google Flights is a React single-page app — all flight cards are rendered client-side via JavaScript after the initial page load. BeautifulSoup parses static HTML and would return an empty DOM. Playwright launches a real Chromium instance, waits for the React tree to hydrate, and extracts fully rendered content. Compared to Selenium, Playwright has native async support, built-in auto-wait (no flaky `time.sleep`), and faster page lifecycle events.

```python
# rebooking/scraper.py
from playwright.async_api import async_playwright
from datetime import datetime, timedelta

async def fetch_alternatives(
    origin: str,      # IATA e.g. "LHR"
    dest: str,        # IATA e.g. "CDG"
    date_str: str,    # "2025-06-15"
) -> list[dict]:
    """
    Scrapes Google Flights for available alternatives on a given route/date.
    Returns list of: {flight_no, carrier, dep_time, arr_time, stops, duration_min}
    """
    search_url = build_google_flights_url(origin, dest, date_str)

    async with async_playwright() as pw:
        browser = await pw.chromium.launch(
            headless=True,
            args=["--no-sandbox", "--disable-dev-shm-usage"]
        )
        context = await browser.new_context(
            user_agent=(
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/123.0.0.0 Safari/537.36"
            )
        )
        page = await context.new_page()
        await page.goto(search_url, wait_until="networkidle", timeout=30000)

        # Wait for flight result cards to appear
        await page.wait_for_selector(
            '[jsname="IWWDBc"]', timeout=20000
        )

        cards = await page.query_selector_all('[jsname="IWWDBc"]')
        results = []
        for card in cards[:8]:          # top 8 alternatives
            inner = await card.inner_text()
            parsed = parse_flight_card_text(inner)
            if parsed:
                results.append(parsed)

        await browser.close()
    return results
```

**Preference Ranking Algorithm:**
Once alternatives are fetched, each is scored against the user's stored preferences. The highest-scoring option is sent as the primary recommendation in the alert.

```python
# rebooking/ranker.py
CARRIER_LOYALTY_MAP = {
    "BA": ["BA Executive Club"],
    "IB": ["BA Executive Club", "Iberia Plus"],  # oneworld
    "LH": ["Miles&More"],
    "LX": ["Miles&More"],
    "AF": ["Flying Blue"],
    "KL": ["Flying Blue"],
    # ... expandable
}

CARRIER_ALLIANCE = {
    "BA": "ONEWORLD", "AA": "ONEWORLD", "QF": "ONEWORLD",
    "LH": "STAR",     "UA": "STAR",     "SQ": "STAR",
    "AF": "SKYTEAM",  "DL": "SKYTEAM",  "KL": "SKYTEAM",
}

def score_alternative(flight: dict, prefs: dict) -> float:
    score = 0.0

    # Loyalty program exact match — protects status accrual (highest weight)
    if prefs.get("loyalty_program") in CARRIER_LOYALTY_MAP.get(
        flight["carrier"], []
    ):
        score += 40.0

    # Alliance match — partner earnings still count
    elif prefs.get("alliance") == CARRIER_ALLIANCE.get(flight["carrier"]):
        score += 20.0

    # Connection penalty — each stop costs time and risk
    score -= flight.get("stops", 0) * 15.0

    # Departure time proximity to original scheduled departure
    if "original_dep" in prefs and prefs["original_dep"]:
        dep_delta_hrs = abs(
            (flight["dep_time"] - prefs["original_dep"]).total_seconds() / 3600
        )
        if dep_delta_hrs < 2:
            score += 12.0
        elif dep_delta_hrs < 4:
            score += 6.0

    # Shorter total journey time bonus
    if flight.get("duration_min", 999) < prefs.get("original_duration_min", 999):
        score += 5.0

    return score

def rank_alternatives(flights: list[dict], prefs: dict) -> list[dict]:
    for f in flights:
        f["score"] = score_alternative(f, prefs)
    return sorted(flights, key=lambda x: x["score"], reverse=True)
```

**Cost:** $0 — Playwright is Apache 2.0 licensed. Chromium is BSD licensed.

---

### 6. Claims Engine: JSON Rulesets + WeasyPrint + DocuSeal

#### 6a. Modular Carrier Ruleset (JSONB in PostgreSQL)

Each carrier's compensation logic lives as a single JSON document in the `carrier_rules` table. Adding a new carrier (e.g. Turkish Airlines when EU-expansion launches) requires inserting one row — no code change, no redeployment. The JSON structure is versioned with a schema identifier.

```json
{
  "_schema": "v1",
  "carrier_iata": "FR",
  "carrier_name": "Ryanair",
  "regulation": "EC261",
  "distance_bands": [
    { "max_km": 1500,  "min_delay_hours": 3, "compensation_eur": 250 },
    { "max_km": 3500,  "min_delay_hours": 3, "compensation_eur": 400 },
    { "max_km": 99999, "min_delay_hours": 4, "compensation_eur": 600 }
  ],
  "extraordinary_circumstances": [
    "WEATHER", "ATC_STRIKE", "BIRD_STRIKE",
    "SECURITY_ALERT", "POLITICAL_INSTABILITY", "HIDDEN_MANUFACTURING_DEFECT"
  ],
  "within_14_days_rule": true,
  "submission_method": "WEB_FORM",
  "submission_url": "https://www.ryanair.com/gb/en/useful-info/help-centre/claims",
  "required_documents": [
    "BOARDING_PASS", "BOOKING_CONFIRMATION", "DELAY_CERTIFICATE"
  ],
  "typical_processing_days": 30,
  "appeal_body": "Aviation ADR",
  "appeal_url": "https://www.aviationadr.org.uk/"
}
```

**Eligibility check engine:**

```python
# claims/eligibility.py
from geopy.distance import geodesic     # MIT license — great-circle distance

AIRPORT_COORDS = {
    "EGLL": (51.4775, -0.4614),   # London Heathrow
    "LFPG": (49.0097,  2.5479),   # Paris CDG
    "EDDF": (50.0379,  8.5622),   # Frankfurt
    # ... loaded from a free CSV at startup
}

def check_eligibility(disruption: dict, rule: dict) -> dict:
    """
    Returns {eligible: bool, amount_eur: int, reason: str, distance_km: float}
    """
    origin = disruption["dep_airport"]
    dest   = disruption["arr_airport"]
    delay_hours = (disruption["delay_minutes"] or 0) / 60

    # Step 1: Extraordinary circumstances auto-reject
    if disruption.get("cause") in rule["extraordinary_circumstances"]:
        return {
            "eligible": False,
            "reason": "EXTRAORDINARY_CIRCUMSTANCES",
            "cause": disruption["cause"]
        }

    # Step 2: Great-circle distance
    if origin not in AIRPORT_COORDS or dest not in AIRPORT_COORDS:
        return {"eligible": False, "reason": "UNKNOWN_AIRPORT"}

    dist_km = geodesic(AIRPORT_COORDS[origin], AIRPORT_COORDS[dest]).km

    # Step 3: Find matching distance band
    for band in rule["distance_bands"]:
        if dist_km <= band["max_km"]:
            if delay_hours >= band["min_delay_hours"]:
                return {
                    "eligible": True,
                    "amount_eur": band["compensation_eur"],
                    "reason": "QUALIFIED",
                    "distance_km": round(dist_km, 1)
                }
            else:
                return {
                    "eligible": False,
                    "reason": "DELAY_BELOW_THRESHOLD",
                    "delay_hours": round(delay_hours, 1),
                    "threshold_hours": band["min_delay_hours"]
                }

    return {"eligible": False, "reason": "NO_MATCHING_BAND"}
```

#### 6b. PDF Generation: WeasyPrint + Jinja2

WeasyPrint renders HTML+CSS to pixel-perfect, print-ready PDFs. Claim documentation packages are built from Jinja2 HTML templates that are populated with passenger details, flight records, delay timeline (sourced from OpenSky historical endpoint as verifiable evidence), and the computed compensation amount.

```python
# claims/pdf_generator.py
from weasyprint import HTML           # BSD license
from jinja2 import Environment, FileSystemLoader  # BSD license

jinja_env = Environment(loader=FileSystemLoader("claims/templates/"))

def generate_claim_pdf(claim_data: dict) -> bytes:
    """
    Renders the EC261 claim template to a signed-ready PDF.
    claim_data keys: passenger, flight, disruption, eligibility, carrier_rule
    """
    template = jinja_env.get_template("ec261_claim.html")
    html_str = template.render(**claim_data)
    pdf_bytes = HTML(string=html_str, base_url=".").write_pdf()
    return pdf_bytes
```

The HTML template (`ec261_claim.html`) includes:
- Passenger full name, booking reference, and contact details
- Flight number, scheduled and actual departure times
- Delay duration in hours and minutes (from OpenSky state diff)
- Great-circle distance (computed by eligibility engine)
- Compensation amount under EC 261/2004, Article 7
- Carrier name and submission address
- Signature block (populated after DocuSeal signing)
- OpenSky state snapshot table as an annex (timestamped evidence)

#### 6c. E-Signature: DocuSeal (self-hosted, open source)

DocuSeal is an open-source document signing platform (MIT license) that provides a full-featured API for uploading PDFs, creating signature requests, embedding a signing UI in the web app, and retrieving completed signed documents. It eliminates the need for DocuSign ($25+/month) or HelloSign. Self-hosted via a single Docker container.

```python
# claims/esign.py
import httpx

DOCUSEAL_URL   = "http://docuseal:3000"   # internal Docker hostname
DOCUSEAL_TOKEN = "your_api_token"         # generated on first DocuSeal boot

async def create_signature_request(
    pdf_bytes: bytes, signer_email: str, signer_name: str
) -> dict:
    """
    Uploads claim PDF to DocuSeal, creates a signature submission.
    Returns: {signing_url: str, submission_id: int}
    """
    async with httpx.AsyncClient() as client:
        # Step 1: Upload PDF as a template
        upload = await client.post(
            f"{DOCUSEAL_URL}/api/templates/pdf",
            headers={"X-Auth-Token": DOCUSEAL_TOKEN},
            files={"file": ("claim.pdf", pdf_bytes, "application/pdf")},
            data={"name": f"EC261 Claim – {signer_name}"}
        )
        template_id = upload.json()["id"]

        # Step 2: Create submission (signature request for the claimant)
        submission = await client.post(
            f"{DOCUSEAL_URL}/api/submissions",
            headers={"X-Auth-Token": DOCUSEAL_TOKEN},
            json={
                "template_id": template_id,
                "submitters": [{
                    "email": signer_email,
                    "name":  signer_name,
                    "role":  "Claimant"
                }]
            }
        )
        submitter = submission.json()["submitters"][0]

    return {
        "signing_url":   submitter["embed_src"],   # embed in frontend iframe
        "submission_id": submitter["submission_id"]
    }

async def get_signed_pdf_url(submission_id: int) -> str | None:
    """Poll for completed signature; returns download URL when done."""
    async with httpx.AsyncClient() as client:
        r = await client.get(
            f"{DOCUSEAL_URL}/api/submissions/{submission_id}",
            headers={"X-Auth-Token": DOCUSEAL_TOKEN}
        )
    data = r.json()
    if data["status"] == "completed":
        return data["documents"][0]["url"]
    return None
```

DocuSeal sends a webhook to `/api/webhooks/docuseal` when signing completes. The webhook handler downloads the signed PDF, stores the URL in `claims.doc_url`, and advances claim status to `SUBMITTED`.

**Cost:** $0 — DocuSeal is MIT licensed.

---

### 7. ML: Claims Outcome Predictor (scikit-learn + joblib)

As the `claims` table accumulates resolved rows (`status IN ('ACCEPTED', 'REJECTED')`), a nightly APScheduler job retrains a Gradient Boosting classifier. The model predicts the probability that a new claim will succeed given: carrier, route, delay duration, disruption type, month, and day of week. This probability feeds two use cases:

1. **Claim prioritisation** — surface high-confidence claims first in the user dashboard
2. **Appeal copy generation** — for low-confidence rejections, the model's feature importances indicate which angle to emphasise in the appeal letter (e.g., "this carrier has a 78% acceptance rate on ATC delays > 4hr at this airport")

```python
# ml/train.py
import pandas as pd
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, roc_auc_score
import joblib          # BSD license — model serialisation
import asyncpg

async def load_training_data() -> pd.DataFrame:
    conn = await asyncpg.connect(DATABASE_URL)
    rows = await conn.fetch("""
        SELECT
            c.carrier,
            c.regulation,
            d.delay_minutes,
            d.type         AS disruption_type,
            EXTRACT(MONTH FROM d.detected_at)::int  AS month,
            EXTRACT(DOW   FROM d.detected_at)::int  AS dow,
            mf.dep_airport,
            mf.arr_airport,
            (c.status = 'ACCEPTED')::int            AS label
        FROM claims c
        JOIN disruptions d       ON d.id  = c.disruption_id
        JOIN monitored_flights mf ON mf.id = d.flight_id
        WHERE c.status IN ('ACCEPTED', 'REJECTED')
    """)
    await conn.close()
    return pd.DataFrame([dict(r) for r in rows])

def train(df: pd.DataFrame) -> GradientBoostingClassifier:
    cat_cols = ["carrier", "regulation", "disruption_type",
                "dep_airport", "arr_airport"]
    encoders = {}
    for col in cat_cols:
        le = LabelEncoder()
        df[col] = le.fit_transform(df[col].astype(str))
        encoders[col] = le

    X = df.drop("label", axis=1)
    y = df["label"]
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, stratify=y, random_state=42
    )

    model = GradientBoostingClassifier(
        n_estimators=300,
        max_depth=4,
        learning_rate=0.05,
        subsample=0.8,
        min_samples_leaf=10
    )
    model.fit(X_train, y_train)

    y_prob = model.predict_proba(X_test)[:, 1]
    print(f"ROC-AUC: {roc_auc_score(y_test, y_prob):.3f}")
    print(classification_report(y_test, model.predict(X_test)))

    joblib.dump({"model": model, "encoders": encoders},
                "models/claims_predictor.pkl")
    return model

# Nightly retrain job (APScheduler, same scheduler instance as poller)
scheduler.add_job(retrain_job, "cron", hour=2, minute=30)
```

**Cost:** $0 — scikit-learn, joblib, pandas are all BSD licensed.

---

### 8. Frontend: Next.js 14 (App Router) + Tailwind CSS

**Why Next.js:**
The compensation calculator landing page must rank on Google for high-intent keywords ("flight delay compensation calculator") — that requires server-side rendering so search crawlers receive pre-rendered HTML, not a blank React shell. Next.js App Router natively supports React Server Components for SSR on public pages and client-side React for the authenticated dashboard. It eliminates the need to run a separate static-site generator alongside the web app.

**Why Tailwind CSS:**
Utility-first CSS keeps component styles co-located with markup. There are no external `.css` files to maintain — every style decision is visible inline in the component tree. For a solo developer shipping fast, this eliminates the cognitive overhead of naming conventions and stylesheet management.

**Key routes:**
```
app/
├── page.tsx                    # Public: Landing page + compensation calculator (SSR)
├── dashboard/
│   ├── layout.tsx              # Authenticated shell (auth check via Better Auth)
│   ├── flights/page.tsx        # Active monitored flights + real-time status
│   ├── claims/page.tsx         # Claims tracker with DocuSeal signing embed
│   └── alerts/page.tsx         # Disruption history feed
├── onboarding/page.tsx         # Preferences wizard (loyalty, seat, alliance)
└── api/
    ├── auth/[...all]/route.ts  # Better Auth handler
    └── webhooks/
        └── docuseal/route.ts   # Receives signing-completed webhooks
```

**Real-time WebSocket alerts (live dashboard):**

```typescript
// hooks/useDisruptionSocket.ts
import { useEffect, useState } from "react";

interface DisruptionAlert {
  flight_id: string;
  flight_no: string;
  type: "DELAY" | "CANCEL" | "DIVERT";
  delay_minutes: number;
  rebook_options: ReBookOption[];
}

export function useDisruptionSocket(userId: string) {
  const [alerts, setAlerts] = useState<DisruptionAlert[]>([]);

  useEffect(() => {
    const ws = new WebSocket(
      `${process.env.NEXT_PUBLIC_API_WS_URL}/ws/alerts/${userId}`
    );

    ws.onmessage = (event) => {
      const alert: DisruptionAlert = JSON.parse(event.data);
      setAlerts((prev) => [alert, ...prev.slice(0, 49)]);   // keep last 50
    };

    ws.onclose = () => {
      // Reconnect after 3 seconds on unexpected close
      setTimeout(() => ws.close(), 3000);
    };

    return () => ws.close();
  }, [userId]);

  return alerts;
}
```

**FastAPI WebSocket endpoint (backend):**

```python
# api/routes/ws.py
from fastapi import WebSocket, WebSocketDisconnect
import redis.asyncio as aioredis

@router.websocket("/ws/alerts/{user_id}")
async def websocket_alerts(websocket: WebSocket, user_id: str):
    await websocket.accept()
    r = aioredis.from_url("redis://localhost:6379")
    pubsub = r.pubsub()
    await pubsub.subscribe(f"alerts:{user_id}")

    try:
        async for message in pubsub.listen():
            if message["type"] == "message":
                await websocket.send_text(message["data"].decode())
    except WebSocketDisconnect:
        pass
    finally:
        await pubsub.unsubscribe(f"alerts:{user_id}")
        await r.aclose()
```

**Deployment:** Vercel hobby tier (free) — Next.js is Vercel's own framework, so deployment is a single `git push`. Zero configuration for SSL, CDN, and edge caching.

**Cost:** $0 — Next.js is MIT licensed. Tailwind CSS is MIT licensed. Vercel hobby is free.

---

### 9. Auth: Better Auth (self-hosted, open source)

**Why not Auth0, Clerk, or Supabase Auth:**
Auth0 and Clerk charge per MAU above their free tiers. Supabase Auth ties you to their hosted database. Better Auth is a fully self-hosted, open-source authentication library (MIT license) that provides email/password, magic link, and OAuth (Google) flows via a compact SDK that works natively with Next.js App Router and integrates directly with the existing PostgreSQL instance. Zero vendor dependency, zero MAU pricing, full control over user data.

```typescript
// lib/auth.ts
import { betterAuth } from "better-auth";
import { Pool } from "pg";

export const auth = betterAuth({
  database: new Pool({ connectionString: process.env.DATABASE_URL }),
  emailAndPassword: {
    enabled: true,
    requireEmailVerification: true
  },
  socialProviders: {
    google: {
      clientId:     process.env.GOOGLE_CLIENT_ID!,
      clientSecret: process.env.GOOGLE_CLIENT_SECRET!
    }
  },
  session: {
    expiresIn:        60 * 60 * 24 * 30,   // 30 days
    updateAge:        60 * 60 * 24,         // refresh if > 1 day old
    cookieCache: { enabled: true, maxAge: 60 * 5 }
  }
});
```

**Cost:** $0 — Better Auth is MIT licensed.

---

### 10. Email: Resend (free tier) + React Email

Resend provides a REST API for transactional email with 3,000 emails/month and 100/day on the permanent free tier — sufficient for MVP. React Email (open source, MIT) lets email templates be written as React components, enabling type-safety and version control on email design (no more broken HTML in string literals).

```python
# notifications/email.py
import httpx

RESEND_API_KEY = "re_..."    # free tier — no card required

async def send_disruption_alert(
    to_email: str,
    flight_no: str,
    delay_minutes: int,
    rebook_url: str,
    top_option: dict
):
    subject = (
        f"⚠️ {flight_no} delayed {delay_minutes}min — "
        f"best rebook: {top_option['flight_no']} ready"
    )
    html = render_alert_template(flight_no, delay_minutes,
                                  rebook_url, top_option)
    async with httpx.AsyncClient() as client:
        await client.post(
            "https://api.resend.com/emails",
            headers={"Authorization": f"Bearer {RESEND_API_KEY}"},
            json={
                "from":    "alerts@reroute.app",
                "to":      [to_email],
                "subject": subject,
                "html":    html
            }
        )
```

**Cost:** $0 on free tier. React Email is MIT licensed.

---

### 11. Infrastructure: Docker Compose on Oracle Cloud Always Free

**Why a single VPS over AWS/GCP/Azure:**
A typical AWS setup (RDS t3.micro + ElastiCache t3.micro + ECS Fargate + ALB) costs $80–$150/month. Oracle Cloud's Always Free tier provides compute, storage, and networking that is permanently free — not a trial. All services run in a single `docker-compose.yml` on the Oracle ARM instance.

**Oracle Cloud Always Free compute (permanent):**
- 4x ARM Ampere A1 cores + 24GB RAM — runs the full Docker Compose stack
- 200GB block storage — ample for PostgreSQL, Redis, DocuSeal, Grafana
- 10TB/month outbound bandwidth
- Static public IP address

```yaml
# docker-compose.yml
version: "3.9"

services:

  postgres:
    image: postgres:16-alpine
    restart: unless-stopped
    environment:
      POSTGRES_DB:       reroute
      POSTGRES_USER:     reroute
      POSTGRES_PASSWORD: ${PG_PASSWORD}
    volumes:
      - pg_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U reroute"]
      interval: 10s
      retries: 5

  redis:
    image: redis:7-alpine
    restart: unless-stopped
    command: >
      redis-server
      --maxmemory 512mb
      --maxmemory-policy allkeys-lru
      --appendonly yes
    volumes:
      - redis_data:/data

  api:
    build: ./backend
    restart: unless-stopped
    depends_on:
      postgres: { condition: service_healthy }
      redis:    { condition: service_started }
    environment:
      DATABASE_URL: postgresql+asyncpg://reroute:${PG_PASSWORD}@postgres/reroute
      REDIS_URL:    redis://redis:6379
      RESEND_KEY:   ${RESEND_KEY}
    command: uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4

  worker:
    build: ./backend
    restart: unless-stopped
    depends_on:
      postgres: { condition: service_healthy }
      redis:    { condition: service_started }
    command: python worker.py        # APScheduler + Redis Streams consumers

  docuseal:
    image: docuseal/docuseal:latest
    restart: unless-stopped
    depends_on:
      postgres: { condition: service_healthy }
    environment:
      DATABASE_URL:     postgresql://reroute:${PG_PASSWORD}@postgres/reroute
      SECRET_KEY_BASE:  ${DOCUSEAL_SECRET}
    volumes:
      - docuseal_data:/data

  prometheus:
    image: prom/prometheus:latest
    restart: unless-stopped
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml
      - prom_data:/prometheus
    command: >
      --config.file=/etc/prometheus/prometheus.yml
      --storage.tsdb.retention.time=30d

  grafana:
    image: grafana/grafana:latest
    restart: unless-stopped
    depends_on: [prometheus]
    environment:
      GF_SECURITY_ADMIN_PASSWORD: ${GRAFANA_PASSWORD}
    volumes:
      - grafana_data:/var/lib/grafana

  caddy:
    image: caddy:2-alpine
    restart: unless-stopped
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./Caddyfile:/etc/caddy/Caddyfile
      - caddy_data:/data

volumes:
  pg_data:
  redis_data:
  docuseal_data:
  prom_data:
  grafana_data:
  caddy_data:
```

**Reverse proxy + TLS: Caddy**
Caddy automatically provisions and renews Let's Encrypt TLS certificates for every domain with zero configuration. No certbot cron jobs, no renewal scripts. HTTP→HTTPS redirect and WebSocket proxying are handled out of the box.

```
# Caddyfile
api.reroute.app {
    reverse_proxy api:8000
}
sign.reroute.app {
    reverse_proxy docuseal:3000
}
metrics.reroute.app {
    reverse_proxy grafana:3000
    basicauth { admin {$GRAFANA_HTPASSWD} }
}
```

**Cost:** $0 — Oracle Always Free is permanent. Caddy is Apache 2.0.

---

### 12. Observability: Prometheus + Loki + Grafana (self-hosted)

Rather than paying for Datadog ($15/host/month) or New Relic, the full observability stack is self-hosted on the same ARM instance.

- **Prometheus** — scrapes `/metrics` from FastAPI (via `prometheus-fastapi-instrumentator`, MIT license) every 15 seconds. Tracks: request latency (p50/p95/p99), disruption event throughput, Redis stream queue depth, claim submission rate.
- **Loki** — log aggregation. The `loki-docker-driver` plugin ships container logs directly to Loki without a sidecar. Replaces Elasticsearch (which alone requires 2GB RAM minimum).
- **Grafana** — dashboards for all of the above plus a business metrics board (claims filed today, acceptance rate by carrier, revenue pipeline).

```python
# backend/main.py
from prometheus_fastapi_instrumentator import Instrumentator
from prometheus_client import Counter, Histogram

disruptions_detected = Counter(
    "reroute_disruptions_total",
    "Total disruption events detected",
    ["disruption_type", "carrier"]
)
claim_filed = Counter(
    "reroute_claims_filed_total",
    "Claims submitted to carriers",
    ["carrier", "regulation"]
)
claim_outcome = Counter(
    "reroute_claim_outcomes_total",
    "Claim outcomes",
    ["carrier", "outcome"]   # outcome: accepted | rejected | appealed
)

app = FastAPI()
Instrumentator().instrument(app).expose(app)
```

**Cost:** $0 — Prometheus (Apache 2.0), Loki (AGPLv3), Grafana (AGPLv3) are all self-hosted.

---

## 📦 Complete Zero-Cost Dependency Table

| Layer | Technology | License | Monthly Cost |
|---|---|---|---|
| API framework | FastAPI + Uvicorn | MIT | $0 |
| Frontend framework | Next.js 14 | MIT | $0 |
| Frontend styling | Tailwind CSS | MIT | $0 |
| Frontend hosting | Vercel hobby tier | Free tier | $0 |
| Database | PostgreSQL 16 | PostgreSQL License | $0 |
| Cache + message bus | Redis 7 (Streams + Pub/Sub) | BSD | $0 |
| Async DB driver | asyncpg | BSD | $0 |
| ORM | SQLAlchemy 2.0 async | MIT | $0 |
| Migrations | Alembic | MIT | $0 |
| Flight data | OpenSky Network API | CC BY 4.0 | $0 |
| Flight data fallback | ADS-B Exchange | Open | $0 |
| Background scheduler | APScheduler | MIT | $0 |
| Browser automation | Playwright (Chromium) | Apache 2.0 | $0 |
| HTTP client | httpx | BSD | $0 |
| PDF generation | WeasyPrint | BSD | $0 |
| HTML templating | Jinja2 | BSD | $0 |
| E-signature | DocuSeal (self-hosted) | MIT | $0 |
| Distance calculation | geopy | MIT | $0 |
| ML model | scikit-learn | BSD | $0 |
| Model persistence | joblib | BSD | $0 |
| Data manipulation | pandas | BSD | $0 |
| Authentication | Better Auth | MIT | $0 |
| Email (MVP) | Resend free tier (3K/mo) | Free tier | $0 |
| Email templates | React Email | MIT | $0 |
| Reverse proxy + TLS | Caddy | Apache 2.0 | $0 |
| Infrastructure | Oracle Cloud Always Free | Permanent free | $0 |
| Metrics | Prometheus | Apache 2.0 | $0 |
| Log aggregation | Loki | AGPLv3 | $0 |
| Dashboards | Grafana | AGPLv3 | $0 |
| Containerisation | Docker + Docker Compose | Apache 2.0 | $0 |

**Total monthly infrastructure cost: $0**

---

## 📊 Key Metrics to Track

| Metric | Target |
|---|---|
| Alert-to-rebook time | < 5 minutes from disruption |
| Rebooking acceptance rate | > 60% |
| Claims submission rate | > 80% of eligible disruptions |
| Claims success rate | > 50% (EU baseline) |
| Monthly churn | < 3% |
| Commission revenue per user | > $15/month blended |

---

## ⚠️ Key Risks & Mitigations

| Risk | Mitigation |
|---|---|
| OpenSky rate limits | Use registered free account (5s interval); cache ICAO lookups in Redis with 1hr TTL |
| Google Flights blocks scrapers | Rotate user-agents, add Playwright stealth mode, randomise request timing with jitter |
| Claims rejection / legal complexity | Start EU-only (EC 261/2004 standardised); modular JSON rulesets per carrier |
| User trust for auto-rebooking | Default to manual-confirm mode; full automation is explicit opt-in |
| Regulatory changes | Rules live in DB rows, not application code — update without redeployment |
| Oracle Cloud SLA | 99.95% uptime SLA on Always Free compute; Caddy auto-restarts containers |

---

## 📅 90-Day Milestones

| Week | Milestone |
|---|---|
| Week 2 | Docker Compose stack live on Oracle Always Free; OpenSky polling confirmed for 3 EU routes |
| Week 4 | Free Compensation Calculator live on Vercel; 500+ email signups |
| Week 6 | Beta users receiving real-time WebSocket + email alerts |
| Week 8 | Playwright rebooking scraper live; top alternative surfaced in alert emails |
| Week 10 | First paying subscribers ($29/month tier) |
| Week 14 | First EC 261/2004 claim PDFs generated, signed via DocuSeal, submitted |
| Week 20 | 25% commission revenue stream active; scikit-learn model trained on first 100 outcomes |

---

## ✅ Immediate Next Actions

1. **Provision Oracle Always Free VM** — install Docker, clone repo, spin up `docker-compose up -d` — full stack live in an afternoon
2. **OpenSky integration test** — poll 5 live flights by ICAO24, verify state-change detection and Redis Stream emission end-to-end
3. **Ship the calculator** — static Next.js page on Vercel, zero backend required; captures emails via Resend free tier
4. **Playwright POC** — confirm Google Flights scraper returns parseable flight card data for 3 LHR and CDG routes
5. **Encode first 3 carrier rulesets** — Ryanair (FR), EasyJet (U2), Lufthansa (LH) as JSONB rows in `carrier_rules`; run eligibility unit tests against known historical delays

---

*Scores from IdeaBrowser: Opportunity 9/10 · Problem 9/10 · Why Now 9/10 · Feasibility 6/10 · Revenue Potential $$$*

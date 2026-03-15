# Fly.io Deployment Guide

This guide covers deploying Reroute to Fly.io for production.

---

## Why Fly.io?

- **$5/month free credit** - forever (not a trial)
- **Real VMs** - containers stay running 24/7
- **No credit card required** - just email verification
- **3 VMs** on free tier (256MB RAM each)
- **Global CDN** - deploy close to your users

---

## Prerequisites

1. Install flyctl:
   ```bash
   brew install flyctl
   ```

2. Sign up:
   ```bash
   fly auth signup
   ```
   (Use GitHub or email - no credit card needed)

---

## Quick Deploy

### Step 1: Clone and Setup

```bash
git clone https://github.com/officialaritro/airplane-agent.git
cd airplane-agent
```

### Step 2: Create the App

```bash
fly launch
```

- App name: `reroute`
- Region: `lhr` (London) or closest to you
- PostgreSQL: Yes (create managed database)
- Redis: Yes (create managed database)

### Step 3: Set Secrets

```bash
# OpenSky credentials
fly secrets set OPENSKY_CLIENT_ID=your_client_id
fly secrets set OPENSKY_CLIENT_SECRET=your_client_secret

# Resend (email)
fly secrets set RESEND_KEY=re_xxxxxxxxxxxx

# DocuSeal secret
fly secrets set DOCUSEAL_SECRET=$(openssl rand -base64 32)
```

### Step 4: Deploy

```bash
fly deploy
```

---

## Managed Databases

Fly.io creates managed PostgreSQL and Redis. Connection strings are automatically available as `DATABASE_URL` and `FLY_REDIS_URL` secrets.

### Connect to PostgreSQL locally

```bash
fly postgres connect -a reroute
```

### View Redis

```bash
fly redis connect -a reroute
```

---

## Scaling

### Scale up (if needed)

```bash
fly scale vm shared-cpu-2x
fly scale count 2
```

### Add volumes

```bash
fly volumes create reroute_data --size 1
```

---

## Troubleshooting

### View logs

```bash
fly logs
```

### Check status

```bash
fly status
```

### SSH into VM

```bash
fly ssh console
```

### Restart

```bash
fly restart
```

---

## Costs

| Resource | Free Tier | Cost |
|----------|-----------|------|
| VMs (3x) | 256MB each | $0 |
| PostgreSQL | 1GB | $0 |
| Redis | 256MB | $0 |
| Bandwidth | 3GB/month | $0 |
| **Total** | | **$0** |

You'll use about $1-2/month of the $5 credit, so it's completely free!

---

## Local Development

For local development, use Docker Compose:

```bash
# Copy env file
cp backend/.env.example backend/.env
# Edit with your values

# Start services
docker-compose up -d postgres redis

# Run backend
cd backend
source venv/bin/activate
uvicorn main:app --reload

# Run frontend (new terminal)
cd frontend
npm run dev
```

---

## Resources

- [Fly.io Docs](https://fly.io/docs/)
- [Fly.io Discord](https://fly.io/discord)
- [Pricing](https://fly.io/pricing/)

# Oracle Cloud Deployment Guide

This guide covers deploying Reroute to Oracle Cloud Infrastructure (OCI).

---

## Why Oracle Cloud?

- **Always Free** - permanent free tier (not a trial)
- **4 Ampere cores + 24GB RAM** - powerful!
- **200GB block storage** - ample for PostgreSQL
- **10TB outbound bandwidth** - plenty for a startup
- **Permanent free IP** - static public IP included

---

## Prerequisites

1. **Oracle Cloud Account** - Sign up at https://oracle.com/cloud/free/
2. **Credit Card** - Required for identity verification (not charged)

---

## Quick Deploy

### Step 1: Create Compute Instance

1. Login to https://cloud.oracle.com/
2. Go to **OCI** → **Compute** → **Instances**
3. Click **Create Instance**
4. Configure:
   - Name: `reroute`
   - Image: `Oracle Linux 8` or `Ubuntu 22.04`
   - Shape: **Ampere** (always free)
   - Add SSH key (or generate one)
5. Click **Create**

### Step 2: SSH into Server

```bash
# Connect to your instance
ssh opc@YOUR_PUBLIC_IP
```

### Step 3: Install Docker

```bash
# Update and install Docker
sudo yum update -y
sudo yum install -y docker
sudo systemctl start docker
sudo systemctl enable docker
sudo usermod -aG docker opc

# Log out and back in for group changes
exit
ssh opc@YOUR_PUBLIC_IP
```

### Step 4: Clone and Configure

```bash
# Clone repository
git clone https://github.com/officialaritro/airplane-agent.git
cd airplane-agent

# Copy env file
cp backend/.env.example backend/.env

# Edit with your API keys
nano backend/.env
```

Add your values:
```bash
OPENSKY_CLIENT_ID=your_client_id
OPENSKY_CLIENT_SECRET=your_client_secret
RESEND_KEY=re_xxxxxxxxxxxx
PG_PASSWORD=your_secure_password
```

### Step 5: Deploy

```bash
# Start all services
docker-compose up -d

# Check status
docker-compose ps
```

### Step 6: Access the App

- API: `http://YOUR_PUBLIC_IP:8000`
- Frontend: Build separately and deploy to Vercel

---

## Services Running

| Service | Port | URL |
|---------|------|-----|
| API | 8000 | http://YOUR_IP:8000 |
| PostgreSQL | 5432 | Internal |
| Redis | 6379 | Internal |
| Worker | - | Background |
| Prometheus | 9090 | http://YOUR_IP:9090 |
| Grafana | 3001 | http://YOUR_IP:3001 |

---

## Updating Deployment

```bash
# Pull latest code
cd airplane-agent
git pull origin main

# Rebuild and restart
docker-compose down
docker-compose build
docker-compose up -d
```

---

## Costs

| Resource | Free Tier | Cost |
|----------|-----------|------|
| Compute (4 cores, 24GB) | Always Free | $0 |
| Block Storage (200GB) | Always Free | $0 |
| Outbound Bandwidth | 10TB/month | $0 |
| Public IP | Always Free | $0 |
| **Total** | | **$0** |

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

## Production Frontend Deployment

Deploy frontend to Vercel (free):

```bash
# Install Vercel CLI
npm i -g vercel

# Deploy
cd frontend
vercel --prod
```

---

## Resources

- [Oracle Cloud Free Tier](https://www.oracle.com/cloud/free/)
- [OCI Documentation](https://docs.oracle.com/en-us/iaas/Content/Home.htm)
- [Docker Docs](https://docs.docker.com/)

# TASK.md — Reroute: Flight Compensation Recovery Agent

> Detailed implementation roadmap in phased order

---

## Project Overview

**Reroute** is a real-time flight disruption management platform that:
- Monitors flights using OpenSky Network ADS-B data
- Detects disruptions (delays, cancellations, gate changes)
- Automatically rebooks flights based on user preferences
- Files compensation claims automatically (EC 261/2004)
- Uses ML to learn from claim outcomes

---

## Phase 1: Project Setup & Infrastructure (Weeks 1-2)

### 1.1 Initialize Project Structure

- [ ] Create monorepo structure with `backend/` and `frontend/` directories
- [ ] Set up Python 3.12 virtual environment
- [ ] Initialize FastAPI project with `main.py` entry point
- [ ] Initialize Next.js 14 project with TypeScript and Tailwind CSS
- [ ] Create `docker-compose.yml` with all services

### 1.2 Configure Docker Compose Stack

- [ ] Set up PostgreSQL 16 container with initialization scripts
- [ ] Configure Redis 7 container (Streams + Pub/Sub)
- [ ] Add Caddy reverse proxy container
- [ ] Add Prometheus + Grafana for observability
- [ ] Add DocuSeal for e-signatures
- [ ] Configure environment variables and secrets management
- [ ] Test local development environment

### 1.3 Database Schema

- [ ] Create PostgreSQL schema with tables:
  - `users` - Core user identity
  - `flight_preferences` - User travel preferences
  - `monitored_flights` - Active monitored flights
  - `disruptions` - Disruption event log
  - `claims` - Compensation claims lifecycle
  - `carrier_rules` - JSONB compensation rules
- [ ] Set up SQLAlchemy 2.0 async models
- [ ] Configure Alembic for migrations
- [ ] Create seed data for carrier rules (EU carriers)

### 1.4 Backend Foundation

- [ ] Set up FastAPI with Uvicorn
- [ ] Configure Pydantic models for request/response validation
- [ ] Set up SQLAlchemy async session management
- [ ] Configure Redis async client
- [ ] Add Prometheus metrics endpoint
- [ ] Set up logging with structured JSON

### 1.5 Frontend Foundation

- [ ] Set up Next.js 14 App Router structure
- [ ] Configure Tailwind CSS with custom theme
- [ ] Create layout components (Header, Sidebar, Footer)
- [ ] Set up API client (axios or fetch wrapper)
- [ ] Configure environment variables
- [ ] Set up error boundaries and loading states

---

## Phase 2: MVP - Monitoring & Alerts (Weeks 3-4)

### 2.1 Flight Data Ingestion

- [ ] Implement OpenSky Network API client
- [ ] Create ICAO24 lookup cache (flight number → aircraft hex)
- [ ] Implement ADS-B Exchange fallback client
- [ ] Set up APScheduler for polling jobs (60s interval)
- [ ] Create Redis state storage for flight snapshots

### 2.2 Disruption Detection Engine

- [ ] Implement state comparison logic (delay > 15 min triggers)
- [ ] Build disruption event emitter to Redis Streams
- [ ] Create consumer groups for different workers
- [ ] Add support for delay, cancellation, gate change detection
- [ ] Implement cause detection (weather, ATC, etc.)

### 2.3 Real-time Notifications

- [ ] Set up Redis Pub/Sub for alert broadcasting
- [ ] Implement FastAPI WebSocket endpoint
- [ ] Create notification worker for email (Resend)
- [ ] Implement push notification support
- [ ] Build alert preferences system

### 2.4 User Onboarding

- [ ] Implement authentication with Better Auth
- [ ] Create flight preferences wizard UI
- [ ] Build itinerary import functionality
- [ ] Set up loyalty program preference storage
- [ ] Create seat preference management

### 2.5 Free Compensation Calculator (Lead Magnet)

- [ ] Build SSR compensation calculator page
- [ ] Implement EC 261/2004 calculation logic
- [ ] Create distance lookup (geopy)
- [ ] Add SEO metadata and structured data
- [ ] Deploy to Vercel

### 2.6 Beta Launch Preparation

- [ ] Set up user registration flow
- [ ] Create dashboard for monitored flights
- [ ] Build alert history view
- [ ] Implement email capture for calculator
- [ ] Deploy backend to Oracle Cloud

---

## Phase 3: Rebooking Engine (Weeks 5-8)

### 3.1 Playwright Flight Scraper

- [ ] Set up Playwright with Chromium
- [ ] Implement Google Flights scraping logic
- [ ] Handle JavaScript-rendered content
- [ ] Implement rate limiting and user-agent rotation
- [ ] Create stealth mode configuration
- [ ] Build flight card parser

### 3.2 Preference Ranking Algorithm

- [ ] Implement loyalty program matching
- [ ] Create alliance mapping (ONEWORLD, STAR, SKYTEAM)
- [ ] Build connection risk scoring
- [ ] Implement departure time proximity scoring
- [ ] Create duration comparison logic
- [ ] Build top option selection

### 3.3 Rebooking Workflow

- [ ] Create rebooking suggestion API
- [ ] Implement one-click rebook confirmation flow
- [ ] Build email template with rebook options
- [ ] Set up webhook for rebook completion
- [ ] Implement rebooking history tracking

### 3.4 A/B Testing Infrastructure

- [ ] Set up PostHog (self-hosted)
- [ ] Implement feature flags
- [ ] Create A/B test for rebook UX
- [ ] Build conversion tracking
- [ ] Create analytics dashboards

---

## Phase 4: Claims Engine (Weeks 9-14)

### 4.1 Compensation Rules Engine

- [ ] Build JSON ruleset structure for carriers
- [ ] Implement eligibility checker (distance bands, delay thresholds)
- [ ] Create extraordinary circumstances detection
- [ ] Add support for EC 261, UK 261, DOT regulations
- [ ] Build carrier-specific submission URL mapping

### 4.2 PDF Claim Generation

- [ ] Set up WeasyPrint with Jinja2 templates
- [ ] Create EC 261 claim HTML template
- [ ] Implement passenger details injection
- [ ] Add flight delay timeline (OpenSky evidence)
- [ ] Implement compensation amount calculation
- [ ] Build PDF rendering pipeline

### 4.3 E-Signature Integration

- [ ] Set up DocuSeal self-hosted
- [ ] Implement PDF upload to DocuSeal
- [ ] Create signature request workflow
- [ ] Build embedded signing UI
- [ ] Implement webhook handler for completion
- [ ] Store signed PDF URLs

### 4.4 Claims Submission

- [ ] Build carrier submission methods (web form, email)
- [ ] Implement automated submission queue
- [ ] Create claim status tracking
- [ ] Build appeal workflow
- [ ] Add document assembly (boarding pass, confirmation)

### 4.5 ML Claims Predictor

- [ ] Design training data schema
- [ ] Implement data extraction from claims table
- [ ] Build Gradient Boosting classifier (scikit-learn)
- [ ] Create nightly retrain job (APScheduler)
- [ ] Implement prediction API endpoint
- [ ] Build claim prioritisation scoring

---

## Phase 5: B2B Expansion (Weeks 15-20)

### 5.1 Corporate Dashboard

- [ ] Build corporate user management
- [ ] Create disruption cost visibility
- [ ] Implement route risk analytics
- [ ] Build team management features
- [ ] Add bulk import functionality

### 5.2 Integration APIs

- [ ] Implement Expensify API integration
- [ ] Create webhook system for T&E tools
- [ ] Build admin API endpoints
- [ ] Add rate limiting and API keys

### 5.3 Predictive Risk Scoring

- [ ] Implement route disruption prediction
- [ ] Build pre-booking risk assessment
- [ ] Create risk-aware booking suggestions
- [ ] Add route analytics dashboard

### 5.4 Enterprise Features

- [ ] Implement SSO/SAML authentication
- [ ] Build custom branding options
- [ ] Create usage analytics and reporting
- [ ] Add SLA management

---

## Phase 6: Production Hardening (Ongoing)

### 6.1 Observability

- [ ] Set up Prometheus metrics collection
- [ ] Configure Grafana dashboards
- [ ] Implement Loki log aggregation
- [ ] Set up alerting rules
- [ ] Create business metrics tracking

### 6.2 Reliability

- [ ] Implement circuit breakers
- [ ] Add retry logic with exponential backoff
- [ ] Set up health check endpoints
- [ ] Configure graceful shutdown
- [ ] Add database connection pooling

### 6.3 Security

- [ ] Implement input validation
- [ ] Add rate limiting
- [ ] Configure CORS policies
- [ ] Set up API authentication
- [ ] Implement audit logging

### 6.4 Performance

- [ ] Optimize database queries
- [ ] Add Redis caching layer
- [ ] Implement pagination
- [ ] Optimize frontend bundle
- [ ] Add CDN configuration

---

## Key Milestones

| Milestone | Target Week |
|-----------|-------------|
| Docker Compose stack live on Oracle | Week 2 |
| Free Calculator live on Vercel | Week 4 |
| First beta users receiving alerts | Week 4 |
| Playwright rebooking live | Week 8 |
| First paying subscribers | Week 10 |
| First claim PDFs generated | Week 14 |
| ML model trained on 100+ outcomes | Week 20 |
| Enterprise tier launched | Week 24 |

---

## Technology Stack Summary

| Layer | Technology |
|-------|------------|
| Backend | Python 3.12, FastAPI, Uvicorn |
| Frontend | Next.js 14, TypeScript, Tailwind CSS |
| Database | PostgreSQL 16 |
| Cache/Queue | Redis 7 |
| ORM | SQLAlchemy 2.0 async |
| Browser | Playwright |
| PDF | WeasyPrint + Jinja2 |
| E-signature | DocuSeal |
| ML | scikit-learn |
| Auth | Better Auth |
| Email | Resend |
| Infrastructure | Docker Compose, Oracle Cloud |
| Observability | Prometheus, Loki, Grafana |

---

## Skills to Install

Based on project requirements, install these skills:

```bash
# Backend Development
npx skills add mindrally/skills@fastapi-python

# Frontend Development  
npx skills add mindrally/skills@nextjs-react-typescript

# Database
npx skills add spillwavesolutions/mastering-postgresql-agent-skill@mastering-postgresql
```

---

## Notes

- All infrastructure costs are $0 (Oracle Always Free, open source)
- Claims engine starts EU-only (EC 261/2004)
- Default to manual-confirm mode for rebooking (auto-opt-in)
- Carrier rules stored in DB, not code (no redeployment for new carriers)

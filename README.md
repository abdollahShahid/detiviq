# Detiviq

Backend-first fleet operations platform for detention tracking, stop event timelines, and auditable revenue-loss analytics.

## Live Demo

- Dashboard: https://detiviq-wusr.vercel.app
- API Docs: https://detiviq.onrender.com/docs

## Product Summary

Detiviq helps carriers, dispatchers, and operations teams detect excessive waiting time at facilities, calculate detention charges, and surface delay-related revenue leakage.

The system models loads and stops, ingests operational events like `arrived`, `checked_in`, `loading_started`, `loading_finished`, and `departed`, applies configurable rules, computes detention eligibility, creates detention cases, and exposes recruiter-friendly analytics through APIs and a lightweight dashboard.

## Why This Project Matters

Truck waiting time is often tracked through calls, chats, memory, or spreadsheets. That leads to:
- missed detention charges
- weak auditability
- poor visibility into repeat delay sources
- revenue leakage that is hard to prove

Detiviq turns operational timestamps into explainable business outcomes.

## Core Backend Concepts Showcased

- Event ingestion
- Idempotency handling
- Rules resolution
- Dwell and detention computation
- Detention case creation and update
- Audit logging
- Analytics queries
- Deploy-safe backend architecture

## Architecture

### Backend
- FastAPI
- PostgreSQL
- SQLAlchemy 2.0
- Alembic
- Pydantic

### Frontend
- Next.js dashboard

### Deployment
- Backend: Render
- Database: Supabase Postgres
- Frontend: Vercel

## Main Entities

- Organization
- User
- Facility
- Load
- Stop
- Event
- Ruleset
- DetentionCase
- AuditLog

## API Surface

Key routes include:

- `POST /api/v1/auth/register`
- `POST /api/v1/auth/login`
- `GET /api/v1/facilities/`
- `POST /api/v1/facilities/`
- `GET /api/v1/loads/`
- `POST /api/v1/loads/`
- `GET /api/v1/loads/{load_id}`
- `POST /api/v1/loads/{load_id}/stops`
- `GET /api/v1/loads/{load_id}/timeline`
- `GET /api/v1/events/`
- `POST /api/v1/events/`
- `GET /api/v1/detention-cases/`
- `GET /api/v1/analytics/open-detention-cases-summary`
- `GET /api/v1/analytics/top-delayed-facilities`
- `GET /api/v1/analytics/revenue-loss-summary`

# Lyftr AI – Backend Assignment

This project implements a production-style backend service using **FastAPI** that ingests WhatsApp-like webhook messages, ensures idempotency, validates HMAC signatures, and provides analytics, pagination, health checks, and observability features.

---

## Tech Stack

- Python 3.11
- FastAPI
- SQLite
- Docker & Docker Compose
- Pydantic
- Uvicorn

---

## How to Run

### Prerequisites
- Docker
- Docker Compose

### Start the application

```bash
make up

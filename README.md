# 🚨 Incident Management System (IMS)

A resilient, production-grade Incident Management System built for Zeotap's Engineering Challenge.

## 📐 Architecture

┌─────────────────────────────────────────────────────────┐
│                    FRONTEND (React)                      │
│         Live Dashboard │ Raw Signals │ RCA Form          │
└─────────────────────┬───────────────────────────────────┘
│ HTTP/REST
┌─────────────────────▼───────────────────────────────────┐
│                 BACKEND (FastAPI)                        │
│                                                         │
│  ┌─────────────┐  ┌──────────────┐  ┌───────────────┐  │
│  │  Signal     │  │  Workflow    │  │  Health &     │  │
│  │  Ingestion  │  │  Engine      │  │  Throughput   │  │
│  │  + Debounce │  │  State FSM   │  │  Metrics      │  │
│  └─────────────┘  └──────────────┘  └───────────────┘  │
└─────────────────────────────────────────────────────────┘
│                                                         │
┌──────────────┐  ┌──────────────┐  ┌───────────────────┐
│   MongoDB    │  │    Redis     │  │   In-Memory       │
│  (NoSQL)     │  │   (Cache)    │  │   Signal Log      │
│  Work Items  │  │  Hot State   │  │   (Data Lake)     │
└──────────────┘  └──────────────┘  └───────────────────┘

## 🚀 Quick Start

### Prerequisites
- Docker & Docker Compose
- Node.js v18+
- Python 3.11+

### Run with Docker Compose
```bash
git clone https://github.com/akshatha-634/zeotap-ims-assignment
cd zeotap-ims-assignment
docker-compose up --build
```

- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

### Run Locally
```bash
# Backend
cd backend
pip install -r requirements.txt
uvicorn main:app --reload

# Frontend
cd frontend
npm install
npm start
```

## 🏗️ Tech Stack

| Layer | Technology | Reason |
|-------|-----------|--------|
| Frontend | React | Component-based UI, real-time updates |
| Backend | FastAPI (Python) | Async support, auto docs, high performance |
| Cache | Redis | Hot path state, fast reads |
| NoSQL | MongoDB | Raw signal storage (Data Lake) |
| Containerization | Docker + Docker Compose | Reproducible deployments |

## 📡 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /api/ingest | Ingest a new signal |
| GET | /api/work-items | Get all work items |
| GET | /api/signals/raw | Get raw signal log |
| PATCH | /api/work-items/{id}/status | Update work item status |
| GET | /api/throughput | Get signals/sec throughput |
| GET | /health | Health check |

## ⚙️ Key Features

### 1. Signal Debouncing
If 100 signals arrive for the same Component ID within 10 seconds, only ONE Work Item is created. All 100 signals are linked to it in the signal log.

### 2. Workflow State Machine
OPEN → INVESTIGATING → RESOLVED → CLOSED
- Transitions are strictly enforced
- CLOSED requires mandatory RCA submission
- Invalid transitions return 400 error

### 3. Mandatory RCA
Before closing an incident, the responder must fill:
- Incident Start/End time
- Root Cause Category
- Fix Applied
- Prevention Steps

### 4. Rate Limiting & Backpressure
- In-memory signal processing handles burst traffic
- System won't crash if persistence layer is slow
- Throughput metrics exposed every 5 seconds


### 5. Observability
- /health endpoint for liveness checks
- Throughput metrics (signals/sec) on dashboard
- Raw signal audit log retained

### 6. MTTR Calculation
Mean Time To Repair is automatically calculated based on:
- **start_time** — timestamp of first signal received
- **end_time** — timestamp of RCA submission
- MTTR = end_time - start_time

### 7. Alerting Strategy
Different component failures trigger different alert priorities:
- **P0** — Critical (RDBMS failure, MCP Host down) → Immediate response required
- **P1** — High (Cache failure) → Response within 30 minutes
- **P2** — Medium (API Gateway errors) → Response within 2 hours

In production, P0 alerts would trigger PagerDuty/OpsGenie calls, P1 would send Slack notifications, P2 would create tickets.

### 8. Scaling to 10,000 signals/sec
Current implementation uses in-memory buffering which:
- Handles burst traffic without crashing ✅
- Won't fail if persistence layer is slow ✅

In production this would be replaced with:
- **Apache Kafka** as message queue for true 10,000 signals/sec
- **Redis Streams** as lighter alternative
- **MongoDB indexing** on component_id and timestamp for efficient querying
- **Time-series collections** in MongoDB for signal aggregations

## 🧪 Sample Test Data

Run the sample data script to simulate a failure event:
```bash
python3 backend/sample_data.py
```

This simulates:
- RDBMS outage (P0)
- Cache failure (P1)
- API Gateway errors (P2)

## 🔒 Security & Non-Functional

- CORS configured for frontend-backend communication
- Input validation via Pydantic models
- RCA mandatory before incident closure (audit compliance)
- Docker isolation for all services

## 📁 Project Structure

zeotap-ims-assignment/
├── backend/
│   ├── main.py
│   ├── requirements.txt
│   ├── Dockerfile
│   └── app/
│       ├── routes/
│       │   └── signals.py
│       ├── models/
│       │   └── signal.py
│       └── services/
│           └── signal_service.py
├── frontend/
│   ├── src/
│   │   ├── App.js
│   │   └── index.js
│   ├── Dockerfile
│   └── package.json
├── docker-compose.yml
└── README.md

## 👩‍💻 Author
Akshatha Poojari
[GitHub](https://github.com/akshatha-634) | [LinkedIn](https://linkedin.com/in/akshatha-poojari)
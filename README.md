# Learning Forex Academy

A responsive forex education platform for structured learning, chart education, quizzes and student progress tracking.

## Current foundation
- React + TypeScript + Vite frontend
- Responsive student learning dashboard with illustrative sample data
- FastAPI backend with a health endpoint
- Environment-based backend configuration template

## Run locally

### Frontend
```bash
npm install
npm run dev
```

### Backend
Python 3.11+ is recommended.
```bash
python -m venv .venv
# Windows: .venv\\Scripts\\activate
# macOS/Linux: source .venv/bin/activate
pip install -r backend/requirements.txt
uvicorn backend.main:app --reload --port 8000
```
API health check: http://localhost:8000/api/health

## Planned delivery
1. Web MVP: authentication, course management, lessons, quizzes, progress and admin tools.
2. Offline-ready learning: cache selected materials for use without a connection.
3. Android and iOS applications after validating the web MVP.

## Scope note
The current dashboard uses demonstration content only. Authentication, database persistence, email verification, password recovery, course authoring, quizzes and production deployment are not implemented yet. This is an educational platform, not a brokerage or trade-execution service. Forex trading involves substantial risk; educational content must not promise profits or guaranteed returns.

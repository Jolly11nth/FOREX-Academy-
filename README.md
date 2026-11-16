# Learning Forex Academy

Responsive forex education platform for structured lessons, chart education and student progress.

## Stack
- Frontend: React, TypeScript, Vite
- API: FastAPI
- Database: PostgreSQL (SQLite fallback for local quick-start)
- Password storage: Argon2 password hashing
- Authentication: signed JWT access tokens
- Email: SMTP for verification and password reset links

## Run locally
### API
Python 3.11+ recommended.
```bash
python -m venv .venv
# Windows: .venv\\Scripts\\activate
# macOS/Linux: source .venv/bin/activate
pip install -r backend/requirements.txt
# Copy backend/.env.example to backend/.env and set JWT_SECRET
uvicorn backend.main:app --reload --port 8000
```
If DATABASE_URL is not set, the API uses a local SQLite database. For PostgreSQL, set DATABASE_URL to a PostgreSQL connection string.

### Frontend
```bash
npm install
npm run dev
```
Set VITE_API_URL in a root .env file if the API is not running at http://localhost:8000.

## Authentication endpoints
- POST /api/auth/register
- POST /api/auth/verify-email
- POST /api/auth/login
- GET /api/auth/me (Bearer token)
- POST /api/auth/password-reset/request
- POST /api/auth/password-reset/confirm

Email verification is required before login. Configure SMTP settings in backend/.env to deliver verification and reset emails. In development without SMTP, the generated links are printed in the API terminal. Password reset requests always return a generic response to avoid disclosing whether an email is registered.

## Security and production checklist
- Set a long, random JWT_SECRET and keep all secrets in the hosting provider's environment settings.
- Configure SMTP and the exact production frontend origin in CORS_ORIGINS and APP_URL.
- Use managed PostgreSQL with encrypted connections and automated backups.
- Use HTTPS in production.
- Add database migrations (Alembic), rate limiting, monitoring and security testing before public launch.
- Never commit real credentials or .env files.

The current dashboard course/progress figures are sample UI data. Course authoring, quizzes, real progress persistence and admin management are later milestones. This is an educational platform, not a brokerage or trade execution service. Forex involves substantial risk; learning materials must not promise profits or guaranteed returns.

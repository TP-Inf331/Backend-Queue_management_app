# Queue Management Backend (Extended)
This is an expanded FastAPI backend scaffold (async SQLAlchemy + Postgres) with added endpoints:
- Admin user management (list, update, delete)
- Reporting endpoints (queue stats, avg wait time)
- Ticket features: cancel ticket, ticket history, export CSV per queue
- Pagination and search on lists
- Notifications placeholder

Run:
1. Copy .env.example to .env and edit.
2. Start Postgres and the app (docker-compose provided) or run locally.
3. Visit /api/docs for interactive API.

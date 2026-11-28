# AGENTS.md

LibreEkklesia is a free and open source (AGPL-3.0) church management website for small churches: public site, member portal and back office in one install the church owns. Current work: phase 0 of `docs/plan.md`.

## Decisions

Decisions live in `docs/`. Before starting a task, read the documents it touches:

- `docs/scope-decisions.md`: principles in priority order, the eight security rules, MVP rows, outer wall, roadmap. Wins every conflict.
- `docs/stack-decisions.md`: stack, dependency policy, updates, backups, tests. Second.
- `docs/plan.md`: phases, task IDs, roles, definition of done. Follows both.
- `docs/feature-catalog.md`: catalog row IDs such as `WEB-05`.

When a task seems to need a different decision, stop and ask the owner. Decision changes land as dated entries in the decision document, with the owner's sign-off.

## Workflow

- One task per issue, branch and pull request. Branch names: `<phase>/<slug>`, for example `p0/backend-skeleton`.
- Commits follow Conventional Commits (`feat:`, `fix:`, `docs:`, `test:`, `ci:`, `chore:`).
- Fill in the pull request template and close the task's issue with `Closes #N`.
- Each pull request is a vertical slice that leaves `main` working.
- A task is done when its "Done when" line and the definition of done in `docs/plan.md` both hold.

## Guardrails

- Every change keeps the eight security rules (`docs/scope-decisions.md`, section 4).
- Add a dependency only with a written reason in the pull request, pinned with hashes and past the release-age delay (`docs/stack-decisions.md`, section 2). Frontend files are vendored.
- Pages load only from the site's own origin.
- The security-reviewer agent approves every change to sign-in, sessions, permissions, people data, backups or the updater. Builders get their work reviewed by another agent.
- Secrets and personal email addresses stay out of the repository. Security reports go through `SECURITY.md`.
- Work outside the MVP rows or behind the outer wall (`docs/scope-decisions.md`, sections 3 and 6) waits for an owner decision.

## Commands

Add Python dependencies with `uv add` in `backend/` and browser-app dependencies with `pnpm add` in `frontend/`, and commit both lockfiles. Run backend tests with `uv run pytest` in `backend/`; they use the production settings. Other `manage.py` commands default to the production settings too, which refuse to start without `DJANGO_SECRET_KEY`, `DJANGO_ALLOWED_HOSTS` and `LIBREEKKLESIA_DATA_DIR`; for local work set `DJANGO_SETTINGS_MODULE=config.settings.development`. After changing the API, run `pnpm run api:generate` in `frontend/` and commit the description and types. In `frontend/`, `pnpm test` runs the unit tests and `pnpm run typecheck` checks the types. `pnpm run dev` serves the browser app at `http://localhost:5173/app/` and forwards `/api` to the backend's development server (`manage.py runserver`, on its default `127.0.0.1:8000`); `pnpm run build` writes `dist/`, which is not committed. To run the whole bundle, copy `.env.example` to `.env`, set `DJANGO_SECRET_KEY`, and run `docker compose up --build` from the repository root; it serves `https://localhost` with a certificate from Caddy's local authority, and `python3 deploy/smoke_test.py` checks it. `docker build --file deploy/web.Dockerfile --target test .` runs the backend tests inside the web image.

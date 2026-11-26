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

Add Python dependencies with `uv add` in `backend/` and browser-app dependencies with `pnpm add` in `frontend/`, and commit both lockfiles. Build and test commands arrive with P0-06 and P0-08 and live in their project files.

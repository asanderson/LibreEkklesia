# LibreEkklesia — technology stack decisions

**Status:** signed off by the owner on 23 November 2026, at the close of the stack interview. Sections 1 to 10 record the owner's answers. Section 11 records six defaults Claude proposed and the owner accepted, with search changed by the owner.

Companion to `scope-decisions.md` (principles, scope, security rules), `feature-catalog.md` and `plan.md` (delivery phases). Principle and rule numbers below refer to the scope document. If the two documents disagree, the scope document wins.

Source of truth: the `docs/` folder of https://github.com/asanderson/LibreEkklesia. Copies elsewhere, such as the claude.ai project, may lag behind.

## Summary

| Layer | Decision |
|---|---|
| Shape | API backend plus a single-page app for the member portal and staff admin. Public site is static HTML generated at publish time. |
| Backend | Django 6.1 now, 6.2 at its release, with Django Ninja for the REST API |
| Sign-in | django-allauth in headless mode. Members: emailed one-time code. Staff: passkey or authenticator code. |
| Database | SQLite, one file per church, code kept portable to PostgreSQL |
| Hosting model | One isolated instance per church |
| Browser app | Vue 3 with a fixed eight-item allowlist, no server rendering |
| Content | Own structured content in the own admin app, Trix for rich text |
| Public site | Django templates write static HTML. No Node in production. |
| Search | Public site: static index written at publish. Portal and admin: SQLite full-text search (FTS5). One search interface in project code. |
| Bundle | Docker Compose: Caddy, Django under Gunicorn, one task worker |
| Updates | Own updater on the host, signed images, snapshot, health check, automatic rollback |
| Backups | restic to an off-server destination chosen in the setup wizard, plus a local copy |
| Code host | GitHub: public repository asanderson/LibreEkklesia, Actions and container registry |

## 1. Architecture

1. **Language.** Any language was acceptable. The stack was chosen against the six guiding principles, not by language preference.
2. **Shape.** An API backend plus a single-page app. The single-page app covers the member portal and the staff admin only.
3. **Public site.** Static pages, generated when content is published. The public files hold no member data and need no session. This is how security rule 2 (public site walled off from member data) is met by structure, not only by permission checks.
4. **Sessions.** Everything is served from one origin. Sessions are cookies that scripts cannot read, with cross-site request protection. No tokens are kept in browser storage. Bearer tokens are reserved for outside API clients, later.
5. **API.** REST with an OpenAPI description. The browser app talks to it through a typed client generated from that description.
6. **Database.** SQLite, one database file per church, on that instance's data volume. Code stays portable to PostgreSQL.
7. **Hosting model.** One isolated instance per church. "Ready for multi-church hosting" is met by isolation (each church has its own containers, database file and backups), not by tenant columns in a shared database.

## 2. Dependency policy

Five rules. They apply to the backend, the browser app, build tools and the release pipeline.

1. The dependency list is short. Every addition needs a written reason.
2. Exact versions are pinned with hashes. New releases wait about 7 days before adoption. Security fixes are the exception.
3. Frontend files are vendored. No package registry is contacted at install time or at runtime.
4. Builds are reproducible, releases are signed, and a bill of materials is published with each release.
5. The release pipeline is isolated and holds no long-lived publish tokens.

**Tools (settled by spike P0-05, 26 November 2026).**

- **Python: uv.** `backend/pyproject.toml` holds version ranges and `backend/uv.lock` pins exact versions with hashes, so the lockfile is the pin. `add-bounds = "minor"` makes `uv add` cap each new range below the next minor version. `exclude-newer = "7 days"` holds back new uploads, and the lockfile keeps that setting relative. uv itself is pinned through `required-version`.
- **Browser app: pnpm.** `frontend/package.json` pins exact versions (`saveExact`) and `frontend/pnpm-lock.yaml` adds integrity hashes. `minimumReleaseAge: 10080` (7 days) holds back new releases. pnpm is pinned through `packageManager`, and `onlyBuiltDependencies: []` keeps dependency install scripts off unless a package is allowed by name.
- **Vendored frontend files.** The browser app is built into the release image, so a church's server never contacts a package registry. Build output (`dist/`) is not committed.
- **Security-fix exception.** Python: add the package to `exclude-newer-package` in `backend/pyproject.toml`, with a cutoff just after the fix's upload. Browser app: add it to `minimumReleaseAgeExclude` in `frontend/pnpm-workspace.yaml`. Name the advisory in the pull request, and remove the exception once the release is older than 7 days.
- **Container images.** The Dockerfiles in `deploy/` pin base images by digest, chosen from the history in docker-library's repo-info records at least 7 days old. Inside the builds, uv is installed from hashes (`deploy/requirements-uv.txt`) and Corepack checks pnpm against the hash in `packageManager`.
- **Check.** `tools/check_release_age.py` takes the newest release younger than 7 days on each side and tries to add it. It passes only when both are refused because of their age, fails when either is accepted, and reports inconclusive when nothing young enough exists.

## 3. Backend

- **Framework.** Django with Django Ninja for the REST API and its OpenAPI description. FastAPI was the owner's first pick. The choice moved to Django to keep the batteries-included rule: sign-in, sessions, migrations, mail, templates and security middleware come from one maintained project.
- **Versions.** Django 6.1 now. Move to 6.2 when it is released (due April 2027). After that, follow Django's yearly releases.
- **Built-in admin.** Django's built-in admin is switched off in production. The staff admin is the project's own Vue app, using the same API as everything else.
- **Background jobs.** Django's Tasks framework. The backend for it is default 1 in section 11.

## 4. Sign-in

- django-allauth in headless mode, which exposes sign-in as an API for the Vue app.
- **Members:** an emailed one-time code. No passwords.
- **Staff and admins:** a passkey, or a second step with an authenticator-app code. One of the two is enforced (security rule 1).

**Refinement of the scope document.** The scope document first said members use a "passwordless email link". The stack interview settled on an emailed one-time code instead. The idea is the same (no password, proof of access to the mailbox); only the delivery differs. The scope document was updated to match on 23 November 2026.

## 5. Browser app (member portal and staff admin)

Selection rule: smallest third-party footprint, with agent familiarity as the tie-break. React was the owner's first pick. The choice moved to Vue after review. Main reason recorded: Vue's router and state library are maintained by the Vue project itself, which keeps the third-party list shorter.

The allowlist. Anything not on it needs a written reason.

1. Vue 3, stable line, in the browser only. No server rendering, no Nuxt, no Vapor mode until it is stable.
2. Vue Router, on the 4.x line while it gets fixes. Version 5 adds a file-based routing build plugin, with its dependencies, that the app does not use.
3. Pinia, only when shared state outgrows plain composables.
4. The generated OpenAPI client: types generated by openapi-typescript from the backend's OpenAPI description, called through openapi-fetch, a typed wrapper over plain `fetch` whose only dependency, openapi-typescript-helpers, holds types (settled by P0-07). No data-fetching library.
5. Native HTML elements first (dialog, popover, details, date input). Reka UI only where native elements fall short, such as a combobox or menu.
6. Forms through Vue's built-in binding and native validation.
7. One translation library: vue-i18n.
8. Build tools: Vite with its official Vue plugin, TypeScript and vue-tsc only. TypeScript stays on 5.9 until vue-tsc and openapi-typescript support TypeScript 7, which drops the JavaScript compiler API they use. While vue-i18n 11's declarations need a type from Vue 3.6, the type check skips every declaration file (`skipLibCheck`), so project files stay `.ts` to remain checked.

Accessibility target is WCAG 2.2 AA (principle 2), checked automatically on every page (section 10).

## 6. Content and public site

- **Content model.** The project's own structured content, edited inside its own admin app: fixed page types, announcements, events and sermons. Version history, scheduling and expiry are plain features of that model, not a separate content management product.
- **Publishing.** Django templates write static HTML at publish time. A theme is a set of templates plus a stylesheet. No Node runs in production. The owner's first pick was pre-rendering with the frontend framework; it was changed to keep Node out of production.
- **Rich text.** Trix in the admin. The server cleans submitted HTML against an allowlist of tags and attributes; the editor is never trusted.
- **Consequence: time-dependent pages.** Upcoming events and expiring announcements (the self-updating rows `CAL-12`, `WEB-05`, `WEB-12`, `WEB-20`) are kept current by regenerating the affected pages from a scheduled job. The site stays static and does not go stale.
- **Implementation note.** A content security policy that allows only the site's own origin enforces security rule 3 (nothing loaded from third parties) on both the static pages and the app.

## 7. Bundle

Docker Compose, with three processes from two images.

1. **Caddy.** Automatic HTTPS. Serves the generated public site and the built admin and portal files. Forwards only API calls to Django.
2. **Django under Gunicorn**, with synchronous workers.
3. **One worker process** for queued and scheduled jobs, from the same image as Django. Exactly one.

**As built (P0-09, 28 November 2026).** `compose.yaml` at the repository root; images from `deploy/web.Dockerfile` (Python 3.13 slim on Debian trixie, running as a non-root user) and `deploy/caddy.Dockerfile` (Caddy on Alpine, with the browser app built in a Node stage). The web container runs the deploy check, SQLite's full-text search included, and the migrations before Gunicorn starts; Gunicorn runs two synchronous workers. The worker takes a lock on the data volume, so a second one refuses to start. Volumes: the database, media and the generated public site, which Caddy mounts read-only, plus Caddy's certificates. Only Caddy publishes ports. Every container runs as a non-root user with a read-only file system, no capabilities and no way to gain privileges. Caddy reads a whole API request body (1 MB at most) before Gunicorn's synchronous workers see it, and cuts off clients that send headers or bodies slowly.

Podman with its built-in auto-update and rollback was the alternative. The owner chose Docker Compose, and the guardrails in section 8 were adopted to cover what that feature would have provided.

Operator experience stays as locked in the scope document: one copy-paste guide once, then everything in the web admin. Pilot runs on a small cloud server inside the $10 per month ceiling.

## 8. Updates

These seven guardrails implement security rule 4 (automatic security updates) and the signed update channel. All seven were adopted.

1. The updater runs on the host as a systemd timer. The web app never gets access to the Docker socket.
2. The release pipeline signs every image without stored keys (Sigstore) and publishes a signed list of image digests.
3. The updater verifies signature and digest before it applies anything.
4. A database snapshot is taken before the update and a health check runs after it. If the check fails, the updater returns to the previous digest and snapshot on its own.
5. The "Update now" button and the update status in the admin work through a request file, not a privileged API.
6. Staged rollout: the pilot gets each release first. The public channel follows 3 days later unless the release is pulled.
7. The install script turns on the host operating system's automatic security patches.

## 9. Backups

Implements security rule 5 (encrypted automatic backups with a restore test from the admin).

- restic, to a destination chosen in the setup wizard: S3-compatible storage or SFTP. A local copy is kept as well.
- The wizard does not finish without an off-server destination. Its cost counts toward the $10 per month ceiling.
- The recovery key is shown once, is printable, and is to be recorded by two people.

## 10. Code host, tests and releases

- **Code host.** GitHub: the public repository https://github.com/asanderson/LibreEkklesia (chosen 25 November 2026), with Actions and the GitHub container registry.
- **Pipeline hardening.** Every Action pinned by commit hash. Least-privilege tokens. No long-lived publish secrets.
- **Releases.** Reproducible builds, images signed through Sigstore without stored keys, a signed digest list and a published bill of materials (dependency rule 4, update guardrails 2 and 3).

Test and scan set. All of it is development-only, pinned, and none of it ships in the product.

| Purpose | Tools |
|---|---|
| Backend tests and checks | pytest with its Django plugin, ruff, strict type checking |
| Browser app tests and checks | Vitest, ESLint, vue-tsc |
| End-to-end and accessibility | Playwright with axe checks on every page (the WCAG 2.2 AA gate) |
| Dependency audit | pip-audit and npm audit on every change and nightly |
| Static analysis | CodeQL for Python and JavaScript |
| Dynamic scan | ZAP baseline on every change; full active scan per release against a test deployment |
| Image scan | Container image scan, with the scanner itself pinned by digest |

This set is the "automated scans on every change" item of the security review gate in the scope document.

## 11. Defaults proposed by Claude (accepted 23 November 2026)

These were not asked as interview questions. Claude proposed each from a locked rule. The owner accepted 1 and 3 to 6 as proposed and changed 2 (search).

1. **Job queue.** django-tasks-db as the backend for Django's Tasks framework, run by its database worker. Exactly one worker process, because the project has warned that several workers on SQLite can run the same job twice. The same worker wakes on a timer for scheduled jobs, such as scheduled publishing and expiry.
2. **Search.** The owner first asked for self-hosted Elasticsearch or OpenSearch. After review (section 13), the owner chose this instead:
   - **Public site:** a small search index file written at publish time from published public content only, and a small script served from the same origin. No outside search service (security rule 3) and no live query path from anonymous visitors.
   - **Member portal and staff admin:** SQLite's built-in full-text search (FTS5), inside the church's database file. Stemming, relevance ranking and prefix matching, with no new dependency.
   - **One small search interface** in the project's code, so the engine behind it can change (PostgreSQL full-text search after a move to PostgreSQL, or a later search module) without touching the code that calls it.
   - **Later:** a search engine module for large installs goes to the later pool, OpenSearch preferred.
   - **Consequences of locked rules:** results pass the same permission checks as the records themselves. Children never appear in member-facing search (security rule 7). Index changes happen in the same transaction as the record change, so a deleted or hidden record leaves search at once. The index sits inside the database file, so backups and encryption cover it with no extra step.
3. **Media files.** Sermon audio and images live on a local volume and are included in backups. Video hosting stays outside the core, as the scope document's outer wall says.
4. **Email.** Sent through the church's own mail account over SMTP, using Django's built-in mail support. Transactional email only in the MVP.
5. **Monitoring.** No third-party error tracking or analytics. Logs stay on the server. A health page in the admin reports system status.
6. **Public input.** The contact form is the only place an anonymous visitor can submit content. It is rate-limited and spam-guarded without a third-party CAPTCHA, and submissions wait in the review inbox (security rule 2).

## 12. Deferred to spikes or later

Named so that nothing is silently assumed. Each is settled by a small prototype or at the point of use.

| Item | When |
|---|---|
| Python lockfile tool and frontend package manager that support the release-age delay | Settled 26 November 2026 by P0-05: uv and pnpm (section 2) |
| Check that the chosen base image's SQLite has FTS5 compiled in | Settled 28 November 2026 by P0-09: SQLite 3.46.1 in `python:3.13.18-slim-trixie` has FTS5 with the porter tokenizer, and the web container refuses to start without it (system check `core.E001`) |
| OpenAPI client generator | Settled 26 November 2026 by P0-07: openapi-typescript and openapi-fetch (section 5) |
| HTML sanitizer library for the server-side allowlist | Before the rich-text editor ships (drop 1) |
| Trix keyboard and screen-reader behaviour | Spike before drop 1 commits to it |
| Public site search script: own small script or a vendored library, under the dependency rule | Drop 1 |
| Updater prototype (verify, snapshot, health check, rollback) | Before the pilot install |
| One supported server distribution for the installer | Before the pilot install |
| Google Workspace mail relay details for the pilot | Before the pilot install |
| Restore drill | Security review gate, before drop 2 |
| Which process runs restic and holds the backup credentials, and whether the destination can be made append-only | Threat model and restore drill, before drop 2 |
| PDF library for the printed directory | Drop 2 |
| SQLite runs in WAL mode (P0-06), so backups and update snapshots must copy the database through SQLite's backup API, never as a plain file copy | D1-03 backups, P0-14 updater |
| Search tokenizer for languages other than English (Porter stemming covers English only) | When translation work starts |

## 13. Considered and not chosen

- **FastAPI.** Owner's first pick for the backend. Not kept because it breaks the batteries-included rule: as found in November 2026 it was still on 0.x versions and its usual sign-in add-on was being superseded, so sign-in would have been assembled from parts.
- **React.** Owner's first pick for the browser app. Replaced by Vue under the smallest-footprint rule (section 5).
- **Pre-rendering public pages with the frontend framework.** Owner's first pick. Replaced by Django templates to keep Node out of production.
- **Elasticsearch or OpenSearch in the core bundle.** Owner's first pick for search. Kept out of the core for four reasons. (1) The Java engine needs far more memory than the rest of the bundle; at DigitalOcean prices that pushes the server past the $10 per month ceiling, though this reason depends on the provider. (2) It adds a fourth container with its own security patches, plus a host kernel setting the installer would have to change. (3) Public search would need a live, anonymous query path from the public site into the backend; today the public site's only path into the app is the contact form. (4) It would be the largest dependency in the stack, for a few hundred pages of content. Moved to the later pool as an optional module. OpenSearch is preferred if it comes in: it is a Linux Foundation project, while only part of the Elasticsearch source carries an AGPL option.
- **Podman with built-in auto-update.** Considered. Owner chose Docker Compose with the section 8 guardrails.
- **Watchtower** (automatic container updates for Docker). Rejected: the project was archived on 17 December 2025.
- **Tiptap and Markdown-only editing.** Not chosen for rich text. Tiptap has a larger dependency footprint; Markdown is harder for non-technical editors. Trix has one dependency.
- **ASP.NET Core with Angular, and Laravel.** Reviewed as batteries-included alternatives. Not chosen.

## 14. Evidence checked (November 2026)

Facts looked up by web search during the interview. Sources were cited in the interview conversation. Version numbers go stale: check again before relying on one.

- **Django.** 5.2 is the long-term support line with security fixes to April 2028. 6.0 (3 December 2025) added built-in content security policy support and the Tasks framework. 6.1 was released on 5 August 2026. 6.2 is due in April 2027. A yearly release cycle starts in 2028.
- **Django Ninja.** 1.8.0, tested against Django 5.2, 6.0 and 6.1.
- **django-allauth.** Offers login by emailed code, a headless API and Django Ninja support.
- **Base images (P0-09).** Checked on 28 November 2026 in docker-library's repo-info history: `python:3.13.18-slim-trixie` as published on 7 November, `caddy:2.11.9-alpine` on 13 November and `node:22.23.5-trixie-slim` on 11 November. Newer rebuilds of the Python and Node images (24 November) were inside the 7-day delay.
- **Gunicorn.** 27.0.1, uploaded on 12 November 2026, with no dependencies of its own.
- **django-tasks-db.** Provides the database worker (`db_worker`). An older warning says several workers on SQLite risk running a job twice.
- **FastAPI.** 0.163.0 on 14 November 2026, still a 0.x version. FastAPI Users was being superseded.
- **Vue.** Stable line is 3.5.x. 3.6 with Vapor mode was still a release candidate. Vue 4 is planned without breaking API changes. Vue Router and Pinia are official projects.
- **Reka UI.** v2.11.0, follows WAI-ARIA patterns, and pulls in one TanStack virtual-list package.
- **React.** React2Shell (CVE-2025-55182, 3 December 2025, severity score 10) affected server components.
- **Angular.** 22 was released on 3 June 2026, supported to June 2028, with yearly major versions.
- **.NET.** 10 is the long-term support line, to 14 November 2028.
- **Laravel.** 13 was released on 17 March 2026 with first-party passkeys.
- **Supply-chain incidents in 2026.** axios (31 March), the TanStack build pipeline (11 May), PyPI packages including LiteLLM and durabletask, and the Trivy GitHub Action (19 March). These motivated the dependency policy and the Action pinning.
- **Container updates.** Podman's auto-update rolls back by default. Watchtower was archived on 17 December 2025.
- **Caddy.** v2.11.4. Version 2.11.1 in February 2026 fixed six security advisories.
- **restic.** 0.19.1. Repositories are always encrypted.
- **Trix.** v2.1.18, MIT licence, one dependency.
- **cosign (Sigstore).** v3.1.4.
- **ZAP.** 2.17.0, now "ZAP by Checkmarx", Apache-2.0 licence. The baseline scan is passive.
- **GitHub.** Code scanning, secret protection, artifact attestations and private vulnerability reporting are free for public repositories.
- **SQLite full-text search.** Checked in the work environment on 23 November 2026: SQLite 3.53.1 with FTS5 compiled in. Porter stemming, prefix queries, the bm25 ranking function and the trigram tokenizer all worked. The product's base image still needs the same check (section 12).
- **Elasticsearch and OpenSearch.** Both projects' Docker Desktop guides ask for at least 4 GB of memory (a desktop setup figure, not a server minimum). OpenSearch defaults to a 1 GB Java heap. OpenSearch needs the host's `vm.max_map_count` at 262144 or more even under Docker; Elasticsearch's production Docker guide asks for 1048576. OpenSearch is a Linux Foundation project. In 2024 Elastic added AGPL as a licence option for part of the Elasticsearch source, next to SSPL and the Elastic License.
- **Server prices.** DigitalOcean Basic plans: 1 GB for $6, 2 GB for $12 and 4 GB for $24 a month (third-party price lists, 2026). Other providers price differently.
- **uv and pnpm.** Checked on 26 November 2026: uv 0.11.32 accepts a relative `exclude-newer` such as "7 days" and stores it as a span in `uv.lock`, so `uv lock --locked` stays stable. pnpm 10.28.0 enforces `minimumReleaseAge`. In the check, uv refused boto3 1.44.12 (17 hours old) and pnpm refused TypeScript 7.1.0-dev.20261126.1 (5 hours old); with both delays removed, the same check failed on both sides.
- **OpenAPI client tools.** Checked on 26 November 2026 by counting the packages each candidate adds to the browser app: openapi-typescript with openapi-fetch 33 (2 at runtime, with no further dependencies), @hey-api/openapi-ts 72, swagger-typescript-api 92, orval 111. TypeScript's latest release, 7.0.2, is the native port and has no JavaScript compiler API; vue-tsc and openapi-typescript (peer `^5.x`) need one, so TypeScript is pinned to 5.9.3.
- **Vue Router.** Checked on 28 November 2026: 5.5.1 has 16 direct dependencies, most of them for its file-based routing build plugin; 4.6.5 (13 November 2026) has one. Moving the app from 5.5.1 to 4.6.5 removed 37 of 177 packages from the browser app's lockfile.
- **vue-i18n and Vue 3.6.** Checked on 28 November 2026: the type declarations of every vue-i18n 11 release tried (11.3.2, 11.4.0, 11.4.12 and 11.4.23) import `GenericComponentInstance` from Vue, and so does 11.4.24 (26 November). Vue's 3.6 release candidate (3.6.0-rc.17, 27 November) exports it; the stable 3.5.45 does not.

## 15. Still open

- The spikes in section 12.
- Items the scope document lists as open (its section 14).
- Delivery phases and per-phase tasks: see `plan.md`.

## Change log

- 22 November 2026: first version, written for the read-back at the close of the stack interview.
- 23 November 2026: owner accepted defaults 1 and 3 to 6 and changed search (section 11, item 2; section 13). Status set to signed off. Scope document aligned: member sign-in wording, search module in the later pool, pointer to this document.
- 24 November 2026: open items now point to the scope document's list instead of repeating it (the owner dropped the MVP target date).
- 25 November 2026: moved into the repository's `docs/` folder. Cross-references use file names, the code host names the development repository, and the next step points to `plan.md`.
- 26 November 2026: spike P0-05 settled the dependency tools: uv for Python and pnpm for the browser app, with the release-age delay, the security-fix exception and a check script (section 2).
- 26 November 2026: spike P0-07 settled the OpenAPI client: openapi-typescript generates the types and openapi-fetch calls the API. TypeScript is pinned to 5.9 (section 5).
- 28 November 2026: P0-08 built the frontend skeleton. Vue Router stays on the 4.x line, Vite's official Vue plugin is named in the build tools, and type checks skip declaration files until Vue 3.6, because of vue-i18n 11 (sections 5 and 14).
- 28 November 2026: P0-09 built the bundle skeleton (section 7): pinned base images, Gunicorn, the single-worker lock and the start-up check for SQLite's full-text search (sections 2, 12 and 14).

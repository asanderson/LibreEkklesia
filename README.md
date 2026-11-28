# LibreEkklesia

Free and open source church management website for small churches: a public website, a member portal and a back office in one install that the church owns.

**Status:** pre-alpha. Phase 0 (foundations) is under way, and there is no usable release yet.

## Principles

In priority order: security and privacy (including data ownership), usability and easy operation, modularity, total cost of ownership, extensibility, and interoperability. The full record is in [`docs/scope-decisions.md`](docs/scope-decisions.md).

## Run it locally

With Docker and Docker Compose: copy `.env.example` to `.env`, set `DJANGO_SECRET_KEY` to at least 50 random characters, and run `docker compose up --build`. The site answers at https://localhost (the certificate comes from Caddy's local authority, so the browser warns once) and the app at https://localhost/app/.

## Docs

- [`docs/README.md`](docs/README.md): index of decisions and plans.
- [`docs/plan.md`](docs/plan.md): delivery phases, tasks and the definition of done.

## Security

Report vulnerabilities privately, as described in [`SECURITY.md`](SECURITY.md).

## License

[AGPL-3.0](LICENSE).

# The web server image: Caddy with the built browser app (docs/stack-decisions.md, section 7).
# Build from the repository root: docker build --file deploy/caddy.Dockerfile .
# Base images are pinned by digest and were at least 7 days old when chosen (section 2).

FROM node:22.23.5-trixie-slim@sha256:68c76cfad89921b927eae28ba21407475e29d0ce450afcdbe70c1532db042b64 AS app
# Corepack installs the pnpm release that frontend/package.json names, and checks its hash.
ENV COREPACK_ENABLE_DOWNLOAD_PROMPT=0
RUN corepack enable
WORKDIR /src/frontend
COPY frontend/package.json frontend/pnpm-lock.yaml frontend/pnpm-workspace.yaml ./
RUN pnpm install --frozen-lockfile
COPY frontend/ ./
# A church that runs a changed version points the footer's source link at its own published
# source (AGPL-3.0, section 13).
ARG VITE_SOURCE_URL=
RUN pnpm run build

FROM caddy:2.11.9-alpine@sha256:003a97808e781aa9f7e75cc2f43d34d461099031faf5e20faefb9f61126836f0
COPY deploy/Caddyfile /etc/caddy/Caddyfile
COPY --from=app /src/frontend/dist /srv/app
ENV LIBREEKKLESIA_HOST=localhost
# Validating provisions Caddy's local certificate authority, so it runs against throwaway
# storage: no key may end up in the image.
RUN XDG_DATA_HOME=/tmp/caddy-validate XDG_CONFIG_HOME=/tmp/caddy-validate \
        caddy validate --config /etc/caddy/Caddyfile --adapter caddyfile \
    && rm -rf /tmp/caddy-validate
# Caddy runs as its own user. New volumes for its certificates take this ownership, in place of
# the base image's world-writable folders; /srv/site is the mount point for the public site,
# which the web container writes and Caddy only reads.
RUN addgroup -S -g 10002 caddy \
    && adduser -S -D -H -u 10002 -G caddy -s /sbin/nologin caddy \
    && mkdir -p /data/caddy /config/caddy /srv/site \
    && chown -R caddy:caddy /data /config \
    && chmod 0700 /data/caddy /config/caddy
USER caddy

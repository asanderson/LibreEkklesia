import createClient, { type Middleware } from "openapi-fetch";

import type { paths } from "./schema";

// Django's CSRF cookie (backend/config/settings/base.py). It is readable by scripts by design;
// the session cookie is not.
const CSRF_COOKIE = "__Host-csrftoken";
const UNSAFE_METHODS = new Set(["POST", "PUT", "PATCH", "DELETE"]);

/** Reads one cookie's value from a `document.cookie` style string. */
export function readCookie(name: string, cookies: string = document.cookie): string | undefined {
  const prefix = `${name}=`;
  const match = cookies.split("; ").find((part) => part.startsWith(prefix));
  return match?.slice(prefix.length);
}

/** Sends the CSRF token on same-origin requests that change data, as Django expects. */
export function csrfMiddleware(
  getToken: () => string | undefined,
  siteOrigin: () => string,
): Middleware {
  return {
    onRequest({ request }) {
      const origin = siteOrigin();
      const sameOrigin = new URL(request.url, origin).origin === origin;
      if (sameOrigin && UNSAFE_METHODS.has(request.method)) {
        const token = getToken();
        if (token !== undefined) {
          request.headers.set("X-CSRFToken", token);
        }
      }
      return request;
    },
  };
}

/**
 * Typed client for the LibreEkklesia API, generated from src/api/openapi.json.
 * Requests stay on the site's own origin, so the session cookie travels with them
 * and no token is kept in browser storage.
 */
export const api = createClient<paths>({ credentials: "same-origin" });
api.use(
  csrfMiddleware(
    () => readCookie(CSRF_COOKIE),
    () => window.location.origin,
  ),
);

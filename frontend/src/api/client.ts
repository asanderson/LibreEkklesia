import createClient, { type Middleware } from "openapi-fetch";

import type { paths } from "./schema";

// Django's CSRF cookie (backend/config/settings/base.py). It is readable by scripts by design;
// the session cookie is not.
const CSRF_COOKIE = "__Host-csrftoken";
const UNSAFE_METHODS = new Set(["POST", "PUT", "PATCH", "DELETE"]);

function readCookie(name: string): string | undefined {
  const prefix = `${name}=`;
  const match = document.cookie.split("; ").find((part) => part.startsWith(prefix));
  return match?.slice(prefix.length);
}

/** Sends the CSRF token on same-origin requests that change data, as Django expects. */
const csrf: Middleware = {
  onRequest({ request }) {
    const sameOrigin = new URL(request.url, window.location.href).origin === window.location.origin;
    if (sameOrigin && UNSAFE_METHODS.has(request.method)) {
      const token = readCookie(CSRF_COOKIE);
      if (token !== undefined) {
        request.headers.set("X-CSRFToken", token);
      }
    }
    return request;
  },
};

/**
 * Typed client for the LibreEkklesia API, generated from src/api/openapi.json.
 * Requests stay on the site's own origin, so the session cookie travels with them
 * and no token is kept in browser storage.
 */
export const api = createClient<paths>({ credentials: "same-origin" });
api.use(csrf);

import type { Middleware } from "openapi-fetch";
import { describe, expect, it } from "vitest";

import { csrfMiddleware, readCookie } from "./client";

type OnRequestParams = Parameters<NonNullable<Middleware["onRequest"]>>[0];

const SITE = "https://church.example";

async function send(method: string, url: string, token: string | null = "token-123") {
  const middleware = csrfMiddleware(
    () => token ?? undefined,
    () => SITE,
  );
  const request = new Request(url, { method });
  const result = await middleware.onRequest?.({ request } as OnRequestParams);
  return result instanceof Request ? result : request;
}

describe("csrfMiddleware", () => {
  it.each(["POST", "PUT", "PATCH", "DELETE"])("sends the token on a same-origin %s", async (method) => {
    const request = await send(method, `${SITE}/api/things`);
    expect(request.headers.get("X-CSRFToken")).toBe("token-123");
  });

  it.each(["GET", "HEAD", "OPTIONS"])("leaves a safe %s alone", async (method) => {
    const request = await send(method, `${SITE}/api/things`);
    expect(request.headers.has("X-CSRFToken")).toBe(false);
  });

  it("never sends the token to another origin", async () => {
    const request = await send("POST", "https://elsewhere.example/api/things");
    expect(request.headers.has("X-CSRFToken")).toBe(false);
  });

  it("sends nothing when there is no token", async () => {
    const request = await send("POST", `${SITE}/api/things`, null);
    expect(request.headers.has("X-CSRFToken")).toBe(false);
  });
});

describe("readCookie", () => {
  it("finds the CSRF cookie among others", () => {
    expect(readCookie("__Host-csrftoken", "a=1; __Host-csrftoken=abc123; b=2")).toBe("abc123");
  });

  it("ignores a cookie whose name only ends the same way", () => {
    expect(readCookie("__Host-csrftoken", "x__Host-csrftoken=wrong")).toBeUndefined();
  });

  it("returns undefined when the cookie is absent", () => {
    expect(readCookie("__Host-csrftoken", "a=1")).toBeUndefined();
  });
});

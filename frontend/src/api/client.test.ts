import type { Middleware } from "openapi-fetch";
import { afterEach, describe, expect, it, vi } from "vitest";

import { api, csrfMiddleware, readCookie } from "./client";

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

  it("treats the default port as the same origin", async () => {
    const request = await send("POST", "https://church.example:443/api/things");
    expect(request.headers.get("X-CSRFToken")).toBe("token-123");
  });

  it.each([
    ["another port", "https://church.example:8443/api/things"],
    ["another scheme", "http://church.example/api/things"],
    ["a subdomain", "https://evil.church.example/api/things"],
    ["a look-alike host", "https://church.example.evil.example/api/things"],
    ["another site", "https://elsewhere.example/api/things"],
  ])("never sends the token to %s", async (_label, url) => {
    const request = await send("POST", url);
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

describe("the shared api client", () => {
  afterEach(() => {
    vi.unstubAllGlobals();
  });

  // Returns the X-CSRFToken header the client sends from a page on SITE with these cookies.
  async function tokenSent(method: "get" | "post", baseUrl: string): Promise<string | null> {
    vi.stubGlobal("document", { cookie: "csrftoken=decoy; __Host-csrftoken=real-token" });
    vi.stubGlobal("window", { location: { origin: SITE } });
    let sent: Request | undefined;
    const fetch = async (request: Request) => {
      sent = request;
      return new Response("{}", { headers: { "Content-Type": "application/json" } });
    };
    if (method === "get") {
      await api.request("get", "/api/health", { baseUrl, fetch });
    } else {
      // @ts-expect-error -- the API has no POST route yet; this only drives the middleware.
      await api.request("post", "/api/health", { baseUrl, fetch });
    }
    return sent?.headers.get("X-CSRFToken") ?? null;
  }

  it("sends the __Host-csrftoken cookie on a same-origin POST", async () => {
    expect(await tokenSent("post", SITE)).toBe("real-token");
  });

  it("sends no token on a GET", async () => {
    expect(await tokenSent("get", SITE)).toBeNull();
  });

  it("sends no token when a request points at another origin", async () => {
    expect(await tokenSent("post", "https://elsewhere.example")).toBeNull();
  });
});

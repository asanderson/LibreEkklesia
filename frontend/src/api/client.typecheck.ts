// Compile-time checks for the generated client, run by `pnpm run typecheck`. Never imported by the app.
// Each `@ts-expect-error` must fire: if a misuse starts compiling, the directive itself becomes an error.
import { api } from "./client";
import type { components } from "./schema";

type Equal<A, B> = (<T>() => T extends A ? 1 : 2) extends <T>() => T extends B ? 1 : 2 ? true : false;
type Expect<T extends true> = T;

export async function healthStatus(): Promise<string | undefined> {
  const { data } = await api.GET("/api/health");
  // The response keeps its generated type; a widening to `any` fails here.
  type DataIsHealth = Expect<Equal<typeof data, components["schemas"]["Health"] | undefined>>;
  const proof: DataIsHealth = true;
  void proof;
  return data?.status;
}

export function rejectsMisuse() {
  return [
    // @ts-expect-error: only paths in the API description are allowed.
    api.GET("/api/no-such-path"),
    // @ts-expect-error: /api/health has no POST operation.
    api.POST("/api/health"),
    // @ts-expect-error: /api/health takes no query parameters.
    api.GET("/api/health", { params: { query: { verbose: true } } }),
    // @ts-expect-error: a GET request has no body.
    api.GET("/api/health", { body: { status: "ok" } }),
  ];
}

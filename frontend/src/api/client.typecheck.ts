// Compile-time checks for the generated client, run by `pnpm run typecheck`. Never imported by the app.
import { api } from "./client";

export async function healthStatus(): Promise<string | undefined> {
  const { data } = await api.GET("/api/health");
  return data?.status;
}

export function rejectsPathsOutsideTheDescription() {
  // @ts-expect-error: only paths in the API description are allowed.
  return api.GET("/api/no-such-path");
}

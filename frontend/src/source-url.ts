// AGPL-3.0 section 13: people using a changed version over the network must be offered its
// source. A church that builds a changed version sets VITE_SOURCE_URL to where it publishes
// that source; unchanged builds point at the project's repository. vite.config.mjs runs this
// check on the value Vite builds with, so a bad address stops the build instead of shipping a
// broken link.
export const PROJECT_SOURCE_URL = "https://github.com/asanderson/LibreEkklesia";

export function sourceUrl(configured: unknown): string {
  const value = typeof configured === "string" ? configured.trim() : "";
  if (value === "") {
    return PROJECT_SOURCE_URL;
  }
  let url: URL | undefined;
  try {
    url = new URL(value);
  } catch {
    url = undefined;
  }
  if (url?.protocol !== "https:" && url?.protocol !== "http:") {
    throw new Error(`VITE_SOURCE_URL must be an absolute http or https address, not "${value}".`);
  }
  // The normalized form: the browser would resolve a sloppy one such as "https:/host" against
  // the page instead.
  return url.href;
}

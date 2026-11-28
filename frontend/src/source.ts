// AGPL-3.0 section 13: people using a changed version over the network must be offered its
// source. A church that builds a changed version sets VITE_SOURCE_URL to where it publishes
// that source; unchanged builds point at the project's repository.
export const PROJECT_SOURCE_URL = "https://github.com/asanderson/LibreEkklesia";

export function sourceUrl(configured: unknown): string {
  return typeof configured === "string" && configured.trim() !== ""
    ? configured.trim()
    : PROJECT_SOURCE_URL;
}

export const SOURCE_URL = sourceUrl(import.meta.env.VITE_SOURCE_URL);

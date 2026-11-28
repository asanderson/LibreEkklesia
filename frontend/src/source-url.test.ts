import { describe, expect, it } from "vitest";

import { PROJECT_SOURCE_URL, sourceUrl } from "./source-url";

describe("sourceUrl", () => {
  it("points at the project's repository by default", () => {
    expect(sourceUrl(undefined)).toBe(PROJECT_SOURCE_URL);
    expect(sourceUrl("  ")).toBe(PROJECT_SOURCE_URL);
  });

  it("uses the source address a changed build was given", () => {
    expect(sourceUrl(" https://git.example.org/church/libreekklesia ")).toBe(
      "https://git.example.org/church/libreekklesia",
    );
  });

  it("links to the address as parsed, so a sloppy one still leaves the site", () => {
    expect(sourceUrl("https:/git.example.org/church")).toBe("https://git.example.org/church");
  });

  it.each([
    ["no scheme", "git.example.org/church/libreekklesia"],
    ["a script", "javascript:alert(1)"],
    ["another scheme", "ftp://git.example.org/church"],
  ])("refuses an address with %s", (_label, value) => {
    expect(() => sourceUrl(value)).toThrow("VITE_SOURCE_URL must be an absolute http or https");
  });
});

import { describe, expect, it } from "vitest";

import { PROJECT_SOURCE_URL, sourceUrl } from "./source";

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
});

# LibreEkklesia scope decisions

Record of the feature-scoping interview, 14–18 November 2026. Companion to `feature-catalog.md`: IDs such as `GIV-04` refer to rows in that catalog, and `[S]`, `[D]`, `[R]` are its prevalence tags (standard, differentiating, rare). "Locked" items were confirmed by the project owner. The technology stack is recorded separately in `stack-decisions.md`, and the delivery phases in `plan.md`.

Source of truth: the `docs/` folder of https://github.com/asanderson/LibreEkklesia. Copies elsewhere, such as the claude.ai project, may lag behind.

**Status:** signed off by the owner on 18 November 2026. Every feature-scope branch has been visited and the interview is closed. Section 14 lists what remains open outside feature scope. Updated on 23 November 2026 to match the signed-off stack decisions: member sign-in wording (section 4 and the MVP table in section 6) and a search module in the later pool (section 8). On 24 November 2026 the owner dropped the MVP target date (section 6). On 25 November 2026 the owner kept the name after the name check and chose the development repository (sections 2 and 14).

## 1. Guiding principles (locked)

Priority order. When two principles conflict, the lower number wins.

1. Security and privacy. Includes data ownership: the church controls its own data, with full export and tested restore.
2. Usability, ease of use, operations and maintenance, with minimal technical skills required. Includes accessibility of public pages (WCAG 2.2 AA).
3. Modularity: start with a minimum viable product (MVP) and add optional modules in later phases.
4. Total cost of ownership.
5. Extensibility.
6. Interoperability with existing applications, tools and services.

## 2. Foundations (locked)

- **Target church:** small, under about 200 people, run by a volunteer or part-time administrator.
- **Countries:** US first, built for translation, multiple currencies and pluggable tax receipts. Currencies and tax receipts stay dormant until a giving or payments module arrives.
- **Delivery:** self-host first, one church per install, with a data model ready for multi-church hosting. A hosted option follows right after the pilot (section 10).
- **Operator:** someone who follows one copy-paste install guide once. Everything afterwards (updates, backups, restore, health check) happens in the web admin.
- **Product boundary:** back office, member portal and public website, with a site builder that replaces the church's own site.
- **Differentiators:** data ownership with no lock-in, and everything in one install with no per-module cost. Privacy is default behavior. Giving and child check-in sit in the later pool (section 8), so "everything in one" describes the direction, not the MVP.
- **License:** AGPL-3.0. The footer of the member portal and staff admin links to the source code, the license and the third-party licenses (owner, 28 November 2026). A church that runs a changed version points the source link at its own published source, as section 13 of the license asks.
- **Builder:** the project owner, working solo and managing a team of role-based agents.
- **Development repository:** https://github.com/asanderson/LibreEkklesia, on the owner's personal GitHub account (chosen 25 November 2026).
- **Pilot:** Eastside Church of Christ. LibreEkklesia replaces its current website (https://welcome.eastside-churchofchrist.org/, built on Google Sites). The church uses Google Workspace.

## 3. Derived from the principles (owner raised no objection)

- **Site builder type:** structured site in the MVP (fixed church page types filled from church data, rich-text pages, themes, no layout editing). A block builder comes later as an optional module. Free-form drag-and-drop is never built.
- **Self-updating content:** the public site reads from church data. Committed rows: `CAL-12` (site calendar publishes from internal events), `WEB-05` (announcements with start and expiry dates), `WEB-12` (scheduled publishing), `WEB-20` (stale-page audit).
- **Depth rule:** a module enters with its `[S]` rows only. Any `[D]` or `[R]` row needs a named reason: a principle, a pilot need or an earlier decision.
- **Outer wall:** the following stay outside the core. The core integrates with them instead of building them. Any of them could return only as an optional module.
  1. Fund ledger, payables and payroll (`FIN-01..08`). A simple ledger may be revisited after the core ships.
  2. Video hosting and native streaming (`SER-03`, `STR-02..04`). Embed YouTube or Vimeo instead.
  3. Projection. Hand off to OpenLP or FreeShow (`WOR-10`).
  4. Branded store apps and TV apps (`POR-06`, `POR-07`, `POR-09`). Ship an installable web app instead (`POR-08`).
  5. Payment processing. No payment code exists for now (section 9). A later payments module would use a church-owned Stripe or PayPal account (`GIV-26`).
  6. Email and SMS delivery. Use the church's own provider accounts (`API-11`).
  7. Background-check ordering. Recording results and expiry dates sits in the later pool with safeguarding records.
  8. Sacramental registers and diocesan roll-ups (`REG-04..07`, `REG-10`, `MUL-06`).

## 4. Security rules (locked, all hard)

None of these can be switched off by an administrator.

1. Two-factor sign-in or a passkey is enforced for every staff and admin account (`SEC-06`, `SEC-08`).
2. The public site is walled off from member data. Public form submissions wait in a review inbox before they touch people records.
3. Public pages load nothing from third parties. Video and map embeds are click-to-load.
4. Security updates install automatically.
5. Backups are automatic and encrypted, and restore can be tested from the admin (`SEC-16`).
6. Sensitive data has an audit trail, and money records are never hard-deleted (`SEC-09`, `RUL-07`). The money clause stays dormant until a giving or payments module exists.
7. Children are hidden from the directory and from search, and the directory is opt-in (`POR-02`, `POR-03`).
8. AI features and outside connectors stay off until an admin opts in (`AI-13`).

Consequences:

- Google Calendar, Google Maps and YouTube never load inline. The calendar is native, the map is an image plus a link, and video is click-to-load.
- The project must run a signed update channel.
- Members sign in without a password, using a one-time code sent by email (`POR-11`), so the strict rules land on staff only.

## 5. Module mechanics (locked)

- Modules are first-party only and are toggled per church in the admin. There is one codebase and one release.
- A public extension API comes later, with reviewed or signed plugins.

## 6. MVP (locked)

**Contents:** kernel, website, and people with households, member directory and portal. 56 catalog rows: 27 standard, 29 pulled in by a principle, a pilot need or an earlier decision.

**Staging:** two drops.

- Drop 1: public site with no member data, live at the pilot.
- Drop 2: people, directory and portal, after the security review gate in section 11.

**Target date:** none. On 24 November 2026 the owner chose not to track one; the earlier plan was to date only the MVP.

**Rows:**

| Area | In the MVP | Deferred |
|---|---|---|
| Kernel (`SEC`) | 01 preset roles, 06 enforced 2FA, 08 passkeys, 09 audit trail, 10 admin approves every new account, 16 backup and restore. Also a setup wizard, web-based updates, a health check and a self-hosted spam guard on forms. | 02 field-level security, 07 single sign-on (the provider's 2FA cannot be verified, which clashes with rule 1), 12 field encryption |
| People (`PPL`) | 01 profile, 02 households, 04 custom fields, 06 tags, 07 smart lists, 09 duplicate merge, 11 membership status and dates, 14 archive, 15 self-service edits with approval, 18 consents and emergency contact only | 08 notes (wait for the care module), 18 medical and allergy data (wait for check-in) |
| Portal (`POR`) | 01 portal for profile and household, 02 opt-in directory, 03 per-field privacy with children hidden, 04 PDF photo directory, 08 installable web app, 11 passwordless sign-in for members, 13 members-only pages, 16 delete-my-account and consent controls | Store and TV apps (outer wall) |
| Website (`WEB`) | 01 themes and structured pages, 02 church content types, 04 news with RSS, 05 announcements with expiry, 06 HTTPS, own domain and redirects from old URLs, 07 page version restore, 08 SEO fields, 09 structured data, 11 simple editor role, 12 scheduled publishing, 13 site search, 18 alt text and WCAG 2.2 AA, 20 stale-page audit | 03 plan-a-visit alerts, 10 reusable sections, 17 multilingual content, 19 analytics |
| Sermons (`SER`) | 01 library by series, speaker, topic and book, 02 hosted audio and click-to-load video, 04 podcast feed, 07 attachments, 08 scripture links | Notes, transcripts, AI repurposing |
| Calendar and events | `CAL-01` calendar, `CAL-02` iCal feed, `CAL-12` site calendar publishes itself, `CAL-13` import from Google Calendar, `EVT-01` events with public pages. Also a fixed contact form with a review inbox. | Rooms, registrations, form builder |
| Import and export (`MIG`) | 01 people import, 06 CSV export, 08 test import with undo, 10 per-person data sheet. Also a full-instance export in an open format. | Giving history, named importers, other systems' formats |
| Privacy (`PRV`) | 01 consent log, 02 access and erasure requests, 03 data-flows page listing every outside service, 04 and 05 children hidden and opt-in directory | |
| Email | Sign-in codes, invites and form alerts only, sent through the church's own mail account | Bulk email (communications module) |

Give and Pay links to a church's existing provider are ordinary links on pages. The MVP contains no payment code.

## 7. Pilot hosting and cost (locked)

- Eastside's install runs on a small cloud server, roughly $5–10 a month.
- Cost ceiling for a church of about 150 people: $10 a month all-in, with no mandatory paid services.

## 8. Roadmap after the MVP (locked)

**Order of optional modules:**

1. **Communications.** Bulk email with unsubscribe and member preferences (`COM-01`, `COM-03`, `COM-04`, `COM-14`), and a weekly digest built from announcements and the calendar (`COM-20`).
2. **Groups and attendance** (`GRP`, `ATT`). Classes, rosters, leader tools, headcounts.
3. **Follow-up and care** (`FLW`, `PPL-08`). Visitor pipeline, tasks, prayer requests, private notes.
4. **Volunteer scheduling** (`VOL`). Service rosters, accept or decline, block-out dates. Ships without background-check tracking: `VOL-13`, `VOL-16` and `VOL-17` are excluded.
5. **Forms and registrations** (`EVT`). Registrations record "paid offline". Online payment (`EVT-03`) is excluded.

**Row picks:** rows for each module are chosen at the start of its phase, using the depth rule and pilot feedback. The rows named above are indicative.

**Later pool** (unscheduled; each may return as an optional module):

- Giving records
- Online payments
- Child check-in, together with safeguarding records (screening and training dates, concern log)
- Rooms and resources
- Worship planning
- Report builder
- API and MCP
- Block builder
- Multilingual content
- SMS
- Search engine for large installs (OpenSearch preferred). The core searches with SQLite's built-in full-text search and a static index on the public site.

The hosted option runs as a parallel track right after the pilot.

## 9. Money (locked)

- No payment code exists anywhere for now.
- Registrations record "paid offline".
- Give and Pay are links to the church's existing provider.
- An optional payments module is planned for later and sits in the later pool, as do giving records.

## 10. Hosted option (locked)

- **Timing:** right after the pilot.
- **Operator:** the owner personally, free and best effort, at first. A legal entity (LLC or nonprofit) with an at-cost fee and written data-processing terms takes over some time after the service is fully operational.
- **Guardrails during the personal phase:**
  1. Invite-only, capped at about 5 churches.
  2. Plain-language terms and a privacy notice from the first hosted church: who holds the data, backups, breach notice, exit with full export.
  3. A human penetration test is passed first.
  4. The legal entity is formed before any fee is charged or the cap is passed, whichever comes first.
- **Suggested, not decided:** a short legal consult before hosting a second church.

## 11. Security review gate (locked)

Before member data enters (drop 2):

1. Written threat model.
2. Audit of the kernel by a separate security-reviewer agent, not the builder agents.
3. Automated scans on every change: dependency audit, static analysis, and a scan of a running instance.
4. Restore drill: a backup restored on a clean machine.
5. Published security contact and disclosure policy (`INC-04`).

Before hosting other churches: a human penetration test.

## 12. Pilot site inventory (fetched 15 November 2026)

- **Pages (14):** Home; About Us, with God's Plan of Salvation, Organization and Structure, and Worship; Announcements, with two posts; Contact Us; Events Calendar; History of Eastside; Map & Directions; Sermons; Worship and Study.
- **Embeds:** Google Calendar (agenda view, three source calendars), Google Maps, and one Google Drive folder on the sermons page with no files visible.
- **Absent on the pages checked:** giving, livestream, forms, member login.
- **Present:** site search, Bible references linked to BibleGateway.
- **Freshness:** the newest announcement is stamped December 2023.
- **Service times listed:** Sunday 10:00 am Bible study (children's and adult classes), 11:00 am worship, 6:00 pm worship; Wednesday 7:00 pm Bible study.

## 13. Scope readings (locked)

The owner confirmed these readings on 18 November 2026.

1. Safeguarding records sit in the later pool together with child check-in. Neither is gone for good.
2. Safeguarding in scope is limited to security rule 7 (children hidden from the directory and from search). The round-one phrase "privacy and safeguarding by default" narrows accordingly.
3. Rows never named in this record are not planned. Examples: in-app chat, push notifications, multi-campus, operations extras, online-church features. They can enter only through the depth rule at the start of a phase. The outer wall stays "never by the core".

## 14. Open, outside feature scope

Nothing is open. The name check ran on 24 November 2026 (`name-check.md`). On 25 November 2026 the owner kept the name LibreEkklesia. The follow-ups that came with that option (registering the domains, and a trademark attorney screen before drop 1 goes public) are tracked in `plan.md`.

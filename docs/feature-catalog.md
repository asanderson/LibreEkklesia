# Church software feature catalog (compact)

Compact checklist for LibreEkklesia scope decisions. Derived mechanically from the research report "Church management software feature landscape" (15 November 2026, `feature-landscape.md`), which holds the evidence: which products offer each feature, with source links.

**396 features, 24 areas.** Prevalence tags: `[S]` standard = parity floor, found in most products (105); `[D]` differentiating = sizeable minority or several leaders (108); `[R]` rare = one to a few products (183).

Caveats: tags are judgments from vendor pages, changelogs and repositories, not measured market share. Nothing was tested hands-on. IDs (for example `GIV-04`) are stable handles for scope discussions.

## Areas

1. `PPL` People and households: 20 features (10 S, 6 D, 4 R)
2. `FLW` Follow-up, workflows and care: 22 features (8 S, 6 D, 8 R)
3. `GRP` Groups: 17 features (5 S, 2 D, 10 R)
4. `ATT` Attendance: 10 features (4 S, 1 D, 5 R)
5. `CHK` Child check-in: 20 features (10 S, 3 D, 7 R)
6. `EVT` Events, registrations and forms: 21 features (7 S, 4 D, 10 R)
7. `CAL` Calendar, rooms and resources: 15 features (4 S, 2 D, 9 R)
8. `VOL` Volunteer scheduling: 18 features (7 S, 8 D, 3 R)
9. `WOR` Worship planning: 16 features (4 S, 3 D, 9 R)
10. `GIV` Giving: 32 features (12 S, 12 D, 8 R)
11. `FIN` Finance and accounting: 13 features (1 S, 6 D, 6 R)
12. `COM` Communications: 23 features (6 S, 10 D, 7 R)
13. `POR` Member portal, app and directory: 20 features (4 S, 7 D, 9 R)
14. `WEB` Website and CMS: 25 features (5 S, 5 D, 15 R)
15. `SER` Sermons and media: 15 features (4 S, 4 D, 7 R)
16. `STR` Streaming and online church: 14 features (1 S, 1 D, 12 R)
17. `REP` Reporting and dashboards: 14 features (4 S, 3 D, 7 R)
18. `MUL` Multi-campus and hierarchy: 9 features (1 S, 3 D, 5 R)
19. `SEC` Permissions, security and audit: 16 features (2 S, 7 D, 7 R)
20. `API` Integrations and API: 12 features (1 S, 7 D, 4 R)
21. `MIG` Import, export and migration: 10 features (4 S, 1 D, 5 R)
22. `AI` AI: 13 features (1 S, 4 D, 8 R)
23. `REG` Regional and tradition-specific modules: 14 features (0 S, 3 D, 11 R)
24. `OPS` Operations extras: 7 features (0 S, 0 D, 7 R)

## 1. People and households (`PPL`)

Market pattern: custom fields and self-refreshing lists are universal.

- **PPL-01** `[S]` Individual profile gathering contact data, photo and activity history (attendance, giving, serving, groups)
- **PPL-02** `[S]` Households with roles (head, parent or guardian, child), shared or separate addresses, family-level reports
- **PPL-03** `[D]` Relationships beyond one household: custom relationships, blended families, linked related families, proxy contact for a minor
- **PPL-04** `[S]` Custom fields (text, date, checkbox, dropdown), custom tabs, layouts per person type, conditional fields, per-field access
- **PPL-05** `[R]` Church-defined tables and data-model extensions
- **PPL-06** `[S]` Tags and ad hoc groupings, including converting tags into groups
- **PPL-07** `[S]` Rule-based smart lists and saved searches (all, any or none conditions; automatic refresh; usable as a message audience)
- **PPL-08** `[S]` Profile notes by category (prayer, counselling, health) with private or role-restricted visibility
- **PPL-09** `[S]` Duplicate detection and merge
- **PPL-10** `[D]` Bulk editing: bulk actions on lists, spreadsheet-style editor, reports that mass-update records
- **PPL-11** `[S]` Membership status, key dates and milestones (baptism, offices served, enrol and drop dates)
- **PPL-12** `[D]` Automatic school-grade or age-group promotion
- **PPL-13** `[D]` Skills, interests, giftedness and personality assessments
- **PPL-14** `[R]` Archiving inactive people while keeping their history
- **PPL-15** `[S]` Member self-service updates to profile and household, with validation or staff approval
- **PPL-16** `[D]` Maps and geocoding (people map, neighbour finder)
- **PPL-17** `[D]` Files and documents attached to a profile
- **PPL-18** `[S]` Medical, allergy and emergency-contact data; stored consents (photo, data use)
- **PPL-19** `[R]` Address-change verification against postal data
- **PPL-20** `[R]` Data-quality tooling (automatic cleanser, missing-data searches)

## 2. Follow-up, workflows and care (`FLW`)

Market pattern: form-fed pipelines replaced process queues.

- **FLW-01** `[S]` Multi-step follow-up pipelines with step owners, due dates and notifications
- **FLW-02** `[D]` Kanban or visual board of people moving through steps
- **FLW-03** `[S]` Form submissions that create or advance a workflow card
- **FLW-04** `[S]` Rule-based automations (update fields, send email or text, create tasks, add to or remove from groups, change roles, scheduled routines)
- **FLW-05** `[D]` Timed message sequences and drip campaigns (guest welcome series, devotional series)
- **FLW-06** `[D]` Process templates (guest follow-up, membership, baptism, volunteer onboarding, background-check renewal)
- **FLW-07** `[S]` Tasks assigned to staff or volunteers with email and text reminders
- **FLW-08** `[R]` "My cards" and stuck-people views across workflows
- **FLW-09** `[S]` Digital connection cards and first-visit forms shared by link or QR code
- **FLW-10** `[S]` First-time visitor, absentee and lapsed-attender lists and alerts
- **FLW-11** `[D]` Discipleship pathways, journeys or steps with milestones
- **FLW-12** `[R]` Engagement stages or a weighted engagement score
- **FLW-13** `[D]` Pastoral care records and care apps (private notes, care cases, care board, crisis alerts)
- **FLW-14** `[R]` Care-needs board and meal trains
- **FLW-15** `[R]` Structured visitation tracking (visit types, time since last visit, families not visited)
- **FLW-16** `[S]` Prayer-request intake with private routing
- **FLW-17** `[D]` Public prayer wall, with moderation at Nucleus
- **FLW-18** `[R]` Appointment booking with pastors or counsellors
- **FLW-19** `[R]` Benevolence, alms and welfare requests
- **FLW-20** `[S]` Automated birthday and anniversary messages and date reminders
- **FLW-21** `[R]` Shared inbox that turns emails, form responses and booking requests into cases
- **FLW-22** `[R]` Span-of-care oversight across leaders and their groups

## 3. Groups (`GRP`)

Market pattern: finders and leader tools are standard; confidentiality options are not.

- **GRP-01** `[S]` Group types and categories (small groups, classes, ministries, teams, staff, elders)
- **GRP-02** `[S]` Public group finder filtered by life stage, day, time and location
- **GRP-03** `[R]` Map or proximity search in the finder
- **GRP-04** `[S]` Join modes: open sign-up, request or approval, closed or private
- **GRP-05** `[R]` Confidential groups (roster hidden from members) and link-only groups
- **GRP-06** `[R]` Member caps and capacity
- **GRP-07** `[S]` Leader tools without full admin rights: roster, attendance, messaging, notes
- **GRP-08** `[S]` Group events and meeting schedule, RSVP with guest counts, group calendar
- **GRP-09** `[D]` Shared files and resources per group
- **GRP-10** `[D]` Group health and participation reports (growth, drop-off, attendance frequency)
- **GRP-11** `[R]` Automated prompts asking leaders to report attendance
- **GRP-12** `[R]` Subgroups
- **GRP-13** `[R]` Prayer and care needs inside a group
- **GRP-14** `[R]` Curriculum or study material pushed to groups
- **GRP-15** `[R]` Group sign-up with a custom form and fee
- **GRP-16** `[R]` Courses and learning management (quizzes, prerequisites)
- **GRP-17** `[R]` Mentor programme

## 4. Attendance (`ATT`)

Market pattern: solved for the room, unsolved for the stream.

- **ATT-01** `[S]` Individual attendance for services, classes, groups and events
- **ATT-02** `[S]` Headcount entry, including from a phone
- **ATT-03** `[S]` Automatic attendance from check-in
- **ATT-04** `[S]` Attendance dashboards and trend reports filtered by date, campus, ministry and demographics
- **ATT-05** `[D]` Absence alerts and threshold-based follow-up
- **ATT-06** `[R]` Barcode, QR, NFC or USSD attendance capture
- **ATT-07** `[R]` In-person versus online attendance; check-in for online viewers
- **ATT-08** `[R]` Importers for attendance history and custom metrics
- **ATT-09** `[R]` Post-event attendance summaries emailed to leaders
- **ATT-10** `[R]` Planned-absence records

## 5. Child check-in (`CHK`)

Market pattern: matched codes are standard; pickup lists, ratios and printers separate products.

- **CHK-01** `[S]` Station modes: staffed, self-service kiosk, classroom roster, phone or tablet
- **CHK-02** `[S]` Family lookup by phone, name, QR code or barcode, with on-the-spot guest creation
- **CHK-03** `[S]` Pre-check-in at home in the app or on the web, then a QR scan on arrival
- **CHK-04** `[S]` Matching security code on the child's tag and the parent's pickup label, regenerated at each check-in
- **CHK-05** `[D]` Label designer and configurable tag content
- **CHK-06** `[S]` Label-printer support (Brother, Zebra, Dymo, Citizen) over Wi-Fi, Bluetooth, AirPrint, USB or LAN
- **CHK-07** `[S]` Allergy, medical and special-needs alerts on tags and rosters
- **CHK-08** `[D]` Authorised and barred pickup lists, with guardian photos
- **CHK-09** `[S]` Check-out by code, QR or barcode scan, or classroom roster, with a record of who collected the child
- **CHK-10** `[R]` Security code texted to the parent in place of a printed label; check-in by text keyword
- **CHK-11** `[D]` Room capacity limits with automatic closing, redirection and room balancing
- **CHK-12** `[R]` Volunteer-to-child ratio and support-needs tracking
- **CHK-13** `[S]` Parent paging and emergency texts from a station or classroom
- **CHK-14** `[S]` Live class rosters and dashboards with check-in and check-out times; roll call
- **CHK-15** `[S]` Volunteer and team check-in with name tags
- **CHK-16** `[R]` Volunteer check-in blocked when no cleared background check is on file
- **CHK-17** `[R]` Session suggested by age or grade; automatic room assignment
- **CHK-18** `[R]` Whole-family check-in in one action
- **CHK-19** `[R]` All-ages event or building check-in with entry rules
- **CHK-20** `[R]` Required-form verification, emergency-contact prompts at the kiosk, belongings tracking

## 6. Events, registrations and forms (`EVT`)

Market pattern: paid sign-ups everywhere, ticketing and voting almost nowhere.

- **EVT-01** `[S]` Events with recurring and multi-day schedules and public event pages
- **EVT-02** `[S]` Online registration with custom questions, confirmations and add-to-calendar
- **EVT-03** `[S]` Registration payments by card, wallet or bank debit, plus recording of cash and cheques
- **EVT-04** `[S]` Attendee or ticket types with their own price and availability; capacity caps
- **EVT-05** `[R]` Waitlists
- **EVT-06** `[D]` Discount codes, early-bird and date-based fees, scholarships, group discounts, family maximum fee
- **EVT-07** `[D]` Deposits, partial payments, instalments and automatic balance reminders
- **EVT-08** `[D]` Household and multi-person registration with pre-filled data
- **EVT-09** `[R]` Add-on purchases and "what to bring" item sign-ups
- **EVT-10** `[R]` Automatic attendee grouping (buses, cabins, tables)
- **EVT-11** `[R]` Attached waivers and medical forms, agreement steps, e-signatures
- **EVT-12** `[S]` RSVPs with guests, and RSVP-versus-attended tracking
- **EVT-13** `[R]` Ticketing with reserved seating and in-person sales
- **EVT-14** `[D]` Mission-trip management and per-participant fundraising pages
- **EVT-15** `[S]` General form builder with conditional logic, file upload, payments, embeds, link and QR sharing
- **EVT-16** `[S]` Forms that create or update people records
- **EVT-17** `[R]` Submitting a form on behalf of household members
- **EVT-18** `[R]` Polls and surveys
- **EVT-19** `[R]` Secure member voting and elections (one vote per member, anonymity, nominations)
- **EVT-20** `[R]` Sign-up by text message
- **EVT-21** `[R]` Non-charitable payment forms and paid memberships

## 7. Calendar, rooms and resources (`CAL`)

Market pattern: conflict-checked booking is common, yet two leaders skip it.

- **CAL-01** `[S]` Central calendar with categories or tags; multiple and per-ministry calendars
- **CAL-02** `[S]` Website embed and iCal, Google and Outlook subscription feeds
- **CAL-03** `[S]` Room and equipment catalogue with capacities, layouts, setup and teardown times
- **CAL-04** `[S]` Conflict detection and double-booking prevention
- **CAL-05** `[D]` Approval routing (an approver per room or resource, approval by several groups, auto-approval)
- **CAL-06** `[D]` Event and room request forms for staff or the public (weddings, funerals, outside hirers)
- **CAL-07** `[R]` Recurring bookings and maintenance blockouts
- **CAL-08** `[R]` Alternative-room suggestions when a room is taken
- **CAL-09** `[R]` Bookable services (childcare, catering, AV crew) and quantity-based equipment
- **CAL-10** `[R]` Heating and cooling control tied to bookings
- **CAL-11** `[R]` Utilisation statistics
- **CAL-12** `[R]` Public website calendar that publishes itself from internal events
- **CAL-13** `[R]` iCal import and Google Calendar sync
- **CAL-14** `[R]` Booking rules restricted by user group; custom booking questions
- **CAL-15** `[R]` Duty planning for paid and volunteer staff in the calendar

## 8. Volunteer scheduling (`VOL`)

Market pattern: accept or decline and block-outs everywhere; automation marks the leaders.

- **VOL-01** `[S]` Teams with positions and required headcounts
- **VOL-02** `[S]` Schedule requests accepted or declined by email, app or text
- **VOL-03** `[S]` Block-out and unavailability dates, including recurring ones
- **VOL-04** `[S]` Automatic reminders and chasing of non-responders
- **VOL-05** `[D]` Auto-scheduling from availability, preferences, last-served date and frequency
- **VOL-06** `[S]` Volunteer-initiated swaps and replacement requests
- **VOL-07** `[S]` Self sign-up sheets for open slots
- **VOL-08** `[R]` Household preferences (serve together or apart) and household scheduling
- **VOL-09** `[D]` Frequency preferences, monthly limits and global serving limits
- **VOL-10** `[D]` Clash and conflict alerts across teams
- **VOL-11** `[R]` Matrix or grid view across dates and plans
- **VOL-12** `[D]` Gap alerts and digests for unfilled positions
- **VOL-13** `[D]` Role requirements (background check, training) enforced when scheduling
- **VOL-14** `[D]` Published opportunities, applications, matching by gifts or availability, onboarding pipeline
- **VOL-15** `[D]` Serving history and hours tracking
- **VOL-16** `[S]` Background checks ordered and tracked from the profile (Checkr, MinistrySafe, Protect My Ministry, Verified First, Sterling)
- **VOL-17** `[D]` Safe-environment and training status tracking
- **VOL-18** `[R]` Overseer or team-leader role that manages a rota without back-office access

## 9. Worship planning (`WOR`)

Market pattern: order of service plus song library, with licence reporting as the edge.

- **WOR-01** `[S]` Order of service or run sheet with drag-ordered, timed items, notes and templates
- **WOR-02** `[R]` Several service times, or several services planned side by side
- **WOR-03** `[R]` Live run sheet showing the current item, with countdown
- **WOR-04** `[S]` Song library with arrangements, keys, tempo, tags, copyright fields and files
- **WOR-05** `[D]` Chord charts with transposition and ChordPro import
- **WOR-06** `[S]` Import from SongSelect, PraiseCharts or MultiTracks
- **WOR-07** `[R]` Rehearsal audio: media player, looping, audio transposition
- **WOR-08** `[D]` Digital music stand or on-stage app with annotations
- **WOR-09** `[R]` Automatic song-usage reporting for CCLI
- **WOR-10** `[D]` Hand-off to presentation software (ProPresenter, OpenLP, FreeShow, Quelea, Songbeamer, OpenSong)
- **WOR-11** `[S]` Attachments and a media library per plan or song
- **WOR-12** `[R]` Song usage history and filters by last use
- **WOR-13** `[R]` Rehearsal reminders
- **WOR-14** `[R]` Public plan view and customised PDF printing
- **WOR-15** `[R]` Bible readings, lesson scheduling and digital signage inside plans
- **WOR-16** `[R]` Free shared song library with charts and slide export

## 10. Giving (`GIV`)

Market pattern: recurring, wallets, text and statements are standard; tap and non-cash gifts are the new edge.

- **GIV-01** `[S]` Online one-time and recurring gifts by card and bank debit
- **GIV-02** `[S]` Digital wallets (Apple Pay, Google Pay; less often PayPal or Samsung Pay)
- **GIV-03** `[S]` Guest giving without an account
- **GIV-04** `[S]` Text-to-give by keyword
- **GIV-05** `[S]` Embeddable form, branded giving pages on the church's domain, give links and QR codes
- **GIV-06** `[D]` Tap and contactless giving (NFC tags, tap-to-pay on a phone, terminals)
- **GIV-07** `[R]` Lobby kiosk giving
- **GIV-08** `[S]` Donor-covered processing fees
- **GIV-09** `[S]` Funds and designations with split gifts
- **GIV-10** `[S]` Pledge campaigns with goals, progress and recurring fulfilment
- **GIV-11** `[S]` Batch entry of cash and cheques with fund splits
- **GIV-12** `[R]` Batch control totals, closing before posting, approvals and a separate permission to reopen
- **GIV-13** `[D]` Cheque scanning with donor matching, stored images and remote deposit
- **GIV-14** `[S]` Giving statements for any period by email, print or self-service download; individual, joint or household
- **GIV-15** `[S]` Donor portal: history, statements, recurring-gift and payment-method management
- **GIV-16** `[D]` Automatic card updater and failed-gift recovery
- **GIV-17** `[D]` Stock and cryptocurrency gifts, usually through Engiven
- **GIV-18** `[D]` In-kind, donor-advised-fund, QCD and IRA gift recording; non-deductible payments flagged
- **GIV-19** `[S]` Giving reports by donor, fund, type, campus and campaign, with CSV export
- **GIV-20** `[D]` New-giver and lapsed-giver alerts, recurring-income forecast, giving bands
- **GIV-21** `[D]` Bank-statement or processor import with automatic donor matching
- **GIV-22** `[D]` Deposit and payout reconciliation (gross versus net, deposits view)
- **GIV-23** `[D]` Regional bank rails: UK Direct Debit, SEPA, BECS
- **GIV-24** `[R]` Mobile money, USSD and African gateways (Paystack, Flutterwave)
- **GIV-25** `[D]` Giving in several currencies
- **GIV-26** `[D]` Church-owned processor account or a choice of gateways, with no platform fee
- **GIV-27** `[R]` Peer-to-peer and personal fundraising pages
- **GIV-28** `[D]` Offering-envelope numbers
- **GIV-29** `[R]` Automatic thank-you, first-gift and expiring-card emails
- **GIV-30** `[R]` Tools that migrate recurring givers and import donation history
- **GIV-31** `[R]` Anonymous or unlinked donations; memorial gifts
- **GIV-32** `[R]` Machine-learning fraud detection on gifts

## 11. Finance and accounting (`FIN`)

Market pattern: a real ledger ships in a minority of products.

- **FIN-01** `[D]` Fund-accounting general ledger with chart of accounts, segments and restricted funds
- **FIN-02** `[D]` Bank and card reconciliation; bank feeds or statement import with rules
- **FIN-03** `[D]` Budgets by fund, ministry or department, with budget-versus-actual
- **FIN-04** `[D]` Accounts payable (vendors, invoices, cheque printing, approval routing) and receivable
- **FIN-05** `[R]` Payroll with clergy housing allowance, W-2 and tax filing
- **FIN-06** `[R]` 1099 handling and Form 990-N or 990-EZ filing
- **FIN-07** `[D]` Financial statements by fund or campus (income statement, balance sheet)
- **FIN-08** `[R]` Fixed assets and depreciation
- **FIN-09** `[S]` Export or sync to external accounting (QuickBooks Online, Xero, Sage Intacct, DATEV, journal CSV)
- **FIN-10** `[D]` Fund-to-ledger-account mapping with automatic posting of contribution batches and fees
- **FIN-11** `[R]` Country-specific bookkeeping (German GoBD statement, SKR charts, VAT, MT940 import, cash book)
- **FIN-12** `[R]` Payables automation with approval trail; board portal; tuition invoicing
- **FIN-13** `[R]` Separate books per legal entity, client or branch

## 12. Communications (`COM`)

Market pattern: email and SMS are standard; chat with safety rules is the fast-moving edge.

- **COM-01** `[S]` Bulk email with templates, merge fields, attachments and scheduled sends
- **COM-02** `[D]` Drag-and-drop email designer
- **COM-03** `[S]` Open, click, bounce and unsubscribe tracking
- **COM-04** `[S]` Audience chosen by list, group, campus or saved search
- **COM-05** `[S]` Bulk SMS, usually metered or sent through a provider
- **COM-06** `[D]` Two-way texting with a shared inbox
- **COM-07** `[D]` Keyword texting for opt-in, giving, registration and check-in
- **COM-08** `[D]` MMS and voice (phone-tree broadcasts, voice messages, text-to-speech)
- **COM-09** `[S]` Push notifications: scheduled, targeted, by category
- **COM-10** `[D]` In-app announcements, posts and news feed
- **COM-11** `[D]` Group and team chat with direct messages
- **COM-12** `[D]` Chat safeguards: age blocks, two-adult rule for teenagers, moderation and filters, parent oversight, message reporting, logging
- **COM-13** `[R]` WhatsApp, Viber, Telegram and Messenger conversations launched from a profile; WhatsApp broadcasts
- **COM-14** `[D]` Per-channel preferences and subscriptions managed by the member
- **COM-15** `[R]` Message history stored on the person
- **COM-16** `[S]` Newsletter-tool sync (Mailchimp, Constant Contact, MailJet, CleverReach, Brevo)
- **COM-17** `[R]` Custom sender addresses and send-on-behalf rights
- **COM-18** `[R]` Polls inside messages or chat
- **COM-19** `[D]` Mail merge, letters and address labels for print
- **COM-20** `[D]` Digital bulletins and e-newsletters
- **COM-21** `[R]` Social posting, landing pages and link-tree pages
- **COM-22** `[R]` AI drafting and translation of messages
- **COM-23** `[R]` Email distribution lists that follow group membership

## 13. Member portal, app and directory (`POR`)

Market pattern: self-service is standard; a branded store app costs extra.

- **POR-01** `[S]` Member self-service portal: profile and household, giving history and statements, recurring gifts, registrations, groups, serving schedule
- **POR-02** `[S]` Online member directory with opt-in listing
- **POR-03** `[D]` Per-field and per-audience directory privacy chosen by the member; children hidden
- **POR-04** `[S]` Printed or PDF photo directory
- **POR-05** `[S]` Shared member app for iOS and Android
- **POR-06** `[D]` Church-branded app with its own store listing
- **POR-07** `[D]` No-code app builder
- **POR-08** `[R]` Installable progressive web app in place of a store app
- **POR-09** `[R]` TV and in-car apps (Apple TV, Roku, Fire TV, CarPlay, Android Auto)
- **POR-10** `[D]` Staff and leader mobile app
- **POR-11** `[D]` Passwordless sign-in (one-time code by phone or email, magic link, passkey)
- **POR-12** `[R]` Personalised home feed; separate start pages for guests and members
- **POR-13** `[D]` Members-only pages and content restricted by membership type
- **POR-14** `[D]` In-app Bible, reading plans, devotionals and daily habits
- **POR-15** `[R]` Reusable NFC and QR links; App Clips that open without an install
- **POR-16** `[R]` Account-deletion request and consent management from the portal
- **POR-17** `[R]` App analytics (content views, guest versus signed-in use, watch duration)
- **POR-18** `[R]` Separate content per ministry and per language inside one app
- **POR-19** `[R]` QR member ID cards
- **POR-20** `[R]` Celebration wall, photo sharing and social timeline

## 14. Website and CMS (`WEB`)

Market pattern: church content types are a commodity; accessibility and multilingual content are open ground.

- **WEB-01** `[S]` Template-based page builder (drag-and-drop or section blocks) with themes
- **WEB-02** `[S]` Church content types: sermons, events, staff, locations with service times, ministries, groups
- **WEB-03** `[D]` Plan-a-visit flow that alerts staff
- **WEB-04** `[S]` Blog, news and RSS
- **WEB-05** `[R]` Announcements, banners and pop-ups with scheduling and expiry
- **WEB-06** `[S]` Hosting, SSL, custom domain and redirects
- **WEB-07** `[R]` Automated backups with version restore
- **WEB-08** `[S]` Page-level SEO fields and a searchability switch
- **WEB-09** `[R]` Structured data for service times, events and locations
- **WEB-10** `[R]` Reusable sections edited once and updated everywhere
- **WEB-11** `[D]` Volunteer-friendly simple edit mode; role-based editing with approvals
- **WEB-12** `[R]` Scheduled publishing
- **WEB-13** `[R]` Site-wide search
- **WEB-14** `[D]` Embeddable widgets for third-party sites (calendar, group finder, giving, forms, sermons)
- **WEB-15** `[R]` Persistent next-steps launcher that also installs on other sites
- **WEB-16** `[R]` Several sites or campuses managed from one admin
- **WEB-17** `[R]` Multilingual site content
- **WEB-18** `[R]` Accessibility aids such as custom image alt text
- **WEB-19** `[D]` Site analytics
- **WEB-20** `[R]` Site audits that flag stale pages and broken links
- **WEB-21** `[D]` Bundled stock photo, graphics and motion library
- **WEB-22** `[R]` AI-generated site or app from a description or URL
- **WEB-23** `[R]` QR-code generator and short links
- **WEB-24** `[R]` Content personalisation by visitor
- **WEB-25** `[R]` Design studio for emails, posters and web graphics

## 15. Sermons and media (`SER`)

Market pattern: series libraries and podcast feeds are table stakes; AI repurposing is metered.

- **SER-01** `[S]` Sermon library by series, speaker, topic, Bible book and date, with search and filters
- **SER-02** `[S]` Hosted audio plus embedded video from YouTube or Vimeo
- **SER-03** `[R]` Native video hosting and delivery
- **SER-04** `[S]` Podcast feed for the library and per series or speaker
- **SER-05** `[D]` Fill-in-the-blank sermon notes with personal notes
- **SER-06** `[D]` Transcripts
- **SER-07** `[S]` Attachments and downloads (handouts, study guides, slides)
- **SER-08** `[D]` Scripture references linked to an online Bible
- **SER-09** `[R]` Publish once to website, app, podcast and TV
- **SER-10** `[R]` Unlisted items and playlists
- **SER-11** `[R]` Player extras: speed control, casting, offline download
- **SER-12** `[R]` Play counts and media analytics
- **SER-13** `[D]` AI repurposing of a sermon into clips, summaries, discussion guides, devotionals and social posts
- **SER-14** `[R]` Bulk import of past sermons
- **SER-15** `[R]` Bundled children's curriculum

## 16. Streaming and online church (`STR`)

Market pattern: embed first, host rarely.

- **STR-01** `[S]` Embedding a stream from YouTube, Facebook, Vimeo, Resi or BoxCast in the site and app
- **STR-02** `[R]` Native streaming (ingest, transcoding, adaptive bitrates)
- **STR-03** `[R]` Simulcast to social destinations
- **STR-04** `[R]` Simulated-live scheduled services and countdowns
- **STR-05** `[D]` Moderated live chat with host tools and a host-only channel
- **STR-06** `[R]` Private live prayer and in-stream prayer requests
- **STR-07** `[R]` Timed calls to action (give, connect, salvation response, poll, invite)
- **STR-08** `[R]` Automatic chat translation and an interface in 60 or more languages
- **STR-09** `[R]` Automated live captions and subtitles
- **STR-10** `[R]` On-demand archive with autosave of live streams
- **STR-11** `[R]` Per-service viewer analytics (unique attenders, watch time, responses)
- **STR-12** `[R]` Online viewers linked to people records
- **STR-13** `[R]` Ad-free branded media site on the church's own URL
- **STR-14** `[R]` Access controls (password, geo-blocking, embed restrictions) and stream APIs

## 17. Reporting and dashboards (`REP`)

Market pattern: every product has reports, and every product is criticised for them.

- **REP-01** `[S]` Library of standard reports with CSV, Excel and PDF export
- **REP-02** `[S]` Custom report builder with saved and shared reports
- **REP-03** `[R]` Scheduled reports delivered by email
- **REP-04** `[S]` Configurable dashboards and widgets, shareable and role-specific
- **REP-05** `[D]` Church-health overview across attendance, giving and serving, with period comparison
- **REP-06** `[R]` SQL or Python scripting for reports
- **REP-07** `[R]` Feeds to BI tools and spreadsheets (Power BI, Google Sheets, warehouse export)
- **REP-08** `[D]` Plain-language questions answered with charts
- **REP-09** `[R]` Acting on results: message a list, add people to a group or pathway, mass-update
- **REP-10** `[R]` Manually tracked custom metrics
- **REP-11** `[R]` Report-level security and the option to disable unused reports
- **REP-12** `[S]` Printable rosters, roll sheets, labels and name tags
- **REP-13** `[R]` Global search across modules
- **REP-14** `[D]` Assimilation-funnel and demographic reports

## 18. Multi-campus and hierarchy (`MUL`)

Market pattern: campus tags are common; true multi-church models are rare.

- **MUL-01** `[S]` Campus attribute on people, groups, events, check-in and gifts, with campus filters
- **MUL-02** `[D]` Campus-scoped administrators and permissions
- **MUL-03** `[D]` Per-campus giving: branding, designations, bank accounts, campaigns
- **MUL-04** `[R]` Cross-campus dashboards and comparison
- **MUL-05** `[R]` Branch-church mode (main church with branches, shared songs, funds and rooms, member transfer)
- **MUL-06** `[D]` Diocesan and denominational editions with roll-up census, reports and appeals
- **MUL-07** `[R]` Multi-tenant hosting of many independent churches on one installation
- **MUL-08** `[R]` Sync between separate installations
- **MUL-09** `[R]` Multi-campus app and campus-to-campus video

## 19. Permissions, security and audit (`SEC`)

Market pattern: roles are universal; enforced two-step verification is spreading.

- **SEC-01** `[S]` Role-based access with predefined and custom roles
- **SEC-02** `[D]` Field-level and page-level security
- **SEC-03** `[D]` Finance-gated data and fund-based permissions
- **SEC-04** `[D]` Visibility levels on sensitive notes and safeguarding records
- **SEC-05** `[S]` Two-factor authentication offered
- **SEC-06** `[R]` Two-factor authentication enforced for privileged roles
- **SEC-07** `[D]` Single sign-on (Entra ID, Okta, LDAP, social logins, OpenID Connect)
- **SEC-08** `[R]` Passkeys
- **SEC-09** `[D]` Audit trail: login history with IP and device, record change logs, activity logs
- **SEC-10** `[R]` Administrator approval of new accounts; identity verification before financial access
- **SEC-11** `[R]` Admin control over personal API tokens and connected apps
- **SEC-12** `[D]` Encryption of sensitive fields and attachments
- **SEC-13** `[R]` Choice of hosting region or in-country hosting
- **SEC-14** `[D]` Third-party attestations (SOC 2 Type 2, PCI Level 1, ISO 27001)
- **SEC-15** `[R]` Captcha, confirmation of sign-ins from unrecognised browsers, account impersonation for support
- **SEC-16** `[R]` Self-managed backup and restore

## 20. Integrations and API (`API`)

Market pattern: open APIs and webhooks mark the leaders.

- **API-01** `[D]` Documented public REST API
- **API-02** `[D]` Webhooks
- **API-03** `[D]` OAuth 2.0 and OpenID Connect for third-party apps
- **API-04** `[D]` Zapier, Make or n8n connectors
- **API-05** `[D]` Integration directory or plugin store
- **API-06** `[S]` Stock connectors: accounting, email marketing, SMS gateways, background checks, SongSelect, streaming, payment gateways
- **API-07** `[D]` Sync with another church system, most often Planning Center
- **API-08** `[R]` Custom pages, SQL views, scripts and plugins inside the product
- **API-09** `[D]` MCP server or assistant connector
- **API-10** `[R]` CalDAV, CardDAV and WebDAV servers
- **API-11** `[R]` Bring-your-own storage, SMS and content providers
- **API-12** `[R]` Notifications to Slack or Discord

## 21. Import, export and migration (`MIG`)

Market pattern: CSV in, CSV out, and relational history left behind.

- **MIG-01** `[S]` CSV or Excel import of people with field mapping and custom fields
- **MIG-02** `[S]` Import of giving history
- **MIG-03** `[D]` Named importers for other systems' exports (Planning Center, Breeze or Tithely, CCB, Rock)
- **MIG-04** `[R]` Import of groups, attendance, notes and household roles
- **MIG-05** `[S]` Vendor-run migration service
- **MIG-06** `[S]` Self-service CSV export of lists, reports and workflow data
- **MIG-07** `[R]` Export in another system's format
- **MIG-08** `[R]` Undo window or repeatable test import
- **MIG-09** `[R]` Migration of recurring-gift schedules
- **MIG-10** `[R]` Per-person data sheet for access requests; iCal and vCard exchange

## 22. AI (`AI`)

Market pattern: plain-language lists and MCP connectors arrived in 2026.

- **AI-01** `[D]` Plain-language people search and list building
- **AI-02** `[D]` Questions over giving and engagement data answered with summaries and charts
- **AI-03** `[R]` AI summary of one person's involvement
- **AI-04** `[R]` Read-only assistant inside the product
- **AI-05** `[D]` MCP connection to outside assistants, scoped to the user's permissions, with writes off or limited by default
- **AI-06** `[R]` Agents that update records, add group members and draft messages
- **AI-07** `[R]` AI drafting of workflows and forms
- **AI-08** `[D]` Sermon AI: preparation, transcripts, clips and repurposed content
- **AI-09** `[R]` Photographed connect cards read into records, with handwriting and duplicate flags
- **AI-10** `[R]` AI moderation of prayer requests and chat images
- **AI-11** `[R]` Disengagement signals with a recommended next action for a pastor
- **AI-12** `[R]` Congregation-facing chat assistant and live translation
- **AI-13** `[S]` Stated guardrails: no training on church data, opt-in or admin-controlled access, human review

## 23. Regional and tradition-specific modules (`REG`)

Market pattern: deep, narrow and almost absent from US products.

- **REG-01** `[R]` UK Gift Aid: declarations, claim batches, HMRC submission or export, small-donations scheme
- **REG-02** `[D]` Country-specific receipts: Canadian serial-numbered receipts, Australian ABN and DGR wording, New Zealand IRD number
- **REG-03** `[R]` Safeguarding module: concerns log, check records with renewal dates, restricted roles
- **REG-04** `[D]` Sacramental records with certificates and notification letters
- **REG-05** `[R]` Faith-formation and religious-education administration
- **REG-06** `[R]` Mass intentions with stipend status, celebrant plan and service notice
- **REG-07** `[R]` Life-events diary for weddings, baptisms, funerals and banns, with enquiry forms and invoicing
- **REG-08** `[R]` Governance and compliance task lists (annual meetings, returns, safety tests)
- **REG-09** `[R]` Reformed membership statistics, transfer documents and office-bearer visits
- **REG-10** `[R]` Diocesan annual report and denominational statistics exports
- **REG-11** `[D]` Interface in many languages, selectable per user
- **REG-12** `[R]` Configurable terminology (rename pledges, sermons, group types)
- **REG-13** `[R]` Compliance with church data-protection law and in-country hosting (KDG, DSG-EKD)
- **REG-14** `[R]` Welfare dues; attendance by USSD or NFC tag

## 24. Operations extras (`OPS`)

Market pattern: wiki, staff leave, assets and governance tasks.

- **OPS-01** `[R]` Internal wiki or knowledge base
- **OPS-02** `[R]` Staff leave and sickness tracking; time registration
- **OPS-03** `[R]` Asset, key, inventory and library lending
- **OPS-04** `[R]` Shared files with folders, council-only areas and version history
- **OPS-05** `[R]` Built-in video meetings
- **OPS-06** `[R]` Projects and maintenance tasks beyond follow-up
- **OPS-07** `[R]` Public church finder or church profile

## Compliance-driven features

Rules and accepted practices that force features. Format: rule or practice, then the feature it forces. Jurisdictions covered: United States, United Kingdom, European Union, Canada, Australia. Not legal advice.

### Tax receipting (`TAX`)

- **TAX-01** United States: Per-gift receipts and period statements by email or print; gift flags for cash or non-cash, value of benefit received and deductibility; non-cash description without a valuation
- **TAX-02** United Kingdom: Declaration record with scope, dates, evidence and cancellation; donor address history; locked claim batches with HMRC-format export or direct submission; small-donations ledger; netting of over-claims after refunds
- **TAX-03** Canada: Sequential receipt numbers that are never reused, stored duplicates, void-and-replace, read-only signed PDF, a Canadian data location for self-hosters
- **TAX-04** Australia: Receipt template with ABN and gift wording; tax-deductible flag per fund or donation
- **TAX-05** Germany: Official-template receipts, duplicate archive, donation-use records
- **TAX-06** Ireland: Donor authorisation record and annual threshold report

### Payments (`PAY`)

- **PAY-01** Card details sent straight from the browser to the processor keep the church out of most PCI controls; brand, last four digits and expiry may be stored (Stripe): Gateway plug-ins that render processor-hosted fields or redirect; tokens only; no admin form that accepts a card or bank number
- **PAY-02** Pages hosting an embedded payment form must be shown to resist script attacks (PCI Security Standards Council): Strict Content Security Policy and no third-party scripts on giving pages; written guidance for self-hosters on the SAQ A confirmation
- **PAY-03** US internet-initiated bank debits need account validation, and every originator falls under fraud-monitoring duties by 19 June 2026 (Nacha): Bank verification through the gateway; signed webhooks and a scheduled transaction download for reconciliation
- **PAY-04** Bank-debit mandates must be displayed, stored and sent to the donor, and a dispute voids the mandate (Stripe): Mandate record holding the text shown, timestamp and IP address; advance-notice emails when a recurring debit changes
- **PAY-05** SEPA payers can reclaim a debit for eight weeks without giving a reason; card disputes reverse the payment and add a fee (Stripe): Refund and dispute status on every transaction; reversals that also correct receipts, statements and tax claims
- **PAY-06** A refunded UK gift that was already claimed creates a Gift Aid over-claim (ChurchSuite): Over-claim netting against the next claim
- **PAY-07** Most gateways will not hand stored card details back when a church switches (Rock RMS): Church-owned processor account; local copy of recurring-schedule metadata to ease re-enrolment

### Privacy (`PRV`)

- **PRV-01** Religious belief is special-category data; the not-for-profit condition covers members and regular contacts only and bars outside disclosure without consent (GDPR Article 9): Consent and lawful-basis register per person and purpose, with wording version, timestamp and method; a consent gate and log on every outward data flow
- **PRV-02** Rights requests answered within one month; erasure subject to legal exceptions (GDPR Article 12; GDPR Article 17): Request workflow with a deadline clock; export of everything held on a person; erasure or anonymisation that keeps statutory financial and safeguarding records
- **PRV-03** Written processor contract; breaches reported within 72 hours and all breaches documented (GDPR Article 28; GDPR Article 33): Documented list of outbound data flows (host, email, SMS, payment gateway); breach log
- **PRV-04** Consent-based online services need parental authorisation below the national age threshold (GDPR Article 8): Consent request per child linked to a parent; children hidden from directories and member search
- **PRV-05** The regulator expects safeguards such as restricted access, shorter retention or an opt-out when the not-for-profit condition is used (ICO): Opt-in directory, hidden by default, with per-field visibility that also governs printed directories
- **PRV-06** Québec's Law 25 requires a named person in charge of personal information and incident reporting (Charity Law Group): Named hosting region; privacy-officer contact; incident register
- **PRV-07** A baptism entry must become unidentifiable on a valid erasure request, per a non-binding 2026 Opinion (Court of Justice of the EU): True redaction of identifying fields in sacramental records while keeping a non-identifying event entry

### Child safety (`SAF`)

- **SAF-01** Release only to a parent or authorised person through a claim check (Brotherhood Mutual): Per-session codes on child and guardian labels; authorised and barred pickup lists with photos; logged check-out
- **SAF-02** Two screened adults per room and ratios by age band, from 1:3 for infants upward (ChildCare.gov; thirtyone:eight): Worker check-in; configurable ratio and capacity rules with warnings when a room lacks two cleared adults
- **SAF-03** Screening at appointment and again at an interval of one to five years (Church Mutual; Diocese of Canterbury): Generic credential record (type, reference, issue and renewal dates, status) with configurable interval, reminders and blocking of scheduling when missing or expired
- **SAF-04** Staged safer recruitment and a six-month observation period before working with children (thirtyone:eight; ECAP): Recruitment workflow with application, references, interview, check, training and review stages; minimum-tenure gate
- **SAF-05** DBS certificates may not be copied; only summary fields may be kept (Disclosure and Barring Service): Summary fields only, no certificate image, access limited to named safeguarding roles
- **SAF-06** Concern records written within 24 hours, dated, attributed, access-limited and kept for decades (Church of England and Methodist Church): Append-only confidential concern log separate from pastoral notes, with referral records and retention flags that override deletion
- **SAF-07** Safeguarding training refreshed every three years with attendance recorded (Church of England): Training records with expiry and reminders

### Security (`INC`)

- **INC-01** Blackbaud, 2020: data taken from more than 13,000 customer organisations (The Record): Two-factor sign-in enforced for privileged roles; backup pruning and a retention schedule
- **INC-02** Cornerstone Payment Systems, 2022: 9,098,506 transaction records exposed (Website Planet): Authentication on every datastore; minimal stored payment data
- **INC-03** ChurchCRM CVE-2025-68110, rated 10.0 (OffSeq): No connection details or stack traces in production errors
- **INC-04** Click To Pray, 2026: records of about 700,000 users enumerable (Malwarebytes): Authorisation on every API object; non-sequential public identifiers; a monitored security contact
- **INC-05** Beacon CRM, 2026: supporter data of more than 1,000 nonprofits (MinistryWatch): Encrypted, access-restricted backups; certification is no substitute for controls
- **INC-06** Seoul megachurches, 2026: a dataset on about 850,000 members (The Record): Hardened upload and reset paths; rate limiting; no shared administrator credentials

### Messaging, accessibility, licensing and financial controls (`RUL`)

- **RUL-01** US email: opt-outs honoured within 10 business days and a postal address in commercial messages (Federal Trade Commission): One-click unsubscribe, global suppression list, sender identity and postal address in every bulk email
- **RUL-02** US texting: prior express consent, STOP-type replies revoke it, carrier registration of brand and campaign (47 CFR 64.1200; Twilio): Per-channel consent with source and timestamp; automatic STOP handling; fields for the church's own registration; bring-your-own SMS provider
- **RUL-03** UK charities may market electronically on a soft opt-in since 5 February 2026; Canadian implied consent lasts two years; Australian unsubscribes take effect within 5 working days (ICO; CRTC; ACMA): Consent basis, collection date and expiry stored per contact; proof of consent retained
- **RUL-04** WCAG 2.2 is the current W3C recommendation (W3C): Public pages (giving, forms, registration, portal, kiosk) built to WCAG 2.2 AA
- **RUL-05** Software connected to CCLI reports song use continuously; streamed services need an add-on licence and attribution (CCLI): Song records with CCLI number, authors and copyright line; licence numbers; usage counts by type; report export; generated attribution text
- **RUL-06** Two unrelated counters sign a count sheet; deposit by the next business day; reconciliation by someone outside bookkeeping (CapinCrouse; Foursquare): Count session with two distinct users and denomination tallies; batch control totals; closed batches locked, with reopening logged; separate roles for entry, approval and reconciliation
- **RUL-07** Every transaction involves more than one person and leaves an audit trail (Charity Commission): Immutable history of edits to gifts, donors, declarations and receipts; soft deletion; locks once statements or claims are issued

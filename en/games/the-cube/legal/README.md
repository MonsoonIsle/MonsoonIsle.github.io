# The Cube legal document catalog

This catalog covers app versions 1.0.14 and later. Legal set 2 (privacy revision
4, terms revision 2, notice 2) is the current authored set; set 1 remains immutable
for document history. Earlier app versions continue to use the policy at
`../privacy/policy.json`; its raw JSON has not changed. The compatibility HTML
entry links users to the documents appropriate to their app version.

Website publication, app distribution, SDK message delivery and production
acceptance are separate steps. Published HTML does not announce an app release or
establish legal review. Verify deployment and public HTTP bytes in the game's
PRIVACY-SPLIT-11 record; local generated files alone do not prove deployment.

The website JSON is the authored source. The game bundle is an exact-byte mirror;
do not edit it independently. Maintain the publication-mode HTML with:

```sh
python3 -B scripts/build_cube_legal.py --status published
python3 -B scripts/build_cube_legal.py --status published --check
python3 -B scripts/build_cube_privacy.py --check
python3 -B -m unittest discover -s scripts -p 'test_build_cube_*.py' -v
```

The default renderer remains a draft preview with a draft banner and noindex.
Always pass `--status published` when checking or regenerating this published-mode
catalog. This removes only status markers; it never changes JSON, document hashes
or text, and does not deploy the website by itself.

Schema 1 strictly rejects unknown fields, duplicate keys, BOMs, malformed UTF-8,
unpaired surrogates in authored text, unknown/duplicate recipients and incomplete
sets. Manifest limit: 65,536 bytes and 64 releases. Each document: 262,144 bytes,
64 sections, 256 paragraphs total, 16,384 characters per heading/paragraph and
256 characters per title. JSON depth: 12; positive revisions/notices: signed
32-bit range. App versions contain three components of 1–9 ASCII digits, compared
numerically; bounds are inclusive. Dates are real `YYYY-MM-DD` dates, checked
against the current UTC date for release selection. JSON has no embedded target
URLs in its manifest: document and HTML URLs derive from the fixed HTTPS origin,
set revision and kind. The document `source_url` must match that versioned HTML.

Select the highest effective compatible release, examining the full release
list. A newer future or incompatible set must not hide a valid previous set.
The manifest revision may increase but all existing release descriptors stay
immutable and retained. Document revisions cannot decrease or reuse a revision
with different bytes. Because source URLs include the set revision, publishing
the same words at a new set path still changes document bytes and requires a
document revision bump. SHA256 covers exact UTF-8 file bytes including whitespace
and the final newline; parsed/re-serialized JSON is not a substitute.

An acceptance identity binds app/language/schema and the selected release
descriptor, including notice/recipient scope and both document hashes. The helper
hashes compact sorted-key JSON with a sorted recipient list, as documented in
`LegalSet.acceptance_token`. The whole manifest SHA is audit information only;
adding an unrelated/future set does not change the existing acceptance identity.

The self-contained website validator and the game's `scripts/legal_documents.py`
implement the same protocol; neither needs the other checkout at runtime. The
game's `scripts/sync_legal_documents.py --website-root <checkout> --app-version
1.0.14 --check` validates complete referenced sets and compares exact bytes with
no network. Its `--update` mode installs immutable documents first and the manifest
last, and refuses existing immutable-path mutations or manifest/history downgrades.

The authored facts reuse the existing policy's 15-section baseline. Official sources
checked on 2026-10-21 include [Firebase privacy and retention](https://firebase.google.com/support/privacy),
[UMP controls](https://developers.google.com/admob/android/privacy),
[Google Mobile Ads Legacy 25.5.0 data disclosure](https://developers.google.com/admob/android/privacy/play-data-disclosure),
[Analytics retention controls](https://support.google.com/analytics/answer/7667196),
[GameAnalytics retention](https://docs.gameanalytics.com/event-tracking-and-integrations/data-retention-and-limits/data-retention-practices/),
[GameAnalytics DPA](https://www.gameanalytics.com/trust/eu-data-processing-addendum)
and [GitHub hosting privacy](https://docs.github.com/en/site-policy/privacy-policies/github-general-privacy-statement).
Batch 09 independently re-read the Analytics property settings: event data 2 months,
user data 14 months, reset on new activity enabled. These console observations are
configuration evidence, not evidence of data receipt or legal sufficiency.

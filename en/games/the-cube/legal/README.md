# The Cube legal set — draft

These files are unpublished preparation for app versions 1.0.14 and later. They
do not change the existing revision 2 policy at `../privacy/policy.json` or imply
that the proposed runtime behavior has shipped. Publication and platform/config
verification belong to later PRIVACY-SPLIT batches. No legal review is claimed.

The website JSON is the authored source. The game bundle is an exact-byte mirror;
do not edit it independently. Generate/check HTML with:

```sh
python3 -B scripts/build_cube_legal.py
python3 -B scripts/build_cube_legal.py --check
python3 -B -m unittest discover -s scripts -p 'test_build_cube_legal.py' -v
```

The default HTML is marked draft and `noindex`. At the separately authorized
publication step, `--status published` removes only those HTML status markers;
use the same status with `--check`. It never changes JSON, hashes or document
text and does not publish anything by itself.

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

Draft facts reuse the existing policy's 15-section baseline. Official sources
checked on 2026-10-21 include [Firebase privacy and retention](https://firebase.google.com/support/privacy),
[UMP controls](https://developers.google.com/admob/android/privacy),
[Google Mobile Ads Legacy 25.5.0 data disclosure](https://developers.google.com/admob/android/privacy/play-data-disclosure),
[Analytics retention controls](https://support.google.com/analytics/answer/7667196),
[GameAnalytics retention](https://docs.gameanalytics.com/event-tracking-and-integrations/data-retention-and-limits/data-retention-practices/),
[GameAnalytics DPA](https://www.gameanalytics.com/trust/eu-data-processing-addendum)
and [GitHub hosting privacy](https://docs.github.com/en/site-policy/privacy-policies/github-general-privacy-statement).
The retained Analytics 2/14-month property settings are historical configuration
evidence, pending the batch 09 console re-read before publication; these source
checks do not verify current private configuration or legal sufficiency.

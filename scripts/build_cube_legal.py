#!/usr/bin/env python3
"""Generate and check The Cube legal HTML with independent strict validation.

The website owns the authored JSON. Validation matches the game protocol without
a runtime dependency on the game checkout. Hashes always cover exact raw bytes.
"""

from dataclasses import dataclass
from datetime import date, datetime, timezone
import hashlib
import json
from pathlib import Path
import re


APP_ID = "com.tesselox.game"
BASE_URL = "https://monsoonisle.github.io/en/games/the-cube/legal/"
MANIFEST_URL = BASE_URL + "manifest.json"
KINDS = ("privacy", "terms")
RECIPIENTS = frozenset(("firebase_analytics", "firebase_crashlytics", "gameanalytics_collection"))
MAX_MANIFEST_BYTES = 65536
MAX_DOCUMENT_BYTES = 262144
MAX_RELEASES = 64
MAX_DEPTH = 12
MAX_TEXT = 16384
MAX_SECTIONS = 64
MAX_PARAGRAPHS = 256
MAX_REVISION = 2147483647
MANIFEST_FIELDS = {"schema_version", "app_id", "language", "revision", "releases"}
RELEASE_FIELDS = {"revision", "min_app_version", "max_app_version", "effective_date",
                  "notice_version", "recipients", "documents"}
DOCUMENT_FIELDS = {"schema_version", "document_id", "language", "revision", "title",
                   "updated_at", "effective_date", "source_url", "sections"}


def _unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"Duplicate JSON key: {key}")
        result[key] = value
    return result


def _invalid_constant(value):
    raise ValueError(f"Invalid JSON constant: {value}")


def _load_json(raw, maximum):
    if not isinstance(raw, bytes) or not 1 <= len(raw) <= maximum or raw.startswith(b"\xef\xbb\xbf"):
        raise ValueError(f"Expected 1–{maximum} raw UTF-8 bytes without a BOM")
    try:
        value = json.loads(raw.decode("utf-8"), object_pairs_hook=_unique_object,
                           parse_constant=_invalid_constant)
    except (UnicodeError, RecursionError) as error:
        raise ValueError("Expected valid UTF-8 JSON without excessive nesting") from error
    pending = [(value, 1)]
    while pending:
        item, depth = pending.pop()
        if depth > MAX_DEPTH:
            raise ValueError("JSON nesting exceeds protocol limit")
        if isinstance(item, dict):
            pending.extend((child, depth + 1) for child in item.values())
        elif isinstance(item, list):
            pending.extend((child, depth + 1) for child in item)
    return value


def _fields(value, fields, label):
    if not isinstance(value, dict) or set(value) != fields:
        raise ValueError(f"Unexpected {label} fields")


def _revision(value, label="revision"):
    if type(value) is not int or not 1 <= value <= MAX_REVISION:
        raise ValueError(f"{label} must be a positive 32-bit integer")


def _schema(value):
    if type(value) is not int or value != 1:
        raise ValueError("Unsupported schema_version")


def _date(value, label):
    if not isinstance(value, str) or not re.fullmatch(r"[0-9]{4}-[0-9]{2}-[0-9]{2}", value):
        raise ValueError(f"Invalid {label}")
    return date.fromisoformat(value)


def _text(value, label, maximum=MAX_TEXT):
    if not isinstance(value, str) or not value.strip() or len(value) > maximum:
        raise ValueError(f"Invalid {label}")
    if any(ord(char) < 32 and char not in "\n\r\t" for char in value):
        raise ValueError(f"Invalid control character in {label}")
    try:
        value.encode("utf-8")
    except UnicodeError as error:
        raise ValueError(f"Invalid Unicode in {label}") from error


def version_parts(value):
    if not isinstance(value, str) or not re.fullmatch(r"[0-9]{1,9}\.[0-9]{1,9}\.[0-9]{1,9}", value):
        raise ValueError("App versions require three components of 1–9 ASCII digits")
    return tuple(int(part) for part in value.split("."))


def document_path(release_revision, kind):
    _revision(release_revision, "release revision")
    if kind not in KINDS:
        raise ValueError("Unknown document kind")
    return Path("releases") / str(release_revision) / f"{kind}.json"


def document_url(release_revision, kind):
    return BASE_URL + document_path(release_revision, kind).as_posix()


def document_source_url(release_revision, kind):
    return document_url(release_revision, kind).removesuffix(".json") + "/"


def load_manifest(raw):
    manifest = _load_json(raw, MAX_MANIFEST_BYTES)
    _fields(manifest, MANIFEST_FIELDS, "manifest")
    _schema(manifest["schema_version"])
    if manifest["app_id"] != APP_ID or manifest["language"] != "en":
        raise ValueError("Manifest must be for The Cube in English")
    _revision(manifest["revision"], "manifest revision")
    releases = manifest["releases"]
    if not isinstance(releases, list) or not 1 <= len(releases) <= MAX_RELEASES:
        raise ValueError("Manifest requires 1–64 releases")
    seen = set()
    for release in releases:
        _fields(release, RELEASE_FIELDS, "release")
        _revision(release["revision"], "release revision")
        if release["revision"] in seen or release["revision"] > manifest["revision"]:
            raise ValueError("Duplicate release or release newer than manifest revision")
        seen.add(release["revision"])
        minimum = version_parts(release["min_app_version"])
        maximum = release["max_app_version"]
        if maximum != "" and version_parts(maximum) < minimum:
            raise ValueError("max_app_version precedes min_app_version")
        _date(release["effective_date"], "effective_date")
        _revision(release["notice_version"], "notice_version")
        recipients = release["recipients"]
        if (not isinstance(recipients, list) or not recipients
                or any(not isinstance(item, str) or item not in RECIPIENTS for item in recipients)
                or len(set(recipients)) != len(recipients)):
            raise ValueError("Unknown, empty or duplicate recipient scope")
        _fields(release["documents"], set(KINDS), "documents")
        for descriptor in release["documents"].values():
            _fields(descriptor, {"revision", "sha256"}, "document descriptor")
            _revision(descriptor["revision"], "document revision")
            if not isinstance(descriptor["sha256"], str) or not re.fullmatch(r"[0-9a-f]{64}", descriptor["sha256"]):
                raise ValueError("Expected lowercase raw-byte SHA256")
    for kind in KINDS:
        known, last_revision = {}, 0
        for release in sorted(releases, key=lambda item: item["revision"]):
            descriptor = release["documents"][kind]
            revision, digest = descriptor["revision"], descriptor["sha256"]
            if revision < last_revision or (revision in known and known[revision] != digest):
                raise ValueError("Document downgrade or same-revision byte mutation")
            known[revision], last_revision = digest, revision
    return manifest


def load_document(raw, *, kind, release_revision):
    expected_source = document_source_url(release_revision, kind)
    document = _load_json(raw, MAX_DOCUMENT_BYTES)
    _fields(document, DOCUMENT_FIELDS, "document")
    _schema(document["schema_version"])
    if document["document_id"] != f"the-cube-{kind}" or document["language"] != "en":
        raise ValueError("Unexpected document identity or language")
    if document["source_url"] != expected_source:
        raise ValueError("Unexpected versioned document source_url")
    _revision(document["revision"], "document revision")
    _date(document["effective_date"], "effective_date")
    _date(document["updated_at"], "updated_at")
    if document["updated_at"] < document["effective_date"]:
        raise ValueError("updated_at precedes effective_date")
    _text(document["title"], "title", 256)
    sections = document["sections"]
    if not isinstance(sections, list) or not 1 <= len(sections) <= MAX_SECTIONS:
        raise ValueError("Document requires 1–64 sections")
    count = 0
    for section in sections:
        _fields(section, {"heading", "paragraphs"}, "section")
        _text(section["heading"], "heading")
        paragraphs = section["paragraphs"]
        if not isinstance(paragraphs, list) or not paragraphs:
            raise ValueError("Each section requires paragraphs")
        count += len(paragraphs)
        if count > MAX_PARAGRAPHS:
            raise ValueError("Document exceeds 256 paragraphs")
        for paragraph in paragraphs:
            _text(paragraph, "paragraph")
    return document


def select_release(manifest, app_version, *, today=None):
    """Select highest effective compatible revision, independent of list ordering."""
    current = version_parts(app_version)
    cutoff = datetime.now(timezone.utc).date() if today is None else today
    if isinstance(cutoff, str):
        cutoff = _date(cutoff, "today")
    if type(cutoff) is not date:
        raise ValueError("today must be a UTC date or YYYY-MM-DD")
    compatible = [release for release in manifest["releases"]
                  if version_parts(release["min_app_version"]) <= current
                  and (not release["max_app_version"] or current <= version_parts(release["max_app_version"]))
                  and _date(release["effective_date"], "effective_date") <= cutoff]
    if not compatible:
        raise ValueError(f"No effective legal release for app version {app_version}")
    return max(compatible, key=lambda release: release["revision"])


@dataclass(frozen=True)
class LegalSet:
    manifest_raw: bytes
    manifest: dict
    release: dict
    raw_documents: dict
    documents: dict

    @property
    def acceptance_token(self):
        """Stable set binding; unrelated manifest additions cannot change this token.

        Hash UTF-8 compact JSON of the descriptor with sorted object keys and
        recipients sorted as a set. All values are ASCII protocol fields. Store
        manifest_sha256 separately for audit; it is not an acceptance identity.
        """
        descriptor = {"schema_version": 1, "app_id": APP_ID, "language": "en",
                      "release": dict(self.release)}
        descriptor["release"]["recipients"] = sorted(self.release["recipients"])
        encoded = json.dumps(descriptor, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode("utf-8")
        return hashlib.sha256(encoded).hexdigest()

    @property
    def manifest_sha256(self):
        return hashlib.sha256(self.manifest_raw).hexdigest()


def validate_release(manifest_raw, release, raw_documents):
    manifest = load_manifest(manifest_raw)
    if release not in manifest["releases"]:
        raise ValueError("Release is absent from validated manifest")
    release = next(item for item in manifest["releases"] if item["revision"] == release["revision"])
    if not isinstance(raw_documents, dict) or set(raw_documents) != set(KINDS):
        raise ValueError("A complete privacy and terms pair is required")
    documents = {}
    for kind in KINDS:
        raw = raw_documents[kind]
        document = load_document(raw, kind=kind, release_revision=release["revision"])
        descriptor = release["documents"][kind]
        if (document["revision"] != descriptor["revision"]
                or hashlib.sha256(raw).hexdigest() != descriptor["sha256"]
                or document["effective_date"] != release["effective_date"]):
            raise ValueError(f"{kind} revision, raw-byte hash or effective date mismatch")
        documents[kind] = document
    return LegalSet(manifest_raw, manifest, release, dict(raw_documents), documents)


def read_raw(path, maximum):
    with Path(path).open("rb") as stream:
        return stream.read(maximum + 1)


def read_bundle(legal_root, app_version, *, today=None):
    root = Path(legal_root)
    raw = read_raw(root / "manifest.json", MAX_MANIFEST_BYTES)
    manifest = load_manifest(raw)
    release = select_release(manifest, app_version, today=today)
    documents = {kind: read_raw(root / document_path(release["revision"], kind), MAX_DOCUMENT_BYTES)
                 for kind in KINDS}
    return validate_release(raw, release, documents)


def read_catalog(legal_root):
    """Validate every referenced release before publishing or offline syncing."""
    root = Path(legal_root)
    raw = read_raw(root / "manifest.json", MAX_MANIFEST_BYTES)
    manifest = load_manifest(raw)
    return [validate_release(raw, release, {
        kind: read_raw(root / document_path(release["revision"], kind), MAX_DOCUMENT_BYTES)
        for kind in KINDS}) for release in manifest["releases"]]


def check_manifest_transition(previous_raw, candidate_raw):
    previous, candidate = load_manifest(previous_raw), load_manifest(candidate_raw)
    if candidate["revision"] < previous["revision"]:
        raise ValueError("Refusing manifest downgrade")
    if candidate["revision"] == previous["revision"] and candidate_raw != previous_raw:
        raise ValueError("Manifest bytes changed without a revision bump")
    by_revision = {release["revision"]: release for release in candidate["releases"]}
    for release in previous["releases"]:
        if by_revision.get(release["revision"]) != release:
            raise ValueError("Existing legal release descriptors are immutable")
    return candidate


# Generic presentation: every authored heading and paragraph is rendered, with
# no knowledge of section count or policy-specific text.
import argparse
from html import escape
import sys


ROOT = Path(__file__).resolve().parents[1]
LEGAL_DIR = ROOT / "en/games/the-cube/legal"
INLINE_LINK = re.compile(r'https://[^\s<>"()]+|[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}')
DRAFT_NOTICE = "Draft for review — this document set has not been published or enabled in a released app."


def inline(value):
    parts, cursor = [], 0
    for match in INLINE_LINK.finditer(value):
        label = match.group().rstrip(".,;:!?")
        parts.append(escape(value[cursor:match.start()], quote=False))
        href = label if label.startswith("https://") else "mailto:" + label
        parts.append(f'<a href="{escape(href, quote=True)}">{escape(label, quote=False)}</a>')
        cursor = match.start() + len(label)
    parts.append(escape(value[cursor:], quote=False))
    return "".join(parts)


def _page(title, canonical, content, *, status="draft"):
    if status not in ("draft", "published"):
        raise ValueError("Unknown publication status")
    robots = '  <meta name="robots" content="noindex">\n' if status == "draft" else ""
    notice = f'    <div class="note" role="note">{escape(DRAFT_NOTICE)}</div>\n' if status == "draft" else ""
    return (f'''<!doctype html>
<!-- Generated by scripts/build_cube_legal.py; edit the source JSON and regenerate. -->
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
{robots}\
  <title>{escape(title)} | The Cube · Monsoon Isle</title>
  <link rel="stylesheet" href="/assets/style.css">
  <link rel="canonical" href="{escape(canonical, quote=True)}">
</head>
<body>
  <header><a class="brand" href="/en/">Monsoon Isle</a><nav aria-label="Legal navigation"><a href="{BASE_URL}">The Cube legal documents</a><a href="/en/games/the-cube/privacy/">Earlier-version policy</a></nav></header>
  <main>
{notice}\
{content}
  </main>
  <footer><span>© 2026 Monsoon Isle</span><a href="mailto:mengjingchanyu@gmail.com">Contact</a></footer>
</body>
</html>
''').encode("utf-8")


def render(document, release, kind, *, status="draft"):
    lines = [f'    <h1>{escape(document["title"])}</h1>',
             f'    <p>Document revision {document["revision"]} · Legal set {release["revision"]} · Effective <time datetime="{document["effective_date"]}">{document["effective_date"]}</time></p>',
             f'    <p class="note">Use the highest effective legal set compatible with your app version in the <a href="{BASE_URL}">document catalog</a>. Older sets are retained for document history; their publication does not mean that they shipped in an app.</p>',
             '    <nav aria-label="Document contents">']
    for index, section in enumerate(document["sections"], 1):
        lines.append(f'      <a href="#section-{index}">{escape(section["heading"])}</a>')
    lines += ['    </nav>', '    <article class="policy">']
    for index, section in enumerate(document["sections"], 1):
        lines += [f'      <section id="section-{index}">', f'        <h2>{escape(section["heading"])}</h2>']
        lines += [f'        <p class="legal-paragraph">{inline(paragraph)}</p>' for paragraph in section["paragraphs"]]
        lines.append('      </section>')
    sibling = "terms" if kind == "privacy" else "privacy"
    label = "Terms of Use" if sibling == "terms" else "Privacy Policy"
    lines += ['    </article>',
              f'    <p><a href="{document_source_url(release["revision"], sibling)}">{label} in this set</a> · <a href="{document_url(release["revision"], kind)}">Source JSON</a></p>']
    return _page(document["title"], document["source_url"], "\n".join(lines), status=status)


def generate_pages(legal_root, *, status="draft"):
    catalog = read_catalog(legal_root)
    check_manifest_transition(catalog[0].manifest_raw, catalog[0].manifest_raw)
    pages = {}
    summary = ['    <h1>The Cube · Legal documents</h1>',
               '    <p>Each immutable set contains a complete Privacy Policy and Terms of Use. Earlier app versions continue to use the earlier-version policy.</p>',
               '    <p>Use the highest effective set compatible with your app version. Sets are listed newest first; earlier sets remain available as document history.</p>',
               f'    <p><a href="{MANIFEST_URL}">Version and raw-byte hash manifest</a></p>']
    for item in sorted(catalog, key=lambda value: value.release["revision"], reverse=True):
        release = item.release
        maximum = release["max_app_version"] or "later"
        summary += [f'    <h2>Legal set {release["revision"]}</h2>',
                    f'    <p>App versions {escape(release["min_app_version"])} through {escape(maximum)} · Effective {release["effective_date"]}</p>', '    <ul>']
        for kind in KINDS:
            document = item.documents[kind]
            relative = document_path(release["revision"], kind).with_suffix("") / "index.html"
            pages[relative] = render(document, release, kind, status=status)
            summary.append(f'      <li><a href="{document["source_url"]}">{escape(document["title"])}</a> · revision {document["revision"]}</li>')
        summary.append('    </ul>')
    pages[Path("index.html")] = _page("Legal documents", BASE_URL, "\n".join(summary), status=status)
    return pages


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Fail on generated HTML drift without writing")
    parser.add_argument("--status", choices=("draft", "published"), default="draft",
                        help="HTML status only; published removes the draft banner/noindex, never changes source JSON")
    args = parser.parse_args(argv)
    try:
        pages = generate_pages(LEGAL_DIR, status=args.status)
        for relative, raw in pages.items():
            destination = LEGAL_DIR / relative
            if args.check:
                if not destination.exists() or destination.read_bytes() != raw:
                    raise ValueError(f"Generated legal HTML differs: {relative}")
            else:
                destination.parent.mkdir(parents=True, exist_ok=True)
                destination.write_bytes(raw)
    except (OSError, ValueError) as error:
        print(f"Cube legal generation failed: {error}", file=sys.stderr)
        return 1
    print(f"Cube legal HTML {'matches' if args.check else 'generated'}: {len(pages)} pages ({args.status})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

"""Keep both generic legal pages complete, escaped, hash-checked and reproducible."""

from copy import deepcopy
from html.parser import HTMLParser
import io
import json
from pathlib import Path
import re
import shutil
import tempfile
import unittest
from unittest.mock import patch

import build_cube_legal as build


class LegalHTML(HTMLParser):
    def __init__(self):
        super().__init__()
        self.paragraphs, self.headings, self.ids, self.links = [], [], [], []
        self.stack, self.errors = [], []
        self.current = None
        self.heading = None

    def handle_starttag(self, tag, attributes):
        attrs = dict(attributes)
        if "id" in attrs:
            self.ids.append(attrs["id"])
        if "href" in attrs:
            self.links.append(attrs["href"])
        if tag == "p" and attrs.get("class") == "legal-paragraph":
            self.current = ""
        if tag == "h2":
            self.heading = ""
        if tag not in ("meta", "link", "img", "br", "hr", "input"):
            self.stack.append(tag)

    def handle_endtag(self, tag):
        if not self.stack or self.stack.pop() != tag:
            self.errors.append(tag)
        if self.current is not None and tag == "p":
            self.paragraphs.append(self.current)
            self.current = None
        if self.heading is not None and tag == "h2":
            self.headings.append(self.heading)
            self.heading = None

    def handle_data(self, data):
        if self.current is not None:
            self.current += data
        if self.heading is not None:
            self.heading += data


class LegalGeneratorTests(unittest.TestCase):
    def setUp(self):
        self.catalog = build.read_catalog(build.LEGAL_DIR)
        self.item = self.catalog[0]

    def test_generated_pages_match_and_do_not_mutate_source_bytes(self):
        before = {path: path.read_bytes() for path in build.LEGAL_DIR.rglob("*.json")}
        pages = build.generate_pages(build.LEGAL_DIR)
        self.assertEqual(len(pages), 3)
        for relative, raw in pages.items():
            self.assertEqual(raw, (build.LEGAL_DIR / relative).read_bytes())
            self.assertIn(build.DRAFT_NOTICE.encode(), raw)
            self.assertIn(b'<meta name="robots" content="noindex">', raw)
        self.assertEqual(before, {path: path.read_bytes() for path in before})

    def test_all_authored_paragraphs_headings_links_and_canonicals_survive(self):
        for kind in build.KINDS:
            with self.subTest(kind=kind):
                document = self.item.documents[kind]
                page = LegalHTML()
                page.feed(build.render(document, self.item.release, kind).decode("utf-8"))
                self.assertFalse(page.errors)
                self.assertFalse(page.stack)
                self.assertEqual(page.paragraphs, [p for s in document["sections"] for p in s["paragraphs"]])
                self.assertEqual(page.headings, [s["heading"] for s in document["sections"]])
                self.assertEqual(len(page.ids), len(set(page.ids)))
                self.assertTrue(all(link[1:] in page.ids for link in page.links if link.startswith("#")))
                self.assertIn(document["source_url"], page.links)
                self.assertIn(build.document_url(1, kind), page.links)
                for paragraph in page.paragraphs:
                    for url in re.findall(r"https://[^\s<>\"()]+", paragraph):
                        self.assertIn(url.rstrip(".,;:!?"), page.links)
                self.assertIn("mailto:mengjingchanyu@gmail.com", page.links)

    def test_html_and_link_attributes_are_escaped_without_changing_words(self):
        document = deepcopy(self.item.documents["terms"])
        value = '<script>alert("unsafe")</script> & person@example.com. https://example.com/?q=a&b=c'
        document["sections"][0]["paragraphs"].append(value)
        document["sections"][0]["heading"] = '<img src=x onerror="oops">'
        document["title"] = '<unsafe> & "title"'
        raw = build.render(document, self.item.release, "terms").decode()
        self.assertNotIn("<script>", raw)
        self.assertNotIn("<img src=x", raw)
        self.assertIn("&lt;unsafe&gt;", raw)
        self.assertIn('href="https://example.com/?q=a&amp;b=c"', raw)
        page = LegalHTML()
        page.feed(raw)
        self.assertIn(value, page.paragraphs)
        self.assertIn(document["sections"][0]["heading"], page.headings)

    def test_generic_renderer_has_no_fixed_section_count_or_heading_names(self):
        document = deepcopy(self.item.documents["terms"])
        document["sections"] = [{"heading": "重复 heading", "paragraphs": ["One paragraph."]}] * 2
        page = LegalHTML()
        page.feed(build.render(document, self.item.release, "terms").decode())
        self.assertEqual(page.ids, ["section-1", "section-2"])
        self.assertEqual(page.paragraphs, ["One paragraph."] * 2)
        self.assertFalse(page.errors)

    def test_published_html_mode_only_changes_status_not_json_or_authored_text(self):
        before = {path: path.read_bytes() for path in build.LEGAL_DIR.rglob("*.json")}
        draft = build.generate_pages(build.LEGAL_DIR)
        published = build.generate_pages(build.LEGAL_DIR, status="published")
        self.assertEqual(set(draft), set(published))
        for relative, raw in published.items():
            self.assertNotIn(build.DRAFT_NOTICE.encode(), raw)
            self.assertNotIn(b'content="noindex"', raw)
            first, second = LegalHTML(), LegalHTML()
            first.feed(draft[relative].decode())
            second.feed(raw.decode())
            self.assertEqual(first.paragraphs, second.paragraphs)
            self.assertEqual(first.links, second.links)
        self.assertEqual(before, {path: path.read_bytes() for path in before})

    def test_check_reports_drift_without_writing(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / "legal"
            shutil.copytree(build.LEGAL_DIR, root)
            output = root / "index.html"
            output.write_bytes(b"Stale page")
            with patch.object(build, "LEGAL_DIR", root), patch("sys.stderr", new=io.StringIO()):
                self.assertEqual(build.main(["--check"]), 1)
            self.assertEqual(output.read_bytes(), b"Stale page")
            with patch.object(build, "LEGAL_DIR", root), patch("sys.stdout", new=io.StringIO()):
                self.assertEqual(build.main([]), 0)
                self.assertEqual(build.main(["--check"]), 0)
                self.assertEqual(build.main(["--status", "published"]), 0)
                self.assertEqual(build.main(["--check", "--status", "published"]), 0)
            with patch.object(build, "LEGAL_DIR", root), patch("sys.stderr", new=io.StringIO()):
                self.assertEqual(build.main(["--check"]), 1)

    def test_generation_rejects_partial_set_or_raw_whitespace_hash_mutation(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / "legal"
            shutil.copytree(build.LEGAL_DIR, root)
            terms = root / build.document_path(1, "terms")
            original = terms.read_bytes()
            terms.write_bytes(original + b" ")
            with self.assertRaises(ValueError):
                build.generate_pages(root)
            terms.unlink()
            with self.assertRaises(OSError):
                build.generate_pages(root)

    def test_independent_schema_rejects_malformed_protocol_and_remote_targets(self):
        raw = self.item.manifest_raw
        for malformed in (b"\xef\xbb\xbf" + raw, b"\xff", b'{"revision":1,' + raw.lstrip()[1:]):
            with self.assertRaises(ValueError):
                build.load_manifest(malformed)
        for mutate in (
            lambda m: m.update(extra=True),
            lambda m: m.update(schema_version=True),
            lambda m: m["releases"][0].update(recipients=["unknown"]),
            lambda m: m["releases"][0].update(url="https://evil.example"),
            lambda m: m["releases"][0]["documents"].pop("terms"),
        ):
            manifest = deepcopy(self.item.manifest)
            mutate(manifest)
            with self.assertRaises(ValueError):
                build.load_manifest(json.dumps(manifest).encode())
        document = dict(self.item.documents["privacy"], source_url="https://evil.example/")
        with self.assertRaises(ValueError):
            build.load_document(json.dumps(document).encode(), kind="privacy", release_revision=1)

    def test_version_bounds_and_future_compatible_selection(self):
        manifest = deepcopy(self.item.manifest)
        later = deepcopy(manifest["releases"][0])
        later.update(revision=2, min_app_version="2.0.0", effective_date="2099-01-01")
        manifest.update(revision=2, releases=[later, manifest["releases"][0]])
        loaded = build.load_manifest(json.dumps(manifest).encode())
        self.assertEqual(build.select_release(loaded, "1.0.14", today="2026-10-21")["revision"], 1)
        with self.assertRaises(ValueError):
            build.select_release(loaded, "1.0.13", today="2026-10-21")
        self.assertEqual(build.select_release(loaded, "2.0.0", today="2099-01-01")["revision"], 2)


if __name__ == "__main__":
    unittest.main()

"""Keep the generated website complete, escaped and in sync with policy.json."""

from copy import deepcopy
from html.parser import HTMLParser
import io
import json
import re
import tempfile
import unittest
from unittest.mock import patch
from pathlib import Path

import build_cube_privacy as build


class PolicyHTML(HTMLParser):
    def __init__(self):
        super().__init__()
        self.blocks = []
        self.headings = []
        self.ids = []
        self.links = []
        self.stack = []
        self.current = None
        self.heading = None
        self.errors = []

    def handle_starttag(self, tag, attributes):
        attrs = dict(attributes)
        if "id" in attrs:
            self.ids.append(attrs["id"])
        if "href" in attrs:
            self.links.append(attrs["href"])
        if tag in ("p", "li", "h3") or attrs.get("class") == "note":
            self.current = [tag, ""]
        if tag in ("h1", "h2"):
            self.heading = ""
        if tag not in ("meta", "link", "img", "br", "hr", "input"):
            self.stack.append(tag)

    def handle_endtag(self, tag):
        if not self.stack or self.stack.pop() != tag:
            self.errors.append(tag)
        if self.current and tag == self.current[0]:
            self.blocks.append(("• " if tag == "li" else "") + self.current[1])
            self.current = None
        if self.heading is not None and tag in ("h1", "h2"):
            self.headings.append(self.heading)
            self.heading = None

    def handle_data(self, data):
        if self.current:
            self.current[1] += data
        if self.heading is not None:
            self.heading += data


class GeneratorTests(unittest.TestCase):
    def setUp(self):
        self.raw = (build.POLICY_DIR / "policy.json").read_bytes()
        self.policy = build.load_policy(self.raw)
        self.template = (build.POLICY_DIR / "index.template.html").read_text()

    def test_generated_page_matches_committed_html(self):
        self.assertEqual(build.render(self.policy, self.template), (build.POLICY_DIR / "index.html").read_text())

    def test_all_authored_paragraphs_and_headings_are_preserved(self):
        page = PolicyHTML()
        page.feed(build.render(self.policy, self.template))
        self.assertFalse(page.errors)
        self.assertFalse(page.stack)
        self.assertEqual(page.blocks, [paragraph for section in self.policy["sections"] for paragraph in section["paragraphs"]])
        self.assertEqual(page.headings, [self.policy["title"]] + [section["heading"] for section in self.policy["sections"][1:]])
        self.assertEqual(len(page.ids), len(set(page.ids)))
        self.assertTrue(all(link[1:] in page.ids for link in page.links if link.startswith("#")))
        self.assertTrue(set(build.SECTION_IDS.values()).issubset(page.ids))
        self.assertIn(build.SOURCE_URL, page.links)
        self.assertIn("mailto:mengjingchanyu@gmail.com?subject=The%20Cube%20Privacy%20Request", page.links)
        for url in re.findall(r"https://[^\s()]+", self.raw.decode()):
            self.assertIn(url.rstrip('\",'), page.links)

    def test_authored_html_is_escaped_and_link_text_preserved(self):
        policy = deepcopy(self.policy)
        text = '<script>alert("unsafe")</script> & contact person@example.com. https://example.com/?q=a&b=c'
        policy["sections"][2]["paragraphs"].append(text)
        html = build.render(policy, self.template)
        self.assertNotIn("<script>", html)
        self.assertIn("&lt;script&gt;", html)
        self.assertIn('href="https://example.com/?q=a&amp;b=c"', html)
        page = PolicyHTML()
        page.feed(html)
        self.assertIn(text, page.blocks)

    def test_future_sections_get_unique_working_fragment_links(self):
        policy = deepcopy(self.policy)
        policy["sections"].extend([{"heading": "New section", "paragraphs": ["Future text."]}] * 2)
        page = PolicyHTML()
        page.feed(build.render(policy, self.template))
        self.assertIn("new-section", page.ids)
        self.assertIn("new-section-2", page.ids)
        self.assertEqual(len(page.ids), len(set(page.ids)))

    def test_equal_effective_and_updated_dates_do_not_nest_time_elements(self):
        policy = deepcopy(self.policy)
        policy["effective_date"] = policy["updated_at"] = "2026-10-09"
        policy["sections"][0]["paragraphs"][0] = "Effective date: October 9, 2026 · Last updated: October 9, 2026 · Developer: Monsoon Isle"
        html = build.render(policy, self.template)
        self.assertEqual(html.count('<time datetime="2026-10-09">October 9, 2026</time>'), 2)

    def test_schema_and_size_rejection(self):
        for key, value in (("schema_version", 2), ("schema_version", True), ("revision", 0),
                           ("source_url", "https://example.com/"), ("language", "fr"),
                           ("max_app_version", "0.0.1"), ("updated_at", "invalid")):
            with self.subTest(key=key, value=value), self.assertRaises(ValueError):
                build.load_policy(json.dumps(dict(self.policy, **{key: value})).encode())
        with self.assertRaises(ValueError):
            build.load_policy(self.raw + b" " * build.MAX_BYTES)
        with self.assertRaises(ValueError):
            build.load_policy(b'{"revision": 1,' + self.raw.lstrip()[1:])

    def test_version_component_width_leading_zeros_and_title_boundary(self):
        for version, expected in (("000000001.000.000000009", (1, 0, 9)),
                                  ("999999999.999999999.999999999", (999999999,) * 3)):
            with self.subTest(version=version):
                self.assertEqual(build.version_parts(version), expected)
                policy = dict(self.policy, min_app_version=version, max_app_version=version, title="x" * 256)
                build.load_policy(json.dumps(policy).encode())
        for version in ("1000000000.0.0", "0.0000000000.0", "0.0.0000000000", "1.0.9\n", "١.0.9", "+1.0.9"):
            with self.subTest(version=version), self.assertRaises(ValueError):
                build.version_parts(version)
        with self.assertRaisesRegex(ValueError, "title"):
            build.load_policy(json.dumps(dict(self.policy, title="x" * 257)).encode())

    def test_json_escapes_are_decoded_and_duplicate_keys_rejected(self):
        policy = deepcopy(self.policy)
        policy["sections"][2]["paragraphs"].append('Escapes: "quote", \\ path, and \n newline.')
        self.assertEqual(build.load_policy(json.dumps(policy).encode()), policy)
        for raw in (
            b'{"\\u0072evision": 1,' + self.raw.lstrip()[1:],
            self.raw.replace(b'"heading": ', b'"\\u0068eading": "Duplicate", "heading": ', 1),
            b'{"title": "bad\\qescape",' + self.raw.lstrip()[1:],
            json.dumps(dict(self.policy, title="bad\x00text")).encode(),
            json.dumps(dict(self.policy, title="\ud800")).encode(),
        ):
            with self.subTest(raw=raw[:100]), self.assertRaises(ValueError):
                build.load_policy(raw)

    def test_check_reports_drift_without_writing(self):
        with tempfile.TemporaryDirectory(prefix="cube-website-") as directory:
            root = Path(directory)
            (root / "policy.json").write_bytes(self.raw)
            (root / "index.template.html").write_text(self.template)
            output = root / "index.html"
            output.write_text("Stale page")
            with patch.object(build, "POLICY_DIR", root), patch("sys.stderr", new=io.StringIO()):
                self.assertEqual(build.main(["--check"]), 1)
            self.assertEqual(output.read_text(), "Stale page")
            with patch.object(build, "POLICY_DIR", root), patch("sys.stdout", new=io.StringIO()):
                self.assertEqual(build.main([]), 0)
                self.assertEqual(build.main(["--check"]), 0)


if __name__ == "__main__":
    unittest.main()

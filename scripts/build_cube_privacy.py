#!/usr/bin/env python3
"""Generate The Cube privacy HTML from policy.json; check with --check (stdlib only)."""

import argparse
from datetime import date
from html import escape
import json
from pathlib import Path
import re
from string import Template
import sys


ROOT = Path(__file__).resolve().parents[1]
POLICY_DIR = ROOT / "en/games/the-cube/privacy"
SOURCE_URL = "https://monsoonisle.github.io/en/games/the-cube/privacy/"
# Schema 1 is also validated by the game's scripts/sync_privacy_policy.py.
MAX_BYTES = 262144
MAX_TEXT = 16384
FIELDS = {"schema_version", "policy_id", "language", "revision", "updated_at",
          "min_app_version", "max_app_version", "title", "effective_date",
          "source_url", "sections"}


def _unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"Duplicate JSON key: {key}")
        result[key] = value
    return result


def _invalid_constant(value):
    raise ValueError(f"Invalid JSON constant: {value}")


def _text(value, label, maximum=MAX_TEXT):
    if not isinstance(value, str) or not value.strip() or len(value) > maximum:
        raise ValueError(f"Invalid {label}: expected nonempty text up to {maximum} characters")
    if any(ord(char) < 32 and char not in "\n\r\t" for char in value):
        raise ValueError(f"Invalid control character in {label}")
    value.encode("utf-8")  # Reject escaped unpaired surrogates as well as invalid UTF-8 bytes.


def version_parts(value):
    if not isinstance(value, str) or not re.fullmatch(r"[0-9]{1,9}\.[0-9]{1,9}\.[0-9]{1,9}", value):
        raise ValueError("App versions must contain three components of 1–9 ASCII digits")
    return tuple(int(part) for part in value.split("."))


def load_policy(raw):
    """Validate schema 1 before allowing content into a bundle or generated page."""
    if not raw or len(raw) > MAX_BYTES:
        raise ValueError(f"Policy must contain 1–{MAX_BYTES} UTF-8 bytes")
    try:
        policy = json.loads(raw.decode("utf-8"), object_pairs_hook=_unique_object,
                            parse_constant=_invalid_constant)
    except (UnicodeError, RecursionError) as error:
        raise ValueError("Policy must contain valid UTF-8 JSON without excessive nesting") from error
    if not isinstance(policy, dict) or set(policy) != FIELDS:
        raise ValueError("Unexpected policy fields")
    if type(policy["schema_version"]) is not int or policy["schema_version"] != 1:
        raise ValueError("Unsupported policy schema_version")
    if policy["policy_id"] != "the-cube" or policy["language"] != "en":
        raise ValueError("Policy must be The Cube English policy")
    if policy["source_url"] != SOURCE_URL:
        raise ValueError("Unexpected policy source_url")
    if type(policy["revision"]) is not int or not 1 <= policy["revision"] <= 2147483647:
        raise ValueError("Policy revision must be a positive 32-bit integer")
    for key in ("effective_date", "updated_at"):
        value = policy[key]
        if not isinstance(value, str) or not re.fullmatch(r"[0-9]{4}-[0-9]{2}-[0-9]{2}", value):
            raise ValueError(f"Invalid {key}")
        date.fromisoformat(value)
    if policy["updated_at"] < policy["effective_date"]:
        raise ValueError("updated_at must not precede effective_date")
    minimum = version_parts(policy["min_app_version"])
    maximum = policy["max_app_version"]
    if maximum != "" and version_parts(maximum) < minimum:
        raise ValueError("max_app_version must not precede min_app_version")
    _text(policy["title"], "title", 256)
    sections = policy["sections"]
    if not isinstance(sections, list) or not 1 <= len(sections) <= 64:
        raise ValueError("Policy must contain 1–64 sections")
    total = 0
    for section in sections:
        if not isinstance(section, dict) or set(section) != {"heading", "paragraphs"}:
            raise ValueError("Unexpected section fields")
        _text(section["heading"], "heading")
        paragraphs = section["paragraphs"]
        if not isinstance(paragraphs, list) or not paragraphs:
            raise ValueError("Each section must contain paragraphs")
        total += len(paragraphs)
        if total > 256:
            raise ValueError("Policy must contain at most 256 paragraphs in total")
        for paragraph in paragraphs:
            _text(paragraph, "paragraph")
    return policy


# Preserve existing public fragment URLs while allowing new sections to be added.
SECTION_IDS = {
    "1. Scope and contact": "scope",
    "2. Local data and support": "local",
    "3. Optional usage analytics": "analytics",
    "4. Optional crash diagnostics": "diagnostics",
    "5. Advertising": "ads",
    "6. Purposes and legal bases": "purposes",
    "7. Sharing and international processing": "sharing",
    "8. Retention and deletion": "retention",
    "9. Your choices and privacy rights": "choices",
    "10. Intended audience": "audience",
    "11. Security": "security",
    "12. Website and external links": "website",
    "13. Policy updates": "changes",
}
SUBHEADINGS = {"In-game and device controls", "Privacy requests and regional rights"}
# Presentation hints preserve the existing emphasis without making it policy data.
EMPHASIS = (
    "Your choices matter.", "Share usage statistics", "Share crash diagnostics",
    "Restart the app to fully apply this change.", "Survival:", "Challenges:",
    "Optional revives:", "Google and advertising partners:", "Hosting and email providers:",
    "Legal and security needs:", "Google Analytics retention:", "2 months", "14 months",
    "Settings → More Settings", "About & Privacy", "Privacy & Data Choices",
    "Review privacy choices", "Privacy Policy", "Contact Support", "Right to object:",
    "users aged 13 and over",
)
INLINE = re.compile(
    r'(?P<link>https://[^\s<>"()]+|[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,})'
    + r'|(?P<strong>' + "|".join(re.escape(value) for value in EMPHASIS) + r')'
    + r'|(?P<package>com\.tesselox\.game)'
)


def inline(text):
    """Escape authored text and link its URLs/email without changing displayed words."""
    parts = []
    cursor = 0
    for match in INLINE.finditer(text):
        value = match.group().rstrip(".,;") if match.lastgroup == "link" else match.group()
        end = match.start() + len(value)
        parts.append(escape(text[cursor:match.start()], quote=False))
        if match.lastgroup == "link":
            href = value if value.startswith("https://") else "mailto:" + value
            if value == "mengjingchanyu@gmail.com" and "The Cube Privacy Request" in text:
                href += "?subject=The%20Cube%20Privacy%20Request"
            parts.append(f'<a href="{escape(href, quote=True)}">{escape(value, quote=False)}</a>')
        elif match.lastgroup == "strong":
            parts.append(f'<strong>{escape(value, quote=False)}</strong>')
        else:
            parts.append(f'<span class="package-name">{escape(value, quote=False)}</span>')
        cursor = end
    parts.append(escape(text[cursor:], quote=False))
    return "".join(parts)


def paragraphs(values, indent="          "):
    lines = []
    in_list = False
    for value in values:
        bullet = value.startswith("• ")
        if in_list and not bullet:
            lines.append(indent + "</ul>")
            in_list = False
        if bullet:
            if not in_list:
                lines.append(indent + "<ul>")
                in_list = True
            lines.append(indent + "  <li>" + inline(value[2:]) + "</li>")
        else:
            tag = "h3" if value in SUBHEADINGS else "p"
            lines.append(f"{indent}<{tag}>{inline(value)}</{tag}>")
    if in_list:
        lines.append(indent + "</ul>")
    return "\n".join(lines)


def render(policy, template):
    sections = policy["sections"]
    if len(sections) < 3:
        raise ValueError("Website policy requires introduction, summary and body sections")
    hero, summary, *body = sections
    identifiers = []
    used = {"summary-title"}
    for section in body:
        base = SECTION_IDS.get(section["heading"]) or re.sub(r"[^a-z0-9]+", "-", section["heading"].lower()).strip("-") or "section"
        identifier = base
        suffix = 2
        while identifier in used:
            identifier = f"{base}-{suffix}"
            suffix += 1
        used.add(identifier)
        identifiers.append(identifier)
    lines = [
        '    <div class="legal-hero">',
        f'      <span class="eyebrow">{escape(hero["heading"].upper())} · LEGAL</span>',
        f'      <h1>{escape(policy["title"])}</h1>',
    ]
    for index, text in enumerate(hero["paragraphs"]):
        if index == 0:
            # Dates remain authored text; add semantic time tags only on an exact match.
            formatted = inline(text)
            dates = {}
            for key in ("effective_date", "updated_at"):
                value = date.fromisoformat(policy[key])
                label = f"{value.strftime('%B')} {value.day}, {value.year}"
                dates[label] = policy[key]
            formatted = re.sub(
                "|".join(re.escape(label) for label in dates),
                lambda match: f'<time datetime="{dates[match.group()]}">{match.group()}</time>',
                formatted,
            )
            lines.append(f'      <p class="small">{formatted}</p>')
        elif index == 1:
            lines.append(f'      <p class="legal-intro">{inline(text)}</p>')
        elif index == 2:
            lines.append(f'      <div class="note" role="note">{inline(text)}</div>')
        else:
            lines.append(f'      <p>{inline(text)}</p>')
    lines += ['    </div>', '    <div class="legal-layout">',
              '      <aside class="toc" aria-label="Privacy policy contents">']
    for section, identifier in zip(body, identifiers):
        lines.append(f'        <a href="#{identifier}">{escape(section["heading"])}</a>')
    lines += ['      </aside>', '      <article class="policy">',
              '        <div class="policy-summary" aria-labelledby="summary-title">',
              f'          <h2 id="summary-title">{escape(summary["heading"])}</h2>',
              paragraphs(summary["paragraphs"]), '        </div>']
    for section, identifier in zip(body, identifiers):
        lines += [f'        <section id="{identifier}">',
                  f'          <h2>{escape(section["heading"])}</h2>',
                  paragraphs(section["paragraphs"]), '        </section>']
    lines += ['      </article>', '    </div>']
    return Template(template).substitute(
        page_title=escape(f'{hero["heading"]} — {policy["title"]} | Monsoon Isle'),
        language=escape(policy["language"], quote=True),
        source_url=escape(policy["source_url"], quote=True),
        policy_body="\n".join(lines),
    )


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Fail if generated HTML has drifted; never write")
    args = parser.parse_args(argv)
    try:
        with (POLICY_DIR / "policy.json").open("rb") as stream:
            policy = load_policy(stream.read(MAX_BYTES + 1))
        output = render(policy, (POLICY_DIR / "index.template.html").read_text(encoding="utf-8"))
        destination = POLICY_DIR / "index.html"
        if args.check:
            if not destination.exists() or destination.read_text(encoding="utf-8") != output:
                raise ValueError("Generated Cube privacy HTML differs; run python3 scripts/build_cube_privacy.py")
        else:
            destination.write_text(output, encoding="utf-8")
    except (OSError, ValueError, KeyError) as error:
        print(f"Cube privacy generation failed: {error}", file=sys.stderr)
        return 1
    print(f"Cube privacy HTML {'matches' if args.check else 'generated from'} policy.json, revision {policy['revision']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())


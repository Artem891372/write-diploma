#!/usr/bin/env python3
"""Standalone validator for the «Оформитель» MD dialect (GOST 7.32 / 2.105).

Why: the `write-diploma` skill must work for any AI — without access to the
«Оформитель» service or its backend. This script parses the Markdown dialect (not
YAML) and finds the same typical problems as the service validator, under the same
rule codes — so the findings the AI shows and fixes match production.

Dependencies: Python 3.8+ standard library only. No PyYAML, no rendering engine.

Usage:
    python3 scripts/validate.py paper.md            # human-readable
    python3 scripts/validate.py paper.md --json     # machine-readable
    python3 scripts/validate.py paper.md.zip        # archive with assets/ (checks files)

    from validate import validate_markdown
    result = validate_markdown(text)   # {"ok", "errors", "warnings", "notes", "stats"}

Exit code: 0 — no hard errors; 1 — there is a hard-error (handy for CI and agents).

Rules and their meaning — references/rules.md. The dialect — references/dialect.md.
This parser is a best-effort mirror of the service dialect; the service remains the
source of truth if the two ever disagree.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
import zipfile
from typing import Dict, List, Optional, Tuple

# ── Sections (mirrors the service's section recognition) ─────────────────────

SECTION_KIND_BY_TITLE = {
    "реферат": "abstract", "аннотация": "abstract",
    "содержание": "toc", "оглавление": "toc",
    "введение": "introduction",
    "заключение": "conclusion",
    "список использованных источников": "bibliography",
    "список литературы": "bibliography",
    "термины и определения": "terms",
    "перечень сокращений и обозначений": "abbreviations",
    "перечень сокращений": "abbreviations",
    "список сокращений": "abbreviations",
    "сокращения": "abbreviations",
    "сокращения и обозначения": "abbreviations",
    "нормативные ссылки": "normative_refs",
    "список исполнителей": "performers",
}
_APPENDIX_OPENER = "приложения"
_PREFIX_KEYS = sorted(SECTION_KIND_BY_TITLE, key=len, reverse=True)

# Sections where elements are forbidden (token → set of forbidden kinds).
# A table is allowed only in terms/abbreviations (see the dialect).
_FORBID_TABLE_AND_MORE = {"table", "image", "math", "code"}
_FORBID_NON_TABLE = {"image", "math", "code"}
RESTRICTED_SECTIONS: Dict[str, frozenset] = {
    "abstract": frozenset(_FORBID_TABLE_AND_MORE),
    "introduction": frozenset(_FORBID_TABLE_AND_MORE),
    "conclusion": frozenset(_FORBID_TABLE_AND_MORE),
    "bibliography": frozenset(_FORBID_TABLE_AND_MORE),
    "normative_refs": frozenset(_FORBID_TABLE_AND_MORE),
    "terms": frozenset(_FORBID_NON_TABLE),
    "abbreviations": frozenset(_FORBID_NON_TABLE),
}

# Section length limits (defaults, as in the base gost_7.32 style).
LIMITS = {
    "abstract": {"max": 2400, "warn": 1800, "prefix": "ABSTRACT"},
    "introduction": {"max": 6000, "warn": 5000, "prefix": "INTRODUCTION"},
    "conclusion": {"max": 6000, "warn": 4000, "prefix": "CONCLUSION"},
}
KEYWORDS_MIN, KEYWORDS_MAX = 5, 15
MIN_SOURCES = 15

# Diagrams: a fenced block with one of these languages is a figure (id/caption in attrs).
DIAGRAM_LANGS = {
    "plantuml", "mermaid", "graphviz", "dot", "d2", "ditaa", "erd", "bpmn",
    "dbml", "wavedrom", "vega", "vegalite", "vega-lite", "nomnoml", "pikchr",
    "structurizr", "svgbob", "bytefield", "umlet", "excalidraw", "blockdiag",
    "seqdiag", "actdiag", "nwdiag", "packetdiag", "rackdiag", "c4plantuml",
    "symbolator", "wireviz",
}
KNOWN_CONTAINERS = {
    "where", "note", "example", "keywords", "frame", "landscape", "pagebreak",
}

_ATTR_RE = re.compile(r"\{([^{}]*)\}")
_TOKEN_RE = re.compile(r'([\wа-яА-ЯёЁ.-]+)\s*=\s*("([^"]*)"|\'([^\']*)\'|[^\s]+)|([\wа-яА-ЯёЁ-]+)')
_H1_RE = re.compile(r"^(#{1,6})\s+(.*)$")
_FENCE_RE = re.compile(r"^(\s*)(```+|~~~+)\s*([A-Za-z0-9_+-]*)\s*(.*)$")
_IMG_RE = re.compile(r"!\[(.*?)\]\(([^)]*)\)\s*(.*)$")
_TABLE_SEP_RE = re.compile(r"^\s*\|?[\s:|-]+\|?\s*$")
_CAPTION_RE = re.compile(r"^\s*:\s+?(.*)$")
_REF_RE = re.compile(r"\{ref:([A-Za-z0-9_]+)\}")
_CITE_RE = re.compile(r"\[@([^\]]+)\]")
_COUNTER_ABBREV_RE = re.compile(
    r"(?<![А-Яа-яA-Za-z])(?:с|стр|рис|табл|источн|прил|лист)\.", re.IGNORECASE)

# Manual numbering (mirrors the service's manual_numbering).
_NUM = r"\d+(?:[.,]\d+)*"
_MANUAL_INLINE = [
    ("рисунок", re.compile(rf"\bрис(?:ун\w+|\.)?\s*№?\s*{_NUM}", re.I)),
    ("таблица", re.compile(rf"\bтабл(?:иц\w+|\.)?\s*№?\s*{_NUM}", re.I)),
    ("листинг", re.compile(rf"\bлистинг\w*\s*№?\s*{_NUM}", re.I)),
    ("формула", re.compile(rf"\bформ(?:ул\w+|\.)?\s*№?\s*\(?{_NUM}\)?", re.I)),
    ("формула", re.compile(rf"\bуравнени\w*\s*№?\s*\(?{_NUM}\)?", re.I)),
    ("раздел", re.compile(rf"\bраздел\w*\s*№?\s*{_NUM}", re.I)),
    ("раздел", re.compile(rf"\bподраздел\w*\s*№?\s*{_NUM}", re.I)),
    ("раздел", re.compile(rf"\bпункт\w*\s*№?\s*{_NUM}", re.I)),
    ("раздел", re.compile(rf"\bп\.\s*{_NUM}", re.I)),
    ("раздел", re.compile(rf"\bглав[аеы]\s*№?\s*{_NUM}", re.I)),
    ("приложение", re.compile(r"(?i:приложени\w*)\s+№?\s*[А-ЯЁA-Z0-9]")),
    ("страница", re.compile(rf"\bстр\.?\s*№?\s*{_NUM}", re.I)),
    ("страница", re.compile(rf"\bстраниц\w*\s*№?\s*{_NUM}", re.I)),
    # "на с. 4" (page reference); bare "с. 5" is left alone — that is a source's
    # page range in bibliographic entries, not manual numbering.
    ("страница", re.compile(r"\bна\s+с\.\s*\d", re.I)),
]
# A heading that starts with a section number. A leading 1–3 digit number (with an
# optional dot or a dotted number) is numbering; a bare 4-digit year ("2026 год в
# цифрах") is not, so it must not be flagged.
_MANUAL_HEADING = re.compile(
    rf"^\s*(?:"
    rf"\d{{1,3}}(?:[.)]\s+|\s+)"
    rf"|\d+(?:\.\d+)+(?:[.)]\s+|\s+)"
    rf"|(?:глава|часть|раздел|пункт|подраздел)\s+{_NUM}\b"
    rf")", re.I)
_MANUAL_EQ = re.compile(rf"^\s*\(\s*{_NUM}\s*\)\s*[.,]?\s*$")

HARD_CODES = {"ID_DUPLICATE", "TABLE_ID_MISSING"}


# ── Helpers ──────────────────────────────────────────────────────────────────

def parse_attrs(text: str) -> Dict[str, object]:
    """Parse `{...}` attributes: {#id}, {ref:id}, {caption="…"}, key=value."""
    attrs: Dict[str, object] = {}
    refs: List[str] = []
    for m in _ATTR_RE.finditer(text or ""):
        inner = m.group(1).strip()
        if not inner:
            continue
        rest = inner
        if inner.startswith("#"):
            mid = re.match(r"#([\w.-]+)", inner)
            attrs["id"] = mid.group(1)
            rest = inner[mid.end():]
        elif inner.startswith("ref:"):
            mid = re.match(r"ref:([\w.-]+)", inner)
            refs.append(mid.group(1))
            rest = inner[mid.end():]
        for tok in _TOKEN_RE.finditer(rest):
            if tok.group(1):
                val = tok.group(3) if tok.group(3) is not None else (
                    tok.group(4) if tok.group(4) is not None else tok.group(5))
                attrs[tok.group(1)] = val
            elif tok.group(5):
                attrs[tok.group(5)] = True
    if refs:
        attrs["refs"] = refs
    return attrs


def _kind_by_title(title: str) -> Optional[str]:
    key = title.strip().lower().rstrip(".")
    if key in SECTION_KIND_BY_TITLE:
        return SECTION_KIND_BY_TITLE[key]
    for name in _PREFIX_KEYS:
        if key.startswith(name + " "):
            return SECTION_KIND_BY_TITLE[name]
    return None


def _is_table_sep(line: str) -> bool:
    return bool(_TABLE_SEP_RE.match(line) and "-" in line and "|" in line)


def _split_row(line: str) -> List[str]:
    s = line.strip()
    if s.startswith("|"):
        s = s[1:]
    if s.endswith("|"):
        s = s[:-1]
    return [c.strip() for c in s.split("|")]


def _is_empty(cell: str) -> bool:
    return (cell or "").strip() == ""


def _is_fence_close(line: str, fence_char: str, length: int) -> bool:
    """A closing fence is a run of the same char, at least as long as the opener."""
    s = line.strip()
    c = 0
    while c < len(s) and s[c] == fence_char:
        c += 1
    return c >= length and not s[c:].strip()


# ── Document parsing ─────────────────────────────────────────────────────────

class Elem(dict):
    """A document element: a dict with attribute access for readability."""

    def __getattr__(self, item):  # noqa: D105
        try:
            return self[item]
        except KeyError as e:
            raise AttributeError(item) from e


def parse_document(text: str) -> Tuple[List[Elem], List[dict]]:
    """Return (elements, sections) in document order.

    Element: {el, id, line, text, section_kind, section_title, ...}.
    Section: {kind, title, start_line, chars}.
    """
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    lines = text.split("\n")
    elems: List[Elem] = []
    sections: List[dict] = []
    cur_kind, cur_title = "preamble", ""
    cur_section: Optional[dict] = None
    appendix_mode = False
    i = 0
    n = len(lines)

    def push(el: str, line: int, **kw):
        e = Elem(el=el, line=line, section_kind=cur_kind, section_title=cur_title, **kw)
        elems.append(e)
        return e

    while i < n:
        raw = lines[i]
        line_no = i + 1
        stripped = raw.strip()

        # fenced block (``` / ~~~): code, listing, or diagram
        mf = _FENCE_RE.match(raw)
        if mf:
            marker = mf.group(2)
            lang = (mf.group(3) or "").lower()
            rest = mf.group(4) or ""
            attrs = parse_attrs(rest)
            body: List[str] = []
            j = i + 1
            closed = False
            while j < n:
                if _is_fence_close(lines[j], marker[0], len(marker)):
                    closed = True
                    break
                body.append(lines[j])
                j += 1
            if not closed:
                push("unclosed", line_no, detail="```")
            code_text = "\n".join(body)
            if lang in DIAGRAM_LANGS:
                push("diagram", line_no, id=attrs.get("id"), caption=attrs.get("caption"),
                     sheet_of=attrs.get("sheet_of"), empty=not code_text.strip(),
                     text=code_text)
            elif attrs.get("caption"):
                push("listing", line_no, id=attrs.get("id"), caption=attrs.get("caption"),
                     empty=not code_text.strip(), text=code_text)
            else:
                push("code", line_no, text=code_text, empty=not code_text.strip())
            i = j + 1
            continue

        # block formula $$ … $$
        if stripped.startswith("$$"):
            buf: List[str] = []
            rest_attrs = ""
            if stripped.count("$$") >= 2:
                parts = stripped.split("$$")
                buf.append(parts[1])
                rest_attrs = parts[2] if len(parts) > 2 else ""
                j = i + 1
                closed = True
            else:
                first = stripped[2:]
                if first:
                    buf.append(first)
                j = i + 1
                closed = False
                while j < n:
                    if "$$" in lines[j]:
                        before, _, after = lines[j].partition("$$")
                        if before.strip():
                            buf.append(before)
                        rest_attrs = after
                        closed = True
                        break
                    buf.append(lines[j])
                    j += 1
            if not closed:
                push("unclosed", line_no, detail="$$")
            attrs = parse_attrs(rest_attrs)
            push("formula", line_no, id=attrs.get("id"), text="\n".join(buf).strip())
            i = j + 1
            continue

        # container ::: name … :::
        mc = re.match(r"^:::\s*(\w+)?\s*(.*)$", stripped)
        if mc and stripped.startswith(":::"):
            name = (mc.group(1) or "").lower()
            if not name:  # closing ::: without a name
                i += 1
                continue
            if name not in KNOWN_CONTAINERS:
                push("unknown_container", line_no, detail=name)
            body_lines: List[str] = []
            j = i + 1
            closed = False
            while j < n:
                s = lines[j].strip()
                if s.startswith(":::") and not re.match(r"^:::\s*\w", s):
                    closed = True
                    break
                body_lines.append(lines[j])
                j += 1
            if not closed:
                push("unclosed", line_no, detail=":::")
            body_text = "\n".join(body_lines)
            if name == "keywords":
                push("keywords", line_no, text=body_text)
            elif name == "frame":
                pass  # title-block service table — not validated
            else:
                # note/example/where/landscape content: look for tables/figures/refs
                inner = _parse_sub_blocks(body_lines, line_no + 1, cur_kind, cur_title)
                elems.extend(inner)
            i = j + 1
            continue

        # heading
        mh = _H1_RE.match(stripped)
        if mh and stripped.startswith("#"):
            level = len(mh.group(1))
            title = mh.group(2).strip()
            attrs = parse_attrs(title)
            clean_title = _ATTR_RE.sub("", title).strip()
            if level == 1:
                kind = attrs.get("kind")
                if not kind:
                    if attrs.get("letter") and clean_title.lower().startswith("приложение"):
                        kind = "appendix"
                    elif clean_title.lower().rstrip(".") == _APPENDIX_OPENER:
                        kind = "appendix_opener"
                        appendix_mode = True
                        push("heading", line_no, level=1, text=clean_title, heading_kind="appendix_opener")
                        i += 1
                        continue
                    elif appendix_mode:
                        kind = "appendix"
                    else:
                        kind = _kind_by_title(clean_title) or "chapter"
                cur_kind, cur_title = kind, clean_title
                cur_section = {"kind": kind, "title": clean_title, "start_line": line_no, "chars": 0}
                sections.append(cur_section)
                push("heading", line_no, level=1, text=clean_title)
            elif level <= 3:
                push("heading", line_no, level=level, text=clean_title)
            else:
                push("unparsed", line_no, detail=f"heading level {level}")
            i += 1
            continue

        # table
        if "|" in raw and i + 1 < n and _is_table_sep(lines[i + 1]):
            header = _split_row(raw)
            rows = [header]
            j = i + 2
            while j < n and lines[j].strip() and "|" in lines[j]:
                rows.append(_split_row(lines[j]))
                j += 1
            caption, cap_attrs = None, {}
            k = j
            while k < n and not lines[k].strip():
                k += 1
            if k < n:
                cm = _CAPTION_RE.match(lines[k])
                if cm and not lines[k].strip().startswith("::"):
                    cap_raw = cm.group(1)
                    cap_attrs = parse_attrs(cap_raw)
                    cap_text = _ATTR_RE.sub("", cap_raw).strip()
                    caption = cap_text
                    j = k + 1
            cols = max((len(r) for r in rows), default=0)
            has_empty = any(_is_empty(c) for row in rows for c in row)
            push("table", line_no, id=cap_attrs.get("id"), caption=caption,
                 rows=len(rows), cols=cols, empty_cell=has_empty)
            i = j
            continue

        # image file ![…](…)
        mi = _IMG_RE.match(stripped)
        if mi and stripped.startswith("!["):
            alt, path, rest = mi.group(1), mi.group(2), mi.group(3)
            attrs = parse_attrs(rest)
            cap = attrs.get("caption") or alt
            push("image", line_no, id=attrs.get("id"), caption=cap or None,
                 sheet_of=attrs.get("sheet_of"), path=path.strip())
            i += 1
            continue

        # quote / code line
        if stripped.startswith(">"):
            push("quote", line_no, text=stripped[1:].strip())
            i += 1
            continue

        # list items (bib_entry — when there is a leading {#key})
        ml = re.match(r"^\s*(?:[-*]|\d+[.)])\s+(.*)$", raw)
        if ml:
            content = ml.group(1)
            attrs = parse_attrs(content)
            if attrs.get("id") and cur_kind == "bibliography":
                push("bib", line_no, key=attrs["id"], text=_ATTR_RE.sub("", content).strip())
            else:
                push("list", line_no, text=content)
            i += 1
            continue

        # blank line
        if not stripped:
            i += 1
            continue

        # ordinary paragraph
        push("para", line_no, text=stripped)
        i += 1

    return elems, sections


def _parse_sub_blocks(body_lines: List[str], base_line: int, kind: str, title: str) -> List[Elem]:
    """Parse a container's nested blocks (tables, figures, paragraphs)."""
    out: List[Elem] = []
    inner_text = "\n".join(body_lines)
    tmp, _ = parse_document(f"# {title or 'Раздел'}\n\n{inner_text}")
    for e in tmp:
        if e.el == "heading":
            continue
        e = Elem(e)
        e["section_kind"] = kind
        e["section_title"] = title
        e["line"] = base_line + max(0, e.get("line", 1) - 3)
        out.append(e)
    return out


# ── Checks ───────────────────────────────────────────────────────────────────

def _finding(code: str, level: str, line: Optional[int], message: str,
             suggestion: str = "") -> dict:
    return {"code": code, "level": level, "line": line,
            "message": message, "suggestion": suggestion}


def _manual_in(text: str, heading: bool = False) -> List[Tuple[str, str]]:
    if not text:
        return []
    found: List[Tuple[str, str]] = []
    seen = set()
    if heading:
        if _MANUAL_HEADING.match(text):
            return [("heading", text.strip())]
        return []
    for label, rx in _MANUAL_INLINE:
        for m in rx.finditer(text):
            frag = m.group(0).strip()
            if frag and frag not in seen:
                seen.add(frag)
                found.append((label, frag))
    m = _MANUAL_EQ.match(text)
    if m and text.strip() not in seen:
        found.append(("formula", text.strip()))
    return found


def validate_markdown(text: str, *, min_sources: int = MIN_SOURCES,
                      assets: Optional[set] = None) -> dict:
    elems, sections = parse_document(text)
    errors: List[dict] = []
    warnings: List[dict] = []
    notes: List[dict] = []
    stats = {"images": 0, "tables": 0, "formulas": 0, "listings": 0,
             "diagrams": 0, "headings": 0, "paragraphs": 0, "bib_entries": 0}

    ids: Dict[str, int] = {}
    refs: List[Tuple[str, int]] = []
    for e in elems:
        if e.get("id"):
            if e["id"] in ids:
                errors.append(_finding("ID_DUPLICATE", "hard-error", e["line"],
                                       f"Duplicate id {e['id']!r} — references are ambiguous.",
                                       "Give each object a unique key."))
            else:
                ids[e["id"]] = e["line"]
        for m in _REF_RE.finditer(e.get("text", "") or ""):
            refs.append((m.group(1), e["line"]))

    for rid, line in refs:
        if rid not in ids:
            warnings.append(_finding("REF_UNRESOLVED", "gost-warning", line,
                                     f"Reference {{ref:{rid}}} has no target.",
                                     "Put the same key on the table, figure, or formula."))

    # MENTION_MISSING + stats + manual numbering + forbidden elements
    seen_refs: set = set()
    cited: set = set()
    bib_keys: Dict[str, int] = {}
    for e in elems:
        kind = e.get("section_kind")
        et = e.el
        text = e.get("text", "") or ""

        if et == "table":
            stats["tables"] += 1
            if not e.get("id"):
                errors.append(_finding("TABLE_ID_MISSING", "hard-error", e["line"],
                                       "Table has no {#id} key.",
                                       "Below the table: «: Название {#tbl_x}»."))
            elif e["id"] not in seen_refs:
                warnings.append(_finding("MENTION_MISSING", "gost-warning", e["line"],
                                         f"No reference {{ref:{e['id']}}} before the table (6.6.2).",
                                         "Refer to the table in the text before it."))
            if not (e.get("caption") and str(e.get("caption")).strip()):
                warnings.append(_finding("TABLE_NAME_MISSING", "gost-warning", e["line"],
                                         "Table without a name (6.6).",
                                         "Add «: Название {#tbl_x}»."))
            if e.get("empty_cell"):
                warnings.append(_finding("TABLE_EMPTY_CELL", "gost-warning", e["line"],
                                         "Empty cell without a dash «–».",
                                         "Put «–» in empty cells."))
            if (e.get("rows") or 0) < 2 or (e.get("cols") or 0) < 2:
                warnings.append(_finding("TABLE_TOO_SMALL", "gost-warning", e["line"],
                                         "Table has fewer than 2 columns or 2 rows.",
                                         "At least two columns and two rows."))
        elif et in ("image", "diagram"):
            stats["images"] += 1
            if et == "diagram":
                stats["diagrams"] += 1
            if et == "image" and not e.get("sheet_of") and not (e.get("caption") or "").strip():
                warnings.append(_finding("CAPTION_MISSING", "gost-warning", e["line"],
                                         "Figure without a caption (6.5.7).",
                                         "![Подпись](assets/file.png){#fig_x}."))
            if et == "diagram" and e.get("empty"):
                warnings.append(_finding("DIAGRAM_INVALID", "gost-warning", e["line"],
                                         "Empty diagram block — nothing to render.",
                                         "Add the diagram code inside ```."))
            if e.get("id") and e["id"] not in seen_refs:
                warnings.append(_finding("MENTION_MISSING", "gost-warning", e["line"],
                                         f"No reference {{ref:{e['id']}}} before the figure (6.5.1).",
                                         "Refer to the figure in the text before it."))
            if et == "image" and assets is not None and e.get("path"):
                name = e["path"].strip().replace("\\", "/").split("/")[-1]
                if name and name not in assets:
                    warnings.append(_finding("IMAGE_MISSING", "gost-warning", e["line"],
                                             f"Image file «{e['path']}» not found next to the document.",
                                             "Add the file under assets/ with that exact name."))
        elif et == "formula":
            stats["formulas"] += 1
            if e.get("id") and e["id"] not in seen_refs:
                warnings.append(_finding("MENTION_MISSING", "gost-warning", e["line"],
                                         f"No reference {{ref:{e['id']}}} before the formula.",
                                         "Refer to the formula in the text before it."))
        elif et == "listing":
            stats["listings"] += 1
            if e.get("empty"):
                warnings.append(_finding("LISTING_EMPTY", "gost-warning", e["line"],
                                         "Listing without code.",
                                         "Add the code inside ```."))
        elif et == "bib":
            stats["bib_entries"] += 1
            bib_keys[e.get("key")] = e["line"]
        elif et == "list" and kind == "bibliography":
            warnings.append(_finding("BIB_FORMAT", "gost-warning", e["line"],
                                     "Source entry has no {#key} at the start.",
                                     "Start the entry with «- {#key} Author …»."))
        elif et == "heading":
            stats["headings"] += 1
        elif et == "para":
            stats["paragraphs"] += 1

        # forbidden elements in reference sections
        if kind in RESTRICTED_SECTIONS:
            token = None
            if et == "table":
                token = "table"
            elif et in ("image", "diagram"):
                token = "image"
            elif et == "formula":
                token = "math"
            elif et in ("code", "listing"):
                token = "code"
            if token and token in RESTRICTED_SECTIONS[kind]:
                warnings.append(_finding("RESTRICTED_IN_SECTION", "gost-warning", e["line"],
                                         f"Element «{token}» is forbidden in this section.",
                                         "Remove the element or change the section type."))

        # manual numbering
        is_heading = et == "heading"
        hits = _manual_in(text, heading=is_heading)
        if hits:
            frags = "», «".join(f for _, f in hits)
            warnings.append(_finding("MANUAL_NUMBERING", "gost-warning", e["line"],
                                     f"Manual numbering: «{frags}».",
                                     "Remove the number — the build adds it; use {ref:id} to refer."))

        # citations
        for cm in _CITE_RE.finditer(text):
            for key in re.split(r"[;,]", cm.group(1)):
                k = key.strip().split()[0] if key.strip() else ""
                k = k.lstrip("@").strip()
                if k:
                    cited.add(k)

        if text:
            for r in _REF_RE.findall(text):
                seen_refs.add(r)

        # section length
        if text:
            sec = sections[_section_index(sections, e["line"])]
            sec["chars"] += len(text)

    # section lengths
    for sec in sections:
        lim = LIMITS.get(sec["kind"])
        if not lim:
            continue
        chars = sec["chars"]
        if lim["max"] and chars > lim["max"]:
            warnings.append(_finding(f"{lim['prefix']}_TOO_LONG", "gost-warning", sec["start_line"],
                                     f"Section is {chars} characters (> {lim['max']}).",
                                     f"Cut about {chars - lim['max']} characters."))
        elif lim["warn"] and chars > lim["warn"]:
            warnings.append(_finding(f"{lim['prefix']}_VERBOSE", "gost-warning", sec["start_line"],
                                     f"Section is {chars} characters (recommended < {lim['warn']}).",
                                     "Tighten the wording."))
        if sec["kind"] == "abstract":
            kw = next((e for e in elems if e.get("section_kind") == "abstract" and e.el == "keywords"), None)
            if kw is None:
                warnings.append(_finding("REQUIRED_MISSING", "gost-warning", sec["start_line"],
                                         "The abstract has no :::keywords block.",
                                         "Add 5–15 keywords in UPPERCASE."))
            else:
                count = len([w for w in re.split(r"[,\n]", kw.get("text", "")) if w.strip()])
                if count < KEYWORDS_MIN or count > KEYWORDS_MAX:
                    warnings.append(_finding("KEYWORDS_COUNT", "gost-warning", kw["line"],
                                             f"{count} keywords (norm {KEYWORDS_MIN}–{KEYWORDS_MAX}).",
                                             "List comma-separated, 5–15 words."))

    # abbreviations in the abstract statistics line
    for e in elems:
        if e.get("section_kind") == "abstract" and e.el == "para" and \
                _COUNTER_ABBREV_RE.search(e.get("text", "") or "") and \
                re.search(r"\{PAGES\}|\{IMAGES_COUNT\}|\{TABLES_COUNT\}", e.get("text", "") or ""):
            warnings.append(_finding("COUNTER_ABBREV", "gost-warning", e["line"],
                                     "The abstract statistics uses abbreviations (с., рис., табл.).",
                                     "Use full words: страниц, рисунков, таблиц."))

    # sources
    if bib_keys:
        for key, line in bib_keys.items():
            if key not in cited:
                warnings.append(_finding("SOURCE_UNMENTIONED", "gost-warning", line,
                                         f"Source {{#{key}}} is not cited in the text (6.16).",
                                         f"Cite [@{key}] in the text or drop the entry."))
        if len(bib_keys) < min_sources:
            b0 = next(s for s in sections if s["kind"] == "bibliography")
            warnings.append(_finding("SOURCES_TOO_FEW", "gost-warning", b0["start_line"],
                                     f"{len(bib_keys)} sources (< {min_sources}).",
                                     "Add sources."))
    for key in cited:
        if key not in bib_keys:
            warnings.append(_finding("CITE_UNRESOLVED", "gost-warning", None,
                                     f"Citation [@{key}] has no entry in the source list.",
                                     f"Add «- {{#{key}}} Author …» to the sources section."))

    # Completeness: a study must have an abstract with keywords and a source list.
    # If the sections are missing entirely, the validator says so — otherwise a short
    # fragment («# Введение») would get a false "ready to build".
    kinds = {s["kind"] for s in sections}
    has_body = bool(kinds & {"chapter", "introduction", "conclusion"})
    if not bib_keys and has_body:
        warnings.append(_finding(
            "SOURCES_TOO_FEW", "gost-warning", None,
            f"0 sources (< {min_sources}).",
            "Add a «Список использованных источников» section and [@key] references."))
    if "abstract" not in kinds and has_body:
        warnings.append(_finding(
            "REQUIRED_MISSING", "gost-warning", None,
            "The paper has no «Реферат» section with keywords.",
            "Add «# Реферат» with a statistics line and :::keywords."))

    # unclosed blocks / not understood
    preamble_reported = False
    for e in elems:
        if e.el == "unclosed":
            warnings.append(_finding("UNCLOSED_BLOCK", "uncertainty", e["line"],
                                     f"Block {e.get('detail', '')} is not closed: the tail fell inside.",
                                     "Close the block with the same line."))
        elif e.el == "unknown_container":
            warnings.append(_finding("UNKNOWN_CONTAINER", "uncertainty", e["line"],
                                     f"Container :::{e.get('detail', '')} is not supported.",
                                     "Use blocks from the dialect."))
        elif e.el == "unparsed":
            warnings.append(_finding("UNPARSED_BLOCK", "uncertainty", e["line"],
                                     f"A line looks like markup but was not parsed ({e.get('detail','')}).",
                                     "Check the markup against the dialect."))
        elif (not preamble_reported and e.get("section_kind") == "preamble"
                and e.el in ("para", "list", "table", "image", "diagram", "formula",
                             "code", "listing", "quote", "bib")):
            preamble_reported = True
            warnings.append(_finding("TEXT_BEFORE_HEADING", "uncertainty", e["line"],
                                     "Text before the first # heading will be dropped.",
                                     "Move the paragraph under a section heading."))

    ok = not errors
    return {"ok": ok, "errors": errors, "warnings": warnings, "notes": notes,
            "stats": stats, "ids": len(ids), "sections": len(sections)}


def _section_index(sections: List[dict], line: int) -> int:
    idx = 0
    for k, s in enumerate(sections):
        if s["start_line"] <= line:
            idx = k
    return idx


# ── CLI ──────────────────────────────────────────────────────────────────────

def _load_source(path: str) -> str:
    if path.endswith(".zip") or zipfile.is_zipfile(path):
        with zipfile.ZipFile(path) as zf:
            md = [n for n in zf.namelist()
                  if n.lower().endswith(".md") and "/" not in n.strip("/")]
            if not md:
                md = [n for n in zf.namelist() if n.lower().endswith(".md")]
            if not md:
                raise SystemExit("no .md file in the archive")
            return zf.read(md[0]).decode("utf-8", "replace")
    with open(path, encoding="utf-8") as fh:
        return fh.read()


def _load_assets(path: str) -> Optional[set]:
    """Basenames of files under assets/ — from a .zip or a sibling folder.

    Returns None when the files are not available (a bare .md without an assets/
    folder): then the image-existence check is skipped, since path-only markup
    without files is a valid intermediate state (see the dialect).
    """
    if path.endswith(".zip") or zipfile.is_zipfile(path):
        with zipfile.ZipFile(path) as zf:
            return {n.replace("\\", "/").split("/")[-1] for n in zf.namelist()
                    if "/" in n and "assets/" in n.replace("\\", "/")}
    folder = os.path.join(os.path.dirname(path) or ".", "assets")
    if os.path.isdir(folder):
        return set(os.listdir(folder))
    return None


def _print_human(path: str, res: dict) -> None:
    def emit(items: List[dict]) -> None:
        for f in items:
            loc = f"line {f['line']}" if f.get("line") else "document"
            print(f"[{f['level']}] {f['code']} @ {loc}: {f['message']}")

    print(f"=== «Оформитель» validator: {path} ===")
    if res["errors"]:
        print("\nErrors (the build will not pass):")
        emit(res["errors"])
    if res["warnings"]:
        print("\nWarnings:")
        emit(res["warnings"])
    if not res["errors"] and not res["warnings"]:
        print("no findings — the document is ready to build")
    s = res["stats"]
    print(f"\nstats: figures {s['images']}, tables {s['tables']}, formulas {s['formulas']}, "
          f"listings {s['listings']}, sources {s['bib_entries']}, headings {s['headings']}")
    print("result:", "no errors" if res["ok"] else f"{len(res['errors'])} error(s)")


def main(argv: Optional[List[str]] = None) -> int:
    ap = argparse.ArgumentParser(description="Validator for the «Оформитель» MD dialect.")
    ap.add_argument("path", help="paper.md or paper.md.zip")
    ap.add_argument("--json", action="store_true", help="print the result as JSON")
    ap.add_argument("--min-sources", type=int, default=MIN_SOURCES,
                    help=f"minimum number of sources (default {MIN_SOURCES})")
    args = ap.parse_args(argv)
    text = _load_source(args.path)
    res = validate_markdown(text, min_sources=args.min_sources,
                            assets=_load_assets(args.path))
    if args.json:
        print(json.dumps(res, ensure_ascii=False, indent=2))
    else:
        _print_human(os.path.basename(args.path), res)
    return 0 if res["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())

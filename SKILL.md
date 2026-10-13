---
name: write-diploma
description: Use when the user wants to write a thesis, coursework, or research report (ВКР/курсовая/НИР) in the Markdown dialect of «Оформитель» (GOST 7.32) — build the structure, write it with practical focus, validate it with the bundled validator, and verify that its sources are real. Also covers the optional safety (БЖД) and economic justification (ТЭО) chapters.
---

# Writing an academic paper in the «Оформитель» dialect

Write a thesis (ВКР), coursework, or research report (НИР) in the Markdown dialect
of the «Оформитель» service (GOST 7.32): structure, content, a pass through the
bundled validator, and source verification before submission.

**Write the paper in Russian** — the dialect, section names, and the final DOCX/PDF
are Russian. The instructions here are in English for token efficiency; the output
is not.

## What is included

- `references/dialect.md` — the **dialect**: tables, figures, diagrams, formulas,
  lists, special blocks, sources, answer format. Output must follow it exactly.
- `references/Humanizer.md` — **MANDATORY to read before writing**: rules for
  natural prose (no AI clichés, varied rhythm, concrete facts). Every paragraph
  must follow them.
- `references/rules.md` — **validator codes** and how to fix them.
- `references/content.md` — **content requirements**: structure per paper type,
  section length, terms, calculations, style.
- `references/safety.md` — optional chapter **«Безопасность и экологичность» (БЖД)**:
  principles, structure, tables, the individual task. Read it only if the paper
  includes this chapter.
- `references/economics.md` — optional chapter **«Экономическое обоснование» (ТЭО)**:
  four calculation types, formulas, rules for numbers. Read it only if the paper
  includes this chapter.
- `references/profiles.md` — recognized sections and formatting profiles.
- `references/fstec.md` — optional: personal-data protection (FSTEC) — use it only
  for ИБ/ПДн topics.
- `scripts/validate.py` — the **standalone validator** (Python 3.8+ standard
  library only). Runs without the service: `python3 scripts/validate.py paper.md`.

## Workflow

1. **Inputs** — ask for what is missing: type (thesis/coursework/research), topic,
   domain + practical context (industry, organization, period, whose problem in
   time/money/risk), tech stack, length (pages), optional chapters (economics /
   safety — for a thesis), title-page data. **Ask whether the department has
   guidelines (методичка)** — required sections, page counts, mandatory tables,
   formulas, the normative coefficient. If the user has them, ask them to paste the
   relevant parts: **department guidelines override the defaults in this skill.**
2. **Plan** — structure by paper type (`references/content.md`) + a source list
   up front, in order of first mention (thesis/research 15–20, coursework 10–15).
3. **Write in stages** (2–6 stages by length). **First read
   `references/Humanizer.md` and write by its rules.** Each optional chapter (БЖД,
   ТЭО) is its own stage: read `references/safety.md` / `references/economics.md`
   before writing it. Each stage is substantive and practical; every claim is a citation or your own conclusion. Markup rules —
   `references/dialect.md`; text requirements — `references/content.md`.
4. **Run the validator.** Save `paper.md` and run the bundled validator:

   ```bash
   python3 scripts/validate.py paper.md          # human-readable
   python3 scripts/validate.py paper.md --json   # machine-readable
   ```

   Parse the output `[level] CODE @ line N: message`: `hard-error` must be fixed
   (exit code 1), `gost-warning` — by judgement, `uncertainty` — figure out the
   markup. Codes and advice — `references/rules.md`. A thesis/research paper
   needs 15 sources; for a **coursework** the minimum is 10, so run
   `--min-sources 10` for it (otherwise it reports `SOURCES_TOO_FEW`).
5. **Verify sources are real** (web search, if available):
   - each academic source — does it exist (DOI, arXiv id, exact title and authors);
   - each GOST/decree/law — current status (for GOST the official registry, for
     decrees the regulator's site, for laws legal-reference systems);
   - replace fabricated ones with real ones (the service re-numbers by first
     mention);
   - if no web search is available — return an explicit list of unverified
     sources marked "verify manually".
6. **Deliver and build.** Default output is `paper.md`. If figures are available,
   deliver `paper.md.zip`: one `.md` at the root, an `assets/` folder with files,
   and `![…](assets/name.png){#fig_…}` in the text (names as in the folder, no
   hashes, no subfolders). The user opens the file in the «Оформитель» service,
   picks the GOST 7.32 profile, and builds DOCX/PDF.

## Critical rules (full list in `references/content.md`)

- **Follow `references/Humanizer.md`.** Natural academic prose: no AI clichés
  ("важно отметить", "играет ключевую роль", "в современном мире"), varied
  sentence rhythm, a concrete fact per claim, no meta-commentary.
- **No manual numbering.** Never number headings, captions, or references by
  hand. Refer to objects with `{ref:id}` in the text BEFORE the object.
- **Abstract** shorter than a retelling of the chapters; statistics line with
  placeholders; 5–15 keywords in UPPERCASE. Introduction and conclusion ≤6000
  characters each.
- **Reference sections** (abstract, introduction, normative references,
  conclusion, sources) — no tables, figures, formulas, or code; terms and
  abbreviations may use a table.
- **Practical focus:** a concrete organization/industry, a real problem, a
  measurable improvement. Not "can be applied in various fields".
- **Finish the calculation** — do not leave "facts to be collected on site".
- **Optional chapters tie to the work.** БЖД: what changes in the working conditions
  after implementation. ТЭО: a priced estimate → effect → numeric coefficient → one
  clear verdict. Numbers add up everywhere; compute them in code, not in your head.
- **Never copy illustrative values** from the references (they are placeholders).
  Real numbers come from the user, a cited source, or a stated assumption.
- **Changing rates** (insurance contributions, tax scale, tariffs, minimum wage) and
  **norms** must be verified by search and cited before use.

## Deliverable

Path to `paper.md` (or `paper.md.zip` with `assets/`, if there are figures) +
validator result (which findings remain and why) + a source report (what was
confirmed, what was replaced, what needs manual verification).

**Two modes, do not mix them.** In this plugin workflow the deliverable is the
file(s) + the validator result + the source report. The strict "output ONLY the
document in one four-backtick block" rule in `references/dialect.md` belongs to the
other mode — when a user pastes the dialect prompt straight into a chat/service and
wants raw document text back. Do not wrap the plugin deliverable in a four-backtick
block.

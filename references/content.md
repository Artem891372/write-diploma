# Content requirements

How to fill the paper in — what to write and in what shape. Workflow and markup
rules live in `SKILL.md` and `references/dialect.md`.

## Practical focus

A concrete organization/industry, a real problem, a measurable improvement over a
baseline (time, money, risk). Not "research for its own sake" and not "can be
applied in various fields".

## Structure by paper type

**Thesis (ВКР):** Abstract → Contents → Introduction → Normative references →
Terms and definitions → List of abbreviations → chapters (analysis → design →
implementation → testing/evaluation) → [optional Economics, Safety and labour
protection] → Conclusion → References → Appendices.

**Coursework:** shorter, without mandatory economics/safety chapters.

**Research report (НИР):** the same reference-section skeleton; chapters follow
the client's plan (analysis, problem statement, methods, precedents), without the
thesis design chapters.

**Appendices:** an opener line `# Приложения`, then each appendix as a normal `#`
heading with its NAME in the text. The service adds the word "Приложение", the
letter, and the `{status=…}` attribute.

## Length and depth

- **Abstract** — shorter and more precise than a retelling of the chapters (soft
  limit 1800 characters, hard 2400). A statistics line with placeholders and full
  words ("страниц", "рисунков", "таблиц", not "с./рис./табл."). Then short
  sentences, one fact each: object, goal, status, a key number, what the set
  includes. No citations, no ";". 5–15 keywords in UPPERCASE.
- **Introduction** ≤6000 characters: context → who/where + why now + what it
  improves → goal → 5–8 tasks → object/subject → novelty → significance →
  structure.
- **Conclusion** ≤6000 characters: 6–9 results, novelty, significance, 2–3
  directions.
- **Depth:** no `###` headings. A `##` subsection is a single substantial block
  (many paragraphs, tables and figures inside). Merge a thin neighbouring `##`
  into its neighbour; the merged heading names all of the content. A `#` chapter
  holds one–three such `##`. No "Conclusions for the section" and no intro
  paragraph right under a chapter heading.

## Reference sections

Abstract, introduction, normative references, conclusion, sources — **no** tables,
figures, formulas, or code. Terms and abbreviations — no figures, formulas, or
code, but a **table is allowed**.

## Terms and abbreviations

One paragraph per entry "Term – definition" (the dash is typed by the author; the
service trims trailing punctuation; no first-line indent) OR a two-column
"term | definition" table (GOST 6.14/6.15). Entries of "Термины и определения",
"Перечень сокращений", and "Нормативные ссылки" get their own subtypes
(`term`/`abbrev`/`normref`) — their look (article numbering, bold up to the dash)
is configured in the style; the author does not mark them up.

## Object, not an organization's data sheet

The organization is a short characterization of the system under study (what is
processed, in which perimeters, who the operator is). Not an institution card:
full legal name, founder, addresses, working hours, director, email, tax IDs,
bank details.

## Finish the calculation — honestly

If the exact number is not in open sources, do not present an invented figure as a
fact. State an explicit assumption, name its basis (class average, published range,
expert estimate), and mark the value as estimated in the text. Then finish the chain
(level, model, measure set) instead of leaving it to an appendix "to be collected on
site".

Domain-specific method: for personal-data protection see `references/fstec.md`. For
other domains use the methodology the department requires.

## Grounds, not the author's device

For each task, write what was done and why it follows from a normative act or from a
fact the act does not contradict. Do not explain how the study is organized, and do
not add self-made scoring scales, selection thresholds, or notes about what was left
out.

## НИР is a stand-alone work

Do not write about transferring into a thesis, the thesis page budget, or "the
thesis practice chapter". The needed pieces are selected for the thesis later; in
the НИР text there is none of that.

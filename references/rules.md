# Validator rules (finding codes)

Codes emitted by `scripts/validate.py` and what to do about them. The codes match
the «Оформитель» service validator, so service and plugin findings read the same.
The validator is a best-effort mirror: if it and the service ever disagree, the
service wins.

Output line format: `[level] CODE @ line N: message`.
Levels: `hard-error` (the build will not pass), `gost-warning` (it will build, but
the issue remains), `uncertainty` (the markup was not understood).

## hard-error — must fix

| Code | Problem | Fix |
|------|---------|-----|
| `TABLE_ID_MISSING` | table has no `{#id}` key | below the table: `: Название {#tbl_x}` (name optional) |
| `ID_DUPLICATE` | one `{#id}` used by two objects | give each a unique key |

## gost-warning — by judgement

| Code | Problem | Fix |
|------|---------|-----|
| `REF_UNRESOLVED` | `{ref:id}` has no target | put the same key on the table/figure/formula |
| `MENTION_MISSING` | object exists but no `{ref:id}` before it in the text | write "… as shown in figure {ref:fig_x}" before the object |
| `MANUAL_NUMBERING` | a hand-typed number: "Рисунок 5", "Таблица 3", "1.2 Section", "п. 2.1", "стр. 12" | remove the number — the build adds it; use `{ref:id}` to refer |
| `TABLE_NAME_MISSING` | table without a name | `: Сравнение показателей {#tbl_x}` |
| `TABLE_EMPTY_CELL` | empty cell | put a dash "–" in empty cells |
| `TABLE_TOO_SMALL` | fewer than 2 columns or 2 rows | at least two columns and two rows |
| `CAPTION_MISSING` | figure without a caption | `![Подпись](assets/file.png){#fig_x}` |
| `DIAGRAM_INVALID` | empty diagram block | add the diagram code inside ` ``` ` |
| `LISTING_EMPTY` | listing without code | add the code |
| `KEYWORDS_COUNT` | not 5–15 keywords | list comma-separated, 5–15 |
| `ABSTRACT_TOO_LONG` / `ABSTRACT_VERBOSE` | abstract > 2400 / > 1800 characters | tighten it |
| `INTRODUCTION_TOO_LONG` / `INTRODUCTION_VERBOSE` | introduction > 6000 / > 5000 | keep goal, tasks, object/subject |
| `CONCLUSION_TOO_LONG` / `CONCLUSION_VERBOSE` | conclusion > 6000 / > 4000 | one result per task |
| `COUNTER_ABBREV` | abstract statistics uses "с./рис./табл." | use full words |
| `RESTRICTED_IN_SECTION` | table/figure/formula/code in a reference section | remove it (a table is allowed in terms/abbreviations) |
| `CITE_UNRESOLVED` | `[@key]` with no entry in the list | add `- {#key} Author …` |
| `SOURCE_UNMENTIONED` | entry exists but no `[@key]` in the text | cite it in the text or drop the entry |
| `BIB_FORMAT` | source entry has no `{#key}` at the start | start the entry with `- {#key} Author …` |
| `SOURCES_TOO_FEW` | fewer than 15 sources (thesis); also fires when there is no sources section at all; for a coursework the minimum is 10 | add entries; run with `--min-sources 10` for a coursework |
| `IMAGE_MISSING` | an image path in the text has no file next to the document (checked for `.zip` / a sibling `assets/`) | add the file under `assets/` with that exact name |
| `REQUIRED_MISSING` | the paper has no "Реферат" section with keywords | add `# Реферат` with a statistics line and `:::keywords` |

## uncertainty — understand the markup

| Code | Problem | Fix |
|------|---------|-----|
| `TEXT_BEFORE_HEADING` | text before the first `#` | move the paragraph under a heading |
| `UNCLOSED_BLOCK` | ` ``` `, `:::`, or `$$` not closed | close the block |
| `UNKNOWN_CONTAINER` | unknown `:::name` | use blocks from the dialect |
| `UNPARSED_BLOCK` | a line looks like markup (e.g. `####`) but was not parsed | check the markup (heading depth up to `###`) |

## Answer format

If findings arrive as lines "CODE · section: description" — fix the document for
each and re-emit the WHOLE document in one four-backtick code block (````).
A three-backtick wrapper would break on the inner code blocks.

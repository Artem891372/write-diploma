# Sections and formatting profiles

## Which `#` headings are recognized as sections

A first-level heading is recognized by its name (case-insensitive, trailing dot
ignored). Any other `#` is a chapter; the service numbers it automatically.

| `#` heading | Section |
|---|---|
| Реферат, Аннотация | abstract |
| Содержание, Оглавление | contents (auto TOC) |
| Введение | introduction |
| Нормативные ссылки | normative references |
| Термины и определения | terms |
| Перечень сокращений и обозначений; Перечень сокращений; Сокращения и обозначения | abbreviations |
| Заключение | conclusion |
| Список использованных источников; Список литературы | references |
| Список исполнителей | performers |
| Приложения | appendix opener (creates no section itself) |

Long names are recognized by their leading part: "Содержание выпускной
квалификационной работы" → contents.

## Profiles (style files)

The profile is chosen in the service at build time; do not put it in the text.

- **gost_7.32** — base working profile, no frame (`frame.kind: none`). The default.
- **gost_2.105** — ESKD: a frame with the title block (GOST 2.104) is enabled.
  Used when the department requires form 2/2a. Title-block cells are filled once
  with the special `::: frame` table (see `references/dialect.md`).

If the department methodology differs from the base preset, the user configures a
custom style in the service builder; this does not affect the Markdown markup.

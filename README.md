# write-diploma — a skill for AI agents

A skill that lets any AI write an academic paper (**thesis / coursework /
research report**) in the Markdown dialect of the
[«Оформитель»](https://оформитель.com) service (GOST 7.32) and validate it before
submission.

## Contents

```
write-diploma/
├── SKILL.md              # agent instructions: workflow and critical rules
├── references/
│   ├── dialect.md        # the MD dialect (tables, figures, formulas, sources…)
│   ├── Humanizer.md      # rules for natural prose (mandatory, anti-AI-clichés)
│   ├── content.md        # content requirements (structure, length, sections)
│   ├── safety.md         # optional chapter: safety and environment (БЖД)
│   ├── economics.md      # optional chapter: economic justification (ТЭО)
│   ├── profiles.md       # recognized sections and formatting profiles
│   ├── fstec.md          # example domain: personal-data protection (FSTEC)
│   └── rules.md          # validator codes and how to fix them
└── scripts/
    └── validate.py       # standalone validator (Python 3.8+ stdlib only)
```

This is an **Agent Skill**, not a Claude Code plugin: installing it means placing
the `write-diploma/` folder where the agent looks for skills. There is no plugin
manifest — a skill needs only `SKILL.md` (plus the references and the script).

In the distributed archive everything sits inside a `write-diploma/` folder (the
name = `name` in the frontmatter). Tests (`tests/`) are not shipped — they exist
only in the repository.

## Usage

1. The agent reads `SKILL.md`, then `references/Humanizer.md` (mandatory before
   writing), and writes the paper in the dialect (`references/dialect.md`; content
   requirements — `references/content.md`).
2. It validates the paper:

   ```bash
   python3 scripts/validate.py paper.md
   python3 scripts/validate.py paper.md --json
   python3 scripts/validate.py paper.md.zip     # if there is an assets/ folder
   ```

   Exit code `0` — no hard errors; `1` — there is a `hard-error` (the build will
   not pass).
3. It fixes the document per the findings (`CODE @ line N: message`) and re-emits
   it whole.
4. It returns `paper.md` (or `paper.md.zip` with `assets/`); the user opens the
   file in «Оформитель», picks the GOST 7.32 profile, and builds DOCX/PDF.

## Installing into different agents

An Agent Skill is just a folder with `SKILL.md`. Where to put it:

- **Claude Code / claude.ai** — `~/.claude/skills/write-diploma/` (personal) or
  `.claude/skills/write-diploma/` (project). *(To ship it as a Claude Code
  **plugin** instead, a plugin needs `.claude-plugin/plugin.json` and the skill
  under `skills/<name>/SKILL.md` — a different layout; this folder is a plain
  skill.)*
- **opencode / Codex-style agents** — `~/.agents/skills/write-diploma/` or the
  project's `.agents/skills/`.
- **Any other agent** — point it at the folder: instructions in `SKILL.md`, the
  reference in `references/`, the script in `scripts/`. Python 3.8+ is enough, no
  external dependencies, no access to the service required.

## Dependencies

The Python standard library only. No PyYAML, no rendering engine.

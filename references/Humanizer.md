# Humanizer — rules for natural academic prose

**Read this before writing. Write every paragraph by these rules.** The text must
read as if a person wrote it, not an LLM. The service fixes numbering, captions,
and typography; it does not fix robotic wording — that is your job. The examples
are in Russian because that is the language of the paper.

## 1. Banned phrases (AI tells) — never use

Empty openers and boosters:

- «важно отметить», «стоит отметить», «необходимо подчеркнуть», «следует отметить»,
  «стоит подчеркнуть»;
- «в современном мире», «в условиях цифровизации», «в эпоху стремительного
  развития технологий», «на сегодняшний день»;
- «играет важную/ключевую роль», «является неотъемлемой частью»,
  «занимает важное место»;
- «широко используется в различных областях», «находит применение в самых разных
  сферах», «может применяться в различных областях»;
- «комплексный подход», «динамично развивающийся», «неотъемлемый элемент».

Filler words: «данный» (use «этот»), «достаточно», «весьма», «в значительной
степени», «по сути», «фактически» (unless literally true), «целый ряд»,
«определённый» as a crutch.

Meta-commentary: «в данной главе будет рассмотрено», «как известно»,
«нетрудно заметить», «очевидно, что», «в заключение хотелось бы отметить»,
«стоит сказать, что».

Chains of bureaucratic verbs: «осуществляется», «производится», «проводится»,
«реализуется» — one of them is fine, a chain of them is a tell.

Cheap rhythm tricks: triads («быстро, качественно и надёжно»), «не только … но и»
repeated in every paragraph, «более того» / «кроме того» as filler connectors.

## 2. Rhythm

- Vary sentence length. Mix short sentences with longer ones.
- Do not start several sentences in a row the same way (e.g. «Система …
  Система … Система …»).
- Break long chains of verbal nouns with a plain verb clause.

## 3. Specificity over generality

Every claim carries a concrete fact: a number, a name, a date, a condition, a unit,
a limit. Replace «высокая нагрузка» with «до 400 запросов в секунду», «крупная
организация» with «оператор связи с 1,2 млн абонентов». If there is no exact
figure, give the estimated one — do not pad with adjectives.

## 4. Nominalizations and genitives

Avoid long genitive chains: «повышение эффективности процесса обработки данных
информационной системы» → «обработка данных ускоряется». Prefer a verb to a
verbal noun when it reads naturally.

## 5. Hedging and boosters

Drop stacks like «как правило, обычно, чаще всего, в большинстве случаев». One
hedge per claim at most. No «очевидно», «безусловно», «несомненно».

## 6. Connectors

Use «однако», «при этом», «поэтому», «также» sparingly and only when the logic
needs them. Do not begin every paragraph with a connector.

## 7. Keep untouched

Do not change: names, numbers, citations `[@key]`, references `{ref:id}`,
section headings, table/figure/diagram/formula markup, keywords. Keep the academic
impersonal voice («был разработан», «проведён анализ») — just not robotic.

## 8. Before / after

Before (AI-ish):

> Важно отметить, что в современном мире информационные системы играют ключевую
> роль в обеспечении эффективной деятельности организаций. Данный факт
> обуславливает необходимость комплексного подхода к обеспечению безопасности.

After (human):

> В отделах, где обрабатывают персональные данные клиентов, система учёта прямо
> влияет на риск утечки. Поэтому безопасность таких систем проверяют отдельно, а
> не «в общем порядке».

The "after" keeps the impersonal academic tone but removes the empty opener, the
banned clichés, and the vague wording, and adds a concrete condition.

## 9. Checklist before finishing

- [ ] no phrase from the banned list;
- [ ] sentence lengths vary, openers do not repeat;
- [ ] every paragraph has at least one concrete fact;
- [ ] no chain of «осуществляется/производится/проводится»;
- [ ] no meta-commentary about the paper itself;
- [ ] reads aloud like a person wrote it.

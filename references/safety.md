# Safety chapter (БЖД) — «Безопасность и экологичность»

Optional chapter of a thesis. Applies to any field (IT, engineering, medicine,
education, services, research), not only to office work. Markup rules are in
`references/dialect.md`, prose rules in `references/Humanizer.md`, depth/length
rules in `references/content.md`. **All illustrative values below are placeholders
in square brackets — never copy them into the paper; take real data from the
user's organization, a measurement, a calculation, or a cited norm.**

## 0. Include it? Whose rules win

- Ask the user whether the chapter is needed (for most Russian technical
  specialties it is part of the required thesis structure).
- **The department's guidelines (методичка) win over everything here.** If the user
  has them, ask for the relevant parts: required subsections and their order, page
  count, mandatory tables, the list of allowed individual tasks, expected wording
  of headings. The defaults below apply only where the guidelines are silent.
- Placement: a normal `#` chapter after testing/evaluation (and after economics, if
  both are included), before «Заключение». The title is by default
  «Безопасность и экологичность»; use the department's wording if it differs
  («Безопасность жизнедеятельности», «Охрана труда и экологичность»).

## 1. The one principle

The chapter is about **this work**, not about safety in general. Analyze what
changes in the working conditions of the people who will use, operate or maintain
the result of the work — **before vs after implementation**. For an experimental
paper (НИР) analyze the conditions of the experiment (laboratory, test rig, field)
and, if the work is computational, the researcher's own workplace.

Forbidden (guidelines usually forbid it explicitly):

- generic reasoning about the importance of safety, not tied to the object;
- retelling norms and statutes — cite the article/clause and move on;
- instruction style («работник должен…», «перед началом работы убедиться…») —
  write descriptively: what is provided, what the norm is, what the actual value is;
- an organization data sheet (legal name, founder, address, tax IDs).

## 2. What "the workplace" is, by kind of work

Pick the case that fits the thesis and analyze **only the factors that exist there**.

| Kind of work | Typical factors to analyze |
|---|---|
| Office, computer, software, analytics, design | microclimate, lighting, noise, display/EMF, visual and mental strain, posture, electrical, fire |
| Equipment, production, repair, installation | moving parts and guards, noise/vibration, electrical, heat/cold, dust and chemical agents, lifting loads, fire |
| Laboratory, experiment | reagents and waste, instruments and radiation, glassware, electrical, ventilation |
| Construction, field, energy, transport, agriculture | work at height, weather and microclimate, machinery, traffic, electrical, fire |
| Healthcare, education, services, retail | biological and psychological load, ergonomics, violence by third parties, fire, evacuation |
| Remote or home workplace | ergonomics, lighting, strain; the employer's duties still apply |

## 3. Structure (default: three substantial `##`)

`references/content.md` allows one to three `##` per chapter, each a full block, and
no intro paragraph under the chapter heading and no «Выводы по разделу». So by
default write:

1. `## Условия труда и защита от вредных факторов` — the opening context (why
   safety matters for this activity, the employer's duties under the Labour Code,
   sector or enterprise statistics with numbers), the workplace characteristic
   (staff, shifts, number and layout of workplaces), the factor table, the
   description of the factors that exist, the individual task, and what changes
   after implementation.
2. `## Электробезопасность и пожарная безопасность` — room class by electric
   shock hazard, protection measures, fire/explosion category of the room, zone
   class, detection and extinguishing, evacuation.
3. `## Чрезвычайные ситуации и охрана окружающей среды` — probable emergencies for
   the region and the object (natural, man-made, social), protection measures; then
   emissions, wastewater, waste by hazard class, disposal of obsolete equipment.

If the department requires separate numbered subsections (often seven: значение и
задачи; условия труда; электробезопасность; пожарная безопасность; ЧС; охрана
окружающей среды; выводы) and a page count — follow it and split accordingly.
Typical sizes in such guidelines: whole chapter 6–10 pages, conditions of labour
2–3 pages, the rest 1 page or less each.

## 4. Mandatory tables

Three summary tables are standard. Put each in the main text, refer to it before it
(`{ref:…}`), and add 4–6 sentences after it: which values exceed the limit, which
measures apply, what changes after implementation. Categories and classes are
**alphanumeric designations**, not adjectives («В4», «П-IIа», «помещение без
повышенной опасности», not «низкий»).

```
Сводные данные об условиях труда на рабочем месте приведены в таблице {ref:tbl_conditions}.

| Вредный производственный фактор | Характер воздействия на здоровье и работоспособность | Предельно допустимый уровень | Фактическое значение |
|---|---|---|---|
| [фактор, единица] | [чем вреден] | [норма с источником [@key]] | [замер, расчёт или данные организации] |

: Условия труда на рабочем месте {#tbl_conditions}
```

- **Conditions of labour:** columns exactly as above (or as the guidelines word
  them); at least five factors that really exist, each with a number and a norm.
- **Electric hazard class of the room:** columns «Помещение», «Факторы, определяющие
  опасность поражения током» (floor, humidity, temperature, dust), «Класс помещения»
  (per ПУЭ).
- **Fire category:** columns «Помещение», «Категория по взрывопожарной и пожарной
  опасности», «Класс зоны».

Also describe, in prose, only what applies: microclimate (norms for the work
category), harmful substances (class, MPC, protection), lighting (normed
illuminance, glare, flicker, natural/artificial/emergency), noise and vibration,
electromagnetic and other radiation, psychophysiological strain, ergonomics of the
workplace. For electric safety add the network (voltage, earthing system, cable),
the protection measures against indirect contact and static electricity; for fire
safety — combustible materials present, detectors, primary extinguishing means,
at least eight concrete measures; for emergencies — probability reasoning from
the local conditions, nearby hazardous objects, and proposals for protection,
resilience and rescue works; for ecology — the scheme «источник → процесс →
выделяющиеся вещества или отходы» for air, water and soil, ФККО hazard class of the
waste, and the disposal order for obsolete equipment (not just «по договору с
лицензированной организацией»).

## 5. Individual task (calculation or assessment)

One task, matched to the kind of work, written as a paragraph block inside the
conditions subsection (no `###`). Typical choices:

| Thesis result | Suitable task |
|---|---|
| Software, analytics, AI | assessment of the intensity (напряжённость) of the work process |
| Radio, video, access-control, wireless equipment | safe distance from an EMF source, or EMF exposure level |
| Server room, electrical equipment | protective earthing/bonding, microclimate justification, evacuation time |
| Noisy or ultrasonic equipment | noise-protection effectiveness (insulation, screens) |
| Workplace redesign, ergonomics | severity of the work process, rational layout sketch |
| Any (fallback) | hazard identification and occupational risk assessment |

Use the method the department or a current official method prescribes (for risk
assessment — the Ministry of Labour recommendations on choosing methods of
occupational risk assessment; for strain/severity — Р 2.2.2006-05). **Do not
invent a scoring scale or thresholds**; name the method and use its scale.

A calculation always has six steps, in this order:

1. the statement (what is calculated and why this one);
2. the source data (a list or a table, with units);
3. the formula, referred to before it;
4. the symbol key (`::: where`);
5. the numeric result with the data substituted;
6. the conclusion: compare with the limit and say «соответствует требованиям …» or
   name the measure that is needed.

```
Расчёт выполняется по формуле {ref:eq_task}.

$$ [левая часть] = [выражение] $$ {#eq_task}

::: where
- $[символ]$ — [смысл], [единица];
- $[символ]$ — [смысл], [единица].
:::
```

For an assessment table (strain, severity, risk) show the class or score **before
and after** implementation, and end with a verdict: the final class, and how
implementation changes it.

## 6. Normative anchors (verify every one before citing)

Cite only documents whose **current** status you confirmed (official registry,
regulator site, legal-reference system). Drop what you cannot confirm. Typical
anchors: Labour Code (Трудовой кодекс РФ); the federal laws on special assessment
of working conditions, on sanitary-epidemiological welfare, on fire safety
requirements (123-ФЗ), on protection from emergencies (68-ФЗ), on environmental
protection (7-ФЗ), on production and consumption waste (89-ФЗ); СанПиН 1.2.3685-21
(hygienic norms; it replaced the old PC-workplace rules such as СанПиН
2.2.2/2.4.1340-03, which must not be cited); СП 2.2.3670-20; Р 2.2.2006-05;
СП 52.13330.2016 (lighting); ПУЭ; the Ministry of Labour rules on electrical
installations (приказ 903н); СП 12.13130.2009 (fire category of premises); the
fire safety regime rules of the Government; the federal classification catalogue
of waste (ФККО); GOST 12.0.003 (hazard classification) and the ergonomic GOSTs for
the workplace. Aim for 15–20 normative items in the shared source list when the
chapter is included.

## 7. Bad → good

| Bad | Good |
|---|---|
| «Безопасность жизнедеятельности играет важную роль на производстве» | a number from the sector or the enterprise with its source, tied to this work |
| a retyped article of the Labour Code or a sanitary rule | «Согласно ст. [N] ТК РФ работодатель обязан …» and move on |
| «Работник должен соблюдать …» | «Для оператора предусмотрены инструктажи и перерывы по [норма]» |
| a factor table without limits and actual values | every factor with a number and a cited norm |
| a task without formula, number or verdict | the six steps, ending in a comparison with the limit |
| fire hazard as «высокий/низкий» | designation of the category and zone class |
| a repealed norm | the current one, status confirmed |
| «утилизация по договору» | waste hazard class, who decides on write-off, the disposal route per component |

## 8. Checklist

- the chapter is about this work and shows before/after;
- department guidelines were requested and followed where they exist;
- three tables present, references to them precede them, designations alphanumeric;
- an individual task with formula or assessment, numbers, and a verdict;
- every number has a source, a measurement, or an explicit assumption marked as such;
- all norms are current and verified; no invented scales;
- Humanizer rules followed; no instruction style; no org data sheet;
- the validator is clean (`scripts/validate.py`).

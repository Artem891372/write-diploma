# Economic justification chapter (ТЭО) — «Экономическое обоснование»

Optional chapter of a thesis. Applies to any field: a purchased solution, a
developed product or method, a process improvement, a launched service. Markup
rules are in `references/dialect.md`, prose rules in `references/Humanizer.md`,
depth/length in `references/content.md`. **Every figure in the examples below is a
placeholder in square brackets — never copy it; take real values from price lists,
statistics, the user's organization, or an explicit stated assumption.**

## 0. Include it? Whose rules win

- Ask whether the chapter is needed and whether the department gives a method.
  **The department's method wins over the defaults here** (formulas, the
  normative coefficient, page count, required tables, heading wording).
- Placement: a `#` chapter after testing/evaluation, before «Заключение» (and before
  the safety chapter if both are included, unless the department orders otherwise).
  Title by default «Экономическое обоснование предложенных решений».

## 1. The one principle

A **simple deterministic chain**: a real cost estimate → operating costs → the
effect → a numeric efficiency coefficient → payback → **one unambiguous
conclusion**. Money effect means what the organization gains: a **prevented loss**
(risk, incident, accident, defect), a **saving** (time, materials, energy, labour),
or **extra revenue**. Say which one it is and why it is credible.

Do **not** build the calculation on ROI, NPV, discounting or sensitivity analysis
by default — a department's student method is usually the simple chain. Add NPV or
discounting only as a short supplement and only if the department asks or the work
is a commercial project with a multi-year cash flow.

## 2. Pick the type of calculation

By what the work delivers (if mixed, take the dominant result):

| Type | The work delivers | Core of the calculation |
|---|---|---|
| A. Introduction of a solution | purchase and installation of equipment, software, protection, a set of measures | estimate → installation → operating costs → payback via prevented loss or saving → efficiency coefficient |
| B. Development | own product, prototype, tool, method | machine time → labour by stages → cost → capital costs → annual saving → effect, coefficient, payback |
| C. Productivity | a tool or method that speeds up staff work, no big purchases | staff costs → productivity gain → saving |
| D. Service or unit | a launched service, centre, line with a team and subscriptions | CAPEX → OPEX → total cost of ownership → effect per rouble → payback |

## 3. Structure (default: three substantial `##`)

By `references/content.md` a chapter has one to three full `##`, no intro paragraph
under the chapter heading, and no «Выводы по главе». Default:

1. `## Затраты` — the cost estimate (table) and operating or labour costs, with
   the opening sentence about the economic idea of the evaluation: effect versus
   cost, the probabilistic nature of risks.
2. `## Эффект` — the source of the effect and its calculation (prevented loss,
   saving, productivity gain, revenue).
3. `## Эффективность и окупаемость` — the efficiency coefficient and the payback;
   **the last paragraph is the verdict** («решение экономически эффективно,
   окупается за [N] мес.»). No separate conclusions subsection.

If the department wants four or five numbered subsections, split accordingly.
Every subsection holds a formula, a table and a number.

## 4. Formulas by type

Write each as `$$ … $$ {#eq_…}`, refer to it **before** it, and explain symbols with
`::: where`. Names below are in LaTeX-like shorthand; keep the author's own
notation consistent through the chapter.

**A — introduction**

- estimate: `Z_m = Σ K_i · C_i` (quantity × unit price over all items);
- installation, only for physical equipment: `S_mr = S · k`, where `k` comes from a
  supplier quote or a stated basis, not from thin air; for software installed by
  the staff itself it is zero;
- yearly operating costs: `R_e = R_zp + R_otch + R_am + R_el + R_rm + R_pr`
  (salary of the service staff, insurance contributions, depreciation, electricity,
  repairs, other);
  - contributions `R_otch = R_zp · k_otch` (the current tariff, verified);
  - depreciation `R_am = C · a / 100` (the rate from the useful life);
  - electricity `R_el = N · T · C_en` (power × hours × tariff);
- payback via prevented loss — choose one way:
  - (a) yearly expected loss `U = P · D / t` (probability, damage, life of the
    solution), payback `T_o = NV / U` (initial investment ÷ yearly effect);
  - (b) coefficient `E_f = U_pr / (Z + U_ost)` (prevented loss ÷ costs plus the
    residual loss).

**B — development**

- machine time: `M = t · C_p`, `C_p = C_kWh · P / 1000`;
- labour by stages (analysis, design, implementation, testing, introduction) in
  days, the total `T_ozh`;
- hourly rate `C_h = O / F` (salary ÷ monthly working-time fund), main wage
  `ZP = C_h · T_ozh · T_d`;
- depreciation of the equipment used `A = C_per · N_a · K_m / 1200`;
- full cost `C` = materials + main wage + contributions + overheads (a table);
- capital costs `K_k = C + Z_vn` (**do not add the wage and overheads a second
  time** — they are already inside `C`; `Z_vn` is the introduction cost);
- yearly saving `E_r = (R_1 - R_2) + ΔR_p` (operating costs before and after, plus
  the productivity saving);
- effect `E = E_r - E_n · K_k` and coefficient `E_rasch = E_r / K_k`, efficient if
  `E_rasch ≥ E_n`; **`E_n` is the normative coefficient — take the value the
  department prescribes** (student guidelines commonly use 0,33; if none is given,
  state the value and why);
- payback `T = 1 / E_rasch` years.

**C — productivity**

- staff costs `Z = n · z · (1 + A_s/100) · (1 + A_p/100)` (headcount, salary,
  contributions, bonuses);
- gain per kind of work `P_i = ΔT_i / (F_i - ΔT_i) · 100` (saved time and time
  before), given in a table by work kind;
- saving `ΔP = Z_p · Σ d_i · P_i / 100`, where `d_i` is the share of working time on
  the i-th kind (if the department's method has no shares, follow the method);
- conclusion about labour and response time.

**D — service or unit**

- CAPEX — a table: equipment and licences, start-up work (introduction, tuning,
  regulations);
- workload `T = t_i · N_i` and staff `C = T / (250 · K_pz)` (250 working days,
  `K_pz` the productive-load coefficient, usually about 0,7; add shifts for round-
  the-clock service);
- cost of an employee — a table (salary, contributions, training, workplace,
  bonuses, insurance);
- OPEX — a table of yearly costs (licences, support, staff, overheads);
- total cost of ownership `TCO = CAPEX + OPEX · n` (n — planning horizon, years);
- yearly cost `Z_g = CAPEX / n + OPEX` and effect per rouble `E = R_sum / Z_g`,
  where `R_sum` is the yearly effect (prevented loss, saving or revenue);
- simple payback `T_ok = CAPEX / (R_sum - OPEX)` years, defined when `R_sum > OPEX`.

## 5. Where the numbers come from

- **Prices:** real products with names, dated price lists or offers, in roubles,
  cited with `[@key]`. No round invented totals.
- **Salaries:** a regional statistics source, a published salary survey, or the
  employer's data for the profession and region; cite it.
- **Rates that change** — insurance contributions, income tax scale, depreciation
  groups and useful lives, electricity tariffs, the minimum wage — **verify the
  current values by search before using them** and cite the source. Never write
  them from memory; the tax scale in particular has changed in recent years.
- **Effect:** justify the damage or saving from the sector or the organization's
  own data. A probability or a share that is an expert estimate is **stated as an
  assumption with its basis**, not as a measured fact.
- **Consistency — compute in code, then paste.** Totals equal the sum of rows;
  payback equals costs ÷ effect; the same number in the table, the formula
  substitution, the text and the verdict; one currency and one unit of time; round
  only at the end. A mismatch between table, text and verdict is a defect.

## 6. Markup example

```
Стоимость оборудования определяется по формуле {ref:eq_estimate}.

$$ З_м = \sum_{i=1}^{m} K_i \cdot Ц_i $$ {#eq_estimate}

::: where
- $K_i$ — количество единиц i-го наименования;
- $Ц_i$ — цена единицы, руб.;
- $m$ — число наименований.
:::

Смета затрат приведена в таблице {ref:tbl_estimate}.

| Наименование | Количество | Цена, руб. | Сумма, руб. |
|---|---|---|---|
| [изделие, модель] | [N] | [цена по прайс-листу [@key]] | [N × цена] |
| Итого | – | – | [сумма строк] |

: Смета затрат на приобретение и установку {#tbl_estimate}
```

Empty cells carry a dash «–»; decimals use a comma.

## 7. Bad → good

| Bad | Good |
|---|---|
| round totals with no basis | a priced item list with sources |
| wage and overheads counted twice in the capital costs | a full cost counted once |
| an effect with no stated source | prevented loss, saving or revenue named, with its basis |
| a probability from nowhere | an assumption stated and explained |
| a verdict like «в целом выгодно» | «окупается за [N] мес.; коэффициент [E] выше нормативного [E_n]» |
| an old tax or contribution rate | the current rate, verified and cited |
| NPV and a sensitivity analysis as the foundation | the simple chain; NPV only as an agreed supplement |

## 8. Checklist

- the type of calculation matches what the work delivers;
- all formulas of that type are present, referred to before, symbols explained;
- the estimate has real items and cited prices; the numbers add up everywhere;
- the efficiency coefficient and the payback are numeric;
- the last paragraph gives an unambiguous verdict;
- changing rates are verified and cited; assumptions are marked as such;
- Humanizer rules followed; the validator is clean.

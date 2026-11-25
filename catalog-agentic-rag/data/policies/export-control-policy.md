# Export Control Policy

**Applies to:** CircuitNova and Hearthwell
**Owner:** Group Trade Compliance
**Version:** 3.0, effective 2026-01-01

## 1. Purpose

Some products contain technology (for example encryption or high-performance electronics) that
governments control. This policy says where such items may be sold.

## 2. What counts as controlled

2.1 Every product has an **export class** in the `export_class` column of `products`. The class is the
same on all rows of a product, including its options.

2.2 The classes are:

| Class | Meaning | Where it may be sold |
|---|---|---|
| `EC-0` | Not controlled | Anywhere |
| `EC-1` | Controlled (mass-market technology) | Anywhere **except** the embargoed countries in section 3 |
| `EC-2` | Controlled (strong encryption) | Inside the EU; anywhere else needs an export licence (section 4). Never in embargoed countries |

2.3 `EC-1` and `EC-2` items are **controlled**. `EC-0` items are not.

## 3. Embargoed countries

3.1 Controlled items **must never be quotable** in these embargoed countries:

| Code | Country |
|---|---|
| CU | Cuba |
| IR | Iran |
| KP | North Korea |
| SY | Syria |
| RU | Russia |
| BY | Belarus |

3.2 If a controlled product is quotable in any embargoed country (in `products` or in
`where_we_sell`), that is a **compliance violation** and must be removed immediately.

## 4. Items that need a licence

4.1 `EC-2` items need an **export licence** for any country **outside the European Union**.

4.2 EU countries: AT, BE, BG, HR, CY, CZ, DK, EE, FI, FR, DE, GR, HU, IE, IT, LV, LT, LU, MT, NL, PL,
PT, RO, SK, SI, ES, SE.

4.3 Sales must check that a licence exists before quoting an `EC-2` item outside the EU.

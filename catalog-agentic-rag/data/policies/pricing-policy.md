# Pricing Policy

**Applies to:** CircuitNova and Hearthwell
**Owner:** Group Pricing Team
**Version:** 3.2, effective 2026-01-01

## 1. Purpose

This policy sets the rules every price in the `price_list` must follow before sales may use it in a
quote. A price that breaks any rule below is **not quotable** until it is fixed.

## 2. Every priced option needs a price

2.1 If `where_we_sell` marks an option with `has_price = Yes`, the `price_list` must contain at
least one row for that option.

2.2 An option marked `has_price = Yes` with no row in the `price_list` is a **pricing gap** and must be
reported to the Pricing Team.

## 3. Missing prices

3.1 A price row with status `Cost and list price missing` is not quotable.

3.2 **Exception for new products:** if the row has `is_npi = Yes` (new product introduction), a missing
price is allowed while the product launches. It doesn't count as a violation, but it should be
listed separately as "NPI, price pending".

3.3 For all other rows (`is_npi = No`), a missing price is a violation.

## 4. Refreshing list prices

4.1 A row with status `List price not refreshed` means the cost price was updated after the list
price. Such a row **must not be quoted** until the Pricing Team refreshes the list price.

## 5. Minimum margin

5.1 The `list_price` must be **at least 1.2 times** the `cost_price` (a minimum margin of 20%).

5.2 Rows where the list price is equal to the cost price and above 0 (zero margin) are treated as a
serious violation and must be escalated to the business unit's pricing manager.

5.3 **Free items:** a row where both the cost price and the list price are 0 is an item included free
of charge. Free items are allowed and are **not** margin violations.

5.4 Rows with a missing cost or list price are covered by section 3, not by this section.

## 6. Currency

6.1 Every row with status `Available` must have a `currency`. An available price without a currency
can't be quoted, because the customer would not know what they are paying.

## 7. Reporting

Pricing violations are reported per **business unit** and per **region**, with the number of affected
rows and option IDs.

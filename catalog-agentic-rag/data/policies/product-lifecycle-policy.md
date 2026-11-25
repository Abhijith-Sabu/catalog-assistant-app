# Product Lifecycle Policy

**Applies to:** CircuitNova and Hearthwell
**Owner:** Group Product Management
**Version:** 2.1, effective 2025-10-01

## 1. Purpose

Products and parts have a life: they are introduced, sold, and eventually retired. This policy says
what may still be sold at each stage.

## 2. Validity

2.1 The `product_validity` sheet holds each item's `valid_from` and `valid_to` dates.

2.2 An item is **expired** when its `valid_to` date is before today.

2.3 A `valid_to` far in the future (such as `9999-12-31`) means the item has no planned end date.

## 3. Expired items must not be sold

3.1 An expired item **must not appear** in `where_we_sell`. If it does, that is a **lifecycle
violation**: sales could still quote a product the company no longer supports.

3.2 Lifecycle violations are reported per product, with the expiry date.

## 4. Obsolete third-party parts

4.1 A third-party part with `catalog_status = Obsolete` is no longer supplied.

4.2 Any product that uses an obsolete part (through `linked_product_id`) must be **reviewed** before it
is sold again. If such a product is still in `where_we_sell`, it must be flagged
"at risk: obsolete part".

## 5. Parts not found in the catalog

5.1 A third-party part with `catalog_status = Not found in catalog` points to a product that doesn't
exist in `products`.

5.2 These parts must be reported to Purchasing so the link can be corrected or the part removed.

## 6. New product introductions (NPI)

6.1 NPI items (`is_npi = Yes` in `price_list`) are newly launched. See the Pricing Policy, section 3.2,
for how missing prices on NPI items are handled.

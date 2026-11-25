# Data Ownership Policy

**Applies to:** CircuitNova and Hearthwell
**Owner:** Group Master Data Office
**Version:** 1.0, effective 2025-01-01

## 1. Purpose

The same product appears in several lists kept by different teams. When the lists disagree, this
policy decides **which list is right** (the "source of truth").

## 2. Source of truth per topic

| Topic | Source of truth | Kept by |
|---|---|---|
| Which products and options exist, product names | `products` | Product team |
| Business unit | `products` | Product team |
| Export class, country of origin | `products` | Product team |
| Where and from when sales may offer it, service | `where_we_sell` | Sales team |
| Owner company, validity dates | `product_validity` | Admin / ERP team |
| Cost price, list price | `price_list` | Pricing team |
| Third-party parts and their status | `third_party_parts` | Purchasing team |

## 3. Every product must be in every system

3.1 Every product in `products` must also appear in `where_we_sell` **and** in `product_validity`.

3.2 A product missing from either list is a **master data gap** and must be created in the missing
system.

## 4. Conflicting values

4.1 If two lists disagree on a topic, the value in the **source of truth** wins, and the other list
must be corrected.

4.2 Example: if `product_validity` shows a different `business_unit` than `products`, the `products`
value is correct and `product_validity` must be updated.

## 5. Reporting data problems

5.1 Every data problem report must name the **product or option IDs** affected, the **lists involved**,
and **which value is correct** according to section 2.

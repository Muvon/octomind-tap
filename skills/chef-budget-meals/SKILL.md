---
name: chef-budget-meals
title: "Budget Meal Planner – Weekly Meals & Priced Grocery List"
description: "Weekly budget meal planner: sale and seasonal price research, grocery list by whole packs, leftovers ledger. Use for a meal plan on a food budget."
license: Apache-2.0
compatibility: "Requires: web search and web page fetching."
capabilities: webfetch
domains: chef
rules:
  - content(budget)
  - content(cheap)
  - content(affordable)
  - content(frugal)
  - match((?i)\b(cost per serving|grocery bill|save money on (food|groceries))\b)
  - match((?i)([$€£]\s?\d+|\d+\s?(dollars|euros|pounds|usd|eur|gbp)).{0,40}\b(week|weekly|month)\b)
---

## Overview

Turns a stated grocery budget and household into a week of affordable meals, a shopping list priced the way the checkout will charge it, and leftovers that are eaten safely. It applies when the user gives a food budget or asks for cheap, affordable or frugal meals. The result is a plan whose total is verified against the cap, or a plainly labelled unpriced draft.

## Mental model

Optimize the checkout bill, not a fantasy cost built from spoonfuls of ingredients nobody owns. Saving money is practical, not a moral test: be encouraging, explain the tradeoff (fewer store trips, less waste, a cheaper ingredient doing the same job), and respect familiar foods, limited equipment and the time the person really has. The session's food-safety and allergy rules apply unchanged; savings never override them.

## Rules

### Intake

- Establish budget, currency, location, shopping week, household portions, meals covered, allergies, preferences, pantry quantities, stores, transport, equipment, and cooking and storage capacity.
- Ask which meals the budget covers. Seven dinners are not a whole week's food budget.
- Scale child portions from the user's guidance, not assumed calorie targets.

### Price research

- Use web search for current local retailer prices, promotion dates, pack sizes and regional seasonality. Read pages with `knowledge(command="read", source="<url>")`. Cite links and the date checked.
- Prefer retailer listings or dated flyers for the correct location. Record currency, pack size, unit price, availability, sale expiry, and membership or multibuy conditions.
- Compare seasonal produce with frozen and canned on usable yield. In season or on sale does not automatically mean cheaper.
- Never invent prices, specs, laws or references. Separate sourced facts, user-provided figures, assumptions and unknowns.
- No live price available: ask for a current flyer, receipt or the user's prices. Otherwise deliver an explicitly unpriced draft, not made-up numbers or a guaranteed saving.

### Building and pricing the week

- Choose overlapping ingredients. Schedule perishables first and freeze later portions promptly.
- Subtract confirmed pantry stock only. Unconfirmed pantry staples are not free.
- Charge the full pack at checkout even when only part is used, so round purchases up to whole packs. Consumed-ingredient cost may be shown separately.
- Include known taxes, deposits, delivery charges and required extras. Flag unknown charges.
- Total the actual basket and reserve a stated contingency inside the budget.
- Over the cap: swap ingredients or simplify dishes before cutting required servings. If the budget is infeasible, say so and name the constraint to relax.
- Don't claim the total fits while unresolved costs could exceed the cap. Don't claim verified affordability without a fully priced basket and disclosed conditions.
- Before delivering, reconcile servings, ingredient quantities, pack costs, leftover portions, storage windows and budget headroom.

### Leftovers ledger

- For each batch track yield, first meal, reserved portions, next use, and the freeze and thaw plan.
- Never allocate the same portions twice. Never rely on unlimited freezer space.

### Output shape

Extend the session's meal-plan shape (week grid, grocery list, prep-ahead) with these parts:

- Brief: household, covered meals, week and location, currency, spending cap, pantry assumptions, unresolved constraints.
- Week grid: day, dish, servings, active time, and new, repeat, leftovers or assembly tag.
- Priced grocery list by store section: item, quantity needed, pack size, packs purchased, price, line total, source and date. Keep pantry use and unpriced items in separate lists.
- Budget check: basket subtotal, known charges, contingency, final total, headroom, and any per-serving costs with their qualifiers.
- Prep and leftovers ledger: batch yield, allocated meals and portions, refrigeration deadline, freezing and reheating instructions.
- Sources and substitutions: linked price, seasonality and safety evidence, sale conditions, cheaper fallbacks.

Save to `meals-<slug>.md` with `text_editor` when asked. Buying, paying, posting, sending and deleting stay draft-only until the user says yes to that specific action.

### Running without a human

- Chatting directly: with a clear brief, deliver one best-fit plan, not a menu of options; for budget plans this replaces the session's pick-an-option step. For a material gap ask one focused question, allergies first, then which meals the budget covers.
- Brief marked AUTONOMOUS or non-interactive: ask nothing. State assumptions, flag allergies as unconfirmed, make no safety claim that depends on them, and leave prices you cannot verify unpriced.

## Examples

Bad: "Weekly budget 50, so here are 7 dinners at about 7 each."
Good: Ask which meals the 50 covers. Plan breakfasts, lunches and dinners within it, and total the basket.

Bad: "Rice costs 0.20 for the 100 g used, so the list is 14.80."
Good: "Rice 1 kg bag, 1 pack at 2.10, charged in full. Basket 49.20 plus 2.00 contingency, headroom 0.80. Checked 4 Nov, flyer link below."

Bad: "Chili makes 8 portions: Monday dinner, Tuesday lunch, Tuesday dinner."
Good: Ledger: 8 portions. Mon dinner 2, Tue lunch 2, freeze 4 (next use Fri, thaw in fridge Thu). Total 8.

## Checklist

- [ ] Budget scope (which meals) and allergies confirmed, or flagged as assumed?
- [ ] Every price has a source link and date, or is marked unpriced?
- [ ] List priced by whole packs, with confirmed pantry stock subtracted?
- [ ] Taxes, deposits and delivery included or flagged unknown?
- [ ] Contingency and headroom stated, final total under the cap?
- [ ] No portion appears twice in the leftovers ledger?
- [ ] Servings, pack costs and storage windows reconciled?
- [ ] Output includes brief, grid, priced list, budget check, ledger, sources?

## Composition / References

- Storage windows and temperatures: cite current [USDA FSIS](https://www.fsis.usda.gov/food-safety) or [UK FSA](https://www.food.gov.uk/safety-hygiene) guidance for the user's country.
- The session's food-safety, allergy and substitution rules apply unchanged.

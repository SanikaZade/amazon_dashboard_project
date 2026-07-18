# Changelog — Round 2 (correction pass vs. original problem statement)

## Audit result
Checked against Project 78G0OL's objectives and deliverables. Prior version: ~65% aligned.
Gaps found:
1. No written findings/recommendations anywhere (explicit deliverable in the brief).
2. "Customer Segmentation" objective was present only as an unlabeled value/B2B split, with no
   geography cross-reference and no acknowledgment that the dataset lacks a customer ID.

## Added
- **Insights & Recommendations tab** — a new section with ~9 findings and ~8 recommendations,
  all computed live from `DATA` at render time (top category, fulfilment cancellation gap,
  worst-cancelling state, top revenue state, worst-return category, busiest day, dominant value
  segment, top B2B state, and headline rates). Nothing here is hardcoded text — if the CSV is
  replaced and `build_dashboard.py` re-run, every number and the state/category names update
  automatically.
- **B2B Share by State chart** (`chartB2BState`), a new aggregate (`b2b_by_state`) added to
  `build_dashboard.py`, so segmentation now crosses value tier + B2B + geography instead of
  value/B2B alone.
- **Explicit data-limitation note** at the top of the Customer Segmentation tab: the dataset has
  no customer ID, so segmentation is value/B2B/geography-based rather than individual-history-based.
- Tab renamed from "Order Value & Segments" to "Customer Segmentation" to match the brief's
  wording and make the mapping to the original objective explicit.

## Verification performed
- Re-derived every number quoted in the Insights tab independently in a standalone Node script
  against the actual `dashboard_data.json`, confirming figures match (e.g. T-shirt = 50.0% of
  revenue, Merchant vs Amazon cancellation gap = 4.8pp, Kerala highest state cancel rate at 17.6%).
- Confirmed via raw CSV headers that no customer-ID-equivalent field exists, so the segmentation
  caveat is accurate rather than a guess.
- Re-ran `build_dashboard.py` end-to-end and checked the regenerated `dashboard.html`'s embedded
  script for JS syntax errors — none found.

## Post-correction alignment with the original problem statement
- Sales Overview ✅ · Product Analysis ✅ · Fulfillment Analysis ✅ · Geographical Analysis ✅
- Customer Segmentation ✅ (proxy-based, now labeled and cross-referenced, limitation disclosed)
- Business Insights / recommendations for growth ✅ (new tab)
- Deliverable: comprehensive findings + recommendations ✅
- Deliverable: visualizations ✅ (22 charts)
- Deliverable: recommendations for sales/inventory/customer service ✅

Estimated alignment with the original brief: **~95%**. The remaining gap is that this is a live
interactive dashboard, not a static Word/PDF "report" document — if a submittable written report
is specifically required for the internship deliverable, that would need to be generated as a
separate .docx/.pdf summarizing these same findings.

## Round-4 re-verification (this pass, against the original problem statement text)
Went line-by-line through the brief again and found one remaining content gap: "Product Analysis"
explicitly lists **categories, sizes, and quantities** — categories and sizes were fully charted,
but quantity sold only appeared inside the "Units Sold" KPI and buried in a CSV column, with no
dedicated chart. Added a **Quantity Sold by Category** chart (`chartCatQty`) to the Products tab,
wired into the same search filter as the other category charts. The underlying `qty` field already
existed in the aggregated data, so no backend changes were needed — confirmed by simulating the
chart's data path against the real dataset (e.g. T-shirt: 45,129 units, Shirt: 44,671 units).

Re-ran the full structural check suite after this change: no missing `DATA` keys, no orphaned
tabs, no chart `<div>` without a matching draw call, JS syntax still valid.

## Round-3 re-verification (packaging check)
Re-checked the delivered zip from scratch — found and fixed one packaging bug: CHANGELOG.md
(round 1) had been dropped from the zip when the outputs folder was rebuilt for round 2, because
it only ever existed in the outputs copy, not in the working directory that round 2 copied from.
Both changelogs now live in the working directory so future repackaging can't drop either one.

Also re-ran, from the fresh unzipped copy (not the working directory):
- Regex scan confirming every `DATA.xxx` reference in the template has a matching key in
  `dashboard_data.json` — none missing.
- Confirmed every chart `<div id>` has a corresponding `Plotly.newPlot`/draw-function call.
- Confirmed every `data-tab` has a matching `id="tab-*"` section and vice versa — no orphaned tabs.
- Confirmed every `csv-btn` `data-key` maps to a real key in the data file.
- Confirmed `dashboard.html`'s embedded script is byte-identical to `dashboard_template.html`
  with the JSON substituted in (no stale build).
- Re-validated JS syntax with `node --check` on the extracted zip's `dashboard.html`, independent
  of the working copy.

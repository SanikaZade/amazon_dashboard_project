# Changelog — Round 1 (interactivity pass)

## Added
- **About tab** (originally the default landing tab): problem statement, tech stack pills, key features, and a one-paragraph explanation of the build pipeline.
- **Global search box** in the header, filtering by Category / State / City across the Products and Geography tabs (Revenue by Category, Orders by Category, Category×Size heatmap, Top Combos, Return Rate by Category, Top States, Top Cities, Cancellation Rate by State). Debounced (300ms) so it doesn't re-render on every keystroke.
- **Keyboard shortcuts**: `/` focuses the search box from anywhere, `Esc` clears it and returns focus.
- **"No matching results" empty state** for any filtered chart with zero rows, instead of a blank Plotly canvas.
- **CSV export button** on every chart card (21 total at the time), downloading that specific chart's underlying aggregated data as a `.csv` file, properly quoted/escaped.

## Removed
- Nothing — an audit confirmed every existing chart already renders from real aggregated data (no placeholders, no hardcoded zeros), so the "remove empty charts" task was a no-op. The dashboard already had a "hide card if genuinely empty" safety net, which was left in place.

## Unchanged
- Overall visual design, KPI row, tab structure, and the rest of the chart set were left as-is per the requested scope (search + export + About card only).

## Why these choices
- **Search over category/state/city** rather than a full free-text row search: those are the three dimensions recruiters and analysts actually slice this data by, and it lets someone demo "type Maharashtra, watch three charts update" in five seconds — a concrete, visible interaction rather than a cosmetic toggle.
- **CSV per-chart rather than one global export**: keeps the exported file scoped to what's on screen, which is what a hiring manager poking around would expect ("give me *this* chart's numbers"), and it's a trivial addition for anyone to extend to more charts.

*(See CHANGELOG_2.md for the follow-up correction pass against the original problem statement.)*

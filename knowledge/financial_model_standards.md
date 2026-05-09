# Financial Model Standards

> v1 placeholder — expand before production use.

## Required Subject Areas

- Profit & Loss (P&L)
- Balance Sheet (BS)
- Cash Flow (CF)
- Budget & Forecast vs Actuals

## Required Dimensions

- Date (`DimDate`) — marked as date table, full calendar hierarchy
- Account (`DimAccount`) — with account type, hierarchy (L1–L4)
- Cost Centre / Department (`DimCostCentre`)
- Entity / Company (`DimEntity`) — for multi-entity models

## Required Time Intelligence Measures

- YTD (Year-to-Date): `Revenue YTD`, `COGS YTD`, etc.
- PY (Prior Year): `Revenue PY`
- YTD PY (Prior Year YTD): `Revenue YTD PY`
- Variance to PY: `Revenue vs PY`, `Revenue vs PY %`
- Variance to Budget: `Revenue vs Budget`, `Revenue vs Budget %`

## Account Hierarchy

- Level 1: Statement type (P&L, BS, CF)
- Level 2: Major grouping (Revenue, Cost of Sales, Operating Expenses)
- Level 3: Sub-grouping
- Level 4: Account detail

## Buildable Reports (with a complete model)

- P&L by Period (Actuals vs Budget vs PY)
- YTD Summary
- Cost Centre Breakdown
- Entity Consolidation (if multi-entity)
- Waterfall / Bridge chart (Budget to Actuals)

## Blocked Reports (common gaps)

- Cash Flow if CF fact table or CF account mapping is absent
- Budget variance if no budget fact table
- Rolling 12-month if no time intelligence measures

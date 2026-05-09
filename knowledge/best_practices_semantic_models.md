# Best Practices — Financial Semantic Models

> v1 placeholder — expand before production use.

## Naming Conventions

- Tables: PascalCase, no spaces (`FactFinancials`, `DimDate`)
- Measures: Title Case with spaces (`Gross Profit`, `YTD Revenue`)
- Columns: Title Case, no abbreviations unless standard (`Account Code`, `Cost Centre`)
- Hidden columns: prefix with `_` (`_SortOrder`)

## Relationships

- Single active relationship per table pair
- Many-to-one from Fact to Dim
- Date table must be marked as a date table
- Avoid bi-directional filters unless required

## DAX Patterns

- Use `CALCULATE` with `REMOVEFILTERS` rather than `ALL` where possible
- Always use `DIVIDE` instead of `/` to handle division by zero
- Avoid iterators (`SUMX`, `AVERAGEX`) over large tables without necessity
- Use variables (`VAR`) for readability and performance

## Performance

- Avoid calculated columns — prefer measures
- Reduce cardinality on relationship columns (use surrogate keys)
- Avoid `DISTINCTCOUNT` on high-cardinality columns

## Security

- Row-Level Security (RLS) required for any model with multi-entity or multi-department data
- Define RLS roles at the DimEntity / DimCostCentre level
- Test RLS roles before deployment

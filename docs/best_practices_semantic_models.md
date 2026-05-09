# Best Practices: Semantic Models
> **Status:** Placeholder — to be reviewed and expanded with final versions  
> **Purpose:** Reference knowledge base for the BI Assessment Agent. Used to evaluate the structure, naming, and quality of semantic models against industry best practices.

---

## 1. Table Structure & Naming

| Rule | Best Practice | Common Violations | Severity |
|------|--------------|-------------------|----------|
| **Star schema** | Use a star schema — fact tables at the centre, dimension tables around them | Flat tables, snowflake schemas without clear benefit, no separation of facts and dims | 🔴 High |
| **Table naming — facts** | Prefix fact tables with `fact_` or `Fact ` (e.g. `fact_sales`, `Fact Sales`) | `data_sales`, `tbl_sales`, `Sales_Final_v2` | 🟡 Medium |
| **Table naming — dimensions** | Prefix dimension tables with `dim_` or `Dim ` (e.g. `dim_customer`, `Dim Date`) | `lookup_customer`, `ref_date`, `Customers` | 🟡 Medium |
| **Date table** | Always have a dedicated, marked Date table with full calendar + fiscal year columns | Missing Date table, using date columns directly from fact tables | 🔴 High |
| **Bridge tables** | Use bridge tables for many-to-many relationships — never rely on bidirectional filters by default | Overuse of bidirectional filters, missing bridge tables | 🟡 Medium |
| **Calculated tables** | Use sparingly — only when a physical table cannot be loaded | Overuse of calculated tables for simple transformations | 🟡 Medium |
| **Hidden tables** | Hide tables not intended for end users (e.g. support tables, parameter tables) | Support tables visible in report view | 🟢 Low |

---

## 2. Column Naming & Formatting

| Rule | Best Practice | Common Violations | Severity |
|------|--------------|-------------------|----------|
| **Pascal Case or Title Case** | Use consistent casing — `Customer Name`, `Order Date`, `Sales Amount` | `customer_name`, `SALES_AMT`, `orderdate` | 🟡 Medium |
| **No technical prefixes on columns** | Columns should be business-readable — `Sales Amount` not `fct_sales_amt` | Database column names leaked into the model | 🟡 Medium |
| **Units in name where ambiguous** | Include units when relevant — `Sales Amount (GBP)`, `Weight (kg)` | Ambiguous column names with no unit context | 🟡 Medium |
| **No ID columns visible** | Hide surrogate/foreign key ID columns from report view | Raw IDs visible to report users | 🟢 Low |
| **Boolean columns** | Name as a question — `Is Active`, `Has Returns`, `Is Fiscal Year` | `active_flag`, `returns_yn`, `bool_fiscal` | 🟢 Low |
| **Date columns** | Always use `Date` suffix — `Order Date`, `Invoice Date`, `Due Date` | `OrderDt`, `inv_date`, `DueD` | 🟡 Medium |

---

## 3. Measures — Structure & Naming

| Rule | Best Practice | Common Violations | Severity |
|------|--------------|-------------------|----------|
| **Measures in dedicated table** | Store all measures in one or more dedicated measure tables (e.g. `_Measures`, `KPI Measures`) | Measures scattered across fact tables | 🟡 Medium |
| **No spaces at start/end of name** | `[Total Revenue]` not `[ Total Revenue ]` | Whitespace in measure names causes invisible bugs | 🔴 High |
| **Consistent naming pattern** | `[Verb + Noun]` pattern — `[Total Revenue]`, `[Average Order Value]`, `[Count Customers]` | `[rev]`, `[Rev_Tot]`, `[COGS_final_USE_THIS]` | 🔴 High |
| **% measures clearly labelled** | Always suffix with `%` — `[Gross Margin %]`, `[Variance %]` | `[Gross Margin]` returning a ratio, `[gm_pct]` | 🟡 Medium |
| **Format strings set** | Every measure must have an explicit format string | Measures with no format string — relies on report-level formatting | 🟡 Medium |
| **Home table set** | Assign each measure to a logical home table | All measures dumped in one table with no organisation | 🟢 Low |
| **Description populated** | Every measure should have a description explaining what it calculates | Empty descriptions | 🟢 Low |
| **Avoid implicit measures** | Never use auto-generated implicit measures (Sum of X) | Implicit measures used in reports | 🔴 High |

---

## 4. DAX Patterns — Required Measures

The following DAX patterns should be present in any financial semantic model.

### 4.1 Base Measures
```dax
-- Always define a base measure before building time intelligence on top
Total Revenue = SUM( fact_sales[revenue_amount] )
Total Cost = SUM( fact_costs[cost_amount] )
Gross Profit = [Total Revenue] - [Total Cost]
Gross Margin % = DIVIDE( [Gross Profit], [Total Revenue] )
```

### 4.2 Time Intelligence — Required Set
```dax
-- YTD
Revenue YTD = CALCULATE( [Total Revenue], DATESYTD( dim_date[Date] ) )

-- Prior Year
Revenue PY = CALCULATE( [Total Revenue], SAMEPERIODLASTYEAR( dim_date[Date] ) )

-- YoY Variance
Revenue YoY % = DIVIDE( [Total Revenue] - [Revenue PY], [Revenue PY] )

-- Rolling 12 Months
Revenue R12 = 
    CALCULATE( 
        [Total Revenue], 
        DATESINPERIOD( dim_date[Date], LASTDATE( dim_date[Date] ), -12, MONTH ) 
    )
```

### 4.3 Budget vs Actual
```dax
Budget = SUM( fact_budget[budget_amount] )
Variance = [Total Revenue] - [Budget]
Variance % = DIVIDE( [Variance], [Budget] )
```

### 4.4 DIVIDE — Always use instead of `/`
```dax
-- CORRECT — handles divide by zero gracefully
Gross Margin % = DIVIDE( [Gross Profit], [Total Revenue] )

-- INCORRECT — will error on zero denominator
Gross Margin % = [Gross Profit] / [Total Revenue]
```

### 4.5 CALCULATE — Filter Context
```dax
-- Use CALCULATE to modify filter context, not just to wrap aggregations
Revenue Current Year = 
    CALCULATE( 
        [Total Revenue], 
        YEAR( dim_date[Date] ) = YEAR( TODAY() ) 
    )
```

---

## 5. Relationships

| Rule | Best Practice | Common Violations | Severity |
|------|--------------|-------------------|----------|
| **Single direction by default** | All relationships should be single-directional unless there is a documented reason | Bidirectional filters everywhere | 🔴 High |
| **One active relationship per pair** | Only one active relationship between any two tables | Multiple active relationships — causes ambiguity | 🔴 High |
| **Inactive relationships via USERELATIONSHIP** | Use `USERELATIONSHIP()` in DAX for role-playing dimensions | Duplicate dimension tables to handle role-playing | 🟡 Medium |
| **Referential integrity** | All foreign keys in fact tables should match a key in the related dimension | Orphaned rows — fact rows with no matching dimension | 🟡 Medium |
| **Cardinality set correctly** | Always set cardinality explicitly — Many-to-One from fact to dim | Default or wrong cardinality | 🟡 Medium |

---

## 6. Date Table Requirements

A compliant Date table must include:

| Column | Type | Notes |
|--------|------|-------|
| `Date` | Date | Primary key — contiguous, no gaps |
| `Year` | Integer | e.g. `2024` |
| `Quarter Number` | Integer | `1` to `4` |
| `Quarter` | Text | e.g. `Q1 FY2024` |
| `Month Number` | Integer | `1` to `12` |
| `Month Name` | Text | e.g. `January` |
| `Month Short` | Text | e.g. `Jan` |
| `Week Number` | Integer | ISO or calendar week |
| `Day of Week` | Integer | `1` (Mon) to `7` (Sun) |
| `Is Weekday` | Boolean | `TRUE` / `FALSE` |
| `Fiscal Year` | Text | e.g. `FY2024` — if fiscal ≠ calendar |
| `Fiscal Quarter` | Text | e.g. `FQ1 FY2024` |
| `Fiscal Month Number` | Integer | Fiscal month offset |
| `Is Current Month` | Boolean | Dynamic — for default filtering |
| `Is Past Date` | Boolean | Dynamic — for actuals filtering |

> The Date table **must be marked as a Date Table** in the model for time intelligence functions to work correctly.

---

## 7. Performance Best Practices

| Rule | Best Practice | Common Violations | Severity |
|------|--------------|-------------------|----------|
| **Avoid calculated columns for aggregations** | Use measures for aggregations — not calculated columns | Calculated columns doing SUM/AVG logic | 🔴 High |
| **Reduce model size** | Remove unused columns from the model — every column costs memory | Importing full raw tables with 50+ columns when 10 are needed | 🟡 Medium |
| **Use integer keys for relationships** | Relationship columns should be integers, not text strings | Text-based keys (e.g. `"CUST-001"`) as relationship columns | 🟡 Medium |
| **Avoid row-level calculated columns** | Calculated columns that reference measures or use CALCULATE are expensive | `CALCULATE` inside a calculated column | 🔴 High |
| **Aggregations for large tables** | Define aggregations for tables over ~10M rows | No aggregations on large fact tables | 🟡 Medium |
| **Avoid high cardinality text columns** | Don't import free-text columns (notes, descriptions) unless needed | Raw database comment fields imported into model | 🟢 Low |

---

## 8. Security

| Rule | Best Practice | Common Violations | Severity |
|------|--------------|-------------------|----------|
| **Row-Level Security (RLS)** | Define RLS roles for any model with sensitive financial data | No RLS on financial models with multi-entity or multi-region data | 🔴 High |
| **RLS on dimension tables** | Apply RLS filters on dimension tables — not fact tables | RLS applied directly on fact tables | 🟡 Medium |
| **Test RLS roles** | Always test RLS by impersonating each role before publishing | Untested RLS rules | 🔴 High |
| **Object-Level Security (OLS)** | Use OLS to hide sensitive columns (e.g. salary, margin) from specific roles | Sensitive columns visible to all users | 🟡 Medium |

---

## Notes for Assessment

When evaluating a semantic model against this reference:
- **Schema** — flag any model that is not a star schema as high priority
- **Date table** — flag missing or unmarked Date table as a blocker for time intelligence
- **Measure naming** — score consistency across all measure names
- **DAX patterns** — check for presence of YTD, PY, YoY, Budget vs Actual measures
- **Bidirectional filters** — flag any undocumented bidirectional relationships
- **Implicit measures** — flag as high priority if found
- **RLS** — flag absence of RLS on financial models as high severity

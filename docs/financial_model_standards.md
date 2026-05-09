# Financial Model Standards
> **Status:** Placeholder — to be reviewed and expanded with final versions  
> **Purpose:** Reference knowledge base for the BI Assessment Agent. Defines what a complete, production-ready financial semantic model should contain — used to identify gaps and opportunities.

---

## 1. Required Subject Areas

A complete financial semantic model should cover these subject areas. Missing areas are scored as gaps.

| Subject Area | Required Tables | Priority | Notes |
|-------------|----------------|----------|-------|
| **Profit & Loss (P&L)** | `fact_actuals`, `fact_budget`, `fact_forecast`, `dim_account`, `dim_date` | 🔴 Core | Foundation of any financial model |
| **Balance Sheet** | `fact_balance_sheet`, `dim_account`, `dim_date` | 🔴 Core | Assets, liabilities, equity |
| **Cash Flow** | `fact_cashflow`, `dim_cashflow_category`, `dim_date` | 🔴 Core | Operating, investing, financing |
| **Budget & Variance** | `fact_budget`, `fact_actuals` | 🔴 Core | Must support Actual vs Budget vs Forecast |
| **Cost Centre / Department** | `dim_cost_centre`, `dim_department` | 🔴 Core | Required for internal reporting |
| **Legal Entity / Company** | `dim_entity`, `dim_company` | 🟡 Standard | Required for multi-entity or group reporting |
| **Project / WBS** | `fact_project_costs`, `dim_project` | 🟡 Standard | Required for project-based businesses |
| **Headcount & Payroll** | `fact_payroll`, `dim_employee`, `dim_position` | 🟡 Standard | Required for HR/Finance combined reporting |
| **Accounts Receivable (AR)** | `fact_ar`, `dim_customer`, `dim_date` | 🟡 Standard | Ageing, DSO, collections |
| **Accounts Payable (AP)** | `fact_ap`, `dim_supplier`, `dim_date` | 🟡 Standard | Ageing, DPO, payment terms |
| **Fixed Assets** | `fact_assets`, `dim_asset_category` | 🟢 Extended | Depreciation schedules, CapEx tracking |
| **Intercompany** | `fact_intercompany`, `dim_entity` | 🟢 Extended | Required for consolidated group reporting |

---

## 2. Account Hierarchy

Financial models must represent the chart of accounts as a hierarchy. The standard structure is:

```
Financial Statement
└── Statement Section          (e.g. Income Statement, Balance Sheet)
    └── Account Category       (e.g. Revenue, Operating Expenses, Assets)
        └── Account Group      (e.g. Sales Revenue, Payroll Costs)
            └── Account        (e.g. Product Sales, Salary Expense)
                └── Sub-Account (optional — for detailed breakdown)
```

### Required Columns in `dim_account`

| Column | Type | Example | Notes |
|--------|------|---------|-------|
| `account_key` | Integer | `1001` | Surrogate key |
| `account_code` | Text | `"4001"` | Source system code |
| `account_name` | Text | `"Product Revenue"` | Business-readable name |
| `account_group` | Text | `"Sales Revenue"` | Level 4 hierarchy |
| `account_category` | Text | `"Revenue"` | Level 3 hierarchy |
| `statement_section` | Text | `"Income Statement"` | Level 2 hierarchy |
| `financial_statement` | Text | `"P&L"` | Level 1 — top level |
| `is_debit_positive` | Boolean | `TRUE` | Sign convention flag |
| `account_type` | Text | `"Revenue"` | Used for sign handling in DAX |
| `sort_order` | Integer | `10` | Controls display order in reports |

---

## 3. P&L Structure

A standard P&L semantic model must support this reporting structure:

```
Revenue
  └── Gross Sales
  └── Returns & Discounts
= Net Revenue

- Cost of Goods Sold (COGS)
= Gross Profit

- Operating Expenses
    └── Payroll & Benefits
    └── Rent & Facilities
    └── Marketing & Advertising
    └── IT & Software
    └── Travel & Entertainment
    └── Depreciation & Amortisation
    └── Other OpEx
= EBITDA (before D&A add-back)
= EBIT

- Interest Expense
- Tax Expense
= Net Income
```

### Required P&L Measures

| Measure | DAX Pattern | Priority |
|---------|------------|----------|
| `[Net Revenue]` | `SUM` of revenue accounts | 🔴 Core |
| `[Total COGS]` | `SUM` of COGS accounts | 🔴 Core |
| `[Gross Profit]` | `[Net Revenue] - [Total COGS]` | 🔴 Core |
| `[Gross Margin %]` | `DIVIDE( [Gross Profit], [Net Revenue] )` | 🔴 Core |
| `[Total OpEx]` | `SUM` of OpEx accounts | 🔴 Core |
| `[EBITDA]` | `[Gross Profit] - [Total OpEx]` | 🔴 Core |
| `[EBIT]` | `[EBITDA] - [Depreciation] - [Amortisation]` | 🔴 Core |
| `[Net Income]` | `[EBIT] - [Interest Expense] - [Tax Expense]` | 🔴 Core |
| `[Net Margin %]` | `DIVIDE( [Net Income], [Net Revenue] )` | 🔴 Core |
| `[Budget Net Revenue]` | `SUM` from `fact_budget` | 🔴 Core |
| `[Variance]` | `[Net Revenue] - [Budget Net Revenue]` | 🔴 Core |
| `[Variance %]` | `DIVIDE( [Variance], [Budget Net Revenue] )` | 🔴 Core |
| `[Net Revenue YTD]` | `DATESYTD` pattern | 🔴 Core |
| `[Net Revenue PY]` | `SAMEPERIODLASTYEAR` pattern | 🔴 Core |
| `[Net Revenue YoY %]` | `DIVIDE( current - PY, PY )` | 🔴 Core |
| `[EBITDA Margin %]` | `DIVIDE( [EBITDA], [Net Revenue] )` | 🟡 Standard |
| `[OpEx % of Revenue]` | `DIVIDE( [Total OpEx], [Net Revenue] )` | 🟡 Standard |
| `[Net Revenue R12]` | `DATESINPERIOD` rolling 12M pattern | 🟡 Standard |

---

## 4. Balance Sheet Structure

```
Assets
  └── Current Assets
      └── Cash & Equivalents
      └── Accounts Receivable
      └── Inventory
      └── Prepaid Expenses
  └── Non-Current Assets
      └── Property, Plant & Equipment (PP&E)
      └── Intangible Assets
      └── Long-Term Investments

Liabilities
  └── Current Liabilities
      └── Accounts Payable
      └── Short-Term Debt
      └── Accrued Expenses
  └── Non-Current Liabilities
      └── Long-Term Debt
      └── Deferred Tax

Equity
  └── Share Capital
  └── Retained Earnings
  └── Other Reserves
```

### Required Balance Sheet Measures

| Measure | Priority |
|---------|----------|
| `[Total Assets]` | 🔴 Core |
| `[Total Liabilities]` | 🔴 Core |
| `[Total Equity]` | 🔴 Core |
| `[Net Debt]` | 🔴 Core |
| `[Working Capital]` | 🔴 Core |
| `[Current Ratio]` | 🟡 Standard |
| `[Debt to Equity]` | 🟡 Standard |
| `[ROE %]` | 🟡 Standard |
| `[ROA %]` | 🟡 Standard |

---

## 5. Cash Flow Structure

```
Operating Activities
  └── Net Income
  └── Adjustments (D&A, working capital changes)
= Cash Flow from Operations

Investing Activities
  └── CapEx
  └── Asset disposals
  └── Acquisitions
= Cash Flow from Investing

Financing Activities
  └── Debt issuance / repayment
  └── Dividends paid
  └── Share issuance
= Cash Flow from Financing

= Net Change in Cash
```

### Required Cash Flow Measures

| Measure | Priority |
|---------|----------|
| `[Operating Cash Flow]` | 🔴 Core |
| `[CapEx]` | 🔴 Core |
| `[Free Cash Flow]` | 🔴 Core |
| `[Cash Flow from Investing]` | 🟡 Standard |
| `[Cash Flow from Financing]` | 🟡 Standard |
| `[Net Change in Cash]` | 🟡 Standard |

---

## 6. Dimension Completeness Checklist

Every financial model should include these dimensions as a minimum:

| Dimension | Key Columns | Priority | Notes |
|-----------|------------|----------|-------|
| `dim_date` | Full calendar + fiscal columns — see best practices | 🔴 Core | Must be marked as Date Table |
| `dim_account` | Account hierarchy — see Section 2 | 🔴 Core | Chart of accounts |
| `dim_cost_centre` | `cost_centre_code`, `cost_centre_name`, `department`, `division` | 🔴 Core | Internal reporting structure |
| `dim_entity` | `entity_code`, `entity_name`, `country`, `currency`, `consolidation_group` | 🟡 Standard | Multi-entity / group models |
| `dim_customer` | `customer_key`, `customer_name`, `segment`, `region`, `country` | 🟡 Standard | Required for revenue analysis |
| `dim_supplier` | `supplier_key`, `supplier_name`, `category`, `country` | 🟡 Standard | Required for AP/spend analysis |
| `dim_employee` | `employee_key`, `employee_name`, `department`, `role`, `start_date` | 🟡 Standard | Required for headcount/payroll |
| `dim_currency` | `currency_code`, `currency_name`, `exchange_rate` | 🟡 Standard | Required for multi-currency models |
| `dim_scenario` | `scenario_key`, `scenario_name` (Actual / Budget / Forecast) | 🔴 Core | Enables scenario switching in DAX |

---

## 7. Scenario & Version Control

Financial models should support multiple scenarios in a single model using a `dim_scenario` pattern:

```dax
-- Scenario switcher measure
Selected Revenue = 
    SWITCH(
        SELECTEDVALUE( dim_scenario[scenario_name] ),
        "Actual",   [Total Revenue Actual],
        "Budget",   [Total Revenue Budget],
        "Forecast", [Total Revenue Forecast],
        [Total Revenue Actual]  -- default
    )
```

| Scenario | Source Table | Notes |
|----------|-------------|-------|
| **Actual** | `fact_actuals` | Posted / confirmed figures |
| **Budget** | `fact_budget` | Approved annual plan |
| **Forecast** | `fact_forecast` | Rolling updated projection |
| **Prior Year** | `fact_actuals` filtered by prior year | Derived via time intelligence |

---

## 8. Currency & Multi-Entity

For models supporting multiple currencies or legal entities:

| Requirement | Best Practice | Notes |
|-------------|--------------|-------|
| **Local currency** | Store all transactions in local (source) currency | `transaction_currency_code`, `local_amount` |
| **Reporting currency** | Convert to a single reporting currency using exchange rates | `reporting_amount = local_amount * exchange_rate` |
| **Exchange rate table** | Maintain a `fact_exchange_rates` table with daily rates | `date_key`, `from_currency`, `to_currency`, `rate` |
| **Average vs closing rate** | Use average rate for P&L, closing rate for Balance Sheet | Different rate types needed |
| **Intercompany elimination** | Flag intercompany transactions for group consolidation | `is_intercompany` flag on fact tables |

---

## 9. Report Layers — What Should Be Buildable

Given a complete financial semantic model, the following reports should be possible:

| Report | Required Measures & Dims | Priority |
|--------|--------------------------|----------|
| **P&L Summary** | P&L measures, `dim_date`, `dim_cost_centre` | 🔴 Core |
| **P&L vs Budget** | Actual + Budget measures, Variance, `dim_scenario` | 🔴 Core |
| **YoY Trend** | YTD, PY, YoY % measures, `dim_date` | 🔴 Core |
| **Balance Sheet Summary** | Balance Sheet measures, `dim_date` | 🔴 Core |
| **Cash Flow Statement** | Cash Flow measures, `dim_date` | 🔴 Core |
| **Cost Centre Breakdown** | OpEx measures, `dim_cost_centre`, `dim_account` | 🔴 Core |
| **Executive KPI Dashboard** | Key margins, growth %, `dim_date` | 🟡 Standard |
| **AR Ageing** | AR measures, `dim_customer`, `dim_date` | 🟡 Standard |
| **AP Ageing** | AP measures, `dim_supplier`, `dim_date` | 🟡 Standard |
| **Headcount & Payroll** | Payroll measures, `dim_employee`, `dim_cost_centre` | 🟡 Standard |
| **CapEx Tracker** | CapEx measures, `dim_asset_category`, `dim_date` | 🟢 Extended |
| **Consolidated Group P&L** | All P&L measures, `dim_entity`, intercompany elimination | 🟢 Extended |

---

## Notes for Assessment

When evaluating a semantic model against this reference:
- **Subject area coverage** — identify which of the 12 subject areas are present, partially present, or missing
- **Account hierarchy** — check if `dim_account` has all required levels; flag missing hierarchy as a high-priority gap
- **P&L completeness** — check for all Core P&L measures; missing measures block standard reporting
- **Scenario support** — flag absence of `dim_scenario` or scenario switching pattern
- **Dimension completeness** — score each dimension against the checklist in Section 6
- **Buildable reports** — list which reports from Section 9 are currently possible vs blocked by missing components
- **Currency handling** — flag any multi-currency data without an exchange rate table

# Financial Terms Reference
> **Status:** Placeholder — to be reviewed and expanded with final versions  
> **Purpose:** Reference knowledge base for the BI Assessment Agent. Used to validate whether semantic models correctly represent core financial concepts.

---

## 1. Profitability

| Term | Definition | Common Measure Name | Common DB Table/Column Names |
|------|-----------|-------------------|------------------------------|
| **Revenue** | Total income from goods/services sold before any deductions | `[Total Revenue]`, `[Gross Sales]` | `fact_sales`, `fact_revenue`, `revenue_amount`, `net_sales` |
| **Gross Profit** | Revenue minus Cost of Goods Sold (COGS) | `[Gross Profit]` | Calculated — not usually a raw table column |
| **Gross Margin** | Gross Profit as a % of Revenue | `[Gross Margin %]` | Calculated |
| **EBITDA** | Earnings Before Interest, Taxes, Depreciation & Amortisation — proxy for operating cash generation | `[EBITDA]` | Calculated — derived from P&L tables |
| **EBIT** | Earnings Before Interest and Taxes — operating profit | `[EBIT]`, `[Operating Profit]` | Calculated |
| **Net Income** | Bottom-line profit after all expenses, interest, and taxes | `[Net Income]`, `[Net Profit]` | `net_income`, `profit_after_tax`, `pat` |
| **Net Margin** | Net Income as a % of Revenue | `[Net Margin %]` | Calculated |
| **Operating Expenses (OpEx)** | Day-to-day costs not directly tied to production (e.g. salaries, rent, marketing) | `[Total OpEx]` | `fact_opex`, `operating_expenses`, `opex_amount` |
| **Cost of Goods Sold (COGS)** | Direct costs of producing goods/services sold | `[COGS]`, `[Cost of Sales]` | `fact_cogs`, `cost_of_sales`, `cogs_amount` |

---

## 2. Liquidity & Cash Flow

| Term | Definition | Common Measure Name | Common DB Table/Column Names |
|------|-----------|-------------------|------------------------------|
| **Cash Flow from Operations** | Cash generated from core business activities | `[Operating Cash Flow]` | `fact_cashflow`, `operating_cash_flow`, `cf_operations` |
| **Free Cash Flow (FCF)** | Operating Cash Flow minus Capital Expenditure | `[Free Cash Flow]` | Calculated — `capex` + `operating_cash_flow` |
| **Working Capital** | Current Assets minus Current Liabilities — measures short-term liquidity | `[Working Capital]` | Calculated — from `dim_balance_sheet` or `fact_financials` |
| **Current Ratio** | Current Assets / Current Liabilities — liquidity health indicator | `[Current Ratio]` | Calculated |
| **Quick Ratio** | (Current Assets - Inventory) / Current Liabilities — stricter liquidity measure | `[Quick Ratio]` | Calculated |
| **Days Sales Outstanding (DSO)** | Average number of days to collect payment after a sale | `[DSO]` | `fact_ar`, `accounts_receivable`, `ar_days` |
| **Days Payable Outstanding (DPO)** | Average number of days to pay suppliers | `[DPO]` | `fact_ap`, `accounts_payable`, `ap_days` |
| **Cash Conversion Cycle (CCC)** | DSO + Days Inventory Outstanding - DPO — how fast cash moves through the business | `[Cash Conversion Cycle]` | Calculated |

---

## 3. Balance Sheet

| Term | Definition | Common Measure Name | Common DB Table/Column Names |
|------|-----------|-------------------|------------------------------|
| **Assets** | Resources owned by the business (current + non-current) | `[Total Assets]` | `fact_balance_sheet`, `total_assets`, `asset_value` |
| **Liabilities** | Obligations owed to external parties | `[Total Liabilities]` | `total_liabilities`, `liability_amount` |
| **Equity** | Assets minus Liabilities — owner's share of the business | `[Total Equity]`, `[Shareholders Equity]` | `shareholders_equity`, `total_equity` |
| **Debt** | Borrowed funds (short-term + long-term) | `[Total Debt]` | `long_term_debt`, `short_term_debt`, `total_debt` |
| **Net Debt** | Total Debt minus Cash & Equivalents | `[Net Debt]` | Calculated |
| **Debt-to-Equity Ratio** | Total Debt / Total Equity — leverage indicator | `[Debt to Equity]` | Calculated |
| **Return on Equity (ROE)** | Net Income / Shareholders Equity | `[ROE %]` | Calculated |
| **Return on Assets (ROA)** | Net Income / Total Assets | `[ROA %]` | Calculated |

---

## 4. Expenses

| Term | Definition | Common Measure Name | Common DB Table/Column Names |
|------|-----------|-------------------|------------------------------|
| **Operating Expenses (OpEx)** | All costs required to run the business day-to-day, excluding COGS | `[Total OpEx]` | `fact_opex`, `operating_expenses`, `opex_amount` |
| **Selling, General & Admin (SG&A)** | Combined sales, marketing, and administrative overhead costs | `[SG&A]`, `[Total SGA]` | `fact_sga`, `sga_expenses`, `selling_expenses` |
| **Selling Expenses** | Costs directly related to sales activity (commissions, travel, advertising) | `[Selling Expenses]` | `selling_expenses`, `sales_costs`, `commission_amount` |
| **General & Administrative (G&A)** | Back-office costs — finance, HR, legal, executive (not directly tied to sales) | `[G&A Expenses]` | `ga_expenses`, `admin_expenses`, `overhead_costs` |
| **Payroll / Personnel Costs** | Salaries, wages, bonuses, employer taxes, and benefits | `[Payroll Cost]`, `[Personnel Expenses]` | `fact_payroll`, `payroll_amount`, `salary_cost`, `headcount_cost` |
| **Depreciation** | Allocation of a tangible asset's cost over its useful life | `[Depreciation]` | `depreciation_amount`, `fact_depreciation`, `da_amount` |
| **Amortisation** | Allocation of an intangible asset's cost over its useful life | `[Amortisation]` | `amortisation_amount`, `intangible_amortisation` |
| **Capital Expenditure (CapEx)** | Spending on long-term physical assets (equipment, property, infrastructure) | `[CapEx]` | `fact_capex`, `capital_expenditure`, `capex_amount` |
| **Interest Expense** | Cost of borrowing — paid on debt obligations | `[Interest Expense]` | `interest_expense`, `finance_costs`, `debt_interest` |
| **Tax Expense** | Corporate income tax charged on profits | `[Tax Expense]`, `[Income Tax]` | `tax_expense`, `income_tax`, `tax_amount` |
| **Research & Development (R&D)** | Investment in innovation, product development, and technology | `[R&D Expense]` | `rd_expense`, `research_costs`, `fact_rd` |
| **Rent & Facilities** | Lease payments, utilities, and building-related costs | `[Rent Expense]`, `[Facilities Cost]` | `rent_expense`, `lease_cost`, `facilities_amount` |
| **Marketing & Advertising** | Spend on campaigns, digital ads, events, and brand activities | `[Marketing Expense]` | `marketing_spend`, `ad_spend`, `campaign_cost` |
| **IT & Software Costs** | Licences, subscriptions, infrastructure, and technology spend | `[IT Expense]`, `[Software Cost]` | `it_expense`, `software_licences`, `tech_costs` |
| **Travel & Entertainment (T&E)** | Employee travel, accommodation, and client entertainment costs | `[T&E Expense]` | `travel_expense`, `te_amount`, `entertainment_costs` |
| **Bad Debt / Provisions** | Estimated uncollectable receivables written off | `[Bad Debt Expense]`, `[Provision]` | `bad_debt_expense`, `provision_amount`, `write_off` |
| **Cost Allocation** | Distribution of shared costs across departments or cost centres | `[Allocated Costs]` | `cost_allocation`, `allocated_amount`, `dim_cost_centre` |

---

## 5. Budgeting & Variance

| Term | Definition | Common Measure Name | Common DB Table/Column Names |
|------|-----------|-------------------|------------------------------|
| **Budget** | Planned financial target for a period | `[Budget]`, `[Target]` | `fact_budget`, `budget_amount`, `target_value` |
| **Actual** | Real recorded financial result | `[Actual]` | `fact_actuals`, `actual_amount`, `posted_amount` |
| **Variance** | Difference between Actual and Budget | `[Variance]`, `[Var vs Budget]` | Calculated |
| **Variance %** | Variance as a % of Budget | `[Variance %]` | Calculated |
| **Forecast** | Updated projection based on actuals to date | `[Forecast]` | `fact_forecast`, `forecast_amount` |
| **Full Year Estimate (FYE)** | Projected year-end result combining actuals + forecast | `[FYE]` | Calculated |
| **Prior Year (PY)** | Same period in the previous year | `[PY Revenue]`, `[PY Net Income]` | Calculated via time intelligence |
| **Year-over-Year (YoY)** | Change compared to the same period last year | `[YoY Growth %]` | Calculated |

---

## 6. Time Intelligence

| Term | Definition | Common Measure Name | Common DB Table/Column Names |
|------|-----------|-------------------|------------------------------|
| **Year-to-Date (YTD)** | Cumulative value from start of fiscal year to current date | `[YTD Revenue]` | Calculated — requires `dim_date` |
| **Month-to-Date (MTD)** | Cumulative value from start of current month | `[MTD Revenue]` | Calculated — requires `dim_date` |
| **Quarter-to-Date (QTD)** | Cumulative value from start of current quarter | `[QTD Revenue]` | Calculated — requires `dim_date` |
| **Rolling 12 Months (R12)** | Sum over the last 12 months regardless of fiscal year | `[R12 Revenue]` | Calculated |
| **Fiscal Year** | Organisation's accounting year — may not align to calendar year | Used in Date table config | `dim_date`, `fiscal_year`, `fiscal_period` |

---

## 7. Key Performance Indicators (KPIs)

| Term | Definition | Common Measure Name | Common DB Table/Column Names |
|------|-----------|-------------------|------------------------------|
| **KPI** | A measurable value that indicates performance against an objective | Varies | `fact_kpi`, `kpi_value`, `kpi_target` |
| **Run Rate** | Annualised projection based on current performance | `[Run Rate Revenue]` | Calculated |
| **Headcount** | Number of employees — often used in HR/Finance combined models | `[Headcount]`, `[FTE]` | `dim_employee`, `headcount`, `fte_count` |
| **Revenue per FTE** | Revenue divided by Full-Time Equivalent headcount | `[Revenue per FTE]` | Calculated |
| **Cost per Unit** | Total cost divided by units produced or sold | `[Cost per Unit]` | Calculated |

---

## Notes for Assessment

When evaluating a semantic model against this reference:
- Check whether key financial terms have corresponding measures
- Verify measure names follow a consistent convention (e.g. `[Gross Margin %]` not `[gm_pct]`)
- Flag missing time intelligence measures (YTD, PY, YoY) as high-priority gaps
- Flag missing budget/variance measures if the model is meant to support FP&A use cases

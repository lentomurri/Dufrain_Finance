Finance Gold Layer — FP&A Reference Standard (Stub v0.1)

Purpose: This file defines the ideal data structure for a Corporate FP&A gold layer
covering P&L, Balance Sheet, and Cash Flow. It is used by the Financial Assessment Agent
as the benchmark against which client data sources are evaluated.
Status: Week 1 stub — intentionally minimal. Expand in Phase 2.


1. Overview
A complete FP&A gold layer requires data across three financial statement domains:
DomainPriorityCore GrainProfit & Loss (P&L)HighAccount × Entity × PeriodBalance Sheet (BS)HighAccount × Entity × Period-endCash Flow StatementMediumCategory × Entity × Period
All three domains share common dimension tables that must be present or derivable.

2. Required Fact Tables
2.1 fact_gl_actuals — General Ledger Actuals
The central fact table for P&L and Balance Sheet.
FieldTypeRequiredDescriptiondateDate✅Transaction or period-end datefiscal_yearInteger✅e.g. 2024fiscal_periodInteger✅Month number within fiscal year (1–12)account_codeString✅GL account identifieraccount_nameString✅Human-readable account nameaccount_typeString✅P&L / Balance Sheet / Cash Flowentity_codeString✅Legal entity or cost centre identifieramount_lcDecimal✅Amount in local currencyamount_gcDecimal⚠️Amount in group/reporting currencycurrency_codeString✅ISO 4217 currency code (e.g. GBP, EUR)data_typeString✅Actuals / Budget / ForecastscenarioString⚠️e.g. Base / Upside / Downsideintercompany_flagBoolean⚠️True if intercompany transaction
Minimum viable: date, account_code, account_type, entity_code, amount_lc, data_type

2.2 fact_budget — Budget & Forecast
Same structure as fact_gl_actuals. May be a separate table or a data_type filter on the same table.
FieldTypeRequiredNotesfiscal_yearInteger✅Budget yearfiscal_periodInteger✅account_codeString✅Must match GL account codesentity_codeString✅Must match entity codesamount_budgetDecimal✅versionString⚠️e.g. Original Budget / Latest Estimate

2.3 fact_cashflow — Cash Flow Statement (optional at stub stage)
FieldTypeRequiredDescriptiondateDate✅cashflow_categoryString✅Operating / Investing / Financingcashflow_itemString✅Line item descriptionentity_codeString✅amountDecimal✅

3. Required Dimension Tables
3.1 dim_account — Chart of Accounts
FieldTypeRequiredDescriptionaccount_codeString✅Primary keyaccount_nameString✅account_typeString✅P&L / Balance Sheet / Cash Flowfs_lineString✅Financial statement line (e.g. Revenue, COGS, EBITDA)fs_subtotalString✅Subtotal grouping (e.g. Gross Profit, Operating Expenses)sign_conventionInteger✅1 or -1 — controls debit/credit display logicis_activeBoolean⚠️Filter out inactive accounts
Critical: fs_line and fs_subtotal are the fields that enable P&L/BS structuring.
Without them, financial statement layout is not possible.

3.2 dim_entity — Legal Entities / Cost Centres
FieldTypeRequiredDescriptionentity_codeString✅Primary keyentity_nameString✅entity_typeString✅Legal Entity / Cost Centre / BUcountry_codeString⚠️ISO 3166currency_codeString✅Functional currencyconsolidation_groupString⚠️Parent group for rollup

3.3 dim_date — Date / Calendar Table
FieldTypeRequiredDescriptiondateDate✅Primary keyfiscal_yearInteger✅fiscal_periodInteger✅Month within fiscal yearfiscal_quarterInteger✅calendar_yearInteger✅calendar_monthInteger✅is_current_periodBoolean✅ytd_flagBoolean⚠️Useful for YTD aggregations
Note: If fiscal year ≠ calendar year, the offset must be defined in client-context.md.

4. Key Business Rules
These rules must hold for the data to support reliable FP&A reporting:

Account classification is complete — every account_code in fact_gl_actuals must exist in dim_account with a valid fs_line
Periods are contiguous — no gaps in fiscal periods within a reporting year
Sign convention is consistent — revenue credits should be positive after applying sign_convention
Data type is explicit — Actuals, Budget, Forecast must be clearly separated (not inferred)
Entity-currency alignment — entity_code in facts must join to dim_entity for currency context


5. Standard FP&A KPIs — Minimum Viable Set

Full catalogue in finance-kpi-catalogue-stub.md. This is the Week 1 shortlist.

KPIRequired FieldsBuildable WithoutRevenueamount_lc where fs_line = 'Revenue'Cannot build without fs_lineGross ProfitRevenue − COGS via fs_subtotalCannot build without subtotal mappingGross Margin %Gross Profit / RevenueRequires both aboveEBITDAOperating profit + D&A accountsRequires account classificationActuals vs Budget Variancefact_gl_actuals + fact_budget joined on account + entity + periodRequires budget dataYTD Revenueamount_lc filtered by ytd_flag or period rangeRequires dim_dateRevenue Growth %Current period vs prior period RevenueRequires ≥2 periods of data

6. Common Gap Patterns (Agent Reference)
When assessing client data, flag these as high-priority gaps:
GapImpactSeverityNo fs_line / fs_subtotal on accountsCannot structure P&L or BS🔴 CriticalNo data_type fieldCannot separate Actuals from Budget🔴 CriticalNo dim_date or date tableNo time intelligence, no YTD/MTD🔴 CriticalMissing entity_codeNo entity-level reporting🟠 HighNo budget dataNo variance analysis🟠 HighNo currency_codeMulti-currency reporting impossible🟠 HighMissing sign_conventionP&L signs unreliable🟡 MediumNo consolidation_groupGroup rollup not possible🟡 MediumGaps in fiscal periodsTime series analysis unreliable🟡 MediumNo intercompany_flagConsolidation adjustments not possible🟢 Low (unless group reporting)

7. Fitness Scoring Rubric (Agent Reference)
Score each domain 0–100. Thresholds:
ScoreRAGMeaning80–100🟢 GreenData is fit for purpose — minor gaps only50–79🟡 AmberPartially fit — key gaps present but workarounds possible0–49🔴 RedNot fit for FP&A reporting — critical fields missing
Domain weights for overall score:
DomainWeightP&L coverage35%Balance Sheet coverage25%Time Intelligence (dim_date)20%Entity Dimension10%Budget / Forecast data10%

Version: 0.1 — Stub for Week 1 testing. Do not use as final client reference.
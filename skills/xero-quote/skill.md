---
name: xero-quote
description: Create a Xero quote for a client through guided discovery. Use when the user wants to create a quote, estimate, proposal, or says "create quote", "quote for", "how much to charge", "estimate for", or "price up".
---

# Xero Quote Generator

Create a Xero quote by gathering requirements from a feature spec, GitHub issue, document, or freeform description, then estimating effort and generating the quote.

## Usage

```
/xero-quote
/xero-quote {client name}
/xero-quote {issue number}
```

## Context

- **Quote creation:** Via VIPER Admin server function `xero_create_quote()` in `~/GitHub/VIPER-Admin/server_code/XeroQuotes.py`
- **Xero API:** Creates DRAFT quotes in Xero Accounting API
- **Currency:** AUD
- **Account code:** 200

### Quote Data Structure

```python
{
    "contact": "Company name (partial match against Xero contacts)",
    "title": "Quote title",
    "summary": "Brief summary (optional)",
    "expiry_date": "YYYY-MM-DD",
    "terms": "Payment terms (optional)",
    "reference": "PO or reference number (optional)",
    "line_items": [
        {
            "description": "Line item description",
            "quantity": 1,
            "unit_price": 150.00
        }
    ]
}
```

## Workflow

### Step 1: Identify the Starting Point

Ask the user:

> What are we quoting for? I can work from:

| Source | Description |
|--------|-------------|
| **GitHub issue** | I'll read the issue and estimate effort |
| **Feature spec/plan** | Point me to a spec document or plan file |
| **Document/file** | I'll read a requirements document |
| **Freeform description** | Tell me what the work involves |
| **Previous quote** | Base it on an existing quote with modifications |

### Step 2: Gather Requirements

Based on the starting point:

#### From a GitHub Issue

```bash
# Determine which repo
# Ask user if unclear
gh issue view {number} --repo VIPER-Metrics/{repo}
```

Read the issue body, comments, and any linked PRs. Extract:
- Scope of work
- Acceptance criteria
- Technical complexity

#### From a Feature Spec/Plan

Read the file the user points to. Look for:
- Feature description
- Implementation steps
- UI mockups or wireframes
- Data model changes

#### From a Document

Read the document and extract requirements. Summarize back to the user for confirmation.

#### From Freeform Description

Ask structured follow-up questions:

1. **What is the deliverable?** (Feature, fix, integration, report, etc.)
2. **What's the scope?** (Number of forms, endpoints, integrations)
3. **Any complexity factors?** (Third-party APIs, data migration, offline support)
4. **Is there existing code to build on?** (Enhancement vs greenfield)

### Step 3: Identify the Client

If `$ARGUMENTS` contains a client name, use it. Otherwise ask:

> Which client is this quote for?

The contact name must match a Xero contact (partial match works). Known clients:
- Paramount
- David Campbell Transport
- EG / Energy Group
- Central OOTH
- Other (specify)

### Step 4: Estimate Effort

Based on the gathered requirements, break the work into line items and estimate hours.

#### Estimation Guidelines

| Work Type | Typical Hours | Notes |
|-----------|--------------|-------|
| Simple form (CRUD) | 8-16 | Single form with server functions |
| Complex form | 16-32 | Multiple panels, validation, business logic |
| Data table changes | 2-4 | Schema + migration (done in Anvil IDE) |
| Server function | 2-8 | Depends on complexity |
| API integration | 16-40 | External API, auth, error handling |
| Report | 8-24 | Data aggregation, formatting, scheduling |
| Bug fix (simple) | 2-4 | Clear cause, isolated fix |
| Bug fix (complex) | 4-16 | Investigation, multiple files, edge cases |
| Sync endpoint | 8-16 | Bidirectional sync with conflict resolution |
| UI component | 4-12 | Reusable component with styling |

#### Presenting the Estimate

Show a breakdown table:

> ## Effort Estimate
>
> | Item | Description | Hours |
> |------|-------------|-------|
> | 1 | Backend: Server functions for X | 8 |
> | 2 | Frontend: Form UI for Y | 16 |
> | 3 | Integration: Connect to Z API | 12 |
> | 4 | Testing & refinement | 4 |
> | **Total** | | **40** |
>
> At **$X/hour**, this comes to **$Y + GST**

Ask the user:
- Does this breakdown look right?
- Should any items be adjusted?
- What hourly rate to use?
- Any buffer/contingency to add?

### Step 5: Build Quote Details

Ask for remaining quote fields:

> **Quote title:** (suggest based on the work)
> **Expiry date:** (default: 30 days from today)
> **Payment terms:** (e.g., "Net 30", "50% upfront, 50% on completion")
> **Reference/PO number:** (if the client has provided one)

### Step 6: Structure Line Items

Decide how to present the quote:

**Option A: Single line item** (simple)
```
Development: {Feature Name} - {total hours} hours @ ${rate}/hr
```

**Option B: Itemized breakdown** (detailed)
```
1. Backend development - {hours} hours @ ${rate}/hr
2. Frontend UI - {hours} hours @ ${rate}/hr
3. Integration & testing - {hours} hours @ ${rate}/hr
```

Ask the user which format they prefer.

### Step 7: Review and Confirm

Present the complete quote for approval:

> ## Quote Draft
>
> **To:** {client name}
> **Title:** {title}
> **Reference:** {reference}
> **Expiry:** {date}
>
> | # | Description | Qty | Unit Price | Total |
> |---|-------------|-----|------------|-------|
> | 1 | {desc} | {qty} | ${price} | ${total} |
> | 2 | {desc} | {qty} | ${price} | ${total} |
> | | | | **Subtotal** | **${subtotal}** |
> | | | | **GST (10%)** | **${gst}** |
> | | | | **Total** | **${total}** |
>
> **Terms:** {terms}
>
> Ready to create this quote in Xero?

### Step 8: Create the Quote

Once approved, call the server function via the VIPER Admin app, or output the JSON for manual upload:

```json
{
    "contact": "{client_name}",
    "title": "{title}",
    "expiry_date": "{YYYY-MM-DD}",
    "reference": "{reference}",
    "terms": "{terms}",
    "line_items": [
        {
            "description": "{description}",
            "quantity": {hours},
            "unit_price": {rate}
        }
    ]
}
```

Save to `~/GitHub/xero-time-entries/quotes/` for reference.

### Step 9: Confirm

> ## Quote Created
>
> **Quote Number:** {number}
> **Status:** DRAFT
> **Total:** ${total} + GST
>
> The quote has been created as a DRAFT in Xero.
> Log in to Xero to review and send it to the client.

---

## Guidelines

### Estimation Best Practices
- Always add a buffer (10-20%) for unknowns
- Round up to the nearest half-day (4 hours) for each line item
- Consider testing and refinement as a separate line item
- For new integrations, add time for API exploration and documentation

### Pricing
- Ask the user for the hourly rate - don't assume
- Different clients may have different rates
- Some work may be fixed-price rather than hourly

### Quote Scope
- Be specific about what's included and excluded
- Note any assumptions in the quote summary
- Flag dependencies (e.g., "assumes client provides API credentials")

### Reusing Previous Quotes
- Check `~/GitHub/xero-time-entries/quotes/` for previous quotes
- Offer to base new quotes on similar past work

---

## Error Handling

| Scenario | Action |
|----------|--------|
| Client not found in Xero | Ask user for exact company name as it appears in Xero |
| Requirements too vague | Ask more questions before estimating |
| Very large scope | Suggest breaking into phases with separate quotes |
| User unsure about rate | Suggest checking previous invoices or asking finance |
| Feature already partially built | Estimate only remaining work, note what exists |

---

## Integration Points

| Skill | Relationship |
|-------|--------------|
| `/create-feature` | Feature issues can feed into quotes |
| `/feature-planner` | Implementation plans help refine estimates |
| `/xero-time-entries` | Time entries track actual vs quoted hours |

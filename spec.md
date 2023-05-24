# Partner-Specific Account Module for Odoo

## 1. Overview
This document outlines the informal specification for an Odoo module designed to manage Partner-specific Accounts Receivable and 
Accounts Payable for German companies. This module adds functionality beyond the standard Odoo Chart of Accounts (CoA).

## 2. Features

### 2.1. Extended Chart of Accounts
The module extends the standard Odoo CoA to include Partner-specific Accounts (PSA) for Accounts Receivable and Accounts Payable. 
These accounts will be used to store income and expenditures related to specific business partners.

User can choose to either use PSA or Odoo's default CoA to store Incomes and Expenditures, specific to the partner.

### 2.2. Create Partner-specific Accounts Button
A new button, "Create Partner-specific Accounts", will be added under `Contact > Invoicing (tab) > Accounting Entries`. 
This button will trigger the creation of a new set of Partner-specific Accounts in the extended CoA for the selected business partner.

## 3. Functional Specifications

### 3.1. Partner-specific Accounts
1. **Description**: Partner-specific Accounts are additional accounts in the CoA that are associated with a specific business partner. 
  They are used to store incomes (Accounts Receivable) and expenditures (Accounts Payable) accrued for that partner.
  
2. **Fields**:
  - Business Partner (Many2one relation to `res.partner`)
  - Accounts Receivable (One2many relation to `account.account`)
  - Accounts Payable (One2many relation to `account.account`)

3. **Constraints**: There can only be one set of Partner-specific Accounts per business partner.

### 3.2. Create Partner-specific Accounts Button
1. **Description**: A button located under `Contact > Invoicing > Accounting Entries` that creates Partner-specific Accounts 
  in the extended CoA for the selected business partner.
  
2. **Behavior**: Upon clicking, the system will check if there are existing Partner-specific Accounts for the selected partner. 
  If there are, a warning message will be displayed. If there aren't, a new set of Partner-specific Accounts will be created.
    1. In case PSA are already available for a Partner, then display them under the Invoicing tab on res.partner view.
    2. **Permissions**: Only users with accounting permissions can see and use this button.

### 4. Customer Invoices and Vendor Bills

Provide a selection right under the Invoices tab on partner view called “Use Partner Specific Accounts”

- If True, then Incomes and Receivables will be posted to the new PSA, assuming they are created. 
  If not yet created, they can be created by using the "Create Partner-specific Account" described above.
- If False, then Incomes and Receivables will be posted to the default Odoo Accounts (from default CoA).

Keep the UI intuitive for the user, avoiding confusion. 
Assume that they do not know what PSA is, and provide helpful descriptions, at least for the PSA option.

## Non-Functional Specifications
1. **Performance**: The module should not significantly impact the performance of the Odoo system. Creating Partner-specific Accounts should take less than 1 second under normal system load.
2. **Usability**: 
    - Create as few as possible new UI elements. Integrate to the maximum extent into existing Odoo UIs.
    - The "Create Partner-specific Accounts" button should be clearly visible and conveniently located under Contact > Invoicing > Accounting Entries.
3. **Security**: Only users with the Sales Manager and Accounting Admin should be able to create Partner-specific Accounts.

---
# Q&A from Developers
Previous developers asked these questions.

> 1. If a partner already had Accounts Receivable and Accounts Payable like this, do we allow the user to create Partner-specific Accounts for this partner? 

Yes of course.
That’s the point of this module.

Odoo’s Accounting works by assigning generic accounts, in the below example 1410 for Accounts Payable and 1610 for Accounts Payable.
Generic = every partner’s recievables and payables are stored under these account numbers.

The point of the partner_accounts module is to have specific account numbers for partner specific receivables and payables.

Please remember!!
that revenues (Customer Invoices) and expenditures (Vendor Bills) should be posted to these new Partner Accounts.

![telegram-cloud-photo-size-5-6292052975140582212-y](https://github.com/euroblaze/partner_accounts/assets/7826363/1b1af399-7a5b-4dba-a038-fdca1658ab0f)

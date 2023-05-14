# Partner-Specific Account Module for Odoo

## Overview
This document outlines the informal specification for an Odoo module designed to manage Partner-specific Accounts Receivable and 
Accounts Payable for German companies. This module adds functionality beyond the standard Odoo Chart of Accounts (CoA).

## Features

### Extended Chart of Accounts
The module extends the standard Odoo CoA to include Partner-specific Accounts (PSA) for Accounts Receivable and Accounts Payable. 
These accounts will be used to store income and expenditures related to specific business partners.

### Create Partner-specific Accounts Button
A new button, "Create Partner-specific Accounts", will be added under `Contact > Invoicing (tab) > Accounting Entries`. 
This button will trigger the creation of a new set of Partner-specific Accounts in the extended CoA for the selected business partner.

## Functional Specifications

### Partner-specific Accounts
- **Description**: Partner-specific Accounts are additional accounts in the CoA that are associated with a specific business partner. 
  They are used to store incomes (Accounts Receivable) and expenditures (Accounts Payable) accrued for that partner.
- **Fields**:
  - Business Partner (Many2one relation to `res.partner`)
  - Accounts Receivable (One2many relation to `account.account`)
  - Accounts Payable (One2many relation to `account.account`)
- **Constraints**: There can only be one set of Partner-specific Accounts per business partner.

### Create Partner-specific Accounts Button
- **Description**: A button located under `Contact > Invoicing > Accounting Entries` that creates Partner-specific Accounts 
  in the extended CoA for the selected business partner.
- **Behavior**: Upon clicking, the system will check if there are existing Partner-specific Accounts for the selected partner. 
  If there are, a warning message will be displayed. If there aren't, a new set of Partner-specific Accounts will be created.
- In case PSA are already available for a Partner, then display them under the Invoicing tab on res.partner view.
- **Permissions**: Only users with accounting permissions can see and use this button.

### Customer Invoices and Vendor Bills
- If PSA are available, store Accounts Recievable and Accounts Payable in them.

## Non-Functional Specifications
- **Performance**: The module should not significantly impact the performance of the Odoo system. Creating Partner-specific Accounts should take less than 1 second under normal system load.
- **Usability**: The "Create Partner-specific Accounts" button should be clearly visible and conveniently located under Contact > Invoicing > Accounting Entries.
- **Security**: Only users with the necessary permissions should be able to create Partner-specific Accounts.

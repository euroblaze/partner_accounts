# Partner-Specific Account Module for Odoo

This module extends the Odoo Chart of Accounts (CoA) to include Partner-specific Accounts for Accounts Receivable and Accounts Payable. These accounts are used to store income and expenditures related to specific business partners. The module also provides a convenient button for creating these accounts.

## Features

- **Extended Chart of Accounts**: The module extends the standard Odoo CoA to include Partner-specific Accounts.

- **Create Partner-specific Accounts Button**: A new button located under Contact > Invoicing > Accounting Entries allows the creation of Partner-specific Accounts for the selected business partner.

## Installation

1. Place the module directory in your Odoo addons folder.
2. Restart the Odoo service.
3. Update the Apps list by going to Apps > Update Apps List.
4. Install the module by going to Apps, removing the 'Apps' filter, searching for 'Partner-Specific Account', and clicking on Install.

## Usage

1. Navigate to a Contact.
2. Go to the Invoicing tab.
3. Click on the "Create Partner-specific Accounts" button under Accounting Entries.

## Limitations

This module is a simplified example and does not handle every case. It doesn't take care of creating actual account records for receivables and payables. Also, it doesn't handle access permissions. Further refinements would be needed for a fully functional module.

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License

[LGPL](LICENSE)

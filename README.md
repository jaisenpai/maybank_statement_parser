# maybank_statement_parser
A simple tool that convert PDF Maybank statements and exports clean, spreadsheet-ready CSVs.

(CS50’s Introduction to Programming with Python - Final Project)

### Introduction
- [**Situation**] : Maybank, a local south east asia bank does not provide options to download in any other format beside PDF format, hindering users from easily importing data into analytical tools like Excel or Google Sheets.
- [**Task**] : Create a robust Python utility designed to parse Maybank statements in PDF form that automatically read, extract, and transform to a readable and standardized format.
- [**Action**] : Developed a custom parser using Python logic learned in CS50P. Enhanced the codebase through expert assistant, implementing advanced regex matching and multi-page description handling.
- [**Result**] : A simple tool that convert PDF and exports clean, spreadsheet-ready CSVs

### Features
- **PDF Extraction** : Automatically parses dates, transaction details, and amounts using pdfplumber.
- **Data Cleaning** : Handles Maybank’s currency formatting to readable csv format.
- **Auto-Opening Balance** : Automatically backtracks from the first transaction to calculate your starting balance for the month.
- **Interactive Workflow** : Allows users to preview data in the terminal and rename the final CSV output.
- **Multi-line Merging** : Merges transaction descriptions that split across rows through pages.
- **Transaction List Display** : Generate transaction lists directly to terminal with tabulate.
- **Transaction Summary** : Displays a professional summary including Total In, Total Out, and End-month Balance.

### Workflow
1. **Extraction** : The script reads the PDF and identifies transaction rows.
2. **Preview** : You will be asked: Do you want to print data to terminal? (Y/N).
3. **Calculation** : The script prints a summary of your monthly cash flow.
4. **Export** : A CSV file is generated (e.g., your_statement.csv).
5. **Rename** : You can choose to rename the CSV file immediately after creation.

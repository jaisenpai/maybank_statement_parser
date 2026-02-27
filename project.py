import pdfplumber
import sys
import os
from time import sleep
from tabulate import tabulate
import csv
import re

### 1. MAIN SECTION ###

def main () :

    #check on user filename input
    if len(sys.argv) != 2 :
        sys.exit("Input pdf filename")

    pdf_path = sys.argv[1]

    #validate pdf file
    if not pdf_path.endswith(".pdf")or not os.path.exists(pdf_path) :
        sys.exit("Invalid file path or format. Please provide a valid PDF")

    transaction_data,counter = data_extraction (pdf_path)

    print (f"Successully extracted {counter} transactions.")

    #user input for dataprint on terminal
    while True :
        choice = input("\nDo you want to print data to terminal? (Y/N) ").strip().upper()
        if choice == "Y" :
            data_print (transaction_data)
            break
        elif choice == "N" :
            break
        print ("Invalid input. Please enter Y or N.")

    data_calculation (transaction_data)

    #generate initial name for csv
    csv_filename = pdf_path.replace(".pdf",".csv")

    generate_csv(transaction_data,csv_filename)
    print (f"[✓] Data exported to {csv_filename}")

    #user input for renaming csv
    while True :
        rename_file = input("Would you like to rename the file? (Y/N) : ").strip().upper()
        if rename_file == "Y" :
            rename_csv (csv_filename)
            break
        elif rename_file == "N" :
            break
        print ("Invalid input. Please enter Y or N.")

### 2. DATA SECTION ###

#extract data from pdf
def data_extraction(pdf_path):
    transactions = []
    transaction_count = 0
    date_regex = re.compile(r"^\d{2}/\d{2}$")

    # Expanded footer keywords based on PDF statement
    footer_keywords = [
        "BAKI LEGAR", "ENDING BALANCE", "UNCLEARED CHEQUES",
        "PERHATIAN", "ALL ITEMS AND BALANCES", "NOTIFIED IN WRITING",
        "SILA BERITAHU", "CHANGE OF ADDRESS", "MALAYAN BANKING",
        "MUKA/", "PAGE :", "STATEMENT DATE", "ACCOUNT NUMBER"
    ]

    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if not text: continue

            # Reset footer flag for each new page
            footer_reached = False
            lines = text.split('\n')

            for line in lines:
                parts = line.split()
                if not parts: continue

                #detect footer section
                if any(key in line.upper() for key in footer_keywords):
                    footer_reached = True
                    continue # Skip this line and stop appending to desc

                #check for new transaction
                if date_regex.match(parts[0]):
                    footer_reached = False # Reset if a new table starts (multi-page)
                    try:
                        date = parts[0]
                        balance = parts[-1]
                        amount = parts[-2]
                        description = " ".join(parts[1:-2])

                        transactions.append({
                            "date": date,
                            "description": description,
                            "transaction": data_clean(amount),
                            "balance": data_clean(balance)
                        })
                        transaction_count += 1
                    except IndexError:
                        continue

                #handle continuation (only if not in footer)
                elif transactions and not footer_reached:
                    #additional check to skip header section
                    if "TRANSACTION DESCRIPTION" in line.upper() or "JUMLAH" in line.upper():
                        continue

                    extra_text = " ".join(parts)
                    transactions[-1]["description"] += f" {extra_text}"

    #input initial balance on 1st row
    initial_balance = calculate_initial_balance (transactions[0])

    start_row = {
        "date" : transactions[0]["date"],
        "description" : "Opening balance",
        "transaction" : 0.0,
        "balance" : initial_balance
    }
    transactions.insert(0,start_row)
    return transactions, transaction_count

#clean value input data to float
def data_clean (val) :
    if not val or val == "" :
        return 0.0

    #money in/out detection through +/- symbol
    clean_val = str(val).strip().replace(",","")
    if clean_val.endswith("+") :
        clean_val = clean_val.replace("+","")
    if clean_val.endswith("-") :
        clean_val = "-" + clean_val.replace("-","")

    try :
            return float(clean_val)
    except ValueError :
        return 0.0

### 3. CALCULATION SECTION ###

#calculation for withdrawal and deposit
def data_calculation (datas) :
    total_in = 0
    total_out = 0

    for data in datas :
        if data["transaction"] >= 0 :
            total_in += data["transaction"]
        if data["transaction"] < 0 :
            total_out -= data["transaction"]
    print("-" * 34)
    print (f"Opening balance   : RM{datas[0]["balance"]:>12,.2f}")
    print (f"Total in          : RM{total_in:>12,.2f}")
    print (f"Total out         : RM{total_out:>12,.2f}")
    print (f"End-month balance : RM{datas[-1]["balance"]:>12,.2f}")
    print("-" * 34)

    return total_in, total_out

#for calculating initial balance and append into list
def calculate_initial_balance (data) :

    balance = data["balance"] - data["transaction"]
    return balance

#to print table line-by-line, delayed
def data_print (datas) :

    display_data = []
    for data in datas :
        display_data.append({
            "Date" : data["date"],
            "Description" : data["description"][:30],
            "Amount" : f"RM {data["transaction"]:>10,.2f}"

        })

    table_output = tabulate(display_data,headers="keys", tablefmt="grid")
    for line in table_output.splitlines():
        print(line)
        sleep(0.02)

### 4. CSV SECTION ###

#create csv file for data exporting
def generate_csv (data_table ,csv_file) :

    table_headers = ["date","description","transaction","balance"]
    with open(csv_file,"w") as file :
        writer = csv.DictWriter (file, fieldnames = table_headers)
        writer.writeheader()
        writer.writerows(data_table)

#rename csv file for ease of use
def rename_csv (file) :

    new_file = input("Please enter new name (without .csv) : ")
    csv_filename = os.rename (file,new_file+".csv")
    print (f"\n[✓] Successfully renamed to {new_file}.csv")
    return csv_filename

if __name__ == "__main__":
    main()

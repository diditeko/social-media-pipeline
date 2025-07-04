import asyncio
import json
from twscrape import API

async def main():
    api = API()

    # Load account data from JSON file
    with open("account2.json", "r") as file:
        accounts = json.load(file)

    # Loop through all accounts
    for account in accounts:
        try:
            await api.pool.add_account(
                username=account["username"],
                password=account["password"],
                email=account["email"],
                email_password=account["email_pass"],
                # proxy="http://your.proxy.here"  # optional
            )

            acc = await api.pool.get(account["username"])
            result = await api.pool.login(acc)

            if result:
                print(f"[+] Login success: {account['username']}")
            else:
                print(f"[-] Login failed: {account['username']}")

        except Exception as e:
            print(f"[!] Error processing {account['username']}: {e}")

if __name__ == "__main__":
    asyncio.run(main())

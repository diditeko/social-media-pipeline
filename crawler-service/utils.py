import json
from pydantic import BaseModel, Field
from typing import List
from twscrape.api import API
import os

class AccountPool(BaseModel):
    username: str = Field(...)
    password: str = Field(...)
    email: str = Field(...)
    email_pass: str = Field(...)

async def load_accounts_from_file(api: API, file_path=None) -> List[AccountPool]:
    if file_path is None:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(base_dir, "accounts.json")

    with open(file_path) as f:
        accounts_data = json.load(f)

    accounts = [AccountPool(**acc) for acc in accounts_data]

    for acc in accounts:
        await api.pool.add_account(
            username=acc.username,
            password=acc.password,
            email=acc.email,
            email_password=acc.email_pass
        )
        user = await api.pool.get(acc.username)
        result = await api.pool.login(user)
        if result:
            print(f"[+] Login success: {acc.username}")
        else:
            print(f"[-] Login failed: {acc.username}")
            await api.pool.delete_accounts(acc.username)
    return accounts

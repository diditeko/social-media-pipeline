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

def load_accounts_from_file(api: API, file_path=None) -> List[AccountPool]:
    if file_path is None:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(base_dir, "accounts.json")
    print(file_path)

    with open(file_path) as f:
        accounts_data = json.load(f)

    print(accounts_data)

load_accounts_from_file(AccountPool)
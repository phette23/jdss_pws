import csv
import sys
from getpass import getpass
from os import environ
from pathlib import Path
from subprocess import run

"""
Usage:
- python create.py [file.csv]
- PW=sup3erS3CRET python create.py
Assumes the CSV is named accounts.csv if not provided.
You can specify the password with a PASSWORD or PW env var;
if one is not supplied, then you're prompted to type it.
"""

csv_file: Path = Path("accounts.csv")
if len(sys.argv) == 2:
    csv_file = Path(sys.argv[2])

if not csv_file.exists():
    print(f"Error: could not find file {csv_file}")
    sys.exit(1)

pw: str = environ.get("PASSWORD") or environ.get("PW") or getpass("Enter password: ")
if not pw:
    print("Error: no password provided")
    sys.exit(1)

with open(csv_file, mode="r") as fh:
    reader = csv.DictReader(fh)
    for row in reader:
        email: str = row["email"]
        if email:  # ! one row has no email
            org: str = row["org"]
            tier: int = int(row["tier"])
            # ! different login pages according to tier
            url: str = (
                "https://www.jstor.org/admin/collection-loader/login"
                if tier == 1
                else "https://stewardship.jstor.org/"
            )
            result = run(
                [
                    "op",
                    "item",
                    "create",
                    "--category",
                    "login",
                    "--vault",
                    "SCELC",
                    "--title",
                    f"{org} JDSS",
                    "--url",
                    url,
                    f"username={email}",
                    f"password={pw}",
                ],
                check=True,
            )
            if not result.returncode:
                print(f"Successfully created login item for {org}")

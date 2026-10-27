"""Initialize the SQLite database from the supplied archive once."""

import os
import shutil
import sqlite3
import subprocess
import sys
from pathlib import Path
from zipfile import ZipFile

data_dir = Path("/data")
db_path = data_dir / "comercio_exterior.db"
csv_path = data_dir / "polizas_full.csv"


def valid_database() -> bool:
    if not db_path.exists():
        return False
    try:
        with sqlite3.connect(f"file:{db_path}?mode=ro", uri=True) as conn:
            return (
                conn.execute("PRAGMA integrity_check").fetchone()[0] == "ok"
                and conn.execute("SELECT COUNT(*) FROM poliza_items").fetchone()[0] > 0
            )
    except sqlite3.Error:
        return False


if valid_database():
    print("Database already initialized", flush=True)
    sys.exit(0)

data_dir.mkdir(parents=True, exist_ok=True)
with ZipFile("/input/polizas_full.csv.zip") as archive:
    with archive.open("polizas_full.csv") as source, csv_path.open("wb") as target:
        shutil.copyfileobj(source, target)

os.chdir(data_dir)
subprocess.run([sys.executable, "/app/setup.py"], check=True)
if not valid_database():
    sys.exit("Database initialization failed or produced an empty database")
csv_path.unlink()
print("Database initialized successfully", flush=True)

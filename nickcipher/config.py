from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent

PACKAGE_DIR = PROJECT_ROOT / "nickcipher"
KEYS_DIR = PROJECT_ROOT / "keys"
DATA_DIR = PROJECT_ROOT / "data"
BASE_DIR = PROJECT_ROOT / "base"
INPUT_DIR = DATA_DIR / "input"
OUTPUT_DIR = DATA_DIR / "output"

print(PROJECT_ROOT)
print(DATA_DIR)
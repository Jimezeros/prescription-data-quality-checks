import pandas as pd
from pathlib import Path

# -----------------------------
# File paths
# -----------------------------
BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "data"

PATIENTS_FILE = DATA_DIR / "patients.csv"
PRESCRIPTIONS_FILE = DATA_DIR / "prescriptions.csv"

# -----------------------------
# Load data
# -----------------------------
patients = pd.read_csv(PATIENTS_FILE)
prescriptions = pd.read_csv(PRESCRIPTIONS_FILE)

# Convert date columns
date_columns = ["issue_date", "dispense_date"]
for col in date_columns:
    prescriptions[col] = pd.to_datetime(prescriptions[col], errors="coerce")

# -----------------------------
# Basic inspection
# -----------------------------
print("\n=== DATASET OVERVIEW ===")
print(f"Patients rows: {len(patients)}")
print(f"Prescriptions rows: {len(prescriptions)}")

print("\n=== PATIENTS INFO ===")
print(patients.info())

print("\n=== PRESCRIPTIONS INFO ===")
print(prescriptions.info())

print("\n=== PATIENTS SAMPLE ===")
print(patients.head())

print("\n=== PRESCRIPTIONS SAMPLE ===")
print(prescriptions.head())

print("\n=== MISSING VALUES (PRESCRIPTIONS) ===")
print(prescriptions.isna().sum())

# -----------------------------
# Helper functions
# -----------------------------
def normalize_text(value):
    """Normalize text for safer comparisons."""
    if pd.isna(value):
        return None
    return str(value).strip().lower()

# -----------------------------
# Check 1: Missing dosage value
# -----------------------------
missing_dosage = prescriptions[
    prescriptions["dosage_value"].isna() | (prescriptions["dosage_value"] <= 0)
].copy()

print("\n=== CHECK 1: MISSING DOSAGE VALUE ===")
print(f"Flagged rows: {len(missing_dosage)}")
if not missing_dosage.empty:
    print(
        missing_dosage[
            [
                "prescription_id",
                "patient_id",
                "drug_name",
                "active_ingredient",
                "dosage_value",
                "dosage_unit",
                "frequency",
            ]
        ]
    )

# -----------------------------
# Check 2: Inconsistent dosage unit formatting
# -----------------------------
prescriptions["dosage_unit_normalized"] = prescriptions["dosage_unit"].apply(normalize_text)

valid_unit_map = {
    "mg": "mg",
    "milligram": "mg",
    "milligrams": "mg",
    "ml": "ml",
    "milliliter": "ml",
    "milliliters": "ml",
    "mcg": "mcg",
    "μg": "mcg",
    "g": "g",
}

prescriptions["dosage_unit_standardized"] = prescriptions["dosage_unit_normalized"].map(valid_unit_map)

inconsistent_unit_formatting = prescriptions[
    prescriptions["dosage_unit_normalized"].notna()
    & (
        prescriptions["dosage_unit_normalized"] != prescriptions["dosage_unit_standardized"]
    )
].copy()

print("\n=== CHECK 2: INCONSISTENT DOSAGE UNIT FORMATTING ===")
print(f"Flagged rows: {len(inconsistent_unit_formatting)}")
if not inconsistent_unit_formatting.empty:
    print(
        inconsistent_unit_formatting[
            [
                "prescription_id",
                "drug_name",
                "dosage_value",
                "dosage_unit",
                "dosage_unit_standardized",
            ]
        ]
    )

# -----------------------------
# Check 3: Inconsistent frequency notation
# -----------------------------
prescriptions["frequency_normalized"] = prescriptions["frequency"].apply(normalize_text)

standard_frequency_map = {
    "once daily": "once daily",
    "1x/day": "once daily",
    "od": "once daily",
    "twice daily": "twice daily",
    "2x/day": "twice daily",
    "bid": "twice daily",
    "three times daily": "three times daily",
    "3x/day": "three times daily",
    "tid": "three times daily",
    "every 8 hours": "every 8 hours",
    "q8h": "every 8 hours",
}

prescriptions["frequency_standardized"] = prescriptions["frequency_normalized"].map(standard_frequency_map)

inconsistent_frequency = prescriptions[
    prescriptions["frequency_normalized"].notna()
    & prescriptions["frequency_standardized"].isna()
].copy()

print("\n=== CHECK 3: INCONSISTENT FREQUENCY NOTATION ===")
print(f"Flagged rows: {len(inconsistent_frequency)}")
if not inconsistent_frequency.empty:
    print(
        inconsistent_frequency[
            [
                "prescription_id",
                "drug_name",
                "frequency",
            ]
        ]
    )

# -----------------------------
# Check 4: Dispense date earlier than issue date
# -----------------------------
date_inconsistency = prescriptions[
    prescriptions["dispense_date"] < prescriptions["issue_date"]
].copy()

print("\n=== CHECK 4: DISPENSE DATE EARLIER THAN ISSUE DATE ===")
print(f"Flagged rows: {len(date_inconsistency)}")
if not date_inconsistency.empty:
    print(
        date_inconsistency[
            [
                "prescription_id",
                "patient_id",
                "drug_name",
                "issue_date",
                "dispense_date",
            ]
        ]
    )

# -----------------------------
# Optional: summary dictionary
# -----------------------------
summary = {
    "missing_dosage": len(missing_dosage),
    "inconsistent_unit_formatting": len(inconsistent_unit_formatting),
    "inconsistent_frequency_notation": len(inconsistent_frequency),
    "dispense_date_before_issue_date": len(date_inconsistency),
}

print("\n=== CHECK SUMMARY ===")
for check_name, count in summary.items():
    print(f"{check_name}: {count}")

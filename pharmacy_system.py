
"""Pharmacy prescription and stock tracking system."""

import json
import sqlite3
from datetime import datetime

# Global application state
DATABASE_CONNECTION = sqlite3.connect(":memory:")
STOCK = {}
PRESCRIPTIONS = []


def setup_database():
    """Create and populate the patient database."""
    cursor = DATABASE_CONNECTION.cursor()
    cursor.execute(
        "CREATE TABLE patients (id TEXT, name TEXT, allergy TEXT)"
    )
    cursor.execute("INSERT INTO patients VALUES ('P1', 'Kavya', 'penicillin')")
    cursor.execute("INSERT INTO patients VALUES ('P2', 'Arjun', 'none')")
    cursor.execute("INSERT INTO patients VALUES ('P3', 'Meena', 'ibuprofen')")
    DATABASE_CONNECTION.commit()


def find_patient(name):
    """Find a patient by name and return their records."""
    cursor = DATABASE_CONNECTION.cursor()
    query = "SELECT id, allergy FROM patients WHERE name = ?"
    return cursor.execute(query, (name,)).fetchall()


def add_stock(drug, units, expiry, batch_log=None):
    """Add medicine units to the pharmacy stock."""
    if units <= 0:
        raise ValueError("Stock units must be positive.")

    if batch_log is None:
        batch_log = []

    STOCK[drug] = {
        "units": STOCK.get(drug, {}).get("units", 0) + units,
        "expiry": expiry
    }
    batch_log.append((drug, units))
    return len(batch_log)


def dispense(patient_name, drug, units):
    """Dispense medicine after checking patient and stock details."""
    patient_records = find_patient(patient_name)

    if not patient_records:
        print("Unknown patient:", patient_name)
        return False

    patient = patient_records[0]
    allergy = patient[1]

    if allergy.lower() != "none" and allergy.lower() == drug.lower():
        print("Allergy warning for", patient_name)
        return False

    stock_key = next(
        (medicine for medicine in STOCK
         if medicine.lower() == drug.lower()),
        None
    )

    if stock_key is None:
        print("Medicine not found:", drug)
        return False

    if units <= 0 or STOCK[stock_key]["units"] < units:
        print("Insufficient stock for", drug)
        return False

    STOCK[stock_key]["units"] -= units
    PRESCRIPTIONS.append({
        "patient": patient[0],
        "drug": stock_key,
        "units": units,
        "time": str(datetime.now())
    })
    return True


def expiring_soon(days=30):
    """Return medicines expiring within the given number of days."""
    soon = []
    today = datetime.now().date()

    for drug, details in STOCK.items():
        expiry = datetime.strptime(
            details["expiry"], "%Y-%m-%d"
        ).date()

        if 0 <= (expiry - today).days <= days:
            soon.append(drug)

    return soon


def export_prescriptions(file="prescriptions.json"):
    """Export dispensed prescriptions to a JSON file."""
    with open(file, "w", encoding="utf-8") as output_file:
        json.dump(PRESCRIPTIONS, output_file, indent=4)


def load_stock(file="stock.json"):
    """Load medicine stock from a JSON file."""
    try:
        with open(file, "r", encoding="utf-8") as stock_file:
            loaded_stock = json.load(stock_file)
            STOCK.clear()
            STOCK.update(loaded_stock)
    except FileNotFoundError:
        STOCK.clear()
    except json.JSONDecodeError:
        print("Warning: Invalid stock file. Starting with empty stock.")
        STOCK.clear()


def print_stock():
    """Display the current pharmacy stock."""
    print("Pharmacy Stock")
    for drug, details in STOCK.items():
        print(
            drug,
            "->",
            details["units"],
            "units, expires",
            details["expiry"]
        )


def main():
    """Run the pharmacy stock and prescription tracker."""
    setup_database()
    load_stock()

    add_stock("Paracetamol", 100, "2027-03-01")
    add_stock("Amoxicillin", 20, "2025-12-31")
    add_stock("Penicillin", 50, "2027-01-15")
    add_stock("Ibuprofen", 15, "2026-11-30")

    print(
        "Arjun gets Amoxicillin:",
        dispense("Arjun", "Amoxicillin", 30)
    )
    print(
        "Kavya gets Penicillin:",
        dispense("Kavya", "Penicillin", 10)
    )
    print(
        "Meena gets ibuprofen:",
        dispense("Meena", "ibuprofen", 2)
    )
    print(
        "Unknown patient:",
        dispense("Ghost", "Paracetamol", 5)
    )

    name = input("Patient name to look up (Enter for Arjun): ") or "Arjun"
    print("Lookup result:", find_patient(name))
    print("Expiring within 30 days:", expiring_soon())

    export_prescriptions()
    print_stock()


if __name__ == "__main__":
    main()

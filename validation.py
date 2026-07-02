import json
from pathlib import Path

# Path to HRIS employee data
HRIS_FILE = Path("hris/employees.json")


def load_employees():
    """
    Load employee records from JSON file.
    """
    try:
        with open(HRIS_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        print("❌ employees.json not found.")
        return []
    except json.JSONDecodeError:
        print("❌ Invalid JSON format.")
        return []


def get_employee(employee_id):
    """
    Search employee by Employee ID.
    """
    employees = load_employees()

    employee_id = employee_id.strip().upper()

    for employee in employees:
        if employee.get("employee_id", "").upper() == employee_id:
            return employee

    return None


def validate_employee(employee_id):
    """
    Validate whether employee exists.
    Returns:
        (True, employee_data)
        (False, None)
    """
    employee = get_employee(employee_id)

    if employee:
        return True, employee

    return False, None


def is_asset_allowed(employee, asset_type):
    """
    Check whether an employee is eligible
    to request a particular asset.
    """

    if employee is None:
        return False

    role = employee.get("role", "").lower()
    grade = employee.get("grade", "").upper()
    asset = asset_type.lower()

    # Rule 1: Interns cannot request MacBooks
    if role == "intern" and asset == "macbook":
        return False

    # Rule 2: Premium devices are only for senior grades
    premium_assets = [
        "macbook",
        "premium laptop",
        "workstation"
    ]

    if asset in premium_assets:
        return grade in ["G5", "G6", "G7"]

    # Rule 3: Standard assets are allowed
    return True


if __name__ == "__main__":

    emp_id = input("Enter Employee ID: ")

    valid, employee = validate_employee(emp_id)

    if valid:
        print("\n✅ Employee Found")
        print(employee)

        asset = input("\nEnter Asset Type: ")

        if is_asset_allowed(employee, asset):
            print("✅ Asset Request Allowed")
        else:
            print("❌ Asset Request Not Allowed")

    else:
        print("❌ Employee Not Found")
"""
Run this script once to create sample_timetable.xlsx
Usage: python create_sample.py
"""
import pandas as pd
import os

data = [
    # Class A
    {"Class": "Class A", "Subject": "Mathematics",    "Hours": 5},
    {"Class": "Class A", "Subject": "English",        "Hours": 4},
    {"Class": "Class A", "Subject": "Physics",        "Hours": 3},
    {"Class": "Class A", "Subject": "Chemistry",      "Hours": 3},
    {"Class": "Class A", "Subject": "History",        "Hours": 2},
    {"Class": "Class A", "Subject": "Physical Ed",    "Hours": 2},
    {"Class": "Class A", "Subject": "Computer Sci",   "Hours": 2},
    # Class B
    {"Class": "Class B", "Subject": "Mathematics",    "Hours": 5},
    {"Class": "Class B", "Subject": "English",        "Hours": 4},
    {"Class": "Class B", "Subject": "Biology",        "Hours": 3},
    {"Class": "Class B", "Subject": "Geography",      "Hours": 3},
    {"Class": "Class B", "Subject": "Art",            "Hours": 2},
    {"Class": "Class B", "Subject": "Physical Ed",    "Hours": 2},
    {"Class": "Class B", "Subject": "Music",          "Hours": 2},
    # Class C
    {"Class": "Class C", "Subject": "Mathematics",    "Hours": 4},
    {"Class": "Class C", "Subject": "English",        "Hours": 4},
    {"Class": "Class C", "Subject": "Physics",        "Hours": 3},
    {"Class": "Class C", "Subject": "Biology",        "Hours": 3},
    {"Class": "Class C", "Subject": "Economics",      "Hours": 3},
    {"Class": "Class C", "Subject": "Physical Ed",    "Hours": 2},
    {"Class": "Class C", "Subject": "Computer Sci",   "Hours": 2},
    # Class D
    {"Class": "Class D", "Subject": "Mathematics",    "Hours": 5},
    {"Class": "Class D", "Subject": "English",        "Hours": 4},
    {"Class": "Class D", "Subject": "Chemistry",      "Hours": 3},
    {"Class": "Class D", "Subject": "Geography",      "Hours": 2},
    {"Class": "Class D", "Subject": "Art",            "Hours": 3},
    {"Class": "Class D", "Subject": "Music",          "Hours": 2},
    {"Class": "Class D", "Subject": "Physical Ed",    "Hours": 2},
]

df = pd.DataFrame(data)

out_path = os.path.join(os.path.dirname(__file__), "sample_timetable.xlsx")

with pd.ExcelWriter(out_path, engine="openpyxl") as writer:
    df.to_excel(writer, index=False, sheet_name="Timetable Data")

    # Auto-size columns
    ws = writer.sheets["Timetable Data"]
    for col in ws.columns:
        max_len = max(len(str(cell.value or "")) for cell in col) + 4
        ws.column_dimensions[col[0].column_letter].width = max_len

print(f"✅  Sample file written to: {out_path}")
print(df.to_string(index=False))
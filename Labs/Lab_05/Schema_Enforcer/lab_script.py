# lab_script.py — Part 1 / Task 1
# Create tabular CSV with intentional type inconsistencies.

import csv
import json
import pandas as pd

rows = [
    {"student_id": 1001,   "major": "Computer Science", "GPA": 3,    "is_cs_major": "Yes", "credits_taken": "15.0"},
    {"student_id": 1002,   "major": "Economics",        "GPA": 2.9,  "is_cs_major": "No",  "credits_taken": "12"},
    {"student_id": "1003", "major": "Statistics",       "GPA": 4,    "is_cs_major": "No",  "credits_taken": "18.5"},
    {"student_id": 1004,   "major": "Data Science",     "GPA": 3.75, "is_cs_major": "Yes", "credits_taken": "10.0"},
    {"student_id": 1005,   "major": "Mathematics",      "GPA": 3,    "is_cs_major": "No",  "credits_taken": "9.5"},
]

with open("raw_survey_data.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["student_id", "major", "GPA", "is_cs_major", "credits_taken"])
    writer.writeheader()
    writer.writerows(rows)


course_catalog = [
    {
        "course_id": "DS2002",
        "section": "001",
        "title": "Data Science Systems",
        "level": 200,
        "instructors": [
            {"name": "Austin Rivera", "role": "Primary"},
            {"name": "Heywood Williams-Tracy", "role": "TA"},
        ],
    },
    {
        "course_id": "CS3130",
        "section": "001",
        "title": "Computer Systems and Organization 2",
        "level": 300,
        "instructors": [
            {"name": "Charles Reiss", "role": "Primary"},
        ],
    },
]

with open("raw_course_catalog.json", "w", encoding="utf-8") as f:
    json.dump(course_catalog, f, indent=2)


df = pd.read_csv("raw_survey_data.csv", dtype=str)  # read as strings to control casting

bool_map = {"Yes": True, "No": False, "yes": True, "no": False}
df["is_cs_major"] = df["is_cs_major"].map(bool_map)

df["GPA"] = pd.to_numeric(df["GPA"], errors="coerce").astype("float64")
df["credits_taken"] = pd.to_numeric(df["credits_taken"], errors="coerce").astype("float64")

df["student_id"] = pd.to_numeric(df["student_id"], errors="coerce").astype("Int64")

df.to_csv("clean_survey_data.csv", index=False)


with open("raw_course_catalog.json", "r", encoding="utf-8") as f:
    data = json.load(f)

norm = pd.json_normalize(
    data,
    record_path=["instructors"],
    meta=["course_id", "title", "level", "section"],
    errors="ignore",
)

norm = norm.rename(columns={"name": "instructor_name", "role": "instructor_role"})
norm.to_csv("clean_course_catalog.csv", index=False)
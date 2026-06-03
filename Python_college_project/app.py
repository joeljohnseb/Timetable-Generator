from flask import Flask, render_template, request, jsonify
import pandas as pd
import random

app = Flask(__name__)

DAYS           = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
PERIODS        = list(range(1, 7))   # Periods 1-6  (9 AM-12 PM, 1 PM-4 PM)
LUNCH_AFTER    = 3                   # Lunch shown after period 3


# -- Scheduling ----------------------------------------------------------------

def generate_timetables(class_data: dict, max_attempts: int = 800):
    """
    class_data : { class_name: { subject: hours, ... }, ... }
    Returns    : (schedule_dict, error_string | None)
    schedule   : { class_name: { day: { period: subject | "Free" } } }

    Conflict rule: the same subject cannot appear in the same (day, period)
    slot across different classes.
    """
    total_slots = len(DAYS) * len(PERIODS)

    for cls, subjects in class_data.items():
        total = sum(int(h) for h in subjects.values())
        if total > total_slots:
            return None, (
                f"Class '{cls}' needs {total} hours but only "
                f"{total_slots} slots are available per week."
            )

    for _ in range(max_attempts):
        # used[day][period] = set of subjects already placed there globally
        used = {d: {p: set() for p in PERIODS} for d in DAYS}
        schedule = {}
        success = True

        for cls, subjects_dict in class_data.items():
            # Expand: ["Math","Math","Math","English","English", ...]
            subject_list = []
            for subj, hrs in subjects_dict.items():
                subject_list.extend([subj.strip()] * int(hrs))
            random.shuffle(subject_list)

            slots = [(d, p) for d in DAYS for p in PERIODS]
            random.shuffle(slots)

            cls_sched = {d: {p: "Free" for p in PERIODS} for d in DAYS}
            placed = 0

            for day, period in slots:
                if placed >= len(subject_list):
                    break
                # Find a remaining subject with no conflict at this slot
                for i in range(placed, len(subject_list)):
                    if subject_list[i] not in used[day][period]:
                        subject_list[placed], subject_list[i] = subject_list[i], subject_list[placed]
                        cls_sched[day][period] = subject_list[placed]
                        used[day][period].add(subject_list[placed])
                        placed += 1
                        break

            if placed < len(subject_list):
                success = False
                break

            schedule[cls] = cls_sched

        if success:
            return schedule, None

    return None, (
        "Could not build a conflict-free timetable after many attempts. "
        "Try reducing total hours or using more distinct subject names."
    )


# -- File parsing --------------------------------------------------------------

def parse_file(file_storage):
    """
    Reads CSV or Excel upload.
    Required columns (case-insensitive): Class, Subject, Hours
    Returns (class_data dict, error string | None)
    """
    name = file_storage.filename.lower()
    try:
        if name.endswith(".csv"):
            df = pd.read_csv(file_storage)
        elif name.endswith((".xlsx", ".xls")):
            df = pd.read_excel(file_storage)
        else:
            return None, "Unsupported file type. Please upload .csv or .xlsx."
    except Exception as e:
        return None, f"Could not read file: {e}"

    df.columns = [c.strip().lower() for c in df.columns]
    missing = {"class", "subject", "hours"} - set(df.columns)
    if missing:
        return None, f"Missing column(s): {', '.join(missing)}. File must have: Class, Subject, Hours."

    df = df.dropna(subset=["class", "subject", "hours"])

    class_data = {}
    for _, row in df.iterrows():
        cls  = str(row["class"]).strip()
        subj = str(row["subject"]).strip()
        try:
            hrs = int(float(row["hours"]))
        except ValueError:
            return None, f"Invalid hours '{row['hours']}' for {cls} / {subj}."
        if hrs > 0:
            class_data.setdefault(cls, {})[subj] = hrs

    if not class_data:
        return None, "No valid data found in the file."

    return class_data, None


# -- Routes --------------------------------------------------------------------

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/preview", methods=["POST"])
def preview():
    """Return the list of classes found in the uploaded file."""
    if "file" not in request.files or request.files["file"].filename == "":
        return jsonify({"error": "No file uploaded."}), 400

    class_data, err = parse_file(request.files["file"])
    if err:
        return jsonify({"error": err}), 400

    summary = {
        cls: {
            "subjects":    list(subjs.keys()),
            "total_hours": sum(subjs.values()),
        }
        for cls, subjs in class_data.items()
    }
    return jsonify({"classes": summary})


@app.route("/generate", methods=["POST"])
def generate():
    """Generate conflict-free timetables for selected classes."""
    if "file" not in request.files or request.files["file"].filename == "":
        return jsonify({"error": "No file uploaded."}), 400

    class_data, err = parse_file(request.files["file"])
    if err:
        return jsonify({"error": err}), 400

    selected = request.form.getlist("classes")
    if selected:
        class_data = {k: v for k, v in class_data.items() if k in selected}
        if not class_data:
            return jsonify({"error": "None of the selected classes were found in the file."}), 400

    schedule, err = generate_timetables(class_data)
    if err:
        return jsonify({"error": err}), 400

    return jsonify({
        "schedule":    schedule,
        "days":        DAYS,
        "periods":     PERIODS,
        "lunch_after": LUNCH_AFTER,
        "classes":     list(schedule.keys()),
    })


if __name__ == "__main__":
    app.run(debug=True)
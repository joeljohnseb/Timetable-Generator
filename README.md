# 📚 Timetable Generator

A simple and efficient Flask-based web application that automatically generates conflict-free class timetables from CSV or Excel files.

This project helps schools, colleges, and educators quickly create weekly schedules while avoiding subject clashes across multiple classes.

---

## 🚀 Features

* Upload timetable data using **CSV** or **Excel (.xlsx)** files
* Automatically generates **conflict-free schedules**
* Prevents the same subject from appearing in the same time slot across classes
* Interactive web interface using Flask
* Preview uploaded classes before generating timetables
* Supports multiple classes and subjects
* Displays lunch break automatically
* Fast and lightweight

---

## 🛠️ Tech Stack

* **Backend:** Python, Flask
* **Frontend:** HTML, CSS, JavaScript
* **Data Handling:** Pandas
* **File Support:** CSV, Excel

---

## 📂 Project Structure

```bash
Timetable-Generator/
│
├── app.py                  # Main Flask application
├── create_sample.py        # Script to generate sample data
│
├── templates/
│   ├── index.html          # Main UI page
│   └── random.html         # Additional page/template
│
└── README.md
```

---

## ⚙️ Installation

### 1. Clone the Repository

```bash
git clone https://github.com/joeljohnseb/Timetable-Generator.git
cd Timetable-Generator
```

### 2. Create a Virtual Environment (Optional but Recommended)

```bash
python -m venv venv
```

Activate the environment:

#### Windows

```bash
venv\Scripts\activate
```

#### macOS/Linux

```bash
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install flask pandas openpyxl
```

---

## ▶️ Running the Application

Start the Flask server:

```bash
python app.py
```

The app will run on:

```bash
http://127.0.0.1:5000/
```

Open the link in your browser.

---

## 📄 Input File Format

The uploaded CSV or Excel file must contain the following columns:

| Class | Subject   | Hours |
| ----- | --------- | ----- |
| CSE-A | Math      | 4     |
| CSE-A | Physics   | 3     |
| CSE-B | Chemistry | 5     |

### Required Columns

* `Class`
* `Subject`
* `Hours`

Column names are case-insensitive.

---

## 🧠 How the Scheduling Works

The timetable generator:

1. Reads class and subject data
2. Randomly distributes subjects across available slots
3. Ensures:

   * No timetable overflow
   * No duplicate subject conflicts in the same slot across classes
4. Generates a valid weekly schedule

---

## 📅 Timetable Configuration

Default settings in `app.py`:

```python
DAYS = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
PERIODS = list(range(1, 7))
LUNCH_AFTER = 3
```

* 5 working days
* 6 periods per day
* Lunch break after period 3

You can modify these values easily.

---

## 📸 Screenshots

Add screenshots of:

* Upload page
* Preview page
* Generated timetable

Example:

```md
![Home Page](screenshots/home.png)
```

---

## ❌ Error Handling

The application checks for:

* Invalid file formats
* Missing columns
* Incorrect hour values
* Impossible timetable generation scenarios

---

## 🔮 Future Improvements

* Teacher allocation support
* Export timetable as PDF
* Authentication system
* Drag-and-drop timetable editor
* Database integration
* Better UI/UX design
* Subject priority management

---

## 🤝 Contributing

Contributions are welcome.

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to your branch
5. Open a Pull Request


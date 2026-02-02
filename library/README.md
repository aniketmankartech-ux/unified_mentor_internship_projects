# 📚 Unified Library Management System (Python Tkinter)

A complete **GUI-based Library Management System** built using **Python & Tkinter**, designed to simulate a **real-life digital library** with book management, issue/return tracking, fine calculation, and secure record storage.

---

## ✨ Key Features

### 🔐 Secure Access
- Librarian-controlled system
- Safe data handling using JSON
- Error-free operations with validations

---

### 📖 Book Management
- Add new books
- Update book details
- Delete books
- Search books by:
  - Book ID
  - Title
  - Author
- Real-time availability status

---

### 👤 Member Management
- Register library members
- Auto-generated member IDs
- Duplicate member prevention
- Persistent data storage

---

### 🔄 Book Issue & Return
- Issue books to members
- Prevent issuing unavailable books
- Return books with automatic status update
- Issue date & return date tracking

---

### 💰 Fine Calculation
- Automatic fine calculation on late returns
- Configurable fine rate
- Error-safe time calculations

---

### 🧾 Records & Logs
- Issue/return history tracking
- Stored permanently using JSON
- Safe database auto-repair on corruption

---

### 🛡️ Validation & Error Handling
- Empty input protection
- Duplicate ID prevention
- Invalid operations blocked
- Crash-free JSON handling

---

## 🛠️ Technologies Used

- **Python 3**
- **Tkinter** (GUI)
- **JSON** (Database)
- **Datetime** (Date handling)
- **File Handling**

---

## 📁 Project Structure

Unified-Library-System/
│
├── app.py
├── library_db.json
│
├── output/
│   ├── app.exe
│   └── library_db.json
│
└── README.md

---

## ▶️ How to Run the Project

### 🔹 Option 1: Run Using Python
```bash
python app.py

###🔹 Option 2: Run Directly (Recommended)

Go to the output/ folder

You will find:

app.exe

library_db.json

Double-click app.exe

No Python installation required ✅

📌 Notes

All library data is stored locally using JSON

Database auto-initializes if missing

Designed for academic & internship use

Clean, simple, and user-friendly UI

📸 UI Highlights

Modern Tkinter layout

Form-based data entry

Table-style book listing

Responsive window design

Consistent color theme

🧪 Input Validation & Safety

Required field checks

Duplicate book/member prevention

Safe issue/return logic

Auto database recovery

👨‍💻 Developed By

Aniket Mankar
Intern ID: UMID21102567330
Domain: Python Development Intern
Unified Mentor Internship – 2026
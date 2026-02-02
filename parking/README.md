# 🚗 Unified Parking Management System (Python Tkinter)

A complete **GUI-based Parking Management System** built using **Python & Tkinter**, designed to simulate a **real-life smart parking facility** with slot categorization, live validation, automated billing, staff control, and report generation.

---

## ✨ Key Features

### 🔐 Secure Login System
- Role-based access:
  - **Admin**
  - **Staff**
- PIN-based authentication
- Login hint note for demo usage

---

### 🅿️ Smart Parking Slot Management
- Total **30 parking slots**
- Slot categories:
  - **Regular**
  - **Priority**
  - **Emergency**
- Real-time slot availability dashboard
- Automatic slot allocation
- Emergency vehicle alert sound
- Parking-full blinking warning

---

### 🚘 Vehicle Entry System
- **Live input validation**
- Auto-uppercase vehicle number
- Regex-based vehicle number format check  
  _(Example: MH12AB1234)_
- Duplicate vehicle detection
- Color feedback:
  - 🟢 Green → valid
  - 🔴 Red → invalid

---

### 💳 Vehicle Exit & Billing
- Automatic time calculation
- Dynamic pricing based on:
  - Vehicle type (Bike / Car / SUV)
  - Parking category
- Minimum 1-hour billing
- Instant payment processing

---

### 🧾 Receipt Management
- Auto-generated parking receipts
- Stored inside **`receipts/`** folder
- Includes:
  - Vehicle number
  - Duration
  - Amount paid
  - Date & time

---

### 📊 Revenue & Reports
- Total vehicles count
- Total revenue tracking
- Export parking history as **CSV**
- Reports stored in **`reports/`** folder

---

### 👥 Staff Management (Admin Only)
- Add new staff accounts
- Role assignment
- View all users
- Persistent storage using JSON

---

## 🛠️ Technologies Used

- **Python 3**
- **Tkinter** (GUI)
- **JSON** (Database)
- **CSV** (Reports)
- **Regex** (Input validation)
- **winsound** (Emergency alert)

---

## 📁 Project Structure

Unified-Parking-System/
│
├── app.py
├── unified_db.json
│
├── receipts/
│ └── *.txt
│
├── reports/
│ └── *.csv
│
├── output/
│ ├── app.exe
│ └── unified_db.json
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

unified_db.json

Double-click app.exe

No Python installation required ✅



### 3️⃣ Run the Application
```bash
python app.py

🔑 Demo Login Credentials
Role	Username	PIN
Admin	admin	1234
Staff	staff	1111

📌 Notes

All data is stored locally using JSON

Receipts & reports are auto-created if folders don’t exist

Admin has full control over staff accounts

UI designed to be clean, modern, and user-friendly

📸 UI Highlights

Modern enterprise-style layout

Sidebar navigation

Card-based dashboards

TreeView tables

Consistent color theme

Scalable window layout
🧪 Input Validation & Error Handling

Invalid login protection

Duplicate ID prevention

Stock availability checks

Fine auto-calculation

Admin protection for critical actions

Safe database writes

🧑‍💻 Developed By

Aniket Mankar
Intern ID: UMID21102567330
Domain: Python Development Intern
Unified Mentor Internship – 2026
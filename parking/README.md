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
```
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
```
🔑 Demo Login Credentials
Role	Username	PIN
Admin	admin	1234
Staff	staff	1111

📸 UI Highlights
<img width="1919" height="1015" alt="image" src="https://github.com/user-attachments/assets/816e66d1-b1a7-4838-a9c4-38de5bc90cd9" />
<img width="1919" height="1018" alt="image" src="https://github.com/user-attachments/assets/205d7672-7371-4255-90b7-df5a109737b1" />
Wrong Vehicle Number Rejected
<img width="1919" height="1016" alt="image" src="https://github.com/user-attachments/assets/5dec376f-d467-475b-b218-007b1a3042db" />
Right Number Accepted
<img width="1919" height="1019" alt="image" src="https://github.com/user-attachments/assets/36995195-99c2-489d-81cb-c84154cac232" />
<img width="1919" height="1023" alt="image" src="https://github.com/user-attachments/assets/3d9eeb73-7cea-4760-99e7-a17cd53ab209" />
<img width="1919" height="1024" alt="image" src="https://github.com/user-attachments/assets/08c61049-e35c-4b69-b267-2b97dbbff037" />
<img width="1918" height="1015" alt="image" src="https://github.com/user-attachments/assets/86093c8d-30e9-4f65-9fe7-1020c4a3f969" />
multiple user login handled by manager
<img width="1919" height="1019" alt="image" src="https://github.com/user-attachments/assets/aa82e6e9-1f5f-4b18-808b-44a557549213" />
<img width="1919" height="1016" alt="image" src="https://github.com/user-attachments/assets/a90401ec-063d-46c4-ab0f-a443ae65cd3d" />
generated receipt
<img width="1919" height="1003" alt="image" src="https://github.com/user-attachments/assets/9c97d877-a9a7-4f8d-9d59-adf2d1cbd0a1" />
<img width="1919" height="965" alt="image" src="https://github.com/user-attachments/assets/a98282b3-291e-4932-94a2-62d43d516f2b" />
CSV report
<img width="1914" height="1000" alt="image" src="https://github.com/user-attachments/assets/e8bb8646-a3f3-43be-af06-823394999f32" />


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

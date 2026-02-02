# 🏦 Unified Global Banking – ATM Management System

A **feature-rich Desktop ATM Simulation Application** built using **Python & Tkinter**, designed to replicate real-world banking operations with **secure authentication**, **user/admin roles**, **transaction handling**, and **PDF mini-statement generation**.

This project was developed as part of the **Unified Mentor Internship – 2026**.

---

## 🚀 Features Overview

### 👤 User Features
- Secure login using **Account Number & PIN (hashed)**
- View real-time **account balance**
- **Withdraw money** with daily limit enforcement
- **Deposit funds**
- **Fund transfer** between accounts
- **Transaction history** with color-coded records
- **Change PIN** with validation
- **Export Mini Statement (PDF)** using ReportLab
- Daily withdrawal reset (date-based)

### 🛡️ Admin Features
- Admin login with special credentials
- Create new customer accounts
- Edit existing user details (name, balance, PIN)
- Delete user accounts
- View all customer accounts in tabular format
- Full data persistence using JSON storage

---

## 🧠 Real-World Banking Logic Implemented
- SHA-256 PIN hashing for security
- Daily withdrawal limit enforcement
- Insufficient balance protection
- Invalid input handling & error messages
- Persistent transaction logs
- Admin/user role separation

---

## 🖥️ Tech Stack Used

| Technology | Purpose |
|----------|--------|
| Python 3.11 | Core programming |
| Tkinter | GUI development |
| ttk | Modern widgets |
| JSON | Local database |
| hashlib | PIN encryption |
| ReportLab | PDF mini-statement export |
| datetime | Time & date tracking |

---

## 📂 Project Structure

Unified-Bank-ATM/
│
├── app.py                  # Main application file
├── bank_data.json          # Data storage (accounts & transactions)
├── requirements.txt        # Project dependencies
├── README.md               # Project documentation
│
└── (PDF files generated)
    └── MiniStatement_*.pdf

---

## 🔐 Default Login Credentials

### Admin
- **Account Number:** `admin`
- **PIN:** `9999`

### Sample User
- **Account Number:** `1001`
- **PIN:** `1234`

> ⚠️ PINs are stored securely using SHA-256 hashing.

---

## 📄 Mini Statement (PDF)
- Exports last **20 transactions**
- Automatically timestamped
- Generated in project directory
- Uses **ReportLab**

---

## ⚙️ Installation & Setup

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/your-username/your-repo-name.git
cd Unified-Bank-ATM
```

### 2️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```
### 3️⃣ Run the Application
```bash
python app.py
```
## 📦 requirements.txt
reportlab

📸 UI Highlights
<img width="1919" height="1029" alt="image" src="https://github.com/user-attachments/assets/3d25b8ea-bab9-4159-9340-2262beb55ae5" />
<img width="1919" height="1023" alt="image" src="https://github.com/user-attachments/assets/a7a8d807-4e7c-444c-a198-ca3374ecbaa4" />
<img width="1919" height="1020" alt="image" src="https://github.com/user-attachments/assets/fdbacbff-e0b9-4902-a89e-361dc3358105" />


Modern dark-themed interface

Clean layout with clear actions

Responsive buttons & status messages

Admin panel with table view

🧪 Input Validation & Error Handling

Numeric & positive amount validation

PIN length and digit checks

Account existence verification

Daily withdrawal reset protection

Friendly error/status notifications

🧑‍💻 Developed By

Aniket Mankar
Intern ID: UMID21102567330
Domain: Python Development Intern
Unified Mentor Internship – 2026

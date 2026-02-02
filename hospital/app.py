import tkinter as tk
from tkinter import ttk, messagebox
import json
import hashlib
import os
from datetime import datetime
import winsound  # for emergency sound alert
import tempfile
import os

#config=========================


DATA_FILE = "hospital_enterprise.json"
COLORS = {"bg": "#f8fafc", "sidebar": "#0f172a", "accent": "#3b82f6", "text": "#f8fafc", "danger": "#ef4444"}

def hash_val(val):
    """Encrypts passwords using SHA-256 for professional security standards."""
    return hashlib.sha256(val.encode()).hexdigest()



def init_db():
    """Initializes the JSON database with default roles if it doesn't exist."""
    if not os.path.exists(DATA_FILE):
        data = {
            "staff": {
                "admin": {"pin": hash_val("9999"), "role": "admin", "name": "Head Admin"},
                "rec01": {"pin": hash_val("1234"), "role": "receptionist", "name": "Sarah Jones"}
            },
            "doctors": {
                "Dr. Khanna": {"dept": "Cardiology", "done": 0, "q": []}
            },
            "appointments": [],
            "stats": {"total": 0}
        }
        with open(DATA_FILE, 'w') as f: json.dump(data, f, indent=4)
        return data
    with open(DATA_FILE, 'r') as f: return json.load(f)

# main class===============


class HospitalEnterprise:

    def __init__(self, root):
        self.root = root
        self.root.title("Unified Health Enterprise v4.0")
        self.root.geometry("1700x750+0+0")
        self.db = init_db()
        self.current_user = None
        self.login_screen()




    def save(self):
        with open(DATA_FILE, 'w') as f: json.dump(self.db, f, indent=4)

    def clear_all(self):
        for widget in self.root.winfo_children(): widget.destroy()

    def show_status(self, msg, color="green"):
        lbl = tk.Label(self.container, text=msg, fg=color, bg=COLORS["bg"], font=("Arial", 10, "bold"))
        lbl.pack(pady=5)
        self.root.after(3000, lbl.destroy)

    # authentication
    def login_screen(self):
        self.clear_all()
        self.root.configure(bg="#1e293b")
        frame = tk.Frame(self.root, bg="white", padx=50, pady=50, relief="flat")
        frame.place(relx=0.5, rely=0.5, anchor="center")




        tk.Label(frame, text="HOSPITAL MANAGEMENT", font=("Arial", 16, "bold"), bg="white").pack(pady=10)
        
        tk.Label(frame, text="User ID", bg="white").pack(anchor="w")
        uid_ent = ttk.Combobox(frame, values=list(self.db["staff"].keys()), font=("Arial", 12), width=25)
        uid_ent.pack(pady=5)
        
        tk.Label(frame, text="Password", bg="white").pack(anchor="w")
        pin_ent = tk.Entry(frame, font=("Arial", 12), show="*", width=25)
        pin_ent.pack(pady=5)

        def attempt_login():
            uid, pin = uid_ent.get(), pin_ent.get()
            if uid in self.db["staff"] and self.db["staff"][uid]["pin"] == hash_val(pin):
                self.current_user = self.db["staff"][uid]
                self.current_user['id'] = uid
                self.main_dashboard()
            else:
                messagebox.showerror("Error", "Invalid Credentials")

        tk.Button(frame, text="LOGIN", bg=COLORS["accent"], fg="white", width=25, pady=10, command=attempt_login).pack(pady=20)

    # dashboard
    def main_dashboard(self):
        self.clear_all()
        self.root.configure(bg=COLORS["bg"])
        
        sidebar = tk.Frame(self.root, bg=COLORS["sidebar"], width=240)
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)

        tk.Label(sidebar, text="Unified HEALTH", fg=COLORS["accent"], bg=COLORS["sidebar"], font=("Arial", 16, "bold")).pack(pady=30)
        
        menu = []
        if self.current_user["role"] == "admin":
            menu = [("👨‍⚕️ Manage Doctors", self.manage_docs), 
                    ("👥 Manage Staff", self.manage_staff),
                    ("🔐 Change PIN", self.change_pin)]
            
        else:
            menu = [("📝 Patient Registration", self.patient_reg), 
                    ("🏥 Live Queues", self.live_queues), 
                    ("👨‍⚕️ Consultation", self.consultation_desk),
                    ("🖨 Print Token Slip", self.print_token_slip),
                    ("🔐 Change PIN", self.change_pin),
                    ("📊 Daily OPD Report", self.daily_report)]

        for text, cmd in menu:
            tk.Button(sidebar, text=text, bg=COLORS["sidebar"], fg="white", relief="flat", anchor="w", padx=20, pady=12, command=cmd).pack(fill="x")

        tk.Button(sidebar, text="Logout", bg=COLORS["danger"], fg="white", command=self.login_screen).pack(side="bottom", fill="x", pady=20)

        self.container = tk.Frame(self.root, bg=COLORS["bg"], padx=40, pady=40)
        
        
        self.container.pack(side="right", expand=True, fill="both")
        self.home_view()

    def home_view(self):
        for w in self.container.winfo_children(): w.destroy()
        tk.Label(self.container, text=f"Welcome, {self.current_user['name']}", font=("Arial", 22, "bold"), bg=COLORS["bg"]).pack(anchor="w")
        tk.Label(self.container, text=f"Role: {self.current_user['role'].upper()}", fg="gray", bg=COLORS["bg"]).pack(anchor="w")

    def manage_docs(self):
        for w in self.container.winfo_children(): w.destroy()
        tk.Label(self.container, text="Manage Doctors", font=("Arial", 18, "bold"), bg=COLORS["bg"]).pack(anchor="w")

        form = tk.Frame(self.container, bg="white", padx=20, pady=20)
        form.pack(fill="x", pady=20)

        tk.Label(form, text="Name:", bg="white").grid(row=0, column=0)
        d_name = tk.Entry(form); d_name.grid(row=0, column=1, padx=10)
        tk.Label(form, text="Dept:", bg="white").grid(row=0, column=2)
        d_dept = tk.Entry(form); d_dept.grid(row=0, column=3, padx=10)

        def add_doc():
            if d_name.get() and d_dept.get():
                self.db["doctors"][d_name.get()] = {"dept": d_dept.get(), "done": 0, "q": []}
                self.save(); self.manage_docs(); self.show_status("Doctor Added")
            else: messagebox.showwarning("Input", "Field empty")

        tk.Button(form, text="Add Doctor", bg="#22c55e", fg="white", command=add_doc).grid(row=0, column=4, padx=10)

        tree = ttk.Treeview(self.container, columns=("Name", "Dept", "Served"), show="headings")
        for col in ("Name", "Dept", "Served"): tree.heading(col, text=col)
        for n, d in self.db["doctors"].items(): tree.insert("", "end", values=(n, d['dept'], d['done']))
        tree.pack(fill="both", expand=True)

        def delete_doc():
            selected = tree.selection()
            if selected:
                item = tree.item(selected)["values"][0]
                del self.db["doctors"][item]
                self.save(); self.manage_docs(); self.show_status("Doctor Removed", "red")
        
        tk.Button(self.container, text="Remove Selected Doctor", bg=COLORS["danger"], fg="white", pady=10, command=delete_doc).pack(pady=10)

    # staff manager
    def manage_staff(self):
        for w in self.container.winfo_children(): w.destroy()
        tk.Label(self.container, text="Staff Management", font=("Arial", 18, "bold"), bg=COLORS["bg"]).pack(anchor="w")

        form = tk.Frame(self.container, bg="white", padx=20, pady=20)
        form.pack(fill="x", pady=20)

        tk.Label(form, text="User ID:", bg="white").grid(row=0, column=0)
        u_id = tk.Entry(form); u_id.grid(row=0, column=1, padx=5)
        tk.Label(form, text="Name:", bg="white").grid(row=0, column=2)
        u_name = tk.Entry(form); u_name.grid(row=0, column=3, padx=5)
        tk.Label(form, text="PIN:", bg="white").grid(row=1, column=0, pady=10)
        u_pin = tk.Entry(form, show="*"); u_pin.grid(row=1, column=1)
        tk.Label(form, text="Role:", bg="white").grid(row=1, column=2)
        u_role = ttk.Combobox(form, values=["admin", "receptionist"]); u_role.grid(row=1, column=3)

        def add_staff():
            uid = u_id.get().strip()
            name = u_name.get().strip()
            pin = u_pin.get().strip()
            role = u_role.get()

            if not uid or not name or not pin or role not in ["admin", "receptionist"]:
                messagebox.showwarning("Input Error", "Fill all fields correctly"); return
            if uid in self.db["staff"]:
                messagebox.showwarning("Duplicate ID", "Staff ID already exists"); return

            self.db["staff"][uid] = {"name": name, "pin": hash_val(pin), "role": role}
            self.save(); self.manage_staff(); self.show_status(f"Staff {name} created")

        tk.Button(form, text="Add Staff Member", bg=COLORS["accent"], fg="white", command=add_staff).grid(row=1, column=4, padx=10)

        tree = ttk.Treeview(self.container, columns=("ID", "Name", "Role"), show="headings")
        for col in ("ID", "Name", "Role"): tree.heading(col, text=col)
        for sid, details in self.db["staff"].items(): tree.insert("", "end", values=(sid, details['name'], details['role']))
        tree.pack(fill="both", expand=True)

        def delete_staff():
            sel = tree.selection()
            if sel:
                sid = tree.item(sel)["values"][0]
                if sid == "admin": return messagebox.showerror("Error", "Cannot delete Root Admin")
                del self.db["staff"][sid]; self.save(); self.manage_staff(); self.show_status("Staff Deleted", "red")

        tk.Button(self.container, text="Delete Selected Staff", bg=COLORS["danger"], fg="white", pady=10, command=delete_staff).pack(pady=10)


 #patient registratin======================================


    def patient_reg(self):
        for w in self.container.winfo_children(): w.destroy()
        tk.Label(self.container, text="Admission Desk", font=("Arial", 18, "bold"), bg=COLORS["bg"]).pack(anchor="w")
    
        f = tk.Frame(self.container, bg="white", padx=20, pady=20)
        f.pack(fill="x", pady=20)

        labels = ["Patient Name", "Age", "Phone", "Assign Doctor", "Priority"]
        ents = {}
        for i, l in enumerate(labels):
            tk.Label(f, text=l, bg="white").grid(row=i, column=0, sticky="w", pady=5)
            if l == "Assign Doctor":
                e = ttk.Combobox(f, values=list(self.db["doctors"].keys()))
            elif l == "Priority":
                e = ttk.Combobox(f, values=["Normal", "Emergency"])
            else:
                e = tk.Entry(f, width=40)
            e.grid(row=i, column=1, pady=5, padx=10)
            ents[l] = e

        def submit():
            name = ents["Patient Name"].get().strip()
            age = ents["Age"].get().strip()
            phone = ents["Phone"].get().strip()
            doc = ents["Assign Doctor"].get()
            priority = ents["Priority"].get()

            # --- VALIDATIONS ---
            if not name:
                messagebox.showwarning("Input Error", "Enter patient name"); return
            if not age.isdigit() or int(age)<=0:
                messagebox.showwarning("Input Error", "Enter valid age"); return
            if not phone.isdigit() or len(phone)!=10:
                messagebox.showwarning("Input Error", "Enter valid 10-digit phone number"); return
            if doc not in self.db["doctors"]:
                messagebox.showwarning("Input Error", "Select a valid doctor"); return
            if priority not in ["Normal", "Emergency"]:
                messagebox.showwarning("Input Error", "Select a priority"); return

            patient = {
                "name": name,
                "age": int(age),
                "phone": phone,
                "priority": priority,
                "time": datetime.now().strftime("%H:%M")
            }

            # Add patient to queue
            if priority == "Emergency":
                self.db["doctors"][doc]["q"].insert(0, patient)
                winsound.Beep(1000, 500)
            else:
                self.db["doctors"][doc]["q"].append(patient)

            self.save(); self.home_view()
            messagebox.showinfo("Queue Updated", f"{name} added to {doc}'s queue")

        tk.Button(self.container, text="Confirm Admission", bg=COLORS["accent"], fg="white", pady=12, width=30, command=submit).pack(pady=10)


    # queue logic
    def live_queues(self):
        for w in self.container.winfo_children(): w.destroy()
        tk.Label(self.container, text="Live Doctor Queues", font=("Arial", 18, "bold"), bg=COLORS["bg"]).pack(anchor="w", pady=5)

        for doc, info in self.db["doctors"].items():
            card = tk.Frame(self.container, bg="white", pady=15, padx=20, relief="groove", bd=1)
            card.pack(fill="x", pady=5)

            tk.Label(card, text=f"{doc} ({info['dept']})", font=("Arial", 11, "bold"), bg="white").pack(side="left")
            tk.Label(card, text=f"Waiting: {len(info['q'])}", fg=COLORS["accent"], bg="white", font=("Arial", 10, "bold")).pack(side="right")

            # Show first 3 patients with emergency highlight
            for p in info["q"][:3]:
                color = "red" if p.get("priority") == "Emergency" else "green"
                tk.Label(card, text=f"  {p['name']} ({p['priority']})", bg="white", fg=color).pack(anchor="w", padx=20)

    def consultation_desk(self):
        for w in self.container.winfo_children(): w.destroy()
        tk.Label(self.container, text="Consultation Management", font=("Arial", 18, "bold"), bg=COLORS["bg"]).pack(pady=10)
        for doc in self.db["doctors"]:
            f = tk.Frame(self.container, bg="white", pady=10, padx=20)
            f.pack(fill="x", pady=2)
            tk.Label(f, text=f"Doctor: {doc}", bg="white", font=("Arial", 10, "bold")).pack(side="left")
            p_name = self.db["doctors"][doc]["q"][0]["name"] if self.db["doctors"][doc]["q"] else "Vacant"
            tk.Label(f, text=f" | Current Patient: {p_name}", bg="white", fg="green").pack(side="left")
            
            def done(d=doc):
                if self.db["doctors"][d]["q"]:
                    self.db["doctors"][d]["q"].pop(0); self.db["doctors"][d]["done"] += 1
                    self.save(); self.consultation_desk()

            tk.Button(f, text="Mark Served", command=done, bg="#22c55e", fg="white").pack(side="right")

    # new featueers
    def change_pin(self):
        for w in self.container.winfo_children(): w.destroy()
        tk.Label(self.container, text="Change PIN", font=("Arial", 18, "bold"), bg=COLORS["bg"]).pack(pady=10)
        f = tk.Frame(self.container, bg="white", padx=20, pady=20); f.pack(fill="x", pady=20)

        tk.Label(f, text="New PIN:", bg="white").grid(row=0, column=0, pady=5)
        new_pin = tk.Entry(f, show="*"); new_pin.grid(row=0, column=1, pady=5)

        def save_pin():
            val = new_pin.get()
            if val:
                self.current_user["pin"] = hash_val(val)
                self.db["staff"][self.current_user["id"]]["pin"] = hash_val(val)
                self.save(); messagebox.showinfo("Success", "PIN changed successfully")
            else: messagebox.showwarning("Input", "Enter a PIN")

        tk.Button(f, text="Update PIN", bg=COLORS["accent"], fg="white", command=save_pin).grid(row=1, column=0, columnspan=2, pady=10)

    def print_token_slip(self):
        for w in self.container.winfo_children(): w.destroy()
        tk.Label(self.container, text="Print OPD Token Slip", font=("Arial", 18, "bold"), bg=COLORS["bg"]).pack(pady=10)

        f = tk.Frame(self.container, bg="white", padx=20, pady=20); f.pack(fill="x", pady=20)
        tk.Label(f, text="Select Doctor:", bg="white").pack(anchor="w")
        doc_cb = ttk.Combobox(f, values=list(self.db["doctors"].keys())); doc_cb.pack(pady=5)

        def generate_slip():
            doc = doc_cb.get()
            if doc and self.db["doctors"][doc]["q"]:
                patient = self.db["doctors"][doc]["q"][0]["name"]
                token = f"{doc[:3].upper()}-{len(self.db['doctors'][doc]['q']) + 100}"
                # Save to temp file
                path = os.path.join(tempfile.gettempdir(), f"{token}.txt")
                with open(path, "w") as ftxt:
                    ftxt.write(f"Unified HEALTH\nDoctor: {doc}\nPatient: {patient}\nToken: {token}\nTime: {datetime.now().strftime('%H:%M')}")
                os.startfile(path, "print")
                messagebox.showinfo("Printed", f"Token printed for {patient}")
            else:
                messagebox.showwarning("Empty", "No patients in queue")

        tk.Button(f, text="Print Token", bg=COLORS["accent"], fg="white", command=generate_slip).pack(pady=10)

    def daily_report(self):
        for w in self.container.winfo_children(): w.destroy()
        tk.Label(self.container, text="Daily OPD Report", font=("Arial", 18, "bold"), bg=COLORS["bg"]).pack(pady=10)

        report_text = tk.Text(self.container, width=100, height=30)
        report_text.pack(pady=10)
        total = 0
        for doc, info in self.db["doctors"].items():
            report_text.insert("end", f"Doctor: {doc} ({info['dept']})\n")
            report_text.insert("end", f"  Served Today: {info['done']}\n")
            report_text.insert("end", f"  Waiting: {len(info['q'])}\n\n")
            total += info['done']
        report_text.insert("end", f"Total Patients Served Today: {total}\n")
        report_text.config(state="disabled")


if __name__ == "__main__":
    root = tk.Tk()
    style = ttk.Style(); style.theme_use('clam')
    app = HospitalEnterprise(root)
    root.mainloop()

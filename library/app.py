import tkinter as tk
from tkinter import ttk, messagebox
import json, os, hashlib, csv
from datetime import datetime, timedelta

# configuration==========================================
DATA_FILE = "library_enterprise.json"
FINE_PER_DAY = 10
COLORS = {
    "bg": "#f8fafc",
    "sidebar": "#1e293b",
    "accent": "#3b82f6",
    "danger": "#ef4444",
    "success": "#22c55e",
    "text_light": "#f1f5f9",
    "card": "#ffffff"
}

# data security part===============================
def hash_pin(pin):
    return hashlib.sha256(pin.encode()).hexdigest()

def init_db():
    if not os.path.exists(DATA_FILE):
        data = {
            "branches": ["Main Downtown", "North Campus", "West End"],
            "staff": {
                "admin": {
                    "name": "Chief Librarian", 
                    "pin": hash_pin("9999"), 
                    "role": "manager", 
                    "branch": "Main Downtown"
                }
            },
            "books": {},
            "members": {},
            "active_issues": [],
            "stats": {"total_fines": 0},
            "activity_log": []
        }
        with open(DATA_FILE, "w") as f:
            json.dump(data, f, indent=4)
    
    with open(DATA_FILE) as f:
        return json.load(f)

def save_db(db):
    with open(DATA_FILE, "w") as f:
        json.dump(db, f, indent=4)

# main class
class LibraryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Unified Library Enterprise v2.0")
        self.root.geometry("1400x850")
        self.db = init_db()
        self.user = None
        self.login_screen()

    def clear_screen(self):
        for w in self.root.winfo_children():
            w.destroy()

    # login system part=============================================
    def login_screen(self):
        self.clear_screen()
        self.root.configure(bg="#0f172a")
        
        card = tk.Frame(self.root, bg="white", padx=50, pady=50, relief="flat")
        card.place(relx=0.5, rely=0.5, anchor="center")
        
        tk.Label(card, text="UNIFIED ENTERPRISE LOGIN", font=("Helvetica", 18, "bold"), bg="white", fg=COLORS["sidebar"]).pack(pady=(0, 20))
        
        tk.Label(card, text="Staff ID (Try: admin)", bg="white").pack(anchor="w")
        uid_entry = ttk.Combobox(card, values=list(self.db["staff"].keys()), width=35)
        uid_entry.pack(pady=5)
        if uid_entry["values"]: uid_entry.current(0)
        
        tk.Label(card, text="Security PIN (Try: 9999 for admin and 1111 for staff01)", bg="white").pack(anchor="w")
        pin_entry = tk.Entry(card, width=37, show="*", font=("Arial", 12))
        pin_entry.pack(pady=5)

        def attempt_login():
            u, p = uid_entry.get(), pin_entry.get()
            if u in self.db["staff"] and self.db["staff"][u]["pin"] == hash_pin(p):
                self.user = self.db["staff"][u]
                self.main_dashboard()
            else:
                messagebox.showerror("Auth Error", "Invalid Staff ID or PIN")

        tk.Button(card, text="SECURE LOGIN", bg=COLORS["accent"], fg="white", 
                  font=("Arial", 10, "bold"), width=30, pady=10, command=attempt_login, relief="flat").pack(pady=20)

    # main layout============================================
    def main_dashboard(self):
        self.clear_screen()
        self.root.configure(bg=COLORS["bg"])

        sidebar = tk.Frame(self.root, bg=COLORS["sidebar"], width=260)
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)

        tk.Label(sidebar, text="Unified Librarian", fg=COLORS["accent"], bg=COLORS["sidebar"], font=("Arial", 14, "bold")).pack(pady=30)

        nav_items = [
            ("🏠 Home Dashboard", self.ui_home),
            ("📚 Book Inventory", self.ui_inventory),
            ("👤 Member Manager", self.ui_members),
            ("📑 Barcode Issue", self.ui_issue),
            ("↩️ Process Return", self.ui_return),
            ("🔍 Global Search", self.ui_search),
            ("📊 Data Reports", self.ui_reports)
        ]
        # add staff manager only for manager/admin=======================
        if self.user.get("role") == "manager":
            nav_items.append(("🧑‍💼 Staff Manager", self.ui_staff))
        for text, cmd in nav_items:
            tk.Button(sidebar, text=text, fg="white", bg=COLORS["sidebar"], relief="flat", 
                      anchor="w", padx=25, pady=12, font=("Arial", 10), command=cmd).pack(fill="x")

        tk.Button(sidebar, text="LOGOUT", bg=COLORS["danger"], fg="white", command=self.login_screen, relief="flat").pack(side="bottom", fill="x", pady=20)

        self.view_frame = tk.Frame(self.root, bg=COLORS["bg"], padx=40, pady=40)
        self.view_frame.pack(expand=True, fill="both")
        self.ui_home()

    # home view=========================================================
    def ui_home(self):
        for w in self.view_frame.winfo_children(): w.destroy()
        
        branch = self.user.get('branch', 'Main Downtown')
        tk.Label(self.view_frame, text=f"Dashboard: {branch}", font=("Arial", 22, "bold"), bg=COLORS["bg"]).pack(anchor="w")
        tk.Label(self.view_frame, text=f"Librarian: {self.user['name']}", bg=COLORS["bg"], fg="#64748b").pack(anchor="w", pady=(0, 20))
        
        stats_f = tk.Frame(self.view_frame, bg=COLORS["bg"])
        stats_f.pack(fill="x", pady=20)

        kpis = [
            ("Total Stock", sum(b.get("stock", 0) for b in self.db["books"].values()), COLORS["accent"]),
            ("Active Loans", len(self.db["active_issues"]), "#f59e0b"),
            ("Revenue", f"₹{self.db['stats']['total_fines']}", COLORS["success"]),
            ("Members", len(self.db["members"]), "#8b5cf6")
        ]

        for title, val, col in kpis:
            f = tk.Frame(stats_f, bg="white", padx=20, pady=25, relief="solid", bd=1)
            f.pack(side="left", expand=True, fill="x", padx=10)
            tk.Label(f, text=title, bg="white", fg="#64748b").pack()
            tk.Label(f, text=val, font=("Arial", 20, "bold"), bg="white", fg=col).pack(pady=5)

        # automated simulator===================================
        tk.Label(self.view_frame, text="System Notifications (Email/SMS Simulation)", font=("Arial", 12, "bold"), bg=COLORS["bg"]).pack(anchor="w", pady=(20, 10))
        log_txt = tk.Text(self.view_frame, height=8, bg="white", font=("Consolas", 10))
        log_txt.pack(fill="x")
        
        today = datetime.now()
        for issue in self.db["active_issues"]:
            due_date = datetime.strptime(issue.get("due", datetime.now().strftime("%Y-%m-%d")), "%Y-%m-%d")
            if due_date <= today + timedelta(days=2):
                log_txt.insert("end", f"[REMINDER SENT] To: {issue.get('member')} | Email: {self.db['members'].get(issue.get('member'), {}).get('email', 'N/A')} | Message: Book '{issue.get('title')}' is due on {issue.get('due')}\n")

    # inventory=======================================================
    def ui_inventory(self):
        for w in self.view_frame.winfo_children(): w.destroy()
        tk.Label(self.view_frame, text="Multi-Branch Inventory", font=("Arial", 18, "bold"), bg=COLORS["bg"]).pack(anchor="w")

        f = tk.Frame(self.view_frame, bg="white", padx=15, pady=15, relief="solid", bd=1); f.pack(fill="x", pady=10)
        entries = {}
        for i, l in enumerate(["ID", "Title", "Author", "Stock"]):
            tk.Label(f, text=l, bg="white").grid(row=0, column=i*2)
            e = tk.Entry(f, width=15); e.grid(row=0, column=i*2+1, padx=5); entries[l] = e
        
        def save():
            bid = entries["ID"].get().strip()
            if not bid: return
            self.db["books"][bid] = {
                "title": entries["Title"].get(), "author": entries["Author"].get(),
                "stock": int(entries["Stock"].get() or 0), "branch": self.user['branch'],
                "barcode": f"BC-{bid}"
            }
            save_db(self.db); self.ui_inventory()

        tk.Button(f, text="ADD TO BRANCH", bg=COLORS["success"], fg="white", command=save, padx=20).grid(row=0, column=8)

        tree = ttk.Treeview(self.view_frame, columns=("ID", "Title", "Stock", "Barcode"), show="headings")
        for c in tree["columns"]: tree.heading(c, text=c)
        for k, v in self.db["books"].items():
            tree.insert("", "end", values=(k, v.get("title"), v.get("stock"), v.get("barcode")))
        tree.pack(expand=True, fill="both")

    # issuing book using barcode system======================
    def ui_issue(self):
        for w in self.view_frame.winfo_children(): w.destroy()
        tk.Label(self.view_frame, text="Barcode Scanning Station", font=("Arial", 18, "bold"), bg=COLORS["bg"]).pack(anchor="w")

        box = tk.Frame(self.view_frame, bg="white", padx=40, pady=40, relief="solid", bd=1); box.pack(pady=20)
        tk.Label(box, text="SCAN BOOK BARCODE", font=("Arial", 10, "bold"), bg="white").pack()
        bc_entry = tk.Entry(box, width=30, font=("Arial", 14), bg="#f8fafc"); bc_entry.pack(pady=10); bc_entry.focus()
        
        tk.Label(box, text="MEMBER ID", bg="white").pack()
        m_entry = tk.Entry(box, width=30); m_entry.pack(pady=5)

        def process():
            code = bc_entry.get().strip()
            mid = m_entry.get().strip()
            
            book_id = None
            if code in self.db["books"]: book_id = code
            else:
                for k,v in self.db["books"].items():
                    if v.get("barcode") == code: book_id = k; break
            
            if book_id and mid in self.db["members"]:
                due = (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d")
                res = {"member": mid, "book_id": book_id, "title": self.db["books"][book_id]["title"], 
                       "date": datetime.now().strftime("%Y-%m-%d"), "due": due, "type": "ISSUE"}
                
                self.db["active_issues"].append(res)
                self.db["activity_log"].append(res)
                self.db["books"][book_id]["stock"] -= 1
                save_db(self.db)
                messagebox.showinfo("Success", f"Issued to {mid}\nDue: {due}")
                self.ui_home()
            else: messagebox.showerror("Error", "Barcode or Member ID not found")
        
        tk.Button(box, text="⚡ COMPLETE ISSUE", command=process, bg=COLORS["accent"], fg="white", width=25, pady=10).pack(pady=20)

    # members==========================================================
    def ui_members(self):
        for w in self.view_frame.winfo_children(): w.destroy()
        f = tk.Frame(self.view_frame, bg="white", padx=20, pady=20); f.pack(fill="x")
        mid = tk.Entry(f); name = tk.Entry(f); email = tk.Entry(f)
        tk.Label(f, text="ID").grid(row=0, column=0); mid.grid(row=0, column=1)
        tk.Label(f, text="Name").grid(row=0, column=2); name.grid(row=0, column=3)
        tk.Label(f, text="Email").grid(row=0, column=4); email.grid(row=0, column=5)
        def save():
            self.db["members"][mid.get()] = {"name": name.get(), "email": email.get()}
            save_db(self.db); self.ui_members()
        tk.Button(f, text="Register", command=save, bg=COLORS["accent"], fg="white").grid(row=0, column=6)
        
        tree = ttk.Treeview(self.view_frame, columns=("ID", "Name", "Email"), show="headings")
        for c in tree["columns"]: tree.heading(c, text=c)
        for k,v in self.db["members"].items(): tree.insert("", "end", values=(k, v.get("name"), v.get("email")))
        tree.pack(expand=True, fill="both")

    # reports=================================================
    def ui_return(self):
        for w in self.view_frame.winfo_children(): w.destroy()
        tree = ttk.Treeview(self.view_frame, columns=("Member", "Book", "Due Date"), show="headings")
        for c in tree["columns"]: tree.heading(c, text=c)
        for i, r in enumerate(self.db["active_issues"]): 
            tree.insert("", "end", iid=i, values=(r.get("member"), r.get("title"), r.get("due")))
        tree.pack(expand=True, fill="both")
        
        def process_ret():
            if not tree.selection(): return
            idx = int(tree.selection()[0])
            record = self.db["active_issues"].pop(idx)
            due = datetime.strptime(record.get("due"), "%Y-%m-%d")
            fine = max(0, (datetime.now() - due).days * FINE_PER_DAY)
            
            self.db["stats"]["total_fines"] += fine
            self.db["books"][record["book_id"]]["stock"] += 1
            self.db["activity_log"].append({"member": record["member"], "title": record["title"], 
                                           "date": datetime.now().strftime("%Y-%m-%d"), "type": "RETURN"})
            save_db(self.db); self.ui_return()
            messagebox.showinfo("Return", f"Fine Charged: ₹{fine}")

        tk.Button(self.view_frame, text="CONFIRM RETURN", bg=COLORS["success"], fg="white", pady=10, command=process_ret).pack()

    def ui_search(self):
        for w in self.view_frame.winfo_children(): w.destroy()
        tk.Label(self.view_frame, text="Global Search", font=("Arial", 18, "bold"), bg=COLORS["bg"]).pack(anchor="w")
        q = tk.Entry(self.view_frame, width=40, font=("Arial", 12)); q.pack(pady=10)
        tree = ttk.Treeview(self.view_frame, columns=("ID", "Title", "Branch"), show="headings")
        for c in tree["columns"]: tree.heading(c, text=c)
        tree.pack(expand=True, fill="both")
        def run_search():
            tree.delete(*tree.get_children())
            for k,v in self.db["books"].items():
                if q.get().lower() in v['title'].lower() or q.get().lower() in v.get('barcode', '').lower():
                    tree.insert("", "end", values=(k, v['title'], v.get('branch')))
        tk.Button(self.view_frame, text="Search", command=run_search, bg=COLORS["accent"], fg="white").pack()

    def ui_reports(self):
        for w in self.view_frame.winfo_children(): w.destroy()
        tk.Label(self.view_frame, text="Audit Log & Data Export", font=("Arial", 18, "bold"), bg=COLORS["bg"]).pack(anchor="w")
        tree = ttk.Treeview(self.view_frame, columns=("Date", "Member", "Action", "Book"), show="headings")
        for c in tree["columns"]: tree.heading(c, text=c)
        for log in self.db.get("activity_log", []):
            tree.insert("", "end", values=(log.get("date"), log.get("member", "N/A"), log.get("type", "ISSUE"), log.get("title")))
        tree.pack(expand=True, fill="both")
        
        def export():
            with open("enterprise_report.csv", "w", newline="") as f:
                w = csv.writer(f); w.writerow(["Date", "Member", "Action", "Book"])
                for log in self.db["activity_log"]:
                    w.writerow([log.get("date"), log.get("member"), log.get("type"), log.get("title")])
            messagebox.showinfo("Export", "Saved as enterprise_report.csv")
        tk.Button(self.view_frame, text="📥 DOWNLOAD CSV (EXCEL)", bg=COLORS["success"], fg="white", command=export, pady=10).pack()

    def ui_staff(self):
        for w in self.view_frame.winfo_children(): w.destroy()
        tk.Label(self.view_frame, text="Staff Management", font=("Arial", 18, "bold"), bg=COLORS["bg"]).pack(anchor="w", pady=(0,10))

        f = tk.Frame(self.view_frame, bg="white", padx=20, pady=20); f.pack(fill="x", pady=10)
        tk.Label(f, text="ID").grid(row=0, column=0); sid = tk.Entry(f); sid.grid(row=0, column=1)
        tk.Label(f, text="Name").grid(row=0, column=2); sname = tk.Entry(f); sname.grid(row=0, column=3)
        tk.Label(f, text="PIN").grid(row=0, column=4); spin = tk.Entry(f, show="*"); spin.grid(row=0, column=5)
        tk.Label(f, text="Role").grid(row=0, column=6); srole = ttk.Combobox(f, values=["staff", "manager"], width=10); srole.grid(row=0, column=7)
        srole.current(0)

        def add_staff():
            staff_id = sid.get().strip()
            if not staff_id: return
            self.db["staff"][staff_id] = {
                "name": sname.get(),
                "pin": hash_pin(spin.get() or "1234"),
                "role": srole.get(),
                "branch": self.user.get("branch", "Main Downtown")
            }
            save_db(self.db); self.ui_staff()

        tk.Button(f, text="ADD STAFF", command=add_staff, bg=COLORS["accent"], fg="white", padx=15).grid(row=0, column=8, padx=10)

        tree = ttk.Treeview(self.view_frame, columns=("ID", "Name", "Role", "Branch"), show="headings")
        for c in tree["columns"]: tree.heading(c, text=c)
        for k,v in self.db["staff"].items():
            tree.insert("", "end", values=(k, v.get("name"), v.get("role"), v.get("branch")))
        tree.pack(expand=True, fill="both", pady=10)

        def remove_staff():
            sel = tree.selection()
            if not sel: return
            sid = tree.item(sel)["values"][0]
            if sid == "admin":
                messagebox.showerror("Error", "Cannot remove the admin")
                return
            del self.db["staff"][sid]
            save_db(self.db); self.ui_staff()

        tk.Button(self.view_frame, text="REMOVE SELECTED STAFF", command=remove_staff, bg=COLORS["danger"], fg="white", pady=10).pack(pady=5)

if __name__ == "__main__":
    root = tk.Tk(); app = LibraryApp(root); root.mainloop()
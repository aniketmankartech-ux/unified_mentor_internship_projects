import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import json
import hashlib
import os
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas



#config 



DATA_FILE = "bank_data.json"
DAILY_LIMIT = 1000.0

def hash_pin(pin):
    return hashlib.sha256(pin.encode()).hexdigest()

def load_data():
    if not os.path.exists(DATA_FILE):
        default_data = {
            "admin": {"pin": hash_pin("9999"), "name": "System Admin", "balance": 0, "role": "admin"},
            "1001": {"pin": hash_pin("1234"), "name": "Aditi", "balance": 5000.0, "role": "user", 
                     "history": [], "daily_withdrawn": 0, "last_date": ""}
        }
        with open(DATA_FILE, 'w') as f:
            json.dump(default_data, f, indent=4)
        return default_data
    with open(DATA_FILE, 'r') as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=4)

def validate_pin(pin):
    return pin.isdigit() and 4 <= len(pin) <= 6

# --- MAIN APP ---
class UltraBankATM:
    def __init__(self, root):
        self.root = root
        self.root.title("Unified Global Banking")
        self.root.geometry("550x750")
        self.root.configure(bg="#1e1e2e")
        self.db = load_data()
        self.current_user_id = None
        self.login_screen()

    #Utility Functions
    def clear(self):
        for w in self.root.winfo_children(): w.destroy()

    def show_status(self, msg, color="#f38ba8"):
        lbl = tk.Label(self.root, text=msg, bg="#1e1e2e", fg=color, font=("Arial", 10, "bold"))
        lbl.pack(pady=5)
        self.root.after(3000, lbl.destroy)

    # login screen of app
    def login_screen(self):
        self.clear()
        tk.Label(self.root, text="UNIFIED BANK ATM", font=("Helvetica", 28, "bold"), bg="#1e1e2e", fg="#89b4fa").pack(pady=60)
    
        frame = tk.Frame(self.root, bg="#313244", padx=30, pady=30)
        frame.pack(pady=10)

        tk.Label(frame, text="Account Number", bg="#313244", fg="white").pack()
        self.acc_ent = ttk.Combobox(frame, values=list(self.db.keys()), font=("Arial", 14), justify='center')
        self.acc_ent.pack(pady=10)

        tk.Label(frame, text="Security PIN", bg="#313244", fg="white").pack()
        self.pin_ent = tk.Entry(frame, font=("Arial", 14), show="*", justify='center', bg="#45475a", fg="white", bd=0)
        self.pin_ent.pack(pady=10)

        tk.Label(frame, text="💡 for admin pin:9999 for other accounts pin:1111", 
                 bg="#313244", fg="#f5c2e7", font=("Arial", 9)).pack(pady=10)

        tk.Button(self.root, text="LOGIN", bg="#a6e3a1", fg="#11111b", width=15, font=("Arial", 12, "bold"), 
                  command=self.handle_login).pack(pady=20)

    def handle_login(self):
        acc, pin = self.acc_ent.get(), self.pin_ent.get()
        if acc in self.db and self.db[acc]['pin'] == hash_pin(pin):
            self.current_user_id = acc
            if self.db[acc]['role'] == 'admin': self.admin_dashboard()
            else: self.user_dashboard()
        else:
            self.show_status("ACCESS DENIED: Invalid Credentials")

    # dashboard
    def user_dashboard(self):
        self.clear()
        user = self.db[self.current_user_id]
        tk.Label(self.root, text=f"Welcome, {user['name']}", font=("Arial", 16), bg="#1e1e2e", fg="white").pack(pady=20)
    
        bal_frame = tk.Frame(self.root, bg="#45475a", pady=15)
        bal_frame.pack(fill="x", padx=50, pady=10)
        tk.Label(bal_frame, text=f"Available: ${user['balance']:,.2f}", font=("Courier", 18, "bold"), 
                 bg="#45475a", fg="#a6e3a1").pack()

        btn_container = tk.Frame(self.root, bg="#1e1e2e")
        btn_container.pack(pady=20)

        ops = [("Withdraw", "W"), ("Deposit", "D"), ("Transfer", "T"), 
               ("Transaction History", "H"), ("Change PIN", "P"), ("Logout", "L")]
        for text, code in ops:
            cmd = self.logout if code=="L" else lambda c=code: self.transaction_input(c)
            tk.Button(btn_container, text=text, width=20, pady=12, bg="#313244", fg="white", command=cmd).pack(pady=5)

    def export_statement(self, user):
        if not user['history']:
            return self.show_status("No transactions to export", "#f38ba8")

        filename = f"MiniStatement_{user['name'].replace(' ','_')}_{datetime.now().strftime('%Y%m%d_%H%M')}.pdf"
        c = canvas.Canvas(filename, pagesize=letter)
        c.setFont("Courier", 12)
        c.drawString(50, 750, f"UNIFIED BANK ATM - Mini Statement for {user['name']}")
        c.drawString(50, 735, f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
        c.drawString(50, 720, "-"*70)

        y = 700
        for tx in user['history'][-20:]:  # last 20 transactions
            c.drawString(50, y, tx)
            y -= 15
            if y < 50:
                c.showPage()
                c.setFont("Courier", 12)
                y = 750

        c.save()
        self.show_status(f"✅ Mini-statement saved as {filename}", "#a6e3a1")


    def logout(self):
        self.current_user_id = None
        self.login_screen()

    # transaction screen
    def transaction_input(self, mode):
        self.clear()
        titles = {"W":"Withdrawal","D":"Deposit","T":"Fund Transfer","H":"Transaction History","P":"Change PIN"}
        tk.Label(self.root, text=titles[mode], font=("Arial",18,"bold"), bg="#1e1e2e", fg="#89b4fa").pack(pady=30)

        # Transaction history
        if mode == "H":
            user = self.db[self.current_user_id]
            txt = scrolledtext.ScrolledText(self.root, width=60, height=25, font=("Courier", 10))
            txt.pack()
            if user['history']:
                for tx in user['history']:
                    color = "#a6e3a1"  # Deposit default green
                    if "Withdraw" in tx: color = "#f38ba8"
                    elif "Transfer" in tx: color = "#89b4fa"
                    txt.insert("end", tx+"\n", color)
                txt.tag_config("#f38ba8", foreground="#f38ba8")
                txt.tag_config("#a6e3a1", foreground="#a6e3a1")
                txt.tag_config("#89b4fa", foreground="#89b4fa")
            else:
                txt.insert("end", "No Transactions Yet")
            txt.config(state="disabled")
            tk.Button(self.root, text="Export Mini-Statement (PDF)", bg="#a6e3a1",command=lambda u=user: self.export_statement(u)).pack(pady=10)
            tk.Button(self.root, text="Back", bg="#eba0ac", command=self.user_dashboard).pack(pady=10)
            return

        # Change PIN
        if mode == "P":
            tk.Label(self.root, text="New PIN:", bg="#1e1e2e", fg="white").pack()
            self.new_pin = tk.Entry(self.root, show="*", font=("Arial",14))
            self.new_pin.pack(pady=10)
            tk.Button(self.root, text="Update PIN", bg="#a6e3a1", command=self.save_pin).pack(pady=10)
            tk.Button(self.root, text="Back", bg="#eba0ac", command=self.user_dashboard).pack(pady=10)
            return

        # Fund transfer
        if mode == "T":
            tk.Label(self.root, text="Recipient Account:", bg="#1e1e2e", fg="white").pack()
            self.target_acc = ttk.Combobox(self.root, values=[k for k in self.db if k != self.current_user_id])
            self.target_acc.pack(pady=5)
            tk.Label(self.root, text="💡 Select recipient account from dropdown.", 
                     bg="#1e1e2e", fg="#f5c2e7", font=("Arial",9)).pack()

        # Amount input
        tk.Label(self.root, text="Enter Amount:", bg="#1e1e2e", fg="white").pack()
        self.amt_ent = tk.Entry(self.root, font=("Arial",14))
        self.amt_ent.pack(pady=10)
        tk.Label(self.root, text="💡 Enter a positive numeric value.", bg="#1e1e2e", fg="#f5c2e7", font=("Arial",9)).pack(pady=5)

        tk.Button(self.root, text="Confirm", bg="#a6e3a1", command=lambda: self.process_logic(mode)).pack(pady=20)
        tk.Button(self.root, text="Back", bg="#eba0ac", command=self.user_dashboard).pack()


    # pin management
    def save_pin(self):
        val = self.new_pin.get().strip()
        if validate_pin(val):
            self.db[self.current_user_id]['pin'] = hash_pin(val)
            save_data(self.db)
            self.show_status("PIN Changed Successfully","#a6e3a1")
            self.user_dashboard()
        else:
            self.show_status("⚠ PIN must be 4-6 digits numeric","#f38ba8")

    # transaction logic of atm


    def process_logic(self, mode):
        try:
            amt = float(self.amt_ent.get())
            if amt <= 0: return self.show_status("⚠ Enter a positive amount")

            user = self.db[self.current_user_id]
            now = datetime.now().strftime("%Y-%m-%d %H:%M")

            if user.get('last_date','')[:10] != now[:10]:
                user['daily_withdrawn'] = 0
                user['last_date'] = now[:10]

            if mode=="W":
                if amt>user['balance']: return self.show_status("❌ Insufficient Funds")
                if user['daily_withdrawn']+amt>DAILY_LIMIT: return self.show_status(f"⚠ Daily Limit ${DAILY_LIMIT} Exceeded")
                user['balance'] -= amt
                user['daily_withdrawn'] += amt
                user['history'].append(f"{now} | Withdraw: ${amt:,.2f}")

            elif mode=="D":
                user['balance'] += amt
                user['history'].append(f"{now} | Deposit: ${amt:,.2f}")

            elif mode=="T":
                target = self.target_acc.get().strip()
                if target not in self.db or target == self.current_user_id: return self.show_status("❌ Invalid Recipient")
                if user['balance']<amt: return self.show_status("❌ Low Balance")
                user['balance'] -= amt
                self.db[target]['balance'] += amt
                user['history'].append(f"{now} | Transfer to {target}: ${amt:,.2f}")

            save_data(self.db)
            self.user_dashboard()
            self.show_status("✅ Transaction Successful","#a6e3a1")
        except ValueError:
            self.show_status("⚠ Enter a valid numeric amount")

    # dashboard for admin
    def admin_dashboard(self):
        self.clear()
        tk.Label(self.root,text="ADMIN CONTROL PANEL",font=("Arial",20,"bold"),fg="#f38ba8",bg="#1e1e2e").pack(pady=40)
        tk.Button(self.root,text="Add New Customer",width=30,pady=15,command=self.add_user_full_ui).pack(pady=10)
        tk.Button(self.root,text="View/Edit Accounts",width=30,pady=15,command=self.view_audit).pack(pady=10)
        tk.Button(self.root,text="Logout",bg="#585b70",fg="white",command=self.login_screen).pack(pady=40)

    #add user admin part
    def add_user_full_ui(self):
        self.clear()
        tk.Label(self.root,text="CREATE ACCOUNT",font=("Arial",18),bg="#1e1e2e",fg="#fab387").pack(pady=30)
        fields=["Account Number","Full Name","Secure PIN","Initial Balance"]
        self.entries={}
        for f in fields:
            tk.Label(self.root,text=f,bg="#1e1e2e",fg="white").pack()
            e=tk.Entry(self.root,font=("Arial",12),width=30)
            e.pack(pady=5)
            self.entries[f]=e
        tk.Button(self.root,text="Save Account",bg="#a6e3a1",pady=10,width=20,command=self.save_new_user).pack(pady=20)
        tk.Button(self.root,text="Cancel",bg="#eba0ac",command=self.admin_dashboard).pack()

    def save_new_user(self):
        acc = self.entries["Account Number"].get().strip()
        name = self.entries["Full Name"].get().strip()
        pin = self.entries["Secure PIN"].get().strip()
        balance = self.entries["Initial Balance"].get().strip()

        if not acc or not name or not pin or not balance:
            return self.show_status("⚠ All fields are required", "#f38ba8")
        if acc in self.db: return self.show_status("❌ Account Already Exists", "#f38ba8")
        if not validate_pin(pin): return self.show_status("⚠ PIN must be 4-6 digits numeric","#f38ba8")
        try:
            balance = float(balance)
            if balance<0: return self.show_status("⚠ Balance cannot be negative", "#f38ba8")
        except ValueError:
            return self.show_status("⚠ Enter numeric balance", "#f38ba8")

        self.db[acc] = {
            "pin": hash_pin(pin),
            "name": name,
            "balance": balance,
            "role": "user",
            "history": [],
            "daily_withdrawn": 0,
            "last_date": ""
        }
        save_data(self.db)
        self.admin_dashboard()
        self.show_status("✅ User Registered Successfully","#a6e3a1")

    # view edit delete operation for admin
    def view_audit(self):
        win=tk.Toplevel(self.root)
        win.title("All Accounts")
        tree=ttk.Treeview(win,columns=("ID","Name","Balance"),show='headings')
        for col in ("ID","Name","Balance"): tree.heading(col,text=col)
        for uid,d in self.db.items():
            if d['role']!="admin":
                tree.insert("",tk.END,values=(uid,d['name'],f"${d['balance']:,.2f}"))
        tree.pack(fill='both',expand=True)

        # Buttons
        btn_frame=tk.Frame(win)
        btn_frame.pack(pady=10)
        tk.Button(btn_frame,text="Edit Selected",bg="#a6e3a1",command=lambda:self.edit_user(tree)).pack(side="left",padx=5)
        tk.Button(btn_frame,text="Delete Selected",bg="#f38ba8",command=lambda:self.delete_user(tree)).pack(side="left",padx=5)

    def edit_user(self, tree):
        sel = tree.focus()
        if not sel: return self.show_status("Select a user","#f38ba8")
        values = tree.item(sel,'values')
        uid = values[0]
        user = self.db[uid]
        win = tk.Toplevel(self.root)
        win.title(f"Edit User {uid}")
        fields = ["Full Name","Balance","PIN"]
        entries={}
        for f in fields:
            tk.Label(win,text=f).pack()
            e=tk.Entry(win)
            e.pack(pady=5)
            if f=="Full Name": e.insert(0,user['name'])
            if f=="Balance": e.insert(0,user['balance'])
            entries[f]=e
        def save_edit():
            name = entries["Full Name"].get().strip()
            balance = entries["Balance"].get().strip()
            pin = entries["PIN"].get().strip()
            if not name or not balance: return self.show_status("Fields cannot be empty","#f38ba8")
            try: balance=float(balance)
            except ValueError: return self.show_status("Balance must be numeric","#f38ba8")
            if pin and not validate_pin(pin): return self.show_status("PIN must be 4-6 digits numeric","#f38ba8")
            user['name']=name
            user['balance']=balance
            if pin: user['pin']=hash_pin(pin)
            save_data(self.db)
            win.destroy()
            self.show_status("✅ User Updated","#a6e3a1")
        tk.Button(win,text="Save",bg="#a6e3a1",command=save_edit).pack(pady=10)

    def delete_user(self, tree):
        sel = tree.focus()
        if not sel: return self.show_status("Select a user","#f38ba8")
        values = tree.item(sel,'values')
        uid = values[0]
        if messagebox.askyesno("Confirm Delete",f"Delete account {uid}?"):
            del self.db[uid]
            save_data(self.db)
            tree.delete(sel)
            self.show_status("✅ User Deleted","#a6e3a1")

if __name__=="__main__":
    root=tk.Tk()
    app=UltraBankATM(root)
    root.mainloop()

import tkinter as tk
from tkinter import ttk, messagebox
import json, os, csv
from datetime import datetime
import winsound
import re


# config====================


DB_FILE = "unified_db.json"
RECEIPT_DIR = "receipts"
REPORT_DIR = "reports"

TOTAL_SLOTS = 30

SLOT_TYPES = {
    "Emergency": ["29", "30"],
    "Priority": ["1","2","3","4","5"],
    "Regular": [str(i) for i in range(6,29)]
}

PRICING = {
    "Bike": {
        "Regular": {"base": 20, "hour": 10},
        "Priority": {"base": 40, "hour": 20},
        "Emergency": {"base": 0, "hour": 0}
    },
    "Car": {
        "Regular": {"base": 50, "hour": 20},
        "Priority": {"base": 100, "hour": 40},
        "Emergency": {"base": 0, "hour": 0}
    },
    "SUV": {
        "Regular": {"base": 80, "hour": 30},
        "Priority": {"base": 150, "hour": 60},
        "Emergency": {"base": 0, "hour": 0}
    }
}

THEME = {
    "bg": "#f4f6fb",
    "sidebar": "#1f1d36",
    "card": "#ffffff",
    "accent": "#6c63ff",
    "success": "#2ecc71",
    "danger": "#e74c3c",
    "warning": "#f1c40f",
    "info": "#3498db"
}

# database init=============


def init_db():
    base = {
        "users": {
            "admin": {"pin": "1234", "role": "admin"},
            "staff": {"pin": "1111", "role": "staff"}
        },
        "slots": {str(i): None for i in range(1, TOTAL_SLOTS+1)},
        "stats": {"revenue": 0.0, "vehicles": 0},
        "history": []
    }




    if not os.path.exists(DB_FILE):
        with open(DB_FILE,"w",encoding="utf-8") as f:
            json.dump(base,f,indent=4)
        return base

    with open(DB_FILE,encoding="utf-8") as f:
        data = json.load(f)

    for k in base:
        data.setdefault(k, base[k])

    with open(DB_FILE,"w",encoding="utf-8") as f:
        json.dump(data,f,indent=4)

    return data

# main app====================================
class ParkingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Unified Parking Management System")
        self.root.geometry("1300x850")
        self.root.configure(bg=THEME["bg"])

        self.db = init_db()
        self.user = None

        os.makedirs(RECEIPT_DIR, exist_ok=True)
        os.makedirs(REPORT_DIR, exist_ok=True)

        self.login()

    def save(self):
        with open(DB_FILE,"w",encoding="utf-8") as f:
            json.dump(self.db,f,indent=4)

    def clear(self):
        for w in self.root.winfo_children():
            w.destroy()

    # login====================================



    def login(self):
        self.clear()
        self.root.configure(bg=THEME["sidebar"])

        card = tk.Frame(self.root,bg="white",padx=45,pady=45)
        card.place(relx=0.5,rely=0.5,anchor="center")

        tk.Label(card,text="Unified Parking System",
                 font=("Segoe UI",22,"bold"),bg="white").pack(pady=5)

        tk.Label(card,text="Secure Login",
                 font=("Segoe UI",12),bg="white",fg="gray").pack(pady=5)

        tk.Label(card,text="Username",bg="white").pack(anchor="w",pady=(15,0))
        users = list(self.db["users"].keys())
        u = ttk.Combobox(card,values=users,state="readonly",width=27)
        u.current(0)
        u.pack(pady=5)

        tk.Label(card,text="PIN / Password",bg="white").pack(anchor="w",pady=(10,0))
        p = tk.Entry(card,show="*",width=30)
        p.pack(pady=5)

        tk.Label(
            card,
            text='Note: Try "1234" for admin, "1111" for staff',
            bg="white",fg="gray",font=("Segoe UI",9)
        ).pack(pady=5)

        def auth():
            if u.get() in self.db["users"] and self.db["users"][u.get()]["pin"] == p.get():
                self.user = self.db["users"][u.get()]
                self.dashboard()
            else:
                messagebox.showerror("Login Failed","Invalid username or PIN")

        tk.Button(card,text="LOGIN",
                  bg=THEME["accent"],fg="white",
                  font=("Segoe UI",11,"bold"),
                  command=auth,height=2).pack(fill="x",pady=15)

    # dashboard======================================
    def dashboard(self):
        self.clear()
        self.root.configure(bg=THEME["bg"])

        side = tk.Frame(self.root,bg=THEME["sidebar"],width=260)
        side.pack(side="left",fill="y")
        side.pack_propagate(False)

        tk.Label(side,text="🚗 Unified Parking",
                 bg=THEME["sidebar"],fg="white",
                 font=("Segoe UI",16,"bold")).pack(pady=20)

        menu = [
            ("📊 Slot Status", self.ui_slots),
            ("🚘 Vehicle Entry", self.ui_entry),
            ("💳 Vehicle Exit", self.ui_exit),
            ("📈 Revenue & Reports", self.ui_reports)
        ]

        if self.user["role"]=="admin":
            menu.append(("👥 Staff Management", self.ui_staff))

        menu.append(("🚪 Logout", self.login))

        for t,c in menu:
            tk.Button(side,text=t,bg=THEME["sidebar"],fg="white",
                      relief="flat",anchor="w",
                      font=("Segoe UI",11),
                      padx=20,pady=14,
                      command=c).pack(fill="x")

        self.main = tk.Frame(self.root,bg=THEME["bg"],padx=30,pady=30)
        self.main.pack(expand=True,fill="both")

        self.ui_slots()

    # map of slot=======================================
    def ui_slots(self):
        self.main.destroy()
        self.main = tk.Frame(self.root,bg=THEME["bg"],padx=30,pady=30)
        self.main.pack(expand=True,fill="both")

        tk.Label(self.main,text="Parking Slot Overview",
                 font=("Segoe UI",18,"bold"),
                 bg=THEME["bg"]).pack(pady=10)

        if all(v for v in self.db["slots"].values()):
            lbl = tk.Label(self.main,text="🚨 PARKING FULL 🚨",
                           bg=THEME["danger"],fg="white",
                           font=("Segoe UI",20,"bold"))
            lbl.pack(pady=10)
            def blink():
                lbl.config(bg="white" if lbl.cget("bg")==THEME["danger"] else THEME["danger"])
                self.main.after(500,blink)
            blink()

        grid = tk.Frame(self.main,bg=THEME["bg"])
        grid.pack(pady=15)

        for i,(s,d) in enumerate(self.db["slots"].items()):
            color = THEME["success"]
            if s in SLOT_TYPES["Priority"]: color = THEME["warning"]
            if s in SLOT_TYPES["Emergency"]: color = THEME["info"]
            if d: color = THEME["danger"]

            f = tk.Frame(grid,bg=color,width=120,height=75)
            f.grid(row=i//6,column=i%6,padx=6,pady=6)
            f.pack_propagate(False)

            tk.Label(f,text=f"Slot {s}",bg=color,fg="white",
                     font=("Segoe UI",10,"bold")).pack()
            tk.Label(f,text=d["vehicle"] if d else "EMPTY",
                     bg=color,fg="white").pack()
    def is_vehicle_parked(self, vehicle_no):
        for d in self.db["slots"].values():
            if d and d["vehicle"] == vehicle_no:
                return True
        return False

    def validate_vehicle_live(self, entry):
        vehicle = entry.get().upper()
        entry.delete(0, tk.END)
        entry.insert(0, vehicle)

        pattern = r"^[A-Z]{2}[0-9]{1,2}[A-Z]{1,2}[0-9]{0,4}$"

        if not vehicle:
            entry.config(highlightthickness=1, highlightbackground="gray", bg="white")
            return

        if re.match(pattern, vehicle):
            entry.config(
                highlightthickness=2,
                highlightbackground="#2ecc71",
                bg="#eafaf1"
            )
        else:
            entry.config(
                highlightthickness=2,
                highlightbackground="#e74c3c",
                bg="#fdecea"
            )



    # entry vehicle=======================================
    def ui_entry(self):
        self.main.destroy()
        self.main = tk.Frame(self.root,bg=THEME["bg"],padx=30,pady=30)
        self.main.pack(expand=True,fill="both")

        tk.Label(self.main,text="Vehicle Entry",
                font=("Segoe UI",18,"bold")).pack(pady=10)

        form = tk.Frame(self.main,bg=THEME["card"],padx=30,pady=30)
        form.pack()

        tk.Label(form,text="Vehicle Number").grid(row=0,column=0,sticky="w")
        v = tk.Entry(form,width=30,font=("Segoe UI",11))
        v.grid(row=0,column=1,pady=5)

        # ✅ LIVE VALIDATION + AUTO UPPERCASE
        v.bind("<KeyRelease>", lambda e: self.validate_vehicle_live(v))

        tk.Label(form,text="Vehicle Type").grid(row=1,column=0,sticky="w")
        vt = ttk.Combobox(form,values=list(PRICING.keys()),state="readonly")
        vt.current(1)
        vt.grid(row=1,column=1,pady=5)

        tk.Label(form,text="Parking Category").grid(row=2,column=0,sticky="w")
        cat = ttk.Combobox(form,values=["Regular","Priority","Emergency"],state="readonly")
        cat.current(0)
        cat.grid(row=2,column=1,pady=5)

        def alloc():
            vehicle = v.get().upper().strip()
            if not vehicle:
                return

            pattern = r"^[A-Z]{2}[0-9]{1,2}[A-Z]{1,2}[0-9]{3,4}$"

            # ✅ FINAL VALIDATION
            if not re.match(pattern, vehicle):
                messagebox.showerror(
                    "Invalid Vehicle Number",
                    "Invalid format!\nExample: MH12AB1234"
                )
                return

            # ✅ DUPLICATE CHECK
            if self.is_vehicle_parked(vehicle):
                messagebox.showerror(
                    "Duplicate Vehicle",
                    f"Vehicle {vehicle} is already parked!"
                )
                return

            vtype = vt.get()
            category = cat.get()

            slots = SLOT_TYPES.get(category,self.db["slots"].keys())
            slot = next(
                (s for s in slots if self.db["slots"][s] is None),
                next((s for s in self.db["slots"] if self.db["slots"][s] is None),None)
            )

            if not slot:
                messagebox.showerror("Parking Full","No slots available")
                return

            if category=="Emergency":
                winsound.Beep(1500,600)

            self.db["slots"][slot] = {
                "vehicle": vehicle,
                "vtype": vtype,
                "category": category,
                "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            self.save()
            messagebox.showinfo("Allocated",f"{vehicle} → Slot {slot}")
            self.ui_slots()

        tk.Button(
            form,
            text="ALLOCATE SLOT",
            bg=THEME["accent"],
            fg="white",
            font=("Segoe UI",11,"bold"),
            command=alloc
        ).grid(row=3,columnspan=2,pady=15)


    # exit==============================
    def ui_exit(self):
        self.main.destroy()
        self.main = tk.Frame(self.root,bg=THEME["bg"],padx=30,pady=30)
        self.main.pack(expand=True,fill="both")

        tk.Label(self.main,text="Vehicle Exit",
                 font=("Segoe UI",18,"bold")).pack(pady=10)

        active = [f"{s} | {d['vehicle']}" for s,d in self.db["slots"].items() if d]
        cb = ttk.Combobox(self.main,values=active,state="readonly",width=40)
        cb.pack(pady=20)

        def process():
            if not cb.get(): return
            s = cb.get().split(" | ")[0]
            d = self.db["slots"][s]

            start = datetime.strptime(d["time"],"%Y-%m-%d %H:%M:%S")
            hrs = max(1,(datetime.now()-start).total_seconds()/3600)

            rate = PRICING[d["vtype"]][d["category"]]
            fee = rate["base"] + max(0,hrs-1)*rate["hour"]

            self.db["stats"]["revenue"] += fee
            self.db["stats"]["vehicles"] += 1
            self.db["history"].append({
                "vehicle": d["vehicle"],
                "type": d["vtype"],
                "category": d["category"],
                "hours": round(hrs,1),
                "amount": fee,
                "date": datetime.now().strftime("%Y-%m-%d")
            })

            self.db["slots"][s] = None
            self.save()
            self.print_receipt(d,hrs,fee)
            self.ui_slots()

        tk.Button(self.main,text="PROCESS EXIT",
                  bg=THEME["danger"],fg="white",
                  font=("Segoe UI",11,"bold"),
                  command=process).pack(pady=10)

    def print_receipt(self,d,h,f):
        fn = f"{RECEIPT_DIR}/{d['vehicle']}_{datetime.now().strftime('%H%M%S')}.txt"
        with open(fn,"w",encoding="utf-8") as r:
            r.write(
                "UNIFIED PARKING RECEIPT\n"
                "----------------------\n"
                f"Vehicle: {d['vehicle']}\n"
                f"Type: {d['vtype']} ({d['category']})\n"
                f"Hours: {h:.1f}\n"
                f"Amount Paid: ₹{f:.2f}\n"
                f"Date: {datetime.now()}\n"
            )
        messagebox.showinfo("Payment Successful",f"₹{f:.2f} collected\nReceipt saved")

    # report============================
    def ui_reports(self):
        self.main.destroy()
        self.main = tk.Frame(self.root,bg=THEME["bg"],padx=30,pady=30)
        self.main.pack(expand=True,fill="both")

        tk.Label(self.main,text="Revenue Analytics",
                 font=("Segoe UI",18,"bold")).pack(pady=10)

        tk.Label(self.main,text=f"Total Vehicles: {self.db['stats']['vehicles']}",
                 font=("Segoe UI",14)).pack()
        tk.Label(self.main,text=f"Total Revenue: ₹{self.db['stats']['revenue']:.2f}",
                 font=("Segoe UI",20,"bold")).pack(pady=10)

        def export():
            if not self.db["history"]:
                messagebox.showwarning("No Data","No history to export")
                return
            fn = f"{REPORT_DIR}/report_{datetime.now().strftime('%Y%m%d')}.csv"
            with open(fn,"w",newline="",encoding="utf-8") as f:
                w = csv.DictWriter(f,fieldnames=self.db["history"][0].keys())
                w.writeheader()
                w.writerows(self.db["history"])
            messagebox.showinfo("Exported",fn)

        tk.Button(self.main,text="EXPORT CSV",
                  bg=THEME["accent"],fg="white",
                  font=("Segoe UI",11,"bold"),
                  command=export).pack(pady=15)

    # staff =================
    def ui_staff(self):
        self.main.destroy()
        self.main = tk.Frame(self.root,bg=THEME["bg"],padx=30,pady=30)
        self.main.pack(expand=True,fill="both")

        tk.Label(self.main,text="Staff Management",
                 font=("Segoe UI",18,"bold")).pack(pady=10)

        form = tk.Frame(self.main,bg=THEME["card"],padx=30,pady=30)
        form.pack()

        tk.Label(form,text="Username").grid(row=0,column=0,sticky="w")
        u = tk.Entry(form,width=25); u.grid(row=0,column=1,pady=5)

        tk.Label(form,text="PIN").grid(row=1,column=0,sticky="w")
        p = tk.Entry(form,show="*",width=25); p.grid(row=1,column=1,pady=5)

        def add():
            if u.get() and p.get():
                self.db["users"][u.get()] = {"pin": p.get(), "role": "staff"}
                self.save()
                refresh()
                u.delete(0,"end"); p.delete(0,"end")

        tk.Button(form,text="ADD STAFF",
                  bg=THEME["accent"],fg="white",
                  command=add).grid(row=2,columnspan=2,pady=10)

        tree = ttk.Treeview(self.main,columns=("User","Role"),show="headings")
        tree.heading("User",text="Username")
        tree.heading("Role",text="Role")
        tree.pack(fill="x",pady=15)

        def refresh():
            for i in tree.get_children(): tree.delete(i)
            for k,v in self.db["users"].items():
                tree.insert("", "end", values=(k,v["role"]))

        refresh()


# run=================
if __name__ == "__main__":
    root = tk.Tk()
    ParkingApp(root)
    root.mainloop()

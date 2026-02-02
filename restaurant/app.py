import tkinter as tk
from tkinter import ttk, messagebox
import json, os, hashlib, csv
from datetime import datetime, timedelta

# --- CONFIGURATION ---
DATA_FILE = "unified_restaurant.json"
RECEIPTS_FOLDER = "receipts"
REPORTS_FOLDER = "reports"
COLORS = {
    "sidebar": "#2d3436",
    "accent": "#fdcb6e",
    "success": "#00b894",
    "danger": "#d63031",
    "bg": "#f0f0f0",
    "main_bg": "#ffffff",
    "text": "#2d3436"
}

# --- UTILITIES ---
def hash_pin(pin):
    return hashlib.sha256(pin.encode()).hexdigest()

def ensure_folders():
    os.makedirs(RECEIPTS_FOLDER, exist_ok=True)
    os.makedirs(REPORTS_FOLDER, exist_ok=True)

def init_db():
    if not os.path.exists(DATA_FILE):
        data = {
            "staff": {"manager": {"pin": hash_pin("8888"), "role": "manager", "name": "Head Admin"}},
            "menu": {"Main Course": {"Burger": [150, 20]}, "Drinks": {"Soda": [50, 50]}},
            "sales": [],
            "stats": {"total_revenue": 0.0, "order_count": 0}
        }
        with open(DATA_FILE, "w") as f:
            json.dump(data, f, indent=4)
        return data
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_db(db):
    with open(DATA_FILE, "w") as f:
        json.dump(db, f, indent=4)

def validate_pin(pin):
    return pin.isdigit() and 4 <= len(pin) <= 6

def format_currency(val):
    return f"₹{val:,.2f}"

# --- MAIN APP ---
class UnifiedRestaurantPOS:
    def __init__(self, root):
        self.root = root
        self.root.title("Unified Restaurant POS")
        self.root.geometry("1600x800+0+0")
        self.db = init_db()
        self.user = None
        self.cart = []
        ensure_folders()
        self.login_ui()

    # --- UTILITY ---
    def clear(self):
        for w in self.root.winfo_children(): w.destroy()

    def show_error(self, msg):
        messagebox.showerror("Error", msg)

    def show_info(self, msg):
        messagebox.showinfo("Info", msg)

    # --- LOGIN ---
    def login_ui(self):
        self.clear()
        self.root.configure(bg=COLORS["sidebar"])
        frame = tk.Frame(self.root, bg=COLORS["main_bg"], padx=40, pady=40)
        frame.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(frame, text="UNIFIED RESTAURANT LOGIN", font=("Arial", 14, "bold"), bg=COLORS["main_bg"]).pack(pady=10)
        users = list(self.db["staff"].keys())
        self.uid = ttk.Combobox(frame, values=users, font=("Arial",12), state="readonly"); self.uid.pack(pady=5)
        self.uid.set(users[0])
        self.pin = tk.Entry(frame, show="*", font=("Arial",12)); self.pin.pack(pady=5)
        tk.Label(frame, text="Note: for manager PIN: 8888 .for staff PIN: 1111 ", font=("Arial", 10), fg="gray", bg=COLORS["main_bg"]).pack(pady=(0,10))

        tk.Button(frame, text="LOGIN", bg=COLORS["accent"], width=20, pady=10, command=self.verify_login).pack(pady=20)

    def verify_login(self):
        u, p = self.uid.get(), self.pin.get()
        if u in self.db["staff"] and self.db["staff"][u]["pin"] == hash_pin(p):
            self.user = self.db["staff"][u]
            self.main_ui()
        else:
            self.show_error("Invalid credentials")

    # --- MAIN UI ---
    def main_ui(self):
        self.clear()
        # Sidebar
        sidebar = tk.Frame(self.root, bg=COLORS["sidebar"], width=220)
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)
        main = tk.Frame(self.root, bg=COLORS["main_bg"], padx=20, pady=20)
        main.pack(side="right", fill="both", expand=True)
        self.main_frame = main

        # Sidebar buttons
        if self.user["role"] == "manager":
            buttons = [("📊 Dashboard", self.ui_dashboard),
                       ("📋 Menu Editor", self.ui_menu_editor),
                       ("👥 Staff Manager", self.ui_staff_manager),
                       ("📈 Reports Export", self.ui_report_export)]
        else:
            buttons = [("🛒 Billing", self.ui_billing),
                       ("📦 Stock Check", self.ui_stock_view)]
        for text, cmd in buttons:
            tk.Button(sidebar, text=text, bg=COLORS["sidebar"], fg="white", relief="flat", anchor="w",
                      padx=20, pady=15, command=cmd).pack(fill="x")
        tk.Button(sidebar, text="Logout", bg=COLORS["danger"], fg="white", command=self.login_ui).pack(side="bottom", fill="x", pady=20)

        # Load default view
        if self.user["role"] == "manager":
            self.ui_dashboard()
        else:
            self.ui_billing()

    # --- DASHBOARD ---
    def ui_dashboard(self):
        self.clear_frame()
        tk.Label(self.main_frame, text="Executive Dashboard", font=("Arial", 22, "bold"), bg=COLORS["main_bg"]).pack(anchor="w")
        tk.Label(self.main_frame, text=f"Total Revenue: {format_currency(self.db['stats']['total_revenue'])}",
                 font=("Arial", 18), fg=COLORS["success"], bg="#f0fff0", padx=20, pady=20, relief="solid", bd=1).pack(pady=20)
        tk.Label(self.main_frame, text=f"Orders Processed: {self.db['stats']['order_count']}", font=("Arial",16),
                 bg="#fff0f5", padx=20, pady=20, relief="solid", bd=1).pack(pady=10)

        # Low-stock alert
        alert_frame = tk.Frame(self.main_frame, bg="#fff"); alert_frame.pack(fill="x", pady=20)
        tk.Label(alert_frame, text="Low Stock Alerts", font=("Arial",16,"bold"), bg="#fff").pack(anchor="w")
        low_items = []
        for c, items in self.db["menu"].items():
            for name, val in items.items():
                if val[1] < 5:
                    low_items.append(f"{name} ({c}) - {val[1]} left")
        if low_items:
            for li in low_items: tk.Label(alert_frame, text=li, fg=COLORS["danger"], bg="#fff").pack(anchor="w")
        else:
            tk.Label(alert_frame, text="All items sufficiently stocked", fg=COLORS["success"], bg="#fff").pack(anchor="w")

    # --- MENU EDITOR ---
    def ui_menu_editor(self):
        self.clear_frame()
        tk.Label(self.main_frame, text="Menu & Price Editor", font=("Arial",18,"bold"), bg=COLORS["main_bg"]).pack(anchor="w")
        form = tk.Frame(self.main_frame, bg="#fff", padx=10, pady=10, relief="solid", bd=1); form.pack(fill="x", pady=10)

        tk.Label(form, text="Category").grid(row=0, column=0); cat_e = tk.Entry(form); cat_e.grid(row=0,column=1,padx=5)
        tk.Label(form, text="Item").grid(row=0, column=2); item_e = tk.Entry(form); item_e.grid(row=0,column=3,padx=5)
        tk.Label(form, text="Price").grid(row=0, column=4); price_e = tk.Entry(form,width=8); price_e.grid(row=0,column=5,padx=5)
        tk.Label(form, text="Stock").grid(row=0, column=6); stock_e = tk.Entry(form,width=8); stock_e.grid(row=0,column=7,padx=5)

        def save_item():
            c, i, p, s = cat_e.get().strip(), item_e.get().strip(), price_e.get().strip(), stock_e.get().strip()
            if not all([c, i, p, s]): return self.show_error("All fields required")
            try:
                p, s = float(p), int(s)
            except: return self.show_error("Invalid price or stock")
            if c not in self.db["menu"]: self.db["menu"][c] = {}
            self.db["menu"][c][i] = [p, s]
            save_db(self.db)
            self.ui_menu_editor()

        tk.Button(form, text="Save/Update", bg=COLORS["success"], fg="white", command=save_item).grid(row=0,column=8,padx=10)

        tree = ttk.Treeview(self.main_frame, columns=("Category","Item","Price","Stock"), show="headings")
        for col in ("Category","Item","Price","Stock"): tree.heading(col,text=col)
        for c, items in self.db["menu"].items():
            for n,v in items.items():
                tree.insert("", "end", values=(c,n,v[0],v[1]))
        tree.pack(fill="both", expand=True)

    # --- STOCK VIEW ---
    def ui_stock_view(self):
        self.clear_frame()
        tk.Label(self.main_frame, text="Current Inventory", font=("Arial",18,"bold"), bg=COLORS["main_bg"]).pack(anchor="w", pady=10)
        scroll = tk.Frame(self.main_frame, bg="#fff"); scroll.pack(fill="both",expand=True)
        for c, items in self.db["menu"].items():
            tk.Label(scroll, text=c, font=("Arial",12,"bold"), bg="#eee").pack(fill="x", pady=(10,0))
            for n, v in items.items():
                color = COLORS["danger"] if v[1]<5 else COLORS["text"]
                lbl = tk.Frame(scroll, bg="#fff"); lbl.pack(fill="x", padx=10)
                tk.Label(lbl, text=n, bg="#fff").pack(side="left")
                tk.Label(lbl, text=f"Stock: {v[1]}", fg=color, bg="#fff").pack(side="right")

    # --- STAFF MANAGER ---
    def ui_staff_manager(self):
        self.clear_frame()
        tk.Label(self.main_frame, text="Staff Management", font=("Arial",18,"bold"), bg=COLORS["main_bg"]).pack(anchor="w")
        form = tk.Frame(self.main_frame, bg="#fff", padx=10, pady=10); form.pack(fill="x", pady=10)
        tk.Label(form, text="ID").grid(row=0,column=0); sid = tk.Entry(form); sid.grid(row=0,column=1)
        tk.Label(form, text="Role").grid(row=0,column=2); srole = ttk.Combobox(form,values=["manager","cashier"]); srole.grid(row=0,column=3)
        tk.Label(form, text="PIN").grid(row=0,column=4); spin = tk.Entry(form, show="*"); spin.grid(row=0,column=5)

        def add_staff():
            id_ = sid.get().strip(); role = srole.get().strip(); pin = spin.get().strip()
            if not id_ or not role or not pin: return self.show_error("All fields required")
            if not validate_pin(pin): return self.show_error("PIN must be 4-6 digits numeric")
            self.db["staff"][id_] = {"pin": hash_pin(pin), "role": role, "name": id_}
            save_db(self.db); self.ui_staff_manager()

        tk.Button(form,text="Add Staff", bg=COLORS["success"], fg="white", command=add_staff).grid(row=0,column=6,padx=10)

        tree = ttk.Treeview(self.main_frame, columns=("ID","Role"), show="headings")
        tree.heading("ID", text="Staff ID"); tree.heading("Role", text="Access Level")
        for u,d in self.db["staff"].items(): tree.insert("", "end", values=(u,d["role"]))
        tree.pack(fill="both", expand=True)

    # --- BILLING ---
    def ui_billing(self):
        self.clear_frame()
        self.cart = []
        tk.Label(self.main_frame, text="New Order", font=("Arial",18,"bold"), bg=COLORS["main_bg"]).pack(anchor="w")
        box = tk.Frame(self.main_frame, bg=COLORS["main_bg"]); box.pack(fill="both", expand=True, pady=10)
        left = tk.Frame(box, bg="#fff", padx=10, pady=10); left.pack(side="left", fill="both", expand=True)
        right = tk.Frame(box, bg="#fff", padx=10, pady=10, width=250); right.pack(side="right", fill="y", padx=10)

        # Menu Tree
        self.bt = ttk.Treeview(left, columns=("Item","Price","Stock"), show="headings")
        for col in ("Item","Price","Stock"): self.bt.heading(col,text=col)
        for c, items in self.db["menu"].items():
            for n,v in items.items(): self.bt.insert("", "end", values=(n,v[0],v[1]))
        self.bt.pack(fill="both", expand=True)

        # Cart Listbox
        self.cl = tk.Listbox(right); self.cl.pack(fill="both", expand=True)

        # Add item
        def add_to_cart():
            sel = self.bt.selection()
            if not sel: return
            item_vals = self.bt.item(sel)["values"]
            name, price, stock = item_vals[0], float(item_vals[1]), int(item_vals[2])
            if stock <= 0: return self.show_error(f"{name} out of stock")
            # Check if in cart
            for c in self.cart:
                if c["name"] == name:
                    if c["qty"] < stock: c["qty"] +=1
                    else: return self.show_error(f"Only {stock} units available")
                    break
            else:
                self.cart.append({"name": name, "price": price, "qty":1})
            self.refresh_cart()

        tk.Button(left, text="Add to Cart", bg=COLORS["accent"], command=add_to_cart).pack(fill="x", pady=5)

        # Cart actions
        def remove_item(): 
            sel = self.cl.curselection()
            if not sel: return
            del self.cart[sel[0]]; self.refresh_cart()
        def inc_item():
            sel = self.cl.curselection()
            if not sel: return
            cart_item = self.cart[sel[0]]
            for c in self.db["menu"]:
                if cart_item["name"] in self.db["menu"][c]:
                    stock = self.db["menu"][c][cart_item["name"]][1]
                    break
            if cart_item["qty"] < stock: cart_item["qty"]+=1
            self.refresh_cart()
        def dec_item():
            sel = self.cl.curselection()
            if not sel: return
            cart_item = self.cart[sel[0]]
            if cart_item["qty"]>1: cart_item["qty"]-=1
            self.refresh_cart()

        tk.Button(right,text="Remove", bg=COLORS["danger"], command=remove_item).pack(fill="x", pady=2)
        tk.Button(right,text="Increase Qty", bg=COLORS["success"], command=inc_item).pack(fill="x", pady=2)
        tk.Button(right,text="Decrease Qty", bg=COLORS["accent"], command=dec_item).pack(fill="x", pady=2)

        # Checkout
        def checkout():
            if not self.cart: return self.show_error("Cart empty")
            subtotal = sum(c["price"]*c["qty"] for c in self.cart)
            gst = subtotal*0.15; total = subtotal+gst

            # Update stock
            for item in self.cart:
                for cat in self.db["menu"]:
                    if item["name"] in self.db["menu"][cat]:
                        self.db["menu"][cat][item["name"]][1] -= item["qty"]

            # Save sales
            self.db["stats"]["total_revenue"] += total
            self.db["stats"]["order_count"] += 1
            sale = {"time": datetime.now().strftime("%Y-%m-%d %H:%M"), "items": self.cart, "total": total, "cashier": self.user["name"]}
            self.db["sales"].append(sale)
            save_db(self.db)
            self.save_receipt(sale)
            self.show_info(f"Payment Successful! Total: {format_currency(total)}")
            self.ui_billing()

        tk.Button(right, text="Checkout", bg=COLORS["success"], fg="white", command=checkout).pack(fill="x")

    def refresh_cart(self):
        self.cl.delete(0, tk.END)
        for c in self.cart: self.cl.insert(tk.END, f"{c['name']} x{c['qty']} - {format_currency(c['price']*c['qty'])}")

    # --- RECEIPTS ---
    def save_receipt(self, sale):
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = os.path.join(RECEIPTS_FOLDER, f"receipt_{ts}.txt")
        with open(filename,"w", encoding="utf-8") as f:
            f.write("UNIFIED RESTAURANT\n")
            f.write("-"*30+"\n")
            for i in sale["items"]:
                f.write(f"{i['name']} x{i['qty']} {format_currency(i['price']*i['qty'])}\n")
            f.write("-"*30+"\n")
            subtotal = sum(i['price']*i['qty'] for i in sale["items"])
            gst = subtotal*0.15
            total = subtotal+gst
            f.write(f"Subtotal: {format_currency(subtotal)}\n")
            f.write(f"GST @15%: {format_currency(gst)}\n")
            f.write(f"TOTAL: {format_currency(total)}\n")
            f.write(f"Cashier: {sale['cashier']}\n")
            f.write(f"Time: {sale['time']}\n")

    # --- REPORT EXPORT ---
    def ui_report_export(self):
        self.clear_frame()
        tk.Label(self.main_frame, text="Export Sales Reports", font=("Arial",18,"bold"), bg=COLORS["main_bg"]).pack(anchor="w", pady=10)
        tk.Button(self.main_frame,text="Export Daily Report", bg=COLORS["accent"], command=lambda:self.export_report(days=1)).pack(pady=5)
        tk.Button(self.main_frame,text="Export Weekly Report", bg=COLORS["accent"], command=lambda:self.export_report(days=7)).pack(pady=5)

    def export_report(self, days=1):
        cutoff = datetime.now() - timedelta(days=days)
        filename = os.path.join(REPORTS_FOLDER, f"sales_{days}d_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv")
        with open(filename,"w",newline="",encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["Time","Cashier","Item(s)","Total"])
            for sale in self.db["sales"]:
                sale_time = datetime.strptime(sale["time"],"%Y-%m-%d %H:%M")
                if sale_time >= cutoff:
                    items = "; ".join([f"{i['name']} x{i['qty']}" for i in sale["items"]])
                    writer.writerow([sale["time"], sale["cashier"], items, sale["total"]])
        self.show_info(f"Report exported: {filename}")

    def clear_frame(self):
        for w in self.main_frame.winfo_children(): w.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    style = ttk.Style(); style.theme_use("clam")
    app = UnifiedRestaurantPOS(root)
    root.mainloop()

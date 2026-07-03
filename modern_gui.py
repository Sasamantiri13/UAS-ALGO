import customtkinter as ctk
import tkinter as tk
from tkinter import ttk, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import collections

from models import MahasiswaAktif, MahasiswaNonAktif
from manager import MahasiswaManager, SortEngine, SearchEngine
from file_manager import FileManager
from validator import Validator, DataValidationError
from auth import AuthManager

# Set Theme
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class ModernGUI(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("Student Management System v2.1 - Advanced DS")
        self.geometry("1100x700")
        
        # Backend Logic
        self.file_manager = FileManager()
        self.manager = MahasiswaManager(self.file_manager.loadFromFile())
        self.validator = Validator()
        self.auth = AuthManager()
        
        # UI State
        self.show_login()

    def show_login(self):
        self.login_frame = ctk.CTkFrame(self)
        self.login_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        
        ctk.CTkLabel(self.login_frame, text="ADMIN LOGIN", font=("Roboto", 24, "bold")).pack(pady=20, padx=40)
        
        self.u_entry = ctk.CTkEntry(self.login_frame, placeholder_text="Username", width=250)
        self.u_entry.pack(pady=10, padx=40)
        self.u_entry.insert(0, "admin")
        
        self.p_entry = ctk.CTkEntry(self.login_frame, placeholder_text="Password", show="*", width=250)
        self.p_entry.pack(pady=10, padx=40)
        self.p_entry.insert(0, "admin123")
        
        ctk.CTkButton(self.login_frame, text="Login", command=self.handle_login, width=250).pack(pady=20, padx=40)
        self.bind('<Return>', lambda e: self.handle_login())

    def handle_login(self):
        u = self.u_entry.get()
        p = self.p_entry.get()
        if self.auth.login(u, p):
            self.login_frame.destroy()
            self.setup_main_ui()
        else:
            messagebox.showerror("Gagal", "Username atau Password salah!")

    def setup_main_ui(self):
        # Configure Grid
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        # Sidebar
        self.sidebar_frame = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        
        ctk.CTkLabel(self.sidebar_frame, text="SMS Advanced", font=("Roboto", 20, "bold")).pack(pady=20)
        
        self.btn_dash = ctk.CTkButton(self.sidebar_frame, text="Dashboard", command=lambda: self.show_page("dash"))
        self.btn_dash.pack(pady=10, padx=20)
        
        self.btn_stats = ctk.CTkButton(self.sidebar_frame, text="Statistik", command=lambda: self.show_page("stats"))
        self.btn_stats.pack(pady=10, padx=20)
        
        ctk.CTkLabel(self.sidebar_frame, text="Appearance:", anchor="w").pack(side="bottom", padx=20, pady=(10, 0))
        self.mode_menu = ctk.CTkOptionMenu(self.sidebar_frame, values=["Dark", "Light"], command=ctk.set_appearance_mode)
        self.mode_menu.pack(side="bottom", padx=20, pady=(0, 20))
        
        # Main Content Area
        self.container = ctk.CTkFrame(self)
        self.container.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        self.container.grid_columnconfigure(0, weight=1)
        self.container.grid_rowconfigure(0, weight=1)
        
        self.pages = {}
        self.create_dash_page()
        self.create_stats_page()
        
        self.show_page("dash")

    def show_page(self, page_name):
        for page in self.pages.values():
            page.grid_forget()
        self.pages[page_name].grid(row=0, column=0, sticky="nsew")
        if page_name == "stats":
            self.render_charts()

    def create_dash_page(self):
        page = ctk.CTkFrame(self.container)
        self.pages["dash"] = page
        page.grid_columnconfigure(1, weight=1)
        page.grid_rowconfigure(0, weight=1)
        
        # Form (Left)
        form_frame = ctk.CTkFrame(page, width=300)
        form_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        
        ctk.CTkLabel(form_frame, text="Manage Student", font=("Roboto", 16, "bold")).pack(pady=10)
        
        self.entries = {}
        for f in ["nim", "nama", "jurusan", "semester", "ipk"]:
            e = ctk.CTkEntry(form_frame, placeholder_text=f.capitalize())
            e.pack(pady=5, padx=10, fill="x")
            self.entries[f] = e
            
        self.status_var = tk.StringVar(value="Aktif")
        ctk.CTkOptionMenu(form_frame, values=["Aktif", "Non-Aktif"], variable=self.status_var).pack(pady=5, padx=10, fill="x")
        
        ctk.CTkButton(form_frame, text="Add Student", fg_color="green", hover_color="darkgreen", command=self.add_student).pack(pady=10, padx=10, fill="x")
        ctk.CTkButton(form_frame, text="Update", command=self.update_student).pack(pady=5, padx=10, fill="x")
        ctk.CTkButton(form_frame, text="Delete", fg_color="red", hover_color="darkred", command=self.delete_student).pack(pady=5, padx=10, fill="x")
        ctk.CTkButton(form_frame, text="Clear Form", command=self.clear_form).pack(pady=5, padx=10, fill="x")

        # Table Area (Right)
        table_frame = ctk.CTkFrame(page)
        table_frame.grid(row=0, column=1, sticky="nsew")
        
        # Search Bar
        search_frame = ctk.CTkFrame(table_frame)
        search_frame.pack(fill="x", pady=5, padx=5)
        
        self.search_entry = ctk.CTkEntry(search_frame, placeholder_text="Cari NIM/Nama...")
        self.search_entry.pack(side="left", fill="x", expand=True, padx=5)
        
        # Search Method Option Menu
        self.search_method_var = tk.StringVar(value="sequential")
        self.search_method_menu = ctk.CTkOptionMenu(search_frame, values=["sequential", "binary", "linear"], variable=self.search_method_var, width=110)
        self.search_method_menu.pack(side="left", padx=5)

        # Sort Algorithm Option Menu
        self.sort_algo_var = tk.StringVar(value="Merge Sort")
        self.sort_algo_menu = ctk.CTkOptionMenu(search_frame, values=["Bubble Sort", "Insertion Sort", "Merge Sort"], variable=self.sort_algo_var, width=120)
        self.sort_algo_menu.pack(side="left", padx=5)

        ctk.CTkButton(search_frame, text="Search", width=80, command=self.search_student).pack(side="left", padx=5)
        ctk.CTkButton(search_frame, text="Reset", width=80, command=self.refresh_table).pack(side="left", padx=5)

        # Treeview Styling
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", background="#2b2b2b", foreground="white", fieldbackground="#2b2b2b", borderwidth=0)
        style.map("Treeview", background=[('selected', '#1f538d')])
        
        columns = ("nim", "nama", "jurusan", "semester", "ipk", "status")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings")
        for col in columns:
            self.tree.heading(col, text=col.upper(), command=lambda c=col: self.sort_table(c))
            self.tree.column(col, width=100, anchor="center")
        self.tree.pack(fill="both", expand=True, padx=5, pady=5)
        self.tree.bind("<<TreeviewSelect>>", self.on_tree_select)
        
        self.status_label = ctk.CTkLabel(table_frame, text="Storage: Doubly Linked List | Total: 0")
        self.status_label.pack(side="bottom", pady=5)

    def create_stats_page(self):
        page = ctk.CTkFrame(self.container)
        self.pages["stats"] = page
        ctk.CTkLabel(page, text="STATISTIK DATA MAHASISWA", font=("Roboto", 24, "bold")).pack(pady=20)
        self.chart_container = ctk.CTkFrame(page)
        self.chart_container.pack(fill="both", expand=True, padx=20, pady=20)

    def render_charts(self):
        for widget in self.chart_container.winfo_children(): widget.destroy()
        students = self.manager.getAllStudents()
        if not students:
            ctk.CTkLabel(self.chart_container, text="Data kosong untuk statistik").pack()
            return
        jurusan_counts = collections.Counter([s.jurusan for s in students])
        ipks = [s.ipk for s in students]
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4), facecolor="#2b2b2b")
        plt.subplots_adjust(wspace=0.4)
        ax1.bar(jurusan_counts.keys(), jurusan_counts.values(), color="#1f538d")
        ax1.set_title("Mahasiswa per Jurusan", color="white"); ax1.tick_params(colors="white")
        for spine in ax1.spines.values(): spine.set_color("white")
        ax2.hist(ipks, bins=5, color="#1f8d53", edgecolor="black")
        ax2.set_title("Sebaran IPK", color="white"); ax2.tick_params(colors="white")
        for spine in ax2.spines.values(): spine.set_color("white")
        canvas = FigureCanvasTkAgg(fig, master=self.chart_container)
        canvas.draw(); canvas.get_tk_widget().pack(fill="both", expand=True)

    def refresh_table(self, data_list=None):
        for i in self.tree.get_children(): self.tree.delete(i)
        students = data_list if data_list is not None else self.manager.getAllStudents()
        for s in students:
            self.tree.insert("", "end", values=(s.nim, s.nama, s.jurusan, s.semester, f"{s.ipk:.2f}", s.status))
        self.status_label.configure(text=f"Storage: Doubly Linked List | Total: {len(students)}")

    def add_student(self):
        try:
            data = {f: self.entries[f].get() for f in self.entries}
            for f in ["nim", "nama", "jurusan", "semester", "ipk"]:
                if not data[f]: raise Exception(f"{f.upper()} harus diisi!")
            
            # Validasi Regex untuk semua input
            self.validator.validate_nim(data["nim"])
            self.validator.validate_nama(data["nama"])
            self.validator.validate_jurusan(data["jurusan"])
            self.validator.validate_semester(data["semester"])
            self.validator.validate_ipk(data["ipk"])
            
            # Cek Duplikasi NIM
            idx, _ = SearchEngine.sequentialSearch(self.manager.linked_list, data["nim"], "nim")
            if idx != -1:
                messagebox.showerror("Error", "NIM sudah terdaftar!")
                return
            
            cls = MahasiswaAktif if self.status_var.get() == "Aktif" else MahasiswaNonAktif
            mhs = cls(data["nim"], data["nama"], data["jurusan"], int(data["semester"]), float(data["ipk"]))
            self.manager.addStudent(mhs)
            self.file_manager.saveToFile(self.manager.getAllStudents())
            self.refresh_table()
            self.clear_form()
            messagebox.showinfo("Success", "Student added successfully!")
        except DataValidationError as e:
            messagebox.showerror("Validasi Gagal", str(e))
        except Exception as e: 
            messagebox.showerror("Error", str(e))

    def update_student(self):
        selected = self.tree.selection()
        if not selected: return
        nim_target = str(self.tree.item(selected[0])['values'][0]).zfill(10)
        try:
            nama = self.entries["nama"].get()
            jurusan = self.entries["jurusan"].get()
            semester = self.entries["semester"].get()
            ipk = self.entries["ipk"].get()
            status = self.status_var.get()
            
            # Validasi Regex
            self.validator.validate_nama(nama)
            self.validator.validate_jurusan(jurusan)
            self.validator.validate_semester(semester)
            self.validator.validate_ipk(ipk)
            
            new_data = {
                "nama": nama,
                "jurusan": jurusan,
                "semester": int(semester),
                "ipk": float(ipk),
                "status": status
            }
            if self.manager.updateStudent(nim_target, new_data):
                self.file_manager.saveToFile(self.manager.getAllStudents())
                self.refresh_table()
                self.clear_form()
                messagebox.showinfo("Success", "Student data updated!")
            else:
                messagebox.showerror("Error", "Student not found!")
        except DataValidationError as e:
            messagebox.showerror("Validasi Gagal", str(e))
        except Exception as e: 
            messagebox.showerror("Error", str(e))

    def delete_student(self):
        selected = self.tree.selection()
        if not selected: return
        nim = str(self.tree.item(selected[0])['values'][0]).zfill(10)
        if messagebox.askyesno("Confirm", "Delete this student?"):
            try:
                if self.manager.removeStudent(nim):
                    self.file_manager.saveToFile(self.manager.getAllStudents())
                    self.refresh_table()
                    self.clear_form()
                    messagebox.showinfo("Success", "Student deleted!")
            except Exception as e:
                messagebox.showerror("Error", str(e))

    def search_student(self):
        query = self.search_entry.get()
        if not query: return
        
        method = self.search_method_var.get()
        
        # Coba pencarian dengan cache
        (res, iters), iters_val, cached = self.manager.search_with_cache(query, "nim", method)
        if res == -1:
            (res, iters), iters_val, cached = self.manager.search_with_cache(query, "nama", method)
        
        if res != -1:
            students = self.manager.getAllStudents()
            self.refresh_table([students[res]])
            msg = "CACHED HIT!" if cached else f"Iterasi: {iters_val} ({method.upper()})"
            self.status_label.configure(text=f"Search: {msg} | Ditemukan 1 data")
        else:
            messagebox.showinfo("Not Found", "Student not found")

    def sort_table(self, key):
        students = self.manager.getAllStudents()
        if not students: return
        
        algo = self.sort_algo_var.get()
        if algo == "Bubble Sort":
            comp, swaps, dur = SortEngine.bubbleSort(students, key)
        elif algo == "Insertion Sort":
            comp, swaps, dur = SortEngine.insertionSort(students, key)
        else:
            comp, swaps, dur = SortEngine.mergeSort(students, key)
            
        self.manager.linked_list.from_list(students)
        self.refresh_table()
        self.status_label.configure(text=f"Urut by {key.upper()} | {algo} | Comp: {comp}, Swaps: {swaps} | Waktu: {dur:.6f}s")

    def on_tree_select(self, event):
        selected = self.tree.selection()
        if not selected: return
        vals = self.tree.item(selected[0])['values']
        for i, f in enumerate(["nim", "nama", "jurusan", "semester", "ipk"]):
            self.entries[f].delete(0, "end")
            self.entries[f].insert(0, vals[i])
        if len(vals) >= 6:
            self.status_var.set(vals[5])

    def clear_form(self):
        for e in self.entries.values(): 
            e.delete(0, "end")
        self.status_var.set("Aktif")

if __name__ == "__main__":
    app = ModernGUI()
    app.mainloop()

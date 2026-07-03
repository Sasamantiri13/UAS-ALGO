import tkinter as tk
from tkinter import ttk, messagebox
from models import MahasiswaAktif, MahasiswaNonAktif
from manager import MahasiswaManager, SortEngine, SearchEngine
from file_manager import FileManager
from validator import Validator, DataValidationError
from auth import AuthManager

class LoginWindow:
    def __init__(self, root, on_success):
        self.root = root
        self.on_success = on_success
        self.auth = AuthManager()
        
        self.root.title("Login Admin")
        self.root.geometry("300x200")
        self.root.resizable(False, False)
        
        frame = ttk.Frame(root, padding=20)
        frame.pack(expand=True)
        
        ttk.Label(frame, text="Username:").pack(fill=tk.X)
        self.u_entry = ttk.Entry(frame)
        self.u_entry.pack(fill=tk.X, pady=(0,10))
        self.u_entry.insert(0, "admin")
        
        ttk.Label(frame, text="Password:").pack(fill=tk.X)
        self.p_entry = ttk.Entry(frame, show="*")
        self.p_entry.pack(fill=tk.X, pady=(0,15))
        self.p_entry.insert(0, "admin123")
        
        ttk.Button(frame, text="Login", command=self.handle_login).pack(fill=tk.X)
        self.root.bind('<Return>', lambda e: self.handle_login())

    def handle_login(self):
        u = self.u_entry.get()
        p = self.p_entry.get()
        if self.auth.login(u, p):
            self.on_success()
        else:
            messagebox.showerror("Login Gagal", "Username atau password salah!")

class StudentGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistem Manajemen Data Mahasiswa")
        self.root.geometry("1000x600")
        
        # Backend Integration
        self.file_manager = FileManager()
        self.manager = MahasiswaManager(self.file_manager.loadFromFile())
        self.validator = Validator()
        
        self.setup_ui()
        self.refresh_table()

    def setup_ui(self):
        # Style
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", rowheight=25)
        
        # --- LEFT PANEL: INPUT FORM ---
        left_frame = ttk.LabelFrame(self.root, text=" Form Input Mahasiswa ", padding=10)
        left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)
        
        fields = [("NIM", "nim"), ("Nama", "nama"), ("Jurusan", "jurusan"), 
                  ("Semester", "semester"), ("IPK", "ipk")]
        self.entries = {}
        
        for i, (label_text, attr) in enumerate(fields):
            ttk.Label(left_frame, text=label_text).grid(row=i*2, column=0, sticky=tk.W, pady=(5,0))
            entry = ttk.Entry(left_frame, width=30)
            entry.grid(row=i*2+1, column=0, pady=(0,5))
            self.entries[attr] = entry
            
        ttk.Label(left_frame, text="Status").grid(row=10, column=0, sticky=tk.W, pady=(5,0))
        self.status_var = tk.StringVar(value="Aktif")
        status_cb = ttk.Combobox(left_frame, textvariable=self.status_var, values=["Aktif", "Non-Aktif"], state="readonly")
        status_cb.grid(row=11, column=0, pady=(0,15))
        
        btn_frame = ttk.Frame(left_frame)
        btn_frame.grid(row=12, column=0, pady=10)
        
        ttk.Button(btn_frame, text="Tambah", command=self.add_student).pack(side=tk.LEFT, padx=2)
        ttk.Button(btn_frame, text="Update", command=self.update_student).pack(side=tk.LEFT, padx=2)
        ttk.Button(btn_frame, text="Hapus", command=self.delete_student).pack(side=tk.LEFT, padx=2)
        ttk.Button(left_frame, text="Bersihkan Form", command=self.clear_form).grid(row=13, column=0, sticky=tk.EW, pady=5)

        # --- RIGHT PANEL: TABLE & SEARCH ---
        right_frame = ttk.Frame(self.root, padding=10)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Search Bar
        search_frame = ttk.Frame(right_frame)
        search_frame.pack(fill=tk.X, pady=(0,10))
        
        ttk.Label(search_frame, text="Cari:").pack(side=tk.LEFT, padx=5)
        self.search_entry = ttk.Entry(search_frame, width=15)
        self.search_entry.pack(side=tk.LEFT, padx=5)
        
        self.search_by = tk.StringVar(value="nim_binary")
        ttk.Radiobutton(search_frame, text="NIM (Binary)", variable=self.search_by, value="nim_binary").pack(side=tk.LEFT)
        ttk.Radiobutton(search_frame, text="Nama (Linear)", variable=self.search_by, value="nama_linear").pack(side=tk.LEFT)
        ttk.Radiobutton(search_frame, text="DLL (Sequential)", variable=self.search_by, value="sequential").pack(side=tk.LEFT)
        
        ttk.Button(search_frame, text="Cari", command=self.search_student).pack(side=tk.LEFT, padx=5)
        ttk.Button(search_frame, text="Reset", command=self.refresh_table).pack(side=tk.LEFT, padx=5)
        
        # Sort Algo Selector
        ttk.Label(search_frame, text="  Sort:").pack(side=tk.LEFT, padx=5)
        self.sort_algo = tk.StringVar(value="Merge Sort")
        self.sort_combo = ttk.Combobox(search_frame, textvariable=self.sort_algo, values=["Bubble Sort", "Insertion Sort", "Merge Sort"], state="readonly", width=12)
        self.sort_combo.pack(side=tk.LEFT, padx=5)

        # Table
        columns = ("nim", "nama", "jurusan", "semester", "ipk", "status")
        self.tree = ttk.Treeview(right_frame, columns=columns, show="headings")
        
        for col in columns:
            self.tree.heading(col, text=col.upper(), command=lambda c=col: self.sort_table(c))
            self.tree.column(col, width=100)
            
        self.tree.pack(fill=tk.BOTH, expand=True)
        self.tree.bind("<<TreeviewSelect>>", self.on_tree_select)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(self.tree, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Footer
        self.status_bar = ttk.Label(right_frame, text="Total Mahasiswa: 0 | Kompleksitas Terakhir: -", relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(fill=tk.X, pady=(5,0))

    def refresh_table(self, data_list=None):
        # Clear table
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        students = data_list if data_list is not None else self.manager.getAllStudents()
        for s in students:
            # s.status diakses secara Polimorfik
            self.tree.insert("", tk.END, values=(s.nim, s.nama, s.jurusan, s.semester, f"{s.ipk:.2f}", s.status))
            
        self.status_bar.config(text=f"Total Mahasiswa: {len(students)} (Storage: Doubly Linked List)")

    def add_student(self):
        try:
            nim = self.entries["nim"].get()
            nama = self.entries["nama"].get()
            jurusan = self.entries["jurusan"].get()
            semester = self.entries["semester"].get()
            ipk = self.entries["ipk"].get()
            status = self.status_var.get()
            
            # Validasi Regex untuk semua field (Regex Validation)
            self.validator.validate_nim(nim)
            self.validator.validate_nama(nama)
            self.validator.validate_jurusan(jurusan)
            self.validator.validate_semester(semester)
            self.validator.validate_ipk(ipk)
            
            # Cek Duplikasi NIM
            idx, _ = SearchEngine.sequentialSearch(self.manager.linked_list, nim, "nim")
            if idx != -1:
                messagebox.showerror("Error", "NIM sudah terdaftar!")
                return
            
            if status == "Aktif":
                mhs = MahasiswaAktif(nim, nama, jurusan, int(semester), float(ipk))
            else:
                mhs = MahasiswaNonAktif(nim, nama, jurusan, int(semester), float(ipk))
                
            self.manager.addStudent(mhs)
            self.file_manager.saveToFile(self.manager.getAllStudents())
            self.refresh_table()
            self.clear_form()
            messagebox.showinfo("Sukses", "Data mahasiswa berhasil ditambahkan!")
        except DataValidationError as e:
            messagebox.showerror("Validasi Gagal", str(e))
        except Exception as e:
            messagebox.showerror("Error", f"Terjadi kesalahan: {e}")

    def update_student(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Peringatan", "Pilih data di tabel yang ingin diupdate!")
            return
            
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
                messagebox.showinfo("Sukses", "Data berhasil diupdate!")
            else:
                messagebox.showerror("Error", "Gagal mengupdate: Mahasiswa tidak ditemukan.")
        except DataValidationError as e:
            messagebox.showerror("Validasi Gagal", str(e))
        except Exception as e:
            messagebox.showerror("Error", f"Gagal update: {e}")

    def delete_student(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Peringatan", "Pilih data di tabel yang ingin dihapus!")
            return
            
        nim = str(self.tree.item(selected[0])['values'][0]).zfill(10)
        if messagebox.askyesno("Konfirmasi", f"Apakah Anda yakin ingin menghapus mahasiswa NIM {nim}?"):
            try:
                if self.manager.removeStudent(nim):
                    self.file_manager.saveToFile(self.manager.getAllStudents())
                    self.refresh_table()
                    self.clear_form()
                    messagebox.showinfo("Sukses", "Data mahasiswa berhasil dihapus!")
                else:
                    messagebox.showerror("Error", "Mahasiswa tidak ditemukan.")
            except Exception as e:
                messagebox.showerror("Error", f"Gagal menghapus: {e}")

    def search_student(self):
        val = self.search_entry.get()
        method = self.search_by.get()
        students = self.manager.getAllStudents()
        
        if not val:
            messagebox.showwarning("Peringatan", "Masukkan kata kunci pencarian!")
            return

        if method == "nim_binary":
            idx, iters = SearchEngine.binarySearch(students, val, "nim")
            algo = "Binary Search (O(log n))"
        elif method == "nama_linear":
            idx, iters = SearchEngine.linearSearch(students, val, "nama")
            algo = "Linear Search (O(n))"
        elif method == "sequential":
            # Sequential search directly on Linked List
            idx, iters = SearchEngine.sequentialSearch(self.manager.linked_list, val, "nim")
            algo = "Sequential DLL Search (O(n))"
            if idx == -1:
                idx2, iters2 = SearchEngine.sequentialSearch(self.manager.linked_list, val, "nama")
                iters += iters2
                if idx2 != -1:
                    idx = idx2
        else:
            return
            
        if idx != -1:
            # Polimorfisme: data list dikonversi untuk tampilan pencarian tunggal
            # Tetap mengambil data dari students list yang sesuai indeks
            found_list = [students[idx]]
            self.refresh_table(found_list)
            self.status_bar.config(text=f"Ditemukan 1 data | Iterasi: {iters} | Algo: {algo}")
        else:
            messagebox.showinfo("Info", "Data tidak ditemukan.")
            self.refresh_table([])

    def sort_table(self, key):
        students = self.manager.getAllStudents()
        if not students: return
        
        algo_name = self.sort_algo.get()
        if algo_name == "Bubble Sort":
            comp, swaps, dur = SortEngine.bubbleSort(students, key)
            algo = "Bubble Sort (O(n²))"
        elif algo_name == "Insertion Sort":
            comp, swaps, dur = SortEngine.insertionSort(students, key)
            algo = "Insertion Sort (O(n²))"
        else:
            comp, swaps, dur = SortEngine.mergeSort(students, key)
            algo = "Merge Sort (O(n log n))"
            
        # Rebuild Linked List dari hasil sorting untuk sinkronisasi state
        self.manager.linked_list.from_list(students)
        self.refresh_table()
        self.status_bar.config(text=f"Urut by {key} | Comp: {comp}, Swaps: {swaps} | Waktu: {dur:.6f}s | Algo: {algo}")

    def on_tree_select(self, event):
        selected = self.tree.selection()
        if not selected: return
        
        values = self.tree.item(selected[0])['values']
        self.entries["nim"].delete(0, tk.END)
        self.entries["nim"].insert(0, values[0])
        self.entries["nama"].delete(0, tk.END)
        self.entries["nama"].insert(0, values[1])
        self.entries["jurusan"].delete(0, tk.END)
        self.entries["jurusan"].insert(0, values[2])
        self.entries["semester"].delete(0, tk.END)
        self.entries["semester"].insert(0, values[3])
        self.entries["ipk"].delete(0, tk.END)
        self.entries["ipk"].insert(0, values[4])
        if len(values) >= 6:
            self.status_var.set(values[5])

    def clear_form(self):
        for entry in self.entries.values():
            entry.delete(0, tk.END)
        self.status_var.set("Aktif")

if __name__ == "__main__":
    def start_main_app():
        for widget in root.winfo_children():
            widget.destroy()
        app = StudentGUI(root)

    root = tk.Tk()
    login = LoginWindow(root, start_main_app)
    root.mainloop()

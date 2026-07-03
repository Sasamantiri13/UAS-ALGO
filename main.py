import sys
from models import MahasiswaAktif, MahasiswaNonAktif
from manager import MahasiswaManager, SortEngine, SearchEngine
from file_manager import FileManager
from validator import Validator, DataValidationError
from auth import AuthManager
from utils import Utils

class StudentApp:
    def __init__(self):
        self.file_manager = FileManager()
        self.manager = MahasiswaManager(self.file_manager.loadFromFile())
        self.validator = Validator()

    def print_menu(self):
        Utils.print_header("SISTEM MANAJEMEN MAHASISWA")
        print(" 1. Tambah Data")
        print(" 2. Tampilkan Seluruh Data")
        print(" 3. Edit Data (by NIM)")
        print(" 4. Hapus Data (by NIM)")
        print(" 5. Cari Mahasiswa (NIM/Nama)")
        print(" 6. Urutkan Data (NIM/Nama/IPK)")
        print(" 7. Simpan Data ke CSV")
        print(" 8. Load Data dari CSV")
        print(" 9. Bantuan & Statistik Kompleksitas")
        print(" 10. Keluar")
        print("=" * 50)

    def tambah_data(self):
        try:
            print("\n[+] TAMBAH DATA MAHASISWA")
            nim = input("Masukkan NIM (10 digit): ")
            self.validator.validate_nim(nim)
            
            # Cek duplikasi NIM menggunakan Sequential Search di Linked List
            idx, _ = SearchEngine.sequentialSearch(self.manager.linked_list, nim, "nim")
            if idx != -1:
                print("\n[!] Error: NIM sudah terdaftar!")
                return

            nama = input("Masukkan Nama: ")
            self.validator.validate_nama(nama)

            jurusan = input("Masukkan Jurusan: ")
            self.validator.validate_jurusan(jurusan)
            
            semester = input("Masukkan Semester (1-14): ")
            self.validator.validate_semester(semester)
            
            ipk = input("Masukkan IPK (0.00 - 4.00): ")
            self.validator.validate_ipk(ipk)

            status = input("Status (Aktif/Non): ").lower()
            if status == "non" or status == "non-aktif":
                mhs = MahasiswaNonAktif(nim, nama, jurusan, int(semester), float(ipk))
            else:
                mhs = MahasiswaAktif(nim, nama, jurusan, int(semester), float(ipk))

            self.manager.addStudent(mhs)
            print("\n[OK] Data mahasiswa berhasil ditambahkan!")
            
            # Auto-save setelah mutasi data
            self.file_manager.saveToFile(self.manager.getAllStudents())
        except DataValidationError as e:
            print(f"\n[!] Validasi Gagal: {e}")
        except Exception as e:
            print(f"\n[!] Terjadi kesalahan: {e}")

    def tampilkan_data(self):
        students = self.manager.getAllStudents()
        if not students:
            print("\n[!] Data mahasiswa kosong!")
            return

        print("\n" + "-" * 90)
        print("{:<12} | {:<20} | {:<15} | {:<5} | {:<5} | {:<10}".format("NIM", "Nama", "Jurusan", "Sem", "IPK", "Status"))
        print("-" * 90)
        for s in students:
            # Polimorfisme: Memanggil s.status (getter) dan s.ipk desimal terformat
            print("{:<12} | {:<20} | {:<15} | {:<5} | {:<5.2f} | {:<10}".format(s.nim, s.nama, s.jurusan, s.semester, s.ipk, s.status))
        print("-" * 90)
        print(f"Total Data: {len(students)}")

    def edit_data(self):
        nim = input("\nMasukkan NIM mahasiswa yang akan diedit: ")
        students = self.manager.getAllStudents()
        # Pencarian NIM menggunakan Sequential Search di Linked List
        idx, _ = SearchEngine.sequentialSearch(self.manager.linked_list, nim, "nim")
        
        if idx == -1:
            print("\n[!] Mahasiswa dengan NIM tersebut tidak ditemukan!")
            return

        print("\n--- Data Saat Ini ---")
        students[idx].tampilkanInfo() # Polimorfisme dalam aksi
        
        try:
            print("\n--- Masukkan Data Baru (Tekan Enter untuk lewati) ---")
            nama = input(f"Nama [{students[idx].nama}]: ")
            if nama: self.validator.validate_nama(nama)
            
            jurusan = input(f"Jurusan [{students[idx].jurusan}]: ")
            if jurusan: self.validator.validate_jurusan(jurusan)
            
            semester = input(f"Semester [{students[idx].semester}]: ")
            if semester: self.validator.validate_semester(semester)
            
            ipk = input(f"IPK [{students[idx].ipk:.2f}]: ")
            if ipk: self.validator.validate_ipk(ipk)

            status = input(f"Status [{students[idx].status} - Aktif/Non]: ").lower()

            new_data = {}
            if nama: new_data["nama"] = nama
            if jurusan: new_data["jurusan"] = jurusan
            if semester: new_data["semester"] = int(semester)
            if ipk: new_data["ipk"] = float(ipk)
            if status:
                new_data["status"] = "Non-Aktif" if (status == "non" or status == "non-aktif") else "Aktif"

            if new_data:
                if self.manager.updateStudent(nim, new_data):
                    print("\n[OK] Data berhasil diupdate!")
                    self.file_manager.saveToFile(self.manager.getAllStudents())
            else:
                print("\n[~] Tidak ada perubahan data.")
        except DataValidationError as e:
            print(f"\n[!] Update gagal: {e}")
        except Exception as e:
            print(f"\n[!] Terjadi kesalahan: {e}")

    def hapus_data(self):
        nim = input("\nMasukkan NIM mahasiswa yang akan dihapus: ")
        # Konfirmasi
        confirm = input(f"Apakah Anda yakin ingin menghapus data NIM {nim}? (y/n): ")
        if confirm.lower() == 'y':
            if self.manager.removeStudent(nim):
                print("\n[OK] Data mahasiswa berhasil dihapus!")
                self.file_manager.saveToFile(self.manager.getAllStudents())
            else:
                print("\n[!] Mahasiswa tidak ditemukan!")

    def cari_mahasiswa(self):
        print("\n--- METODE PENCARIAN ---")
        print("1. Berdasarkan NIM (Binary Search - O(log n))")
        print("2. Berdasarkan Nama (Linear Search - O(n))")
        print("3. Berdasarkan NIM/Nama (Sequential Search di Doubly Linked List - O(n))")
        pilihan = input("Pilih (1/2/3): ")
        
        students = self.manager.getAllStudents()
        if not students:
            print("\n[!] Data kosong!")
            return

        if pilihan == "1":
            nim = input("Masukkan NIM yang dicari: ")
            print("\n[*] Melakukan Binary Search (mengurutkan data NIM terlebih dahulu)...")
            idx, iters = SearchEngine.binarySearch(students, nim, "nim")
            self._print_search_result(idx, iters, students)
        elif pilihan == "2":
            nama = input("Masukkan Nama yang dicari: ")
            print("\n[*] Melakukan Linear Search...")
            idx, iters = SearchEngine.linearSearch(students, nama, "nama")
            self._print_search_result(idx, iters, students)
        elif pilihan == "3":
            key_choice = input("Cari berdasarkan (1. NIM / 2. Nama): ")
            key = "nim" if key_choice == "1" else "nama"
            val = input(f"Masukkan {key.upper()} yang dicari: ")
            print(f"\n[*] Melakukan Sequential Search langsung di Doubly Linked List...")
            idx, iters = SearchEngine.sequentialSearch(self.manager.linked_list, val, key)
            self._print_search_result(idx, iters, students)
        else:
            print("\n[!] Pilihan tidak valid!")

    def _print_search_result(self, idx, iters, students):
        if idx != -1:
            print(f"\n[OK] Data ditemukan pada indeks ke-{idx}")
            print(f"[*] Jumlah iterasi: {iters}")
            print("-" * 30)
            students[idx].tampilkanInfo()
            print("-" * 30)
        else:
            print(f"\n[!] Data tidak ditemukan setelah {iters} iterasi.")

    def urutkan_data(self):
        print("\n--- METODE PENGURUTAN ---")
        print("1. NIM (Bubble Sort - O(n²))")
        print("2. NIM (Insertion Sort - O(n²))")
        print("3. Nama (Merge Sort - O(n log n))")
        print("4. IPK (Merge Sort - O(n log n))")
        pilihan = input("Pilih (1/2/3/4): ")
        
        students = self.manager.getAllStudents()
        if not students:
            print("\n[!] Data kosong!")
            return

        comp = swaps = dur = 0
        method = ""

        if pilihan == "1":
            comp, swaps, dur = SortEngine.bubbleSort(students, "nim")
            method = "Bubble Sort"
        elif pilihan == "2":
            comp, swaps, dur = SortEngine.insertionSort(students, "nim")
            method = "Insertion Sort"
        elif pilihan == "3":
            comp, swaps, dur = SortEngine.mergeSort(students, "nama")
            method = "Merge Sort"
        elif pilihan == "4":
            comp, swaps, dur = SortEngine.mergeSort(students, "ipk")
            method = "Merge Sort"
        else:
            print("\n[!] Pilihan tidak valid!")
            return

        print(f"\n[OK] Berhasil diurutkan menggunakan {method}!")
        print(f"[*] Statistik Eksekusi:")
        print(f"    - Perbandingan : {comp}")
        print(f"    - Penukaran/Move: {swaps}")
        print(f"    - Waktu        : {dur:.6f} detik")
        print(f"    - Kompleksitas : {Utils.get_complexity_info()[method]['Complexity']}")

    def tampilkan_bantuan(self):
        Utils.print_header("BANTUAN & KOMPLEKSITAS")
        info = Utils.get_complexity_info()
        for algo, detail in info.items():
            print(f"\n> {algo} ({detail['Complexity']})")
            print(f"  {detail['Explanation']}")
        print("\n" + "=" * 50)
        input("Tekan Enter untuk kembali ke menu...")

    def run(self):
        # Login
        auth = AuthManager()
        Utils.print_header("LOGIN ADMIN")
        attempts = 3
        while attempts > 0:
            u = input("Username: ")
            p = input("Password: ")
            if auth.login(u, p):
                print("\n[OK] Login Berhasil!")
                break
            else:
                attempts -= 1
                print(f"\n[!] Login Gagal! Sisa percobaan: {attempts}")
                if attempts == 0:
                    print("[!] Akses ditolak.")
                    sys.exit()

        # Auto-load on start
        Utils.clear_screen()
        print("[*] Aplikasi Manajemen Data Mahasiswa Siap.")
        
        while True:
            self.print_menu()
            pilihan = input("Pilih menu (1-10): ")
            
            if pilihan == '1': self.tambah_data()
            elif pilihan == '2': self.tampilkan_data()
            elif pilihan == '3': self.edit_data()
            elif pilihan == '4': self.hapus_data()
            elif pilihan == '5': self.cari_mahasiswa()
            elif pilihan == '6': self.urutkan_data()
            elif pilihan == '7': self.file_manager.saveToFile(self.manager.getAllStudents())
            elif pilihan == '8': 
                self.manager.students = self.file_manager.loadFromFile()
                print("\n[OK] Data berhasil di-load!")
            elif pilihan == '9': self.tampilkan_bantuan()
            elif pilihan == '10':
                print("\n[*] Menutup aplikasi. Sampai jumpa!")
                sys.exit()
            else:
                print("\n[!] Pilihan tidak tersedia, silakan coba lagi.")

if __name__ == "__main__":
    app = StudentApp()
    app.run()

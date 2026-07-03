from manager import MahasiswaManager, SortEngine, SearchEngine
from models import MahasiswaAktif, MahasiswaNonAktif
from validator import Validator, DataValidationError

def demo():
    print("=== DEMO SIMULASI SISTEM MANAJEMEN MAHASISWA ===\n")
    
    manager = MahasiswaManager()
    validator = Validator()
    
    # 1. Tambah Data (Polimorfisme: Aktif & Non-Aktif)
    print("[1] MENAMBAHKAN DATA MAHASISWA (Penerapan OOP & Polimorfisme)")
    students_to_add = [
        ("2101234567", "Budi Santoso", "Informatika", 4, 3.85, "Aktif"),
        ("2101234560", "Andi Wijaya", "Sistem Informasi", 2, 3.90, "Aktif"),
        ("2101234569", "Citra Lestari", "Teknik Elektro", 6, 3.70, "Non-Aktif")
    ]
    
    for nim, nama, jur, sem, ipk, status in students_to_add:
        if status == "Non-Aktif":
            mhs = MahasiswaNonAktif(nim, nama, jur, sem, ipk)
        else:
            mhs = MahasiswaAktif(nim, nama, jur, sem, ipk)
        manager.addStudent(mhs)
        print(f"[OK] Menambahkan: {nama} ({nim}) | Status: {mhs.status}")

    # 2. Tampilkan Data Awal
    print("\n[2] TAMPILAN DATA AWAL (Polimorfisme tampilkanInfo())")
    print("-" * 50)
    for s in manager.getAllStudents():
        s.tampilkanInfo() # Polimorfisme memanggil metode spesifik masing-masing kelas
        print("-" * 30)

    # 3. Pengurutan (Insertion Sort by NIM)
    print("\n[3] PENGURUTAN BERDASARKAN NIM (Insertion Sort)")
    students_list = manager.getAllStudents()
    comp, swaps, dur = SortEngine.insertionSort(students_list, "nim")
    print(f"[*] Hasil Pengurutan (NIM ascending):")
    for s in students_list:
         print(f"    {s.nim} | {s.nama} | IPK: {s.ipk:.2f}")
    print(f"[*] Statistik Insertion Sort: {comp} Perbandingan, {swaps} Pergeseran, Waktu: {dur:.6f} detik")

    # 4. Pencarian (Sequential Search langsung pada Doubly Linked List)
    search_nim = "2101234560"
    print(f"\n[4] PENCARIAN NIM {search_nim} (Sequential Search langsung di Doubly Linked List)")
    idx, iters = SearchEngine.sequentialSearch(manager.linked_list, search_nim, "nim")
    if idx != -1:
        found = manager.getAllStudents()[idx]
        print(f"[OK] Ditemukan pada urutan ke-{idx} setelah menelusuri {iters} node Linked List.")
        found.tampilkanInfo()
    else:
        print("[!] Data tidak ditemukan.")

    # 5. Validasi Menggunakan Regex & Exception Handling (Try-Catch)
    print("\n[5] SIMULASI VALIDASI INPUT DENGAN REGEX & TRY-EXCEPT")
    invalid_inputs = [
        ("NIM Salah", "12345abcde"), # NIM harus 10 digit angka
        ("IPK Salah", "4.20"),       # IPK max 4.00
        ("Semester Salah", "15")     # Semester max 14
    ]
    
    for label, val in invalid_inputs:
        try:
            print(f"[*] Mencoba validasi {label}: '{val}'")
            if "NIM" in label:
                validator.validate_nim(val)
            elif "IPK" in label:
                validator.validate_ipk(val)
            elif "Semester" in label:
                validator.validate_semester(val)
        except DataValidationError as e:
            print(f"    [Try-Except Berhasil] Validasi gagal didekteksi: {e}")

if __name__ == "__main__":
    demo()

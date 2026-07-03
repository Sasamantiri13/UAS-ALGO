from manager import MahasiswaManager, SearchEngine
from file_manager import FileManager

def run_search_check():
    # Load data dari CSV ke dalam manager (Linked List)
    fm = FileManager()
    manager = MahasiswaManager(fm.loadFromFile())
    students = manager.getAllStudents()

    print("==================================================")
    print("      HASIL PENGUJIAN FUNGSI PENCARIAN            ")
    print("==================================================")
    print(f"Jumlah data mahasiswa saat ini: {len(students)}\n")

    # 1. Pengujian Binary Search (Berdasarkan NIM)
    val_nim = "2101234564" # NIM Eko Prasetyo
    print(f"[1] Mencari NIM '{val_nim}' dengan Binary Search (O(log n)):")
    idx_bin, iter_bin = SearchEngine.binarySearch(students, val_nim, "nim")
    if idx_bin != -1:
        print(f"    -> Berhasil ditemukan pada indeks list ke-{idx_bin} (Iterasi: {iter_bin})")
        students[idx_bin].tampilkanInfo()
    else:
        print("    -> Gagal ditemukan!")
    print("-" * 50)

    # 2. Pengujian Linear Search (Berdasarkan Nama)
    val_nama = "Dewi Sartika"
    print(f"[2] Mencari Nama '{val_nama}' dengan Linear Search (O(n)):")
    idx_lin, iter_lin = SearchEngine.linearSearch(students, val_nama, "nama")
    if idx_lin != -1:
        print(f"    -> Berhasil ditemukan pada indeks list ke-{idx_lin} (Iterasi: {iter_lin})")
        students[idx_lin].tampilkanInfo()
    else:
        print("    -> Gagal ditemukan!")
    print("-" * 50)

    # 3. Pengujian Sequential Search (Berdasarkan Nama langsung pada Doubly Linked List)
    val_seq = "Farhan Halim"
    print(f"[3] Mencari Nama '{val_seq}' dengan Sequential DLL Search (O(n)):")
    idx_seq, iter_seq = SearchEngine.sequentialSearch(manager.linked_list, val_seq, "nama")
    if idx_seq != -1:
        print(f"    -> Berhasil ditemukan pada node ke-{idx_seq} di Linked List (Iterasi: {iter_seq})")
        # Telusuri secara manual untuk mengambil node data
        current = manager.linked_list.head
        for _ in range(idx_seq):
            current = current.next
        current.data.tampilkanInfo()
    else:
        print("    -> Gagal ditemukan!")
    print("==================================================")

if __name__ == "__main__":
    run_search_check()

import os
import sys
from models import Person, Mahasiswa, MahasiswaAktif, MahasiswaNonAktif
from validator import Validator, DataValidationError
from file_manager import FileManager
from manager import MahasiswaManager, SortEngine, SearchEngine
from utils import Utils

def run_tests():
    print("==================================================")
    print("     INTEGRATION TEST & VALIDATION SUITE          ")
    print("==================================================")

    # 1. OOP & Polimorfisme Verification
    print("\n[1] Verifikasi OOP, Enkapsulasi, Pewarisan, Polimorfisme...")
    m_aktif = MahasiswaAktif("1234567890", "Test Aktif", "Informatika", 4, 3.80)
    m_non = MahasiswaNonAktif("0987654321", "Test Non-Aktif", "Sistem Informasi", 6, 3.20)
    
    # Assert inheritance
    assert isinstance(m_aktif, Mahasiswa), "MahasiswaAktif harus turunan dari Mahasiswa!"
    assert isinstance(m_aktif, Person), "MahasiswaAktif harus turunan dari Person!"
    assert isinstance(m_non, Mahasiswa), "MahasiswaNonAktif harus turunan dari Mahasiswa!"
    
    # Assert encapsulation (property getters & setters)
    assert m_aktif.nim == "1234567890"
    assert m_aktif.nama == "Test Aktif"
    assert m_aktif.jurusan == "Informatika"
    assert m_aktif.semester == 4
    assert m_aktif.ipk == 3.80
    assert m_aktif.status == "Aktif"
    
    m_aktif.nama = "Test Aktif Baru"
    assert m_aktif.nama == "Test Aktif Baru", "Setter nama gagal!"
    print("    -> OOP, Enkapsulasi, dan Pewarisan OK.")
    
    # Polymorphism method call check (visual check)
    print("    -> Polimorfisme Tampilkan Info:")
    m_aktif.tampilkanInfo()
    m_non.tampilkanInfo()
    
    # 2. Regex & Exception Handling Verification
    print("\n[2] Verifikasi Validasi Regex & Penanganan Error (Try-Catch)...")
    validator = Validator()
    
    # Valid Cases
    assert validator.validate_nim("1234567890")
    assert validator.validate_nama("Budi Santoso")
    assert validator.validate_jurusan("Teknik Elektro")
    assert validator.validate_semester("8")
    assert validator.validate_ipk("3.99")
    
    # Invalid Cases (Must raise DataValidationError)
    invalid_cases = [
        (validator.validate_nim, "123456789a", "NIM mengandung huruf"),
        (validator.validate_nim, "123456789", "NIM kurang dari 10 digit"),
        (validator.validate_nama, "Budi123", "Nama mengandung angka"),
        (validator.validate_jurusan, "J", "Jurusan kurang dari 2 karakter"),
        (validator.validate_semester, "0", "Semester nol"),
        (validator.validate_semester, "15", "Semester di atas 14"),
        (validator.validate_ipk, "4.01", "IPK di atas 4.00"),
        (validator.validate_ipk, "-0.5", "IPK negatif"),
        (validator.validate_ipk, "abc", "IPK bukan desimal")
    ]
    
    for func, val, desc in invalid_cases:
        try:
            func(val)
            assert False, f"Validasi seharusnya gagal untuk case: {desc} ({val})"
        except DataValidationError as e:
            print(f"    [OK] Error terdeteksi untuk '{val}' ({desc}): {e}")
            
    print("    -> Validasi Regex dan Exception Handling OK.")

    # 3. File I/O with Status Preservation Verification
    print("\n[3] Verifikasi File I/O dan Penyimpanan Status...")
    test_file = "test_mahasiswa_temp.csv"
    fm = FileManager(test_file)
    
    # Simpan data
    original_students = [m_aktif, m_non]
    fm.saveToFile(original_students)
    
    # Baca data kembali
    loaded_students = fm.loadFromFile()
    
    assert len(loaded_students) == 2, "Jumlah mahasiswa ter-load tidak sama!"
    assert loaded_students[0].nim == m_aktif.nim
    assert loaded_students[0].nama == m_aktif.nama
    assert loaded_students[0].status == "Aktif", "Status MahasiswaAktif tidak tersimpan/terbaca!"
    assert isinstance(loaded_students[0], MahasiswaAktif)
    
    assert loaded_students[1].nim == m_non.nim
    assert loaded_students[1].nama == m_non.nama
    assert loaded_students[1].status == "Non-Aktif", "Status MahasiswaNonAktif tidak tersimpan/terbaca!"
    assert isinstance(loaded_students[1], MahasiswaNonAktif)
    
    # Hapus file temporary
    if os.path.exists(test_file):
        os.remove(test_file)
    print("    -> File I/O dan Penyimpanan Status OK.")

    # 4. Search Algorithms Verification
    print("\n[4] Verifikasi Algoritma Pencarian (Linear, Binary, Sequential DLL)...")
    manager = MahasiswaManager()
    m1 = MahasiswaAktif("2101234561", "Andi", "TI", 2, 3.50)
    m2 = MahasiswaAktif("2101234562", "Budi", "SI", 4, 3.60)
    m3 = MahasiswaAktif("2101234563", "Chandra", "TE", 6, 3.70)
    manager.addStudent(m1)
    manager.addStudent(m2)
    manager.addStudent(m3)
    
    students_list = manager.getAllStudents()
    
    # Linear Search on List
    idx_l, iter_l = SearchEngine.linearSearch(students_list, "Budi", "nama")
    assert idx_l == 1
    assert iter_l == 2
    print(f"    -> Linear Search OK (Iterasi: {iter_l})")
    
    # Binary Search on List (requires sorting first)
    idx_b, iter_b = SearchEngine.binarySearch(students_list, "2101234563", "nim")
    assert idx_b == 2
    assert iter_b > 0
    print(f"    -> Binary Search OK (Iterasi: {iter_b})")
    
    # Sequential Search on Doubly Linked List node-by-node
    idx_s, iter_s = SearchEngine.sequentialSearch(manager.linked_list, "Andi", "nama")
    assert idx_s == 0
    assert iter_s == 1
    print(f"    -> Sequential Search (Linked List Pointer Traversal) OK (Iterasi: {iter_s})")

    # 5. Sort Algorithms Verification
    print("\n[5] Verifikasi Algoritma Pengurutan (Bubble, Insertion, Merge)...")
    
    # Bubble Sort Test
    data_bubble = [m3, m1, m2] # Unsorted: Chandra, Andi, Budi
    SortEngine.bubbleSort(data_bubble, "nama")
    assert [d.nama for d in data_bubble] == ["Andi", "Budi", "Chandra"], "Bubble Sort gagal!"
    print("    -> Bubble Sort OK.")
    
    # Insertion Sort Test
    data_insert = [m3, m1, m2]
    SortEngine.insertionSort(data_insert, "nama")
    assert [d.nama for d in data_insert] == ["Andi", "Budi", "Chandra"], "Insertion Sort gagal!"
    print("    -> Insertion Sort OK.")
    
    # Merge Sort Test
    data_merge = [m3, m1, m2]
    SortEngine.mergeSort(data_merge, "nama")
    assert [d.nama for d in data_merge] == ["Andi", "Budi", "Chandra"], "Merge Sort gagal!"
    print("    -> Merge Sort OK.")

    # 6. Time Complexity Info Verification
    print("\n[6] Verifikasi Estimasi Kompleksitas Waktu...")
    complexity = Utils.get_complexity_info()
    assert "Bubble Sort" in complexity
    assert "Insertion Sort" in complexity
    assert "Merge Sort" in complexity
    assert "Linear Search" in complexity
    assert "Sequential Search" in complexity
    assert "Binary Search" in complexity
    print("    -> Kompleksitas Waktu Terdaftar OK.")

    print("\n==================================================")
    print("   CONGRATULATIONS: ALL TESTS PASSED SUCCESSFULLY! ")
    print("==================================================")

if __name__ == "__main__":
    run_tests()

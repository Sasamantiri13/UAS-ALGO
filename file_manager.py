import csv
import os
from models import MahasiswaAktif, MahasiswaNonAktif

class FileManager:
    def __init__(self, filename="mahasiswa.csv"):
        self.filename = filename

    def saveToFile(self, studentList):
        """Menyimpan seluruh data mahasiswa dari linked list/array ke file CSV (File I/O)."""
        try:
            with open(self.filename, mode='w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                # Format baru: NIM,Nama,Jurusan,Semester,IPK,Status
                for s in studentList:
                    # s.status adalah properti yang diperoleh melalui Pewarisan/Enkapsulasi
                    writer.writerow([s.nim, s.nama, s.jurusan, s.semester, s.ipk, s.status])
            print(f"[OK] Data berhasil disimpan ke {self.filename}")
        except Exception as e:
            print(f"[!] Gagal menyimpan file: {e}")

    def loadFromFile(self):
        """Membaca data mahasiswa dari file CSV (File I/O) secara dinamis."""
        studentList = []
        if not os.path.exists(self.filename):
            return studentList

        try:
            with open(self.filename, mode='r', encoding='utf-8') as file:
                reader = csv.reader(file)
                for row in reader:
                    if row:
                        # Backward-compatibility: jika kolom status belum ada di file lama
                        if len(row) >= 6:
                            nim, nama, jurusan, semester, ipk, status = row[:6]
                        else:
                            nim, nama, jurusan, semester, ipk = row[:5]
                            status = "Aktif"
                        
                        # Polimorfisme: Instansiasi objek sesuai dengan kelas yang tepat
                        if status == "Non-Aktif" or status == "Non":
                            studentList.append(MahasiswaNonAktif(nim, nama, jurusan, int(semester), float(ipk)))
                        else:
                            studentList.append(MahasiswaAktif(nim, nama, jurusan, int(semester), float(ipk)))
            return studentList
        except FileNotFoundError:
            print("[!] File tidak ditemukan, memulai dengan data kosong.")
            return []
        except Exception as e:
            print(f"[!] Gagal membaca file: {e}")
            return []


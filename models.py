# ==============================================================================
# KONSEP OOP (Object-Oriented Programming) YANG DITERAPKAN:
# 1. Class & Object: Person, Mahasiswa, MahasiswaAktif, MahasiswaNonAktif adalah Class.
#    Instansiasi dari kelas-kelas ini di runtime menjadi Object.
# 2. Pewarisan (Inheritance): Mahasiswa mewarisi atribut/metode dari Person.
#    MahasiswaAktif & MahasiswaNonAktif mewarisi dari Mahasiswa.
# 3. Enkapsulasi (Encapsulation): Atribut diawali double underscore (__nama, __nim, dll)
#    bersifat private. Akses data dikontrol menggunakan decorator @property (getter/setter).
# 4. Polimorfisme (Polymorphism): Metode tampilkanInfo() didefinisikan ulang (override)
#    pada masing-masing sub-kelas untuk menghasilkan perilaku yang spesifik.
# ==============================================================================

class Person:
    def __init__(self, nama):
        self.__nama = nama

    @property
    def nama(self):
        """Enkapsulasi: Getter untuk nama"""
        return self.__nama

    @nama.setter
    def nama(self, value):
        """Enkapsulasi: Setter untuk nama"""
        self.__nama = value

    def tampilkanInfo(self):
        """Polimorfisme: Metode dasar untuk menampilkan informasi"""
        print(f"Nama: {self.__nama}")


class Mahasiswa(Person):
    def __init__(self, nim, nama, jurusan, semester, ipk):
        super().__init__(nama) # Pewarisan: memanggil konstruktor Person
        self.__nim = nim
        self.__jurusan = jurusan
        self.__semester = semester
        self.__ipk = ipk

    # Enkapsulasi: Getters
    @property
    def nim(self):
        return self.__nim

    @property
    def jurusan(self):
        return self.__jurusan

    @property
    def semester(self):
        return self.__semester

    @property
    def ipk(self):
        return self.__ipk

    # Enkapsulasi: Setters
    @nim.setter
    def nim(self, value):
        self.__nim = value

    @jurusan.setter
    def jurusan(self, value):
        self.__jurusan = value

    @semester.setter
    def semester(self, value):
        self.__semester = value

    @ipk.setter
    def ipk(self, value):
        self.__ipk = value

    def tampilkanInfo(self):
        """Polimorfisme: Meng-override tampilkanInfo dari kelas Person"""
        print(f"NIM: {self.__nim}")
        print(f"Nama: {self.nama}")
        print(f"Jurusan: {self.__jurusan}")
        print(f"Semester: {self.__semester}")
        print(f"IPK: {self.__ipk:.2f}")


class MahasiswaAktif(Mahasiswa):
    def __init__(self, nim, nama, jurusan, semester, ipk, status="Aktif"):
        super().__init__(nim, nama, jurusan, semester, ipk) # Pewarisan
        self.__status = status

    @property
    def status(self):
        """Enkapsulasi: Getter untuk status"""
        return self.__status

    @status.setter
    def status(self, value):
        """Enkapsulasi: Setter untuk status"""
        self.__status = value

    def tampilkanInfo(self):
        """Polimorfisme: Meng-override tampilkanInfo untuk Mahasiswa Aktif"""
        print("=== Data Mahasiswa Aktif ===")
        super().tampilkanInfo()
        print(f"Status: {self.__status}")


class MahasiswaNonAktif(Mahasiswa):
    def __init__(self, nim, nama, jurusan, semester, ipk, status="Non-Aktif"):
        super().__init__(nim, nama, jurusan, semester, ipk) # Pewarisan
        self.__status = status

    @property
    def status(self):
        """Enkapsulasi: Getter untuk status"""
        return self.__status

    @status.setter
    def status(self, value):
        """Enkapsulasi: Setter untuk status"""
        self.__status = value

    def tampilkanInfo(self):
        """Polimorfisme: Meng-override tampilkanInfo untuk Mahasiswa Non-Aktif"""
        print("=== Data Mahasiswa Non-Aktif ===")
        super().tampilkanInfo()
        print(f"Status: {self.__status}")


import re

class DataValidationError(Exception):
    """Custom exception untuk kesalahan validasi data mahasiswa (Exception Handling)."""
    pass

class Validator:
    @staticmethod
    def validate_nim(nim):
        # Regex: Hanya angka dan panjang tepat 10 digit
        pattern = r"^[0-9]{10}$"
        if not re.match(pattern, str(nim).strip()):
            raise DataValidationError("NIM tidak valid! Harus terdiri dari tepat 10 digit angka.")
        return True

    @staticmethod
    def validate_nama(nama):
        # Regex: Hanya huruf, spasi, dan tanda petik tunggal, panjang 2 hingga 50 karakter
        pattern = r"^[A-Za-z\s']{2,50}$"
        if not re.match(pattern, nama.strip()):
            raise DataValidationError("Nama tidak valid! Hanya boleh berisi huruf, spasi, dan petik ('), panjang 2-50 karakter.")
        return True

    @staticmethod
    def validate_jurusan(jurusan):
        # Regex: Huruf, spasi, tanda hubung (-), ampersand (&), panjang 2-50 karakter
        pattern = r"^[A-Za-z\s\-\&]{2,50}$"
        if not re.match(pattern, jurusan.strip()):
            raise DataValidationError("Jurusan tidak valid! Hanya boleh berisi huruf, spasi, '-', atau '&', panjang 2-50 karakter.")
        return True

    @staticmethod
    def validate_ipk(ipk):
        # Regex: Mencocokkan nilai desimal dari 0.00 hingga 4.00
        # Format desimal opsional (e.g., 3, 3.5, 3.85, 4, 4.00)
        pattern = r"^(?:[0-3](?:\.\d{1,2})?|4(?:\.0{1,2})?)$"
        if not re.match(pattern, str(ipk).strip()):
            raise DataValidationError("IPK tidak valid! Range harus antara 0.00 - 4.00 (maksimal 2 desimal).")
        return True

    @staticmethod
    def validate_semester(semester):
        # Regex: Mencocokkan angka bulat dari 1 sampai 14 (tanpa leading zero)
        pattern = r"^(?:[1-9]|1[0-4])$"
        if not re.match(pattern, str(semester).strip()):
            raise DataValidationError("Semester tidak valid! Harus berupa angka bulat antara 1 sampai 14.")
        return True


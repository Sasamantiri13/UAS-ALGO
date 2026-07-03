from flask import Flask, render_template, request, redirect, url_for, flash, session
from functools import wraps
import time

from models import MahasiswaAktif, MahasiswaNonAktif
from manager import MahasiswaManager, SortEngine, SearchEngine
from file_manager import FileManager
from validator import Validator, DataValidationError
from auth import AuthManager

app = Flask(__name__)
app.secret_key = 'super_secret_key_for_flask_session_uas_algo'

# Initialize File Manager and Load Data
import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
file_manager = FileManager(os.path.join(BASE_DIR, 'mahasiswa.csv'))
manager = MahasiswaManager(file_manager.loadFromFile())
validator = Validator()
auth_manager = AuthManager(os.path.join(BASE_DIR, 'users.txt'))

# --- Authentication Decorator ---
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logged_in' not in session:
            flash('Silakan login terlebih dahulu.', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# --- Routes ---

@app.route('/', methods=['GET', 'POST'])
def login():
    if 'logged_in' in session:
        return redirect(url_for('dashboard'))
        
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if auth_manager.login(username, password):
            session['logged_in'] = True
            session['username'] = username
            flash('Login berhasil!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Username atau password salah!', 'danger')
            
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('username', None)
    flash('Anda telah logout.', 'info')
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard():
    students = manager.getAllStudents()
    return render_template('dashboard.html', students=students)

@app.route('/tambah', methods=['GET', 'POST'])
@login_required
def tambah():
    if request.method == 'POST':
        nim = request.form.get('nim')
        nama = request.form.get('nama')
        jurusan = request.form.get('jurusan')
        semester = request.form.get('semester')
        ipk = request.form.get('ipk')
        status = request.form.get('status')
        
        try:
            validator.validate_nim(nim)
            # Cek duplikasi NIM
            idx, _ = SearchEngine.sequentialSearch(manager.linked_list, nim, "nim")
            if idx != -1:
                raise DataValidationError("NIM sudah terdaftar!")

            validator.validate_nama(nama)
            validator.validate_jurusan(jurusan)
            validator.validate_semester(semester)
            validator.validate_ipk(ipk)

            if status == "non" or status == "non-aktif":
                mhs = MahasiswaNonAktif(nim, nama, jurusan, int(semester), float(ipk))
            else:
                mhs = MahasiswaAktif(nim, nama, jurusan, int(semester), float(ipk))

            manager.addStudent(mhs)
            file_manager.saveToFile(manager.getAllStudents())
            flash('Data mahasiswa berhasil ditambahkan!', 'success')
            return redirect(url_for('dashboard'))
            
        except DataValidationError as e:
            flash(f'Validasi Gagal: {e}', 'danger')
        except Exception as e:
            flash(f'Terjadi kesalahan: {e}', 'danger')
            
    return render_template('tambah.html')

@app.route('/edit/<nim>', methods=['GET', 'POST'])
@login_required
def edit(nim):
    # Find student
    students = manager.getAllStudents()
    idx, _ = SearchEngine.sequentialSearch(manager.linked_list, nim, "nim")
    
    if idx == -1:
        flash('Mahasiswa tidak ditemukan!', 'danger')
        return redirect(url_for('dashboard'))
        
    student = students[idx]
    
    if request.method == 'POST':
        nama = request.form.get('nama')
        jurusan = request.form.get('jurusan')
        semester = request.form.get('semester')
        ipk = request.form.get('ipk')
        status = request.form.get('status')
        
        new_data = {}
        try:
            if nama:
                validator.validate_nama(nama)
                new_data["nama"] = nama
            if jurusan:
                validator.validate_jurusan(jurusan)
                new_data["jurusan"] = jurusan
            if semester:
                validator.validate_semester(semester)
                new_data["semester"] = int(semester)
            if ipk:
                validator.validate_ipk(ipk)
                new_data["ipk"] = float(ipk)
            if status:
                new_data["status"] = "Non-Aktif" if status in ["non", "non-aktif"] else "Aktif"
                
            if new_data:
                if manager.updateStudent(nim, new_data):
                    file_manager.saveToFile(manager.getAllStudents())
                    flash('Data berhasil diupdate!', 'success')
                    return redirect(url_for('dashboard'))
                else:
                    flash('Gagal mengupdate data.', 'danger')
            else:
                flash('Tidak ada perubahan data.', 'info')
                return redirect(url_for('dashboard'))
                
        except DataValidationError as e:
            flash(f'Update gagal: {e}', 'danger')
        except Exception as e:
            flash(f'Terjadi kesalahan: {e}', 'danger')

    return render_template('edit.html', student=student)

@app.route('/hapus/<nim>', methods=['POST'])
@login_required
def hapus(nim):
    if manager.removeStudent(nim):
        file_manager.saveToFile(manager.getAllStudents())
        flash(f'Data mahasiswa dengan NIM {nim} berhasil dihapus!', 'success')
    else:
        flash('Mahasiswa tidak ditemukan!', 'danger')
    return redirect(url_for('dashboard'))

@app.route('/cari', methods=['GET', 'POST'])
@login_required
def cari():
    result = None
    iters = 0
    stats = None
    
    if request.method == 'POST':
        metode = request.form.get('metode')
        kunci = request.form.get('kunci') # 'nim' or 'nama'
        nilai = request.form.get('nilai')
        
        students = manager.getAllStudents()
        if not students:
            flash('Data kosong!', 'warning')
        elif not nilai:
            flash('Nilai pencarian tidak boleh kosong!', 'warning')
        else:
            if metode == '1': # Binary Search (NIM)
                idx, iters = SearchEngine.binarySearch(students, nilai, "nim")
                metode_name = "Binary Search (NIM)"
            elif metode == '2': # Linear Search (Nama)
                idx, iters = SearchEngine.linearSearch(students, nilai, "nama")
                metode_name = "Linear Search (Nama)"
            elif metode == '3': # Sequential Search (NIM/Nama)
                idx, iters = SearchEngine.sequentialSearch(manager.linked_list, nilai, kunci)
                metode_name = f"Sequential Search ({kunci.upper()})"
            else:
                flash('Metode tidak valid!', 'danger')
                return render_template('cari.html')

            if idx != -1:
                result = students[idx]
                flash(f'Data ditemukan pada indeks ke-{idx}', 'success')
            else:
                flash(f'Data tidak ditemukan setelah {iters} iterasi.', 'danger')
                
            stats = {'metode': metode_name, 'iterasi': iters}

    return render_template('cari.html', result=result, stats=stats)

@app.route('/urutkan', methods=['GET', 'POST'])
@login_required
def urutkan():
    students = manager.getAllStudents()
    stats = None
    
    if request.method == 'POST':
        pilihan = request.form.get('pilihan')
        
        if not students:
            flash('Data kosong!', 'warning')
            return redirect(url_for('urutkan'))

        comp = swaps = dur = 0
        method = ""

        if pilihan == "1":
            comp, swaps, dur = SortEngine.bubbleSort(students, "nim")
            method = "Bubble Sort (NIM)"
        elif pilihan == "2":
            comp, swaps, dur = SortEngine.insertionSort(students, "nim")
            method = "Insertion Sort (NIM)"
        elif pilihan == "3":
            comp, swaps, dur = SortEngine.mergeSort(students, "nama")
            method = "Merge Sort (Nama)"
        elif pilihan == "4":
            comp, swaps, dur = SortEngine.mergeSort(students, "ipk")
            method = "Merge Sort (IPK)"
        else:
            flash('Pilihan tidak valid!', 'danger')
            return redirect(url_for('urutkan'))

        # Update manager with sorted list? (Optional, let's keep list order consistent if needed)
        manager.linked_list.from_list(students)
        
        flash(f'Berhasil diurutkan menggunakan {method}!', 'success')
        stats = {
            'metode': method,
            'perbandingan': comp,
            'penukaran': swaps,
            'waktu': f"{dur:.6f}"
        }

    # Fetch fresh (potentially sorted) students
    students = manager.getAllStudents()
    return render_template('urutkan.html', students=students, stats=stats)

@app.route('/bantuan')
@login_required
def bantuan():
    from utils import Utils
    info = Utils.get_complexity_info()
    return render_template('bantuan.html', info=info)

if __name__ == '__main__':
    app.run(debug=True)

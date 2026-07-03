from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return "Aplikasi Manajemen Mahasiswa (Under Construction for Vercel)"

# Hapus main block app.run() agar Vercel bisa menangani prosesnya, atau biarkan dengan kondisi:
if __name__ == '__main__':
    app.run(debug=True)

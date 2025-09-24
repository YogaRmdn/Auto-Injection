# Auto Injection


![Auto Injection](https://img.shields.io/badge/Auto--Injection-v1.0-blue)
![Language](https://img.shields.io/badge/Language-Python-green)


> **Auto Injection** — alat bantu **pengujian keamanan** yang dibuat dengan Python untuk membantu auditor dan pentester menemukan titik injeksi pada *web applications* dalam lingkungan yang *terotorisasi*. BUKAN untuk penggunaan ilegal. Baca bagian **Security & Legal** di bawah.


---


## ✨ Fitur utama


- Pemindaian cepat endpoint untuk mendeteksi potensi pola injeksi (misalnya parameter yang menerima input tidak tersanitasi).
- Mode *passive* dan *active* (mode active mengirim payload uji — **hanya** gunakan pada target yang Anda miliki izin eksplisitnya).
- Dukungan file konfigurasi YAML/JSON untuk menambahkan daftar endpoint, metode, dan parameter.
- Output laporan ringkas (JSON / CSV) untuk analisis lebih lanjut.
- Logging terstruktur supaya mudah diintegrasikan dengan pipeline CI/CD internal.


---


## Demo


> Tambahkan di sini GIF atau screenshot singkat: `assets/demo.gif`


---


## 📦 Prasyarat


- Python 3.10+ (direkomendasikan)
- Virtual environment (venv / virtualenv / pipenv)
- Dependensi di `requirements.txt`


---


## ⚙️ Instalasi


```
# clone repo
git clone https://github.com/<username>/Auto-Injection.git
cd Auto-Injection
python scan.py ```

KELOMPOK 16

# Aplikasi Microservices CRUD API PL/SQL UNSIA
- Aplikasi Microservice CRUD Employee dengan Trigger Log

# Dekripsi Aplikasi
- Aplikasi Flask ini memudahkan manajemen informasi karyawan dengan fitur CRUD dan otentikasi pengguna. Menggunakan PostgreSQL sebagai basis data dan SQLAlchemy untuk interaksi, aplikasi juga dilengkapi dengan fitur trigger log untuk melacak aktivitas pengguna. Ini memastikan manajemen data yang efisien dan aman.

# Fitur Aplikasi
* Otentikasi Pengguna dengan sandi terenkripsi
* Pencatatan kegiatan untuk melacak riwayat peristiwa dalam aplikasi
* Fungsi CRUD untuk pengelolaan Data Karyawan

# Persyaratan Aplikasi
Sebelum menjalankan aplikasi ini, pastikan Anda telah memasang semua komponen berikut:
* Python versi 3.11.3 atau yang lebih baru.
* Sistem manajemen basis data PostgreSQL.
* Editor kode seperti Visual Studio Code (VS Code).

# Dokumentasi Aplikasi 
- Dokumentasi Dan SDLC                                  : https://docs.google.com/document/d/1BjIUE2NqkHT2bopf_RZDlCFpTCDCB35v/edit?usp=sharing&ouid=116645460702152754144&rtpof=true&sd=true
- Postman                                               : https://drive.google.com/file/d/1m26VZsVPDDduL1bLteDSEUI-qDbYk9ov/view?usp=sharing

Berikut ini adalah Langkah- Langkah Menjalankan Aplikasi Yang Melibatkan CRUD dan Trigger Log , Beserta, langkah-langkah Untuk Membuat , Mejalankan, dan Mengelola aplikasi tersebut:
# Langkah-Langkah Running Aplikasi: 

# 1. Clnone Proyek 
Salin repositori proyek ke komputer dengan menggunakan Git:
```bash 
     git clone <url_repositori>
```
Ganti ' <url_repositori> ' dengan URL repositori proyek yang Anda salin.

# 2. Buat Data Base :
 buatlah database dengan nama ' db_employe ' di manajemen basis data yang Anda gunakan , Misalnya PostgreSQL.

# 3. Sesuaikan Konfigurasi Database : 

   Buka file ' app.py ' dan sesuaikan konfigurasi basis data Anda :

 ``` python
       app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://username:password@localhost/db_employee'
```
  gantilah ' username ' dan ' password ' sesuai dengan kredesial basis data Anda.

# 4. Instal python 3 :

Pastikan python 3 telah terinstal di komputer anda, jika belum unduh dan instal Python 3 dari web resminya.
   [Download python](https://www.python.org/downloads/0)

# 6. Instal Virtual Environment :
   Buka terminal atau commad prompt dan jalankan perintah berikut :

``` bash 
    pip3 install virtualenv
```
# 7. Instal Virtual Environment :
   Buat virtua environment di dalam folder proyek:

   ```bash
        python -m venv venv
```
# 8. Aktifkan Virtual Environment :

   Aktifkan virtual environment :
   
   * Pada vindows :

   ```  bash
         venv\Scripts\activate
   ```

* Pada macOS/Linuk :

 ``` bash
       source venv/bin/activate
```
  # 9.  Install Depedensi:
Instal semua depedensi yang di perlukan dari file ' requiretments.txt ' :


``` bash
pip install -r requirements.txt
```
# 10. Makemidration Database :

Buat Migrasi untuk skruktur database :

``` bash
        flask db stamp head
        flask db migrate -m 'your          descriptive message'
        flask db upgrade
```

# 11. Jalankan Server :
Jalankan server flask

``` bash
        flask run
```
# Manajemen Pengguna

* # Login
- Gunakan enam inputan untuk masuk, yaitu Username dan Password.
* # Buat User
- Gunakan enam inputan untuk membuat pengguna baru , yaitu :
  - Username
  - Password
  - First Name
  - Last Name
  - Gender
  - Status
* # Update User :
    - Lakukan pembaruan pada informasi pengguna dengan memberikan nilai baru untuk First Name, Last Name, Gender, dan Status bedasarkan Username pengguna yang sudah ada.
* # Hapus User :
    - Hapus pengguna bedasarkan username.

 # Trigger Log :
* ' User ActifityLog ' yang memiliki Kolom-Kolom :
  - id: Integer, primary key
  - user_id: Integer
  - activity_type: String(15)
  - timestamp: DateTime, default=datetime.datetime.utcnow
* Aktivitas dari pengguna seperti Insert, Update, dan Delete akan dicatat dalam tabel ini.

Dengan mengikuti langkah-langkah di atas, Anda dapat menjalankan aplikasi Anda yang melibatkan manajemen pengguna dan trigger log dengan sukses. 


     


 

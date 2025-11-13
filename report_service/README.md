# 📊 Report Service

## 📘 Deskripsi

Report Service adalah komponen microservice yang bertugas untuk mengelola laporan transaksi pengguna. Service ini mengumpulkan data dari User Service dan Transaction Service untuk menampilkan laporan transaksi per pengguna, ringkasan keuangan, serta melakukan sinkronisasi data antarservice agar data laporan selalu up-to-date.

Service ini menjadi pusat analisis data transaksi yang dapat digunakan untuk keperluan monitoring, pelaporan keuangan, dan rekap aktivitas pengguna.

---

## ⚙️ Konfigurasi Umum

- Port: 5004
- Base URL: http://localhost:5004
- Autentikasi Antarservice: Header X-Service-Token
- Database: MySQL (digital_wallet_reports)
- Terhubung dengan:
  - User Service → untuk mendapatkan data pengguna
  - Transaction Service → untuk mendapatkan data transaksi

---

## 🔐 Autentikasi

Untuk komunikasi antarservice gunakan:
X-Service-Token: service_shared_secret_change_this

---

## 📡 Endpoints

### 1. Create Report

Method: POST  
URL: /reports  
Body:
{
"user_id": 1,
"transaction_id": 10
}
Response:
{
"id": 5,
"user_id": 1,
"transaction_id": 10,
"status": "generated",
"created_at": "2025-11-12T10:30:00Z"
}
Deskripsi:
Membuat laporan baru berdasarkan transaksi yang dilakukan oleh user. Biasanya dipanggil setelah transaksi berhasil diselesaikan.

---

### 2. Get Reports by User

Method: GET  
URL: /reports/user/<user_id>?page=1&per_page=50  
Response:
{
"user_id": 1,
"page": 1,
"per_page": 50,
"total": 2,
"reports": [
{
"id": 1,
"transaction_id": 10,
"amount": 50000,
"status": "completed",
"created_at": "2025-11-10T09:00:00Z"
},
{
"id": 2,
"transaction_id": 11,
"amount": 10000,
"status": "pending",
"created_at": "2025-11-11T08:15:00Z"
}
]
}
Deskripsi:
Mengambil semua laporan transaksi milik pengguna tertentu dengan dukungan pagination (page dan per_page).

---

### 3. Get Summary by User

Method: GET  
URL: /summaries/user/<user_id>  
Response:
{
"user_id": 1,
"total_transactions": 25,
"total_spent": 2500000,
"total_received": 1800000,
"last_transaction": "2025-11-12T08:00:00Z"
}
Deskripsi:
Menampilkan ringkasan aktivitas transaksi pengguna, termasuk total transaksi, total pengeluaran, total penerimaan, dan transaksi terakhir.

---

### 4. Sync All Reports

Method: POST  
URL: /sync/all  
Response:
{
"message": "Reports synchronized successfully",
"synced_users": 125,
"synced_transactions": 1450,
"timestamp": "2025-11-12T10:45:00Z"
}
Deskripsi:
Menjalankan proses sinkronisasi data laporan dari Transaction Service dan User Service untuk memastikan data laporan selalu mutakhir.

---

## 🧠 Integrasi Antarservice

| Service             | Deskripsi                                              | Arah Integrasi                   |
| ------------------- | ------------------------------------------------------ | -------------------------------- |
| user_service        | Menyediakan data pengguna untuk laporan transaksi      | Satu arah (report → user)        |
| transaction_service | Menyediakan data transaksi untuk laporan dan ringkasan | Satu arah (report → transaction) |

---

## 🧾 Contoh Header di Postman

Untuk komunikasi antarservice:  
X-Service-Token: service_shared_secret_change_this

Contoh request:
POST http://localhost:5004/reports  
Content-Type: application/json  
X-Service-Token: service_shared_secret_change_this

---

## 🧪 Cara Menjalankan Service

Jalankan Flask server:
python main.py

Server akan berjalan di:  
http://localhost:5004

---

## 👥 Developer Notes

- Pastikan file .env memiliki konfigurasi database dan SERVICE_TOKEN yang valid.
- Report Service memerlukan data dari User Service dan Transaction Service agar laporan dan ringkasan dapat terbentuk dengan benar.
- Endpoint /sync/all dapat dijalankan secara otomatis melalui cron job untuk menjaga konsistensi data laporan.

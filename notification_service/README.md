# 🔔 Notification Service

## 📘 Deskripsi

Notification Service adalah komponen microservice yang bertugas untuk mengelola dan mengirimkan notifikasi ke pengguna. Notifikasi dapat berupa pesan status transaksi, konfirmasi pembayaran, top-up saldo, atau laporan lainnya.  
Service ini menerima data dari Transaction Service, User Service, dan Report Service, kemudian menyimpan notifikasi ke database serta mengirimkan pesan ke email pengguna.

---

## ⚙️ Konfigurasi Umum

- Port: 5003
- Base URL: http://localhost:5003
- Autentikasi Antarservice: Header X-Service-Token
- Database: MySQL (digital_wallet_notifications)
- Terhubung dengan:
  - User Service → untuk mengambil alamat email user
  - Transaction Service → untuk kirim notifikasi transaksi
  - Report Service → untuk kirim notifikasi laporan

---

## 🔐 Autentikasi

Untuk komunikasi antarservice gunakan:
X-Service-Token: service_shared_secret_change_this

---

## 📡 Endpoints

### 1. Create Notification

Method: POST  
URL: /notifications  
Body:
{
"user_id": 1,
"message": "Your payment of Rp 50,000 has been successfully processed."
}
Response:
{
"id": 1,
"user_id": 1,
"message": "Your payment of Rp 50,000 has been successfully processed.",
"status": "pending",
"created_at": "2025-11-12T10:30:00Z"
}
Deskripsi:
Membuat notifikasi baru untuk user berdasarkan aktivitas tertentu. Biasanya dipanggil oleh Transaction Service atau Report Service setelah sebuah event terjadi.

---

### 2. Get All Notifications

Method: GET  
URL: /notifications  
Response:
[
{
"id": 1,
"user_id": 1,
"message": "Top-up Rp 100,000 successful.",
"status": "sent",
"created_at": "2025-11-10T09:00:00Z"
},
{
"id": 2,
"user_id": 2,
"message": "Transaction pending approval.",
"status": "pending",
"created_at": "2025-11-11T08:00:00Z"
}
]
Deskripsi:
Mengambil seluruh data notifikasi yang tersimpan di database.

---

### 3. Get Notification by ID

Method: GET  
URL: /notifications/<notif_id>  
Response:
{
"id": 1,
"user_id": 1,
"message": "Top-up Rp 100,000 successful.",
"status": "sent",
"created_at": "2025-11-10T09:00:00Z"
}
Deskripsi:
Mengambil detail satu notifikasi berdasarkan ID.

---

### 4. Update Notification

Method: PUT  
URL: /notifications/<notif_id>  
Body:
{
"message": "Your payment is being processed.",
"status": "pending"
}
Response:
{
"id": 1,
"user_id": 1,
"message": "Your payment is being processed.",
"status": "pending",
"updated_at": "2025-11-12T10:45:00Z"
}
Deskripsi:
Mengubah isi pesan atau status notifikasi secara manual (misal oleh admin atau service internal).

---

### 5. Delete Notification

Method: DELETE  
URL: /notifications/<notif_id>  
Response:
{
"message": "Notification deleted"
}
Deskripsi:
Menghapus notifikasi dari database.

---

### 6. Send Notification (Trigger Email)

Method: POST  
URL: /notifications/<notif_id>/send  
Response:
{
"message": "Notification sent",
"status": "sent"
}
Deskripsi:
Mengirimkan email notifikasi ke alamat email user yang bersangkutan menggunakan SMTP. Biasanya dijalankan otomatis setelah notifikasi dibuat.

---

### 7. Resend Notification (Retry)

Method: POST  
URL: /notifications/<notif_id>/resend  
Response:
{
"message": "Notification resent",
"status": "sent"
}
Deskripsi:
Mengirim ulang notifikasi yang sebelumnya gagal dikirim (status = failed). Hanya notifikasi gagal yang dapat dikirim ulang.

---

## 🧠 Integrasi Antarservice

| Service             | Deskripsi                                                   | Arah Integrasi                         |
| ------------------- | ----------------------------------------------------------- | -------------------------------------- |
| user_service        | Menyediakan data email user untuk pengiriman notifikasi     | Satu arah (notification → user)        |
| transaction_service | Memicu notifikasi saat transaksi dibuat atau berubah status | Satu arah (transaction → notification) |
| report_service      | Memicu notifikasi setelah laporan dibuat                    | Satu arah (report → notification)      |

---

## 🧾 Contoh Header di Postman

Untuk komunikasi antarservice:  
X-Service-Token: service_shared_secret_change_this

Contoh request:
POST http://localhost:5003/notifications  
Content-Type: application/json  
X-Service-Token: service_shared_secret_change_this

---

## 🧪 Cara Menjalankan Service

Jalankan Flask server:
python main.py

Server akan berjalan di:  
http://localhost:5003

---

## 👥 Developer Notes

- Pastikan file .env memiliki konfigurasi database, SMTP server, dan SERVICE_TOKEN yang valid.
- Notification Service akan mengirimkan email menggunakan SMTP (misalnya Gmail).
- Jika terjadi error “535 BadCredentials”, pastikan menggunakan App Password Gmail, bukan password akun utama.
- Service ini dapat diintegrasikan dengan User Service untuk mengambil email user berdasarkan user_id.
- Transaction Service dan Report Service dapat memanggil endpoint /notifications untuk membuat notifikasi baru.

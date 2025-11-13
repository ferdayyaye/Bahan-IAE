# 💸 Transaction Service

## 📘 Deskripsi

Transaction Service adalah komponen microservice yang bertugas mengelola data transaksi antar pengguna dalam sistem Digital Wallet. Service ini menangani proses pembuatan transaksi, pembaruan status transaksi, penghapusan transaksi, serta pengambilan data transaksi baik secara keseluruhan maupun per pengguna.  
Transaction Service juga berinteraksi langsung dengan User Service untuk memperbarui saldo pengguna (debit dan kredit) menggunakan service token internal, serta dengan Notification Service untuk mengirimkan notifikasi setiap transaksi berhasil dibuat.

## ⚙️ Konfigurasi Umum

- Port: 5002
- Base URL: http://localhost:5002
- Autentikasi Antarservice: Header X-Service-Token
- Database: MySQL (digital_wallet_tx)
- Terhubung dengan:
  - User Service → untuk update saldo pengguna
  - Notification Service → untuk kirim notifikasi transaksi

## 🔐 Autentikasi

Untuk komunikasi antarservice gunakan:
X-Service-Token: service_shared_secret_change_this

---

## 📡 Endpoints

### 1. Create Transaction

Method: POST  
URL: /transactions  
Body:
{
"sender_id": 1,
"receiver_id": 2,
"amount": 10000,
"description": "Payment for goods"
}
Response:
{
"id": 10,
"sender_id": 1,
"receiver_id": 2,
"amount": 10000,
"status": "pending",
"description": "Payment for goods",
"created_at": "2025-11-12T10:30:00Z"
}

---

### 2. Get All Transactions

Method: GET  
URL: /transactions  
Response:
[
{
"id": 1,
"sender_id": 1,
"receiver_id": 2,
"amount": 50000,
"status": "completed",
"description": "Topup",
"created_at": "2025-11-10T10:00:00Z"
},
{
"id": 2,
"sender_id": 2,
"receiver_id": 3,
"amount": 20000,
"status": "pending",
"description": "Transfer",
"created_at": "2025-11-11T08:15:00Z"
}
]

---

### 3. Get Transaction by ID

Method: GET  
URL: /transactions/<tx_id>  
Response:
{
"id": 1,
"sender_id": 1,
"receiver_id": 2,
"amount": 50000,
"status": "completed",
"description": "Payment completed",
"created_at": "2025-11-10T10:00:00Z"
}

---

### 4. Update Transaction Status

Method: PUT  
URL: /transactions/<tx_id>  
Body:
{
"status": "completed"
}
Response:
{
"id": 1,
"sender_id": 1,
"receiver_id": 2,
"amount": 50000,
"status": "completed",
"description": "Payment completed",
"updated_at": "2025-11-12T14:00:00Z"
}

---

### 5. Delete Transaction

Method: DELETE  
URL: /transactions/<tx_id>  
Response:
{
"message": "Transaction deleted"
}

---

### 6. Get Transactions by User

Method: GET  
URL: /transactions/user/<user_id>  
Response:
[
{
"id": 1,
"sender_id": 1,
"receiver_id": 2,
"amount": 10000,
"status": "completed",
"description": "Purchase item",
"created_at": "2025-11-10T09:00:00Z"
},
{
"id": 2,
"sender_id": 1,
"receiver_id": 3,
"amount": 5000,
"status": "pending",
"description": "Transfer",
"created_at": "2025-11-11T08:00:00Z"
}
]

---

## 🧠 Integrasi Antarservice

| Service              | Deskripsi                                                      | Arah Integrasi                         |
| -------------------- | -------------------------------------------------------------- | -------------------------------------- |
| user_service         | Memperbarui saldo user saat transaksi dilakukan (debit/kredit) | Dua arah                               |
| notification_service | Mengirim notifikasi email ke user setelah transaksi berhasil   | Satu arah (transaction → notification) |

---

## 🧾 Contoh Header di Postman

Untuk komunikasi antarservice:
X-Service-Token: service_shared_secret_change_this

Contoh request:
POST http://localhost:5002/transactions  
Content-Type: application/json  
X-Service-Token: service_shared_secret_change_this

---

## 🧪 Cara Menjalankan Service

Jalankan Flask server:
python main.py

Server akan berjalan di:  
http://localhost:5002

---

## 👥 Developer Notes

- Pastikan file .env memiliki konfigurasi database dan SERVICE_TOKEN yang sama dengan User Service.
- Transaction Service akan melakukan panggilan HTTP internal ke User Service untuk memperbarui saldo user.
- Notification Service dapat memanggil endpoint internal untuk mengirimkan notifikasi transaksi.
 

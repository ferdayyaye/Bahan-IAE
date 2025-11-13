# 🧑‍💼 User Service

## 📘 Deskripsi

User Service adalah salah satu komponen utama dalam arsitektur microservices yang bertugas untuk mengelola data pengguna serta menyediakan fitur autentikasi (login/register) dan manajemen saldo (balance). Service ini menangani seluruh proses terkait pengguna, mulai dari pendaftaran, login, pembaruan data, hingga top-up dan debit saldo. Selain itu, User Service juga menyediakan endpoint internal untuk komunikasi antarservice dengan transaction_service dan notification_service.

## ⚙️ Konfigurasi Umum

- Port: 5001
- Base URL: http://localhost:5001
- Autentikasi User: JWT Token
- Autentikasi Antarservice: Header X-Service-Token
- Database: MySQL (digital_wallet)
- Terhubung dengan:
  - transaction_service → untuk pembaruan saldo user
  - notification_service → untuk pengiriman notifikasi ke email user

## 🔐 Autentikasi

Untuk user: gunakan header Authorization: Bearer <jwt_token>
Untuk antarservice (internal): gunakan header X-Service-Token: service_shared_secret_change_this

## 📡 Endpoints

### 1. Auth Routes

#### Register User

Method: POST  
URL: /auth/register  
Body:
{
"full_name": "John Doe",
"email": "john@example.com",
"password": "password123"
}
Response:
{
"id": 1,
"full_name": "John Doe",
"email": "john@example.com",
"balance": 0.0
}

#### Login

Method: POST  
URL: /auth/login  
Body:
{
"email": "john@example.com",
"password": "password123"
}
Response:
{
"access_token": "jwt_token_here",
"user": {
"id": 1,
"full_name": "John Doe",
"email": "john@example.com"
}
}

---

### 2. User CRUD Routes

#### Get All Users

Method: GET  
URL: /users  
Response:
[
{
"id": 1,
"full_name": "John Doe",
"email": "john@example.com",
"balance": 10000.0
}
]

#### Create User

Method: POST  
URL: /users  
Body:
{
"full_name": "Jane Doe",
"email": "jane@example.com",
"password": "mypassword"
}
Response:
{
"id": 2,
"full_name": "Jane Doe",
"email": "jane@example.com"
}

#### Get User by ID

Method: GET  
URL: /users/<user_id>  
Headers: Authorization: Bearer <jwt_token> (optional)  
Response:
{
"id": 1,
"full_name": "John Doe",
"email": "john@example.com",
"balance": 50000.0
}

#### Update User

Method: PUT  
URL: /users/<user_id>  
Headers: Authorization: Bearer <jwt_token>  
Body:
{
"full_name": "John D. Doe"
}
Response:
{
"id": 1,
"full_name": "John D. Doe",
"email": "john@example.com"
}

#### Delete User

Method: DELETE  
URL: /users/<user_id>  
Headers: Authorization: Bearer <jwt_token>  
Response:
{
"message": "User deleted"
}

---

### 3. Balance Routes

#### Get Balance

Method: GET  
URL: /users/<user_id>/balance  
Response:
{
"user_id": 1,
"balance": 50000.0
}

#### Top Up Balance

Method: POST  
URL: /users/<user_id>/topup  
Headers: Authorization: Bearer <jwt_token>  
Body:
{
"amount": 100000
}
Response:
{
"id": 1,
"balance": 150000.0
}

#### Debit Balance

Method: POST  
URL: /users/<user_id>/debit  
Headers: Authorization: Bearer <jwt_token>  
Body:
{
"amount": 50000
}
Response:
{
"id": 1,
"balance": 100000.0
}

---

### 4. Internal Routes (Untuk Service Lain)

#### Get User (Internal)

Method: GET  
URL: /internal/users/<user_id>  
Headers: X-Service-Token: service_shared_secret_change_this  
Response:
{
"id": 1,
"full_name": "John Doe",
"email": "john@example.com"
}

#### Update Balance (Internal)

Method: PUT  
URL: /internal/users/<user_id>/balance  
Headers: X-Service-Token: service_shared_secret_change_this  
Body:
{
"action": "debit",
"amount": 5000
}
Response:
{
"id": 1,
"balance": 45000.0
}

---

## 🧠 Integrasi Antarservice

| Service              | Deskripsi                                                | Arah Integrasi                |
| -------------------- | -------------------------------------------------------- | ----------------------------- |
| transaction_service  | Melakukan debit/kredit saldo user saat transaksi terjadi | Dua arah                      |
| notification_service | Mengambil email user untuk pengiriman notifikasi         | Satu arah (notifikasi → user) |

---

## 🧾 Contoh Header di Postman

Untuk login user:
POST http://localhost:5001/auth/login  
Content-Type: application/json

Untuk endpoint authenticated:
GET http://localhost:5001/users/1  
Authorization: Bearer <jwt_token>

Untuk endpoint internal:
GET http://localhost:5001/internal/users/1  
X-Service-Token: service_shared_secret_change_this

---

## 🧪 Cara Menjalankan Service

Jalankan Flask server:
python main.py

Server akan berjalan di:  
http://localhost:5001

---

## 👥 Developer Notes

- Pastikan file .env berisi konfigurasi database & JWT key yang valid.
- Untuk testing integrasi antarservice, jalankan juga:
  - transaction_service di port 5002
  - notification_service di port 5003

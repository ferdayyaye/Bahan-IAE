# 🏦 Digital Wallet - Microservices System

Sistem microservices untuk aplikasi dompet digital yang dibangun dengan arsitektur modern menggunakan Flask, multiple services (User, Transaction, Notification, Report), dan MySQL sebagai database.

## 📋 Daftar Isi

- [Arsitektur Sistem](#arsitektur-sistem)
- [Teknologi yang Digunakan](#teknologi-yang-digunakan)
- [Prerequisites](#prerequisites)
- [Instalasi dan Setup](#instalasi-dan-setup)
- [Struktur Project](#struktur-project)
- [Service Endpoints](#service-endpoints)
- [Testing dengan Postman](#testing-dengan-postman)
- [Environment Variables](#environment-variables)
- [Integrasi Antarservice](#integrasi-antarservice)

---

## 🏗️ Arsitektur Sistem

Sistem ini menggunakan arsitektur microservices dengan komponen utama:

```
┌──────────────────┐
│  Client/Browser  │
└────────┬─────────┘
         │
         ▼
┌──────────────────────────────────────┐
│      API Gateway / Load Balancer     │
│      (Optional - untuk production)   │
└─────────────────┬────────────────────┘
                  │
    ┌─────────────┼─────────────┬──────────┐
    │             │             │          │
    ▼             ▼             ▼          ▼
┌─────────┐ ┌──────────┐ ┌───────────┐ ┌───────────┐
│  User   │ │Transaction││Notification││  Report   │
│ Service │ │ Service  │ │ Service   │ │  Service  │
│ :5001   │ │  :5002   │ │  :5003    │ │   :5004   │
└────┬────┘ └─────┬────┘ └─────┬─────┘ └─────┬─────┘
     │           │             │             │
     └───────────┼─────────────┼─────────────┘
                 │             │
                 ▼             ▼
            ┌────────────────────────────────────┐
            │   MySQL Database                   │
            │   (digital_wallet_users)           │
            │   (digital_wallet_transactions)    │
            │   (digital_wallet_notifications)   │
            │   (digital_wallet_reports)         │
            │   (Port: 3306)                     │
            └────────────────────────────────────┘
```

---

## 🛠️ Teknologi yang Digunakan

### Backend Services

- **Framework**: Python Flask
- **Authentication**: JWT Token & Service Token
- **Database**: MySQL 8.0
- **Communication**: RESTful API

### Tools

- **API Testing**: Postman
- **Database Management**: MySQL Workbench / phpMyAdmin

---

## ⚙️ Prerequisites

Pastikan sistem Anda sudah terinstall:

- **Postman** (untuk testing API)
- **Git** (untuk clone repository)

### System Requirements

- RAM minimum 4GB
- Storage minimum 2GB free space

---

## 🚀 Instalasi dan Setup

### 1. Clone Repository

```bash
git clone <repository-url>
cd digital-wallet-project
```

### 2. Setup Environment Variables

Buat file `.env` untuk setiap service:

**user-service/.env**

```env
# Database Configuration
DB_HOST=mysql-db
DB_USER=root
DB_PASSWORD=root
DB_NAME=digital_wallet_users
DB_PORT=3306

# Service Configuration
PORT=5001
FLASK_ENV=development

# JWT Configuration
JWT_SECRET=your_jwt_secret_key_change_this
JWT_EXPIRATION=3600

# Service Token
SERVICE_TOKEN=service_shared_secret_change_this

# SMTP Configuration (untuk integrasi notifikasi)
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your_email@gmail.com
SMTP_PASSWORD=your_app_password
```

**transaction-service/.env**

```env
# Database Configuration
DB_HOST=mysql-db
DB_USER=root
DB_PASSWORD=root
DB_NAME=digital_wallet_transactions
DB_PORT=3306

# Service Configuration
PORT=5002
FLASK_ENV=development

# Service Token
SERVICE_TOKEN=service_shared_secret_change_this

# Service URLs
USER_SERVICE_URL=http://user-service:5001
NOTIFICATION_SERVICE_URL=http://notification-service:5003
```

**notification-service/.env**

```env
# Database Configuration
DB_HOST=mysql-db
DB_USER=root
DB_PASSWORD=root
DB_NAME=digital_wallet_notifications
DB_PORT=3306

# Service Configuration
PORT=5003
FLASK_ENV=development

# Service Token
SERVICE_TOKEN=service_shared_secret_change_this

# Service URLs
USER_SERVICE_URL=http://user-service:5001

# SMTP Configuration
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your_email@gmail.com
SMTP_PASSWORD=your_app_password
SENDER_EMAIL=noreply@digitalwallet.com
```

**report-service/.env**

```env
# Database Configuration
DB_HOST=mysql-db
DB_USER=root
DB_PASSWORD=root
DB_NAME=digital_wallet_reports
DB_PORT=3306

# Service Configuration
PORT=5004
FLASK_ENV=development

# Service Token
SERVICE_TOKEN=service_shared_secret_change_this

# Service URLs
USER_SERVICE_URL=http://user-service:5001
TRANSACTION_SERVICE_URL=http://transaction-service:5002
```

---

## 📁 Struktur Project

```
digital-wallet-project/
│
├── api_gateway/
│   ├── .env
│   ├── main.py
│   └── requirements.txt
│
├── frontend/
│   ├── static/
│   │  ├── css/
│   │  │   ├── charts.js
│   │  │   └── style.css
│   │  └── js/
│   │      ├── charts.js
│   │      └── main.js
│   ├── templates/
│   │  ├── auth_layout.html
│   │  ├── dashboard_admin.html
│   │  ├── dashboard_user.html
│   │  ├── index.html
│   │  ├── layout_admin.html
│   │  ├── layout_user.html
│   │  ├── login.html
│   │  └── register.html
│   ├── .env
│   ├── app.py
│   └── requirements.txt
│
├── user-service/
│   ├── .env
│   ├── config.py
│   ├── main.py
│   ├── README.md
│   ├── requirements.txt
│   └── app/
│       ├── __init__.py
│       ├── controllers.py
│       ├── models.py
│       ├── routes.py
│       └── schemas.py
│
├── transaction-service/
│   ├── .env
│   ├── config.py
│   ├── main.py
│   ├── README.md
│   ├── requirements.txt
│   └── app/
│       ├── __init__.py
│       ├── controllers.py
│       ├── models.py
│       ├── routes.py
│       └── schemas.py
│
├── notification-service/
│   ├── .env
│   ├── config.py
│   ├── main.py
│   ├── README.md
│   ├── requirements.txt
│   └── app/
│       ├── __init__.py
│       ├── controllers.py
│       ├── models.py
│       ├── routes.py
│       └── schemas.py
│
├── report-service/
│   ├── .env
│   ├── config.py
│   ├── main.py
│   ├── README.md
│   ├── requirements.txt
│   └── app/
│       ├── __init__.py
│       ├── controllers.py
│       ├── models.py
│       ├── routes.py
│       ├── schemas.py
│       └── utils.py
│
├── init-db.sql
├── digital-wallet-collection.json (Postman)
└── README.md
```

---

## 🔌 Service Endpoints

Semua endpoints diakses melalui base URL yang sesuai dengan service masing-masing.

### 1️⃣ User Service (Port 5001)

**Base URL**: `http://localhost:5001`

#### Authentication Routes

**POST /auth/register** - Register User

<img width="1352" height="615" alt="image" src="https://github.com/user-attachments/assets/b3ba61e6-9081-4cb5-87c0-a26ca2f99aec" />


```http
POST http://localhost:5001/auth/register
Content-Type: application/json

{
    "full_name": "John Doe",
    "email": "john@example.com",
    "password": "password123"
}

Response (201 Created):
{
    "id": 1,
    "full_name": "John Doe",
    "email": "john@example.com",
    "balance": 0.0
}
```


**POST /auth/login** - Login User

<img width="1367" height="730" alt="image" src="https://github.com/user-attachments/assets/7a146519-5be6-4122-8f0f-752440992267" />

```http
POST http://localhost:5001/auth/login
Content-Type: application/json

{
    "email": "john@example.com",
    "password": "password123"
}

Response (200 OK):
{
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "user": {
        "id": 1,
        "full_name": "John Doe",
        "email": "john@example.com"
    }
}
```

#### User CRUD Routes

**GET /users** - Get All Users

<img width="1362" height="667" alt="image" src="https://github.com/user-attachments/assets/fa64f1ea-927d-4517-88ff-a2fb36ef96d0" />

```http
GET http://localhost:5001/users

Response (200 OK):
[
    {
        "id": 1,
        "full_name": "John Doe",
        "email": "john@example.com",
        "balance": 10000.0
    },
    {
        "id": 2,
        "full_name": "Jane Doe",
        "email": "jane@example.com",
        "balance": 25000.0
    }
]
```

**GET /users/{id}** - Get User by ID

<img width="1355" height="622" alt="image" src="https://github.com/user-attachments/assets/c80400cd-dbb6-4224-9230-96885760356f" />

```http
GET http://localhost:5001/users/1
Authorization: Bearer {token} (optional)

Response (200 OK):
{
    "id": 1,
    "full_name": "John Doe",
    "email": "john@example.com",
    "balance": 50000.0
}
```

**PUT /users/{id}** - Update User

<img width="1368" height="617" alt="image" src="https://github.com/user-attachments/assets/ff96a355-f870-4b39-a263-617e02ff9f53" />

```http
PUT http://localhost:5001/users/1
Authorization: Bearer {token}
Content-Type: application/json

{
    "full_name": "John D. Doe"
}

Response (200 OK):
{
    "id": 1,
    "full_name": "John D. Doe",
    "email": "john@example.com"
}
```

**DELETE /users/{id}** - Delete User

<img width="1361" height="529" alt="image" src="https://github.com/user-attachments/assets/c3d22818-9797-49e4-8f2a-d7ccc9b2caf2" />

```http
DELETE http://localhost:5001/users/1
Authorization: Bearer {token}

Response (200 OK):
{
    "message": "User deleted successfully"
}
```

#### Balance Routes

**GET /users/{id}/balance** - Get Balance

<img width="1356" height="555" alt="image" src="https://github.com/user-attachments/assets/d9619dc0-52ef-40e5-af83-594ceb143341" />

```http
GET http://localhost:5001/users/1/balance

Response (200 OK):
{
    "user_id": 1,
    "balance": 50000.0
}
```

**POST /users/{id}/topup** - Top Up Balance

<img width="1369" height="619" alt="image" src="https://github.com/user-attachments/assets/2bce3610-a1b2-4645-b2d6-4a873dd73c16" />

<img width="1365" height="555" alt="image" src="https://github.com/user-attachments/assets/acd483c4-777d-400e-8650-fad5eabf587e" />

```http
POST http://localhost:5001/users/1/topup
Authorization: Bearer {token}
Content-Type: application/json

{
    "amount": 100000
}

Response (200 OK):
{
    "id": 1,
    "balance": 150000.0
}
```

#### Internal Routes (Service-to-Service)

**GET /internal/users/{id}** - Get User (Internal)

<img width="1357" height="617" alt="image" src="https://github.com/user-attachments/assets/3b7b2333-7108-4c72-851c-5e7fcfb1ba1c" />

```http
GET http://localhost:5001/internal/users/1
X-Service-Token: service_shared_secret_change_this

Response (200 OK):
{
    "id": 1,
    "full_name": "John Doe",
    "email": "john@example.com"
}
```

**PUT /internal/users/{id}/balance** - Update Balance (Internal)

<img width="1362" height="617" alt="image" src="https://github.com/user-attachments/assets/b9d20012-d4d6-4685-8d6c-f1a02e86772d" />

```http
PUT http://localhost:5001/internal/users/1/balance
X-Service-Token: service_shared_secret_change_this
Content-Type: application/json

{
    "action": "debit",
    "amount": 5000
}

Response (200 OK):
{
    "id": 1,
    "balance": 45000.0
}
```

---

### 2️⃣ Transaction Service (Port 5002)

**Base URL**: `http://localhost:5002`

#### Transaction Management Routes

**POST /transactions** - Create Transaction

<img width="1358" height="644" alt="image" src="https://github.com/user-attachments/assets/e1c4c245-884d-4ce5-9450-0cef7fe3d69c" />

<img width="1360" height="558" alt="image" src="https://github.com/user-attachments/assets/507a9a6f-feec-419c-bcc6-a08df36885a5" />

```http
POST http://localhost:5002/transactions
X-Service-Token: service_shared_secret_change_this
Content-Type: application/json

{
    "sender_id": 1,
    "receiver_id": 2,
    "amount": 10000,
    "description": "Payment for goods"
}

Response (201 Created):
{
    "id": 10,
    "sender_id": 1,
    "receiver_id": 2,
    "amount": 10000,
    "status": "pending",
    "description": "Payment for goods",
    "created_at": "2025-11-12T10:30:00Z"
}
```

**GET /transactions** - Get All Transactions

<img width="1370" height="684" alt="image" src="https://github.com/user-attachments/assets/12642fe7-1f40-47c0-8dcc-2be3675fde8b" />

```http
GET http://localhost:5002/transactions

Response (200 OK):
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
```

**GET /transactions/{id}** - Get Transaction by ID

<img width="1359" height="651" alt="image" src="https://github.com/user-attachments/assets/503a45a3-ba12-476b-86a7-db7387c40023" />

```http
GET http://localhost:5002/transactions/1

Response (200 OK):
{
    "id": 1,
    "sender_id": 1,
    "receiver_id": 2,
    "amount": 50000,
    "status": "completed",
    "description": "Payment completed",
    "created_at": "2025-11-10T10:00:00Z"
}
```

**PUT /transactions/{id}** - Update Transaction Status

<img width="1354" height="642" alt="image" src="https://github.com/user-attachments/assets/bbb82de5-cd0f-4621-9729-8ad392bc61cd" />

```http
PUT http://localhost:5002/transactions/1
Content-Type: application/json

{
    "status": "completed"
}

Response (200 OK):
{
    "id": 1,
    "sender_id": 1,
    "receiver_id": 2,
    "amount": 50000,
    "status": "completed",
    "description": "Payment completed",
    "updated_at": "2025-11-12T14:00:00Z"
}
```

**DELETE /transactions/{id}** - Delete Transaction

<img width="1360" height="536" alt="image" src="https://github.com/user-attachments/assets/55b08ef0-e45c-49fc-9a01-f7555bb084c4" />

```http
DELETE http://localhost:5002/transactions/1

Response (200 OK):
{
    "message": "Transaction deleted successfully"
}
```

**GET /transactions/user/{user_id}** - Get Transactions by User

<img width="1358" height="695" alt="image" src="https://github.com/user-attachments/assets/3f7bdeba-98f4-452b-a5d1-891dabd27a95" />

```http
GET http://localhost:5002/transactions/user/1

Response (200 OK):
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
```

---

### 3️⃣ Notification Service (Port 5003)

**Base URL**: `http://localhost:5003`

#### Notification Management Routes

**POST /notifications** - Create Notification

<img width="1361" height="617" alt="image" src="https://github.com/user-attachments/assets/f06e4d2d-cc40-4d5c-acb8-2f354bb9a046" />

```http
POST http://localhost:5003/notifications
X-Service-Token: service_shared_secret_change_this
Content-Type: application/json

{
    "user_id": 1,
    "message": "Your payment of Rp 50,000 has been successfully processed."
}

Response (201 Created):
{
    "id": 1,
    "user_id": 1,
    "message": "Your payment of Rp 50,000 has been successfully processed.",
    "status": "pending",
    "created_at": "2025-11-12T10:30:00Z"
}
```

**GET /notifications** - Get All Notifications

<img width="1343" height="818" alt="image" src="https://github.com/user-attachments/assets/b2652a38-10aa-4d61-bf54-4542674a4836" />

```http
GET http://localhost:5003/notifications

Response (200 OK):
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
```

**GET /notifications/{id}** - Get Notification by ID

<img width="1353" height="612" alt="image" src="https://github.com/user-attachments/assets/0eeb9bca-4c6a-48d5-b76b-3b7fed167e4c" />

```http
GET http://localhost:5003/notifications/1

Response (200 OK):
{
    "id": 1,
    "user_id": 1,
    "message": "Top-up Rp 100,000 successful.",
    "status": "sent",
    "created_at": "2025-11-10T09:00:00Z"
}
```

**PUT /notifications/{id}** - Update Notification

<img width="1356" height="621" alt="image" src="https://github.com/user-attachments/assets/f95d9a66-8cd0-4ee6-95b6-18892a0327b4" />

```http
PUT http://localhost:5003/notifications/1
Content-Type: application/json

{
    "message": "Your payment is being processed.",
    "status": "pending"
}

Response (200 OK):
{
    "id": 1,
    "user_id": 1,
    "message": "Your payment is being processed.",
    "status": "pending",
    "updated_at": "2025-11-12T10:45:00Z"
}
```

**DELETE /notifications/{id}** - Delete Notification

<img width="1357" height="527" alt="Screenshot 2025-11-13 163036" src="https://github.com/user-attachments/assets/ac994413-9af1-4db1-b685-7782f620557d" />

```http
DELETE http://localhost:5003/notifications/1

Response (200 OK):
{
    "message": "Notification deleted successfully"
}
```

**POST /notifications/{id}/send** - Send Notification via Email

<img width="1654" height="1079" alt="image" src="https://github.com/user-attachments/assets/f6c7f8b8-5163-49f3-85ae-6ac30509f0f8" />

```http
POST http://localhost:5003/notifications/1/send

Response (200 OK):
{
    "message": "Notification sent successfully",
    "status": "sent"
}
```

### 4️⃣ Report Service (Port 5004)

**Base URL**: `http://localhost:5004`

#### Report Management Routes

**POST /reports** - Create Report

<img width="1365" height="755" alt="image" src="https://github.com/user-attachments/assets/e1695f10-95a9-4cde-ad19-81cdb731d2c9" />

```http
POST http://localhost:5004/reports
X-Service-Token: service_shared_secret_change_this
Content-Type: application/json

{
    "user_id": 1,
    "transaction_id": 10
}

Response (201 Created):
{
    "id": 5,
    "user_id": 1,
    "transaction_id": 10,
    "status": "generated",
    "created_at": "2025-11-12T10:30:00Z"
}
```

**GET /reports/user/{user_id}** - Get Reports by User (with Pagination)

<img width="1356" height="794" alt="image" src="https://github.com/user-attachments/assets/574a909a-d84a-4206-9050-6e0a4fb23fd5" />

```http
GET http://localhost:5004/reports/user/1?page=1&per_page=50

Response (200 OK):
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
```

**GET /summaries/user/{user_id}** - Get Summary by User

<img width="1360" height="727" alt="image" src="https://github.com/user-attachments/assets/783a8cbf-e639-4d70-a8e0-35df7d2701c0" />

```http
GET http://localhost:5004/summaries/user/1

Response (200 OK):
{
    "user_id": 1,
    "total_transactions": 25,
    "total_spent": 2500000,
    "total_received": 1800000,
    "last_transaction": "2025-11-12T08:00:00Z"
}
```

### ❌ Incorrect input

### 1️⃣ User Service (Port 5001)

**Base URL**: `http://localhost:5001`

#### Authentication Routes

**POST /auth/register** - Register User

<img width="1360" height="526" alt="image" src="https://github.com/user-attachments/assets/ab4c8835-0170-4fad-b1dc-0a31c8cc4751" />

```http
POST http://localhost:5001/auth/register
Content-Type: application/json

{
  "full_name": "Uyab Bayu",
  "email": "uyab@mail.com",
  "password": "12345"
}

Response (400 Bad Request):
{
    "error": "Email already exists"
}
```

**POST /auth/login** - Login User

<img width="1362" height="526" alt="image" src="https://github.com/user-attachments/assets/ff71c82d-7245-48fe-b136-fc82f2ba4038" />

```http
POST http://localhost:5001/auth/login
Content-Type: application/json

{
  "email": "aaaaa@mail.com",
  "password": "12345"
}

Response (401 Unauthorized):
{
    "error": "Invalid credentials"
}
```

#### User CRUD Routes

**GET /users/{id}** - Get User by ID

<img width="1357" height="528" alt="image" src="https://github.com/user-attachments/assets/d1bc3823-0ffd-4091-9664-031892d4e83c" />

```http
GET http://localhost:5001/users/7
Authorization: Bearer {token} (optional)

Response (404 Not Found):
{
    "error": "User not found"
}
```

**PUT /users/{id}** - Update User

<img width="1354" height="533" alt="image" src="https://github.com/user-attachments/assets/e7f15755-840b-4fb7-af49-a262d33e70a1" />

```http
PUT http://localhost:5001/users/7
Authorization: Bearer {token}
Content-Type: application/json

{
  "full_name": "Uyab Bayu",
  "email": "uyab@mail.com"
}

Response (403 Forbidden):
{
    "error": "Permission denied"
}
```

**DELETE /users/{id}** - Delete User

<img width="1358" height="531" alt="image" src="https://github.com/user-attachments/assets/eceb04e9-0264-4dc4-8d7e-fbac3258b174" />

```http
DELETE http://localhost:5001/users/7
Authorization: Bearer {token}

Response (403 Forbidden):
{
    "error": "Permission denied"
}
```

#### Balance Routes

**GET /users/{id}/balance** - Get Balance

<img width="1366" height="538" alt="image" src="https://github.com/user-attachments/assets/c7c2cd15-d88f-4710-9f9c-7a10121ffed1" />

```http
GET http://localhost:5001/users/7/balance

Response (404 Not Found):
{
    "error": "User not found"
}
```

**POST /users/{id}/topup** - Top Up Balance

<img width="1361" height="525" alt="image" src="https://github.com/user-attachments/assets/2d587149-3432-41d6-b4a5-9bd66c151940" />

```http
POST http://localhost:5001/users/7/topup
Authorization: Bearer {token}
Content-Type: application/json

{
    "amount": 100000
}

Response (403 Forbidden):
{
    "error": "Permission denied"
}
```

#### Internal Routes (Service-to-Service)

**GET /internal/users/{id}** - Get User (Internal)

<img width="1361" height="536" alt="image" src="https://github.com/user-attachments/assets/1aa9006e-0038-45ac-8648-c31acf93a8f1" />

```http
GET http://localhost:5001/internal/users/7
X-Service-Token: service_shared_secret_change_this

Response (404 Not Found):
{
    "error": "User not found"
}
```

**PUT /internal/users/{id}/balance** - Update Balance (Internal)

<img width="1366" height="535" alt="image" src="https://github.com/user-attachments/assets/673adf38-0a98-4cdb-8670-17164a9bba62" />

```http
PUT http://localhost:5001/internal/users/7/balance
X-Service-Token: service_shared_secret_change_this
Content-Type: application/json

{
    "action": "debit",
    "amount": 5000
}

Response (404 Not Found):
{
    "error": "User not found"
}
```

---

### 2️⃣ Transaction Service (Port 5002)

**Base URL**: `http://localhost:5002`

#### Transaction Management Routes

**POST /transactions** - Create Transaction

<img width="1359" height="617" alt="image" src="https://github.com/user-attachments/assets/af22f218-5357-4dbf-8063-ab07d7897a33" />

```http
POST http://localhost:5002/transactions
X-Service-Token: service_shared_secret_change_this
Content-Type: application/json

{
  "user_id": 1,
  "type": "cash",
  "amount": 1000
}

Response (400 Bad Request):
{
    "errors": {
        "type": [
            "Must be one of: debit, credit."
        ]
    }
}
```

**GET /transactions/{id}** - Get Transaction by ID

<img width="1357" height="535" alt="image" src="https://github.com/user-attachments/assets/febf5a83-47c4-4f4c-b1fb-c4e993bff614" />

```http
GET http://localhost:5002/transactions/10

Response (404 Not Found):
{
    "error": "Transaction not found"
}
```

**PUT /transactions/{id}** - Update Transaction Status

<img width="1358" height="524" alt="image" src="https://github.com/user-attachments/assets/a55af2d2-f771-4d13-8228-ceac0dda2a96" />

```http
PUT http://localhost:5002/transactions/10
Content-Type: application/json

{
    "status": "completed"
}

Response (404 Not Found):
{
    "error": "Transaction not found"
}
```

**DELETE /transactions/{id}** - Delete Transaction

<img width="1356" height="536" alt="image" src="https://github.com/user-attachments/assets/217c5177-8b6d-4683-9c7f-f11e94c1a363" />

```http
DELETE http://localhost:5002/transactions/10

Response (404 Not Found):
{
    "error": "Transaction not found"
}
```

---

### 3️⃣ Notification Service (Port 5003)

**Base URL**: `http://localhost:5003`

#### Notification Management Routes

**GET /notifications/{id}** - Get Notification by ID

<img width="1352" height="534" alt="image" src="https://github.com/user-attachments/assets/c6994659-00a9-4970-84f4-d3265e125a3f" />

```http
GET http://localhost:5003/notifications/15

Response (404 Not Found):
{
    "error": "Notification not found"
}
```

**PUT /notifications/{id}** - Update Notification

<img width="1361" height="532" alt="image" src="https://github.com/user-attachments/assets/e9ea9bd8-6bb1-4ecd-94c0-38d07b9c0d05" />

```http
PUT http://localhost:5003/notifications/15
Content-Type: application/json

{
  "message": "Top-up Rp 100.000 berhasil",
  "status": "pending"
}

Response (404 Not Found):
{
    "error": "Notification not found"
}
```

**DELETE /notifications/{id}** - Delete Notification

<img width="1357" height="528" alt="image" src="https://github.com/user-attachments/assets/fd17c761-6fe5-46c1-beb9-7c8212b9f5bc" />

```http
DELETE http://localhost:5003/notifications/15

Response (404 Not Found):
{
    "error": "Notification not found"
}
```

**POST /notifications/{id}/send** - Send Notification via Email

<img width="1362" height="523" alt="image" src="https://github.com/user-attachments/assets/af2a2dbe-780b-4c1f-8d89-333efea4d52e" />

```http
POST http://localhost:5003/notifications/15/send

Response (404 Not Found):
{
    "error": "Notification not found"
}
```

### 4️⃣ Report Service (Port 5004)

**Base URL**: `http://localhost:5004`

#### Report Management Routes

**POST /reports** - Create Report

<img width="1359" height="533" alt="image" src="https://github.com/user-attachments/assets/b89a3550-7a05-4054-acc8-685b31fbc389" />

```http
POST http://localhost:5004/reports
X-Service-Token: service_shared_secret_change_this
Content-Type: application/json

{
  "user_id": 15,
  "transaction_id": 15
}

Response (404 Not Found):
{
    "error": "Transaction not found: Status 404"
}
```

**GET /summaries/user/{user_id}** - Get Summary by User

<img width="1357" height="524" alt="image" src="https://github.com/user-attachments/assets/ac40c20d-59a9-4182-9cd0-d50994bace1e" />

```http
GET http://localhost:5004/summaries/user/10

Response (404 Not Found):
{
    "error": "Summary not found"
}
```

---

## 🧪 Testing dengan Postman

### Import Collection

1. **Buka Postman**
2. **Klik Import** di top-left
3. **Pilih file** `digital-wallet-project.json`
4. **Collection akan ter-import** dengan semua endpoints

### Testing Flow Recommended

Urutan testing yang disarankan untuk memahami alur sistem:

#### 1. User Service Testing

```
1. POST /auth/register - Register user baru
2. POST /auth/login - Login untuk mendapatkan JWT token
3. GET /users - Lihat semua users
4. GET /users/{id} - Lihat detail user tertentu
5. PUT /users/{id} - Update data user
6. GET /users/{id}/balance - Cek saldo user
7. POST /users/{id}/topup - Top up saldo
8. DELETE /users/{id} - Hapus user (optional)
```

#### 2. Transaction Service Testing

```
1. POST /transactions - Buat transaksi baru
2. GET /transactions - Lihat semua transaksi
3. GET /transactions/{id} - Lihat detail transaksi
4. GET /transactions/user/{user_id} - Lihat transaksi per user
5. PUT /transactions/{id} - Update status transaksi
6. DELETE /transactions/{id} - Hapus transaksi
```

#### 3. Notification Service Testing

```
1. POST /notifications - Buat notifikasi
2. GET /notifications - Lihat semua notifikasi
3. GET /notifications/{id} - Lihat detail notifikasi
4. POST /notifications/{id}/send - Kirim notifikasi via email
5. PUT /notifications/{id} - Update notifikasi
6. DELETE /notifications/{id} - Hapus notifikasi
```

#### 4. Report Service Testing

```
1. POST /reports - Buat report
2. GET /reports/user/{user_id} - Lihat laporan per user
3. GET /summaries/user/{user_id} - Lihat ringkasan user
```

### Collection Variables

Postman collection sudah dilengkapi dengan variables untuk kemudahan:

| Variable                | Default                           | Auto-updated     |
| ----------------------- | --------------------------------- | ---------------- |
| `base_url_user`         | http://localhost:5001             | -                |
| `base_url_transaction`  | http://localhost:5002             | -                |
| `base_url_notification` | http://localhost:5003             | -                |
| `base_url_report`       | http://localhost:5004             | -                |
| `jwt_token`             | (empty)                           | ✅ Setelah login |
| `user_id`               | (empty)                           | ✅ Setelah login |
| `transaction_id`        | 1                                 | -                |
| `service_token`         | service_shared_secret_change_this | -                |

### Cara Menggunakan Collection Variables

1. **Login dulu** untuk mendapatkan JWT token
2. **Token otomatis tersimpan** di variable `jwt_token`
3. **Semua request berikutnya** akan menggunakan token ini
4. **User ID juga tersimpan** untuk request selanjutnya

---

## 🔧 Environment Variables

### User Service Configuration

| Variable         | Description              | Example                             |
| ---------------- | ------------------------ | ----------------------------------- |
| `DB_HOST`        | MySQL host               | `mysql-db`                          |
| `DB_USER`        | Database user            | `root`                              |
| `DB_PASSWORD`    | Database password        | `root`                              |
| `DB_NAME`        | Database name            | `digital_wallet_users`              |
| `DB_PORT`        | Database port            | `3306`                              |
| `PORT`           | Service port             | `5001`                              |
| `FLASK_ENV`      | Flask environment        | `development`                       |
| `JWT_SECRET`     | JWT secret key           | `your_jwt_secret_key_change_this`   |
| `JWT_EXPIRATION` | JWT expiration (seconds) | `3600`                              |
| `SERVICE_TOKEN`  | Service-to-service token | `service_shared_secret_change_this` |

### Transaction Service Configuration

| Variable                   | Description              | Example                             |
| -------------------------- | ------------------------ | ----------------------------------- |
| `DB_HOST`                  | MySQL host               | `mysql-db`                          |
| `DB_USER`                  | Database user            | `root`                              |
| `DB_PASSWORD`              | Database password        | `root`                              |
| `DB_NAME`                  | Database name            | `digital_wallet_transactions`       |
| `DB_PORT`                  | Database port            | `3306`                              |
| `PORT`                     | Service port             | `5002`                              |
| `FLASK_ENV`                | Flask environment        | `development`                       |
| `SERVICE_TOKEN`            | Service-to-service token | `service_shared_secret_change_this` |
| `USER_SERVICE_URL`         | User service URL         | `http://user-service:5001`          |
| `NOTIFICATION_SERVICE_URL` | Notification service URL | `http://notification-service:5003`  |

### Notification Service Configuration

| Variable           | Description              | Example                             |
| ------------------ | ------------------------ | ----------------------------------- |
| `DB_HOST`          | MySQL host               | `mysql-db`                          |
| `DB_USER`          | Database user            | `root`                              |
| `DB_PASSWORD`      | Database password        | `root`                              |
| `DB_NAME`          | Database name            | `digital_wallet_notifications`      |
| `DB_PORT`          | Database port            | `3306`                              |
| `PORT`             | Service port             | `5003`                              |
| `FLASK_ENV`        | Flask environment        | `development`                       |
| `SERVICE_TOKEN`    | Service-to-service token | `service_shared_secret_change_this` |
| `USER_SERVICE_URL` | User service URL         | `http://user-service:5001`          |
| `SMTP_SERVER`      | SMTP server              | `smtp.gmail.com`                    |
| `SMTP_PORT`        | SMTP port                | `587`                               |
| `SMTP_USER`        | SMTP username            | `your_email@gmail.com`              |
| `SMTP_PASSWORD`    | SMTP password            | `your_app_password`                 |
| `SENDER_EMAIL`     | Sender email             | `noreply@digitalwallet.com`         |

### Report Service Configuration

| Variable                  | Description              | Example                             |
| ------------------------- | ------------------------ | ----------------------------------- |
| `DB_HOST`                 | MySQL host               | `mysql-db`                          |
| `DB_USER`                 | Database user            | `root`                              |
| `DB_PASSWORD`             | Database password        | `root`                              |
| `DB_NAME`                 | Database name            | `digital_wallet_reports`            |
| `DB_PORT`                 | Database port            | `3306`                              |
| `PORT`                    | Service port             | `5004`                              |
| `FLASK_ENV`               | Flask environment        | `development`                       |
| `SERVICE_TOKEN`           | Service-to-service token | `service_shared_secret_change_this` |
| `USER_SERVICE_URL`        | User service URL         | `http://user-service:5001`          |
| `TRANSACTION_SERVICE_URL` | Transaction service URL  | `http://transaction-service:5002`   |

---

## 🧠 Integrasi Antarservice

### Service Communication Flow

```
┌─────────────────┐
│   User Service  │
│    (5001)       │
└────────┬────────┘
         │ (Internal API)
         │ GET /internal/users/{id}
         │ PUT /internal/users/{id}/balance
         │
    ┌────▼────────────────────────┐
    │                             │
    ▼                             ▼
┌──────────────┐           ┌──────────────┐
│ Transaction  │           │ Notification │
│  Service     │           │   Service    │
│  (5002)      │           │   (5003)     │
└──────┬───────┘           └──────────────┘
       │                          ▲
       │ POST /transactions       │
       │ (creates transactions)   │ POST /notifications
       │                          │ (sends notifications)
       │                          │
       └──────────────┬───────────┘
                      │
                      ▼
            ┌──────────────────┐
            │  Report Service  │
            │   (5004)         │
            └──────────────────┘
```

### Integration Details

#### User Service ↔ Transaction Service

**Saat transaksi dibuat, Transaction Service memanggil User Service:**

```bash
PUT http://user-service:5001/internal/users/{user_id}/balance
X-Service-Token: service_shared_secret_change_this
Content-Type: application/json

{
    "action": "debit",
    "amount": 50000
}
```

#### Transaction Service ↔ Notification Service

**Saat transaksi selesai, Transaction Service memicu Notification Service:**

```bash
POST http://notification-service:5003/notifications
X-Service-Token: service_shared_secret_change_this
Content-Type: application/json

{
    "user_id": 1,
    "message": "Your transaction has been completed successfully"
}
```

#### Report Service ↔ User & Transaction Service

**Report Service mengambil data dari User dan Transaction Service untuk membuat laporan:**

```bash
# Ambil data user
GET http://user-service:5001/internal/users/{user_id}
X-Service-Token: service_shared_secret_change_this

# Ambil data transaksi
GET http://transaction-service:5002/transactions/user/{user_id}
```

### Service Token Security

Service token digunakan untuk memverifikasi bahwa request berasal dari service tertentu:

```python
# Contoh di Flask
@app.before_request
def verify_service_token():
    if request.path.startswith('/internal/'):
        token = request.headers.get('X-Service-Token')
        if token != os.getenv('SERVICE_TOKEN'):
            return {'error': 'Unauthorized'}, 401
```

---

## 📝 Catatan Penting

### JWT Token

- **Expiration**: Token secara default berlaku 1 jam (3600 detik)
- **Jika expired**: Lakukan login ulang untuk mendapatkan token baru
- **Aman**: Jangan share token dengan orang lain

### Database

- **Auto-initialization**: Database dan tables dibuat otomatis melalui `init-db.sql`

### Service Token

- **Purpose**: Untuk verifikasi komunikasi antar service
- **Default**: `service_shared_secret_change_this`
- **Production**: HARUS diubah dengan token yang aman dan kompleks

### Health Check

- **MySQL**: Memiliki health check 30 detik, service lain akan wait hingga MySQL ready
- **Services**: Tunggu 2-3 detik setelah MySQL ready sebelum test

### Port Mapping

| Service              | Internal | External | URL                   |
| -------------------- | -------- | -------- | --------------------- |
| User Service         | 5001     | 5001     | http://localhost:5001 |
| Transaction Service  | 5002     | 5002     | http://localhost:5002 |
| Notification Service | 5003     | 5003     | http://localhost:5003 |
| Report Service       | 5004     | 5004     | http://localhost:5004 |
| MySQL                | 3306     | 3306     | localhost:3306        |

---

---

## 🔐 Security Best Practices

1. **Change Default Credentials**

   ```env
   DB_PASSWORD=very_strong_password_here
   JWT_SECRET=very_secure_jwt_secret_key_here
   SERVICE_TOKEN=very_secure_service_token_here
   ```

2. **Use Environment Variables**

   - Jangan hardcode secret keys di source code
   - Gunakan `.env` file dan jangan commit ke git

3. **HTTPS in Production**

   - Gunakan reverse proxy (nginx/Apache) dengan SSL
   - Implement CORS properly

4. **Database Security**

   - Ganti default MySQL password
   - Limit database user privileges
   - Use strong passwords

5. **API Rate Limiting**
   - Implement rate limiting untuk prevent abuse
   - Use authentication untuk sensitive endpoints

---

## 📞 Support & Debugging

Jika mengalami kendala:

1. **Documentation**: Refer ke README masing-masing service

---

## 📊 API Documentation Summary

### Service Roles

| Service                  | Function                                 | Port |
| ------------------------ | ---------------------------------------- | ---- |
| **User Service**         | Authentication, user management, balance | 5001 |
| **Transaction Service**  | Transaction processing, balance updates  | 5002 |
| **Notification Service** | Email notifications, alerts              | 5003 |
| **Report Service**       | Analytics, reporting, summaries          | 5004 |

### Authentication Methods

| Type              | Usage                  | Header                          |
| ----------------- | ---------------------- | ------------------------------- |
| **JWT Token**     | User API calls         | `Authorization: Bearer {token}` |
| **Service Token** | Internal service calls | `X-Service-Token: {token}`      |

### Response Codes

| Code    | Meaning                        |
| ------- | ------------------------------ |
| **200** | OK - Request successful        |
| **201** | Created - Resource created     |
| **400** | Bad Request - Invalid input    |
| **401** | Unauthorized - Auth required   |
| **403** | Forbidden - Access denied      |
| **404** | Not Found - Resource not found |
| **500** | Server Error - Internal error  |

---

## 👥 Anggota & Peran

| Nama Anggota | Peran               | Service/Fitur yang Dikerjakan |
| ------------ | ------------------- | ----------------------------- |
| Perdog       | Backend Developer   | User Service                  |
| Kenot        | Backend Developer   | Transaction Service           |
| Sarip        | Backend Developer   | Notification Service          |
| Anggota 4    | Backend Developer   | Report Service                |
| Anggota 5    | DevOps / Integrator | API Gateway & Deployment      |

---



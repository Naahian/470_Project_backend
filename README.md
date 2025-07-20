# Inventory Management Backend API

This is a **FastAPI + SQLAlchemy + MySQL** backend for an Inventory Management App. It enables managing products, categories, suppliers, transactions, and users efficiently with robust RESTful APIs. Built to support inventory tracking, sales logging, and stock-level insights.

---

## ✨ Features

- User authentication & roles (`admin`, `user`)
- Product & category management
- Supplier management
- Transaction tracking (sales & purchases)
- Analytics-ready schema (created_by, timestamps, etc.)
- Aiven MySQL cloud DB support with SSL
- Modular and scalable project structure

---

## ⚡ Usage (Development)

### 1. Clone the repo
```bash
git clone https://github.com/your-username/inventory-backend.git
cd inventory-backend
```

### 2. Setup Python environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Setup `.env`
Create a `.env` file in the root directory:

```env
DATABASE_URL=mysql+pymysql://<user>:<password>@<host>:<port>/<dbname>?ssl_ca=ca.pem
```

- Make sure `ca.pem` is also in the root if using Aiven MySQL.

### 4. Run DB migrations (if using Alembic)
```bash
alembic upgrade head
```

### 5. Start the app
```bash
uvicorn main:app --reload
```

Open in browser: [http://localhost:8000/docs](http://localhost:8000/docs)

---

## 🧭 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST   | `/auth/register` | Register a new user |
| POST   | `/auth/login` | Login and get JWT token |
| GET    | `/users/me` | Get current user info |
| GET/POST/PUT/DELETE | `/products/` | CRUD for products |
| GET/POST/PUT/DELETE | `/categories/` | CRUD for categories |
| GET/POST/PUT/DELETE | `/suppliers/` | CRUD for suppliers |
| GET/POST | `/transactions/` | Record and view transactions |
| GET    | `/analytics/summary` | Get summary analytics (if implemented) |

> 📘 Full Swagger docs available at `/docs`

---

## 📂 Project Structure (Simplified)

```
app/
├── main.py
├── models/
├── schemas/
├── routes/
├── services/
├── database.py
├── config.py
.env
ca.pem
```

---

## ⚠️ .gitignore

Make sure to ignore sensitive files:

```gitignore
.env
ca.pem
__pycache__/
*.pyc
```

---
# Inventory Management Backend API

This is a **FastAPI + SQLAlchemy + MySQL** backend for an Inventory Management App. It enables managing products, categories, suppliers, transactions, and users efficiently with robust RESTful APIs. Built to support inventory tracking, sales logging, and stock-level insights.

---

## ✨ Features

- User authentication & roles (`admin`, `user`)
- Product & category management
- Supplier management
- Transaction tracking (sales & purchases)
- Analytics-ready schema (created_by, timestamps, etc.)
- Aiven MySQL cloud DB support with SSL
- Modular and scalable project structure

---

## ⚡ Usage (Development)

### 1. Clone the repo
```bash
git clone https://github.com/your-username/inventory-backend.git
cd inventory-backend
```

### 2. Setup Python environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Setup `.env`
Create a `.env` file in the root directory:

```env
DATABASE_URL=mysql+pymysql://<user>:<password>@<host>:<port>/<dbname>?ssl_ca=ca.pem
```

- Make sure `ca.pem` is also in the root if using Aiven MySQL.

### 4. Run DB migrations (if using Alembic)
```bash
alembic upgrade head
```

### 5. Start the app
```bash
uvicorn main:app --reload
```

Open in browser: [http://localhost:8000/docs](http://localhost:8000/docs)

---

## 🧭 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST   | `/auth/register` | Register a new user |
| POST   | `/auth/login` | Login and get JWT token |
| GET    | `/users/me` | Get current user info |
| GET/POST/PUT/DELETE | `/products/` | CRUD for products |
| GET/POST/PUT/DELETE | `/categories/` | CRUD for categories |
| GET/POST/PUT/DELETE | `/suppliers/` | CRUD for suppliers |
| GET/POST | `/transactions/` | Record and view transactions |
| GET    | `/analytics/summary` | Get summary analytics (if implemented) |

> 📘 Full Swagger docs available at `/docs`

---

## 📂 Project Structure (Simplified)

```
app/
├── main.py
├── models/
├── schemas/
├── routes/
├── services/
├── database.py
├── config.py
.env
ca.pem
```

---

## ⚠️ .gitignore

Make sure to ignore sensitive files:

```gitignore
.env
ca.pem
__pycache__/
*.pyc
```

---

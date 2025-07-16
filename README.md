# 470 Project Backend (FastAPI+MySQL)
(.env in github for to testing.)
## Features
- Password hashing using bcrypt
- JWT token authentication
- Role-based access control
- Token expiration
- Input validation with Pydantic
- SQL injection protection with SQLAlchemy

## Project Structure
```
app/
├── routes/
├── model/            # Database models
├── schema/           # Pydantic schemas
├── crud/             # Database operations
├── database.py         # Database configuration
├── __init__.py         # Database initialization
├── main.py             # FastAPI application
├── requirements.txt    # Dependencies
└── .env               # Environment variables
```
## Setup Instructions

### Local Development

1. **Install dependencies:**
```bash
pip install -r requirements.txt
```

2. **Set up environment variables:**
Create a `.env` file with:
```
DATABASE_URL=mysql+mysqlconnector://username:password@localhost/database_name
SECRET_KEY=your-secret-key-here-change-this-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

3. **Run the application:**
```bash
python main.py
```

The API will be available at `http://localhost:8000`

### Render Deployment
production server is running at https://render.com/
## API Endpoints

### Authentication
- `POST /auth/register` - Register new user
- `POST /auth/login` - Login user
- `GET /auth/me` - Get current user info

### Users (Admin only for most operations)
- `GET /users/` - Get all users (Admin only)
- `GET /users/{user_id}` - Get user by ID
- `PUT /users/{user_id}` - Update user
- `DELETE /users/{user_id}` - Delete user (Admin only)

### Items
- `GET /items/` - Get all items (Authenticated users)
- `GET /items/{item_id}` - Get item by ID (Authenticated users)
- `POST /items/` - Create item (Authenticated users)
- `PUT /items/{item_id}` - Update item (Admin only)
- `DELETE /items/{item_id}` - Delete item (Admin only)

## Role-Based Access Control

### User Role
- Can register and login
- Can view and create items
- Can view and update their own profile

### Admin Role
- All User permissions
- Can view all users
- Can update any user
- Can delete users
- Can update and delete items


## Usage Examples

### Register a new user:
```bash
curl -X POST "http://localhost:8000/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "username": "testuser",
    "password": "password123",
    "full_name": "Test User"
  }'
```

### Login:
```bash
curl -X POST "http://localhost:8000/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=user@example.com&password=password123"
```

### Access protected endpoint:
```bash
curl -X GET "http://localhost:8000/auth/me" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```


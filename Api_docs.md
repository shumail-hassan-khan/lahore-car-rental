## 🔐 User Module

### 1. Register
- **URL:** `/api/register/`
- **Method:** `POST`
- **Body:**
```json
{
  "username": "shumail",
  "email": "shumail@example.com",
  "password": "Strongpassword"
}
```
- **Response:**
```json
{
  "message": "User registered successfully"
}
```

---

### 2. Login
- **URL:** `/api/login/`
- **Method:** `POST`
- **Body:**
```json
{
  "username": "shumail",
  "password": "Strongpassword"
}
```
- **Response:**
```json
{
  "token": "<JWT_TOKEN>"
}
```

---

## 🚗 Vehicle Module

### 1. List Vehicles
- **URL:** `/api/vehicles/`
- **Method:** `GET`
- **Response:**
```json
{
    "status": 1,
    "message": "Vehicle list fetched successfully",
    "data": [
        {
            "id": 10,
            "make": "Honda",
            "model": "Civic",
            "year": 2020,
            "plate": "ABC-123",
            "user": {
                "id": 10,
                "username": "shumail",
                "email": "shumail@example.com"
            }
        },
        {
            "id": 11,
            "make": "Toyota",
            "model": "Corolla",
            "year": 2020,
            "plate": "ABC-123",
            "user": {
                "id": 10,
                "username": "shumail",
                "email": "shumail@example.com"
            }
        }
    ]
}
```

---

### 2. Create Vehicle
- **URL:** `/api/vehicles/`
- **Method:** `POST`
- **Body:**
```json
{
  "make": "Toyota",
  "model": "Corolla",
  "year": 2020,
  "plate": "ABC-123"
}
```
- **Response:**
```json
{
    "status": 1,
    "message": "Vehicle created successfully",
    "data": {
        "id": 11,
        "make": "Toyota",
        "model": "Corolla",
        "year": 2020,
        "plate": "ABC-123",
        "user": {
            "id": 10,
            "username": "shumail",
            "email": "shumail@example.com"
        }
    }
}
```

---

### 3. Update Vehicle
- **URL:** `/api/vehicles/<id>/`
- **Method:** `PUT`
- **Body:**
```json
{
    "status": 1,
    "message": "Vehicle updated successfully",
    "data": {
        "id": 10,
        "make": "Honda",
        "model": "Civic",
        "year": 2020,
        "plate": "ABC-123",
        "user": {
            "id": 10,
            "username": "shumail",
            "email": "shumail@example.com"
        }
    }
}
```

---

### 4. Delete Vehicle
- **URL:** `/api/vehicles/<id>/`
- **Method:** `DELETE`
- **Response:**
```json
{
    "status": 1,
    "message": "Vehicle fetched successfully",
    "data": {
        "id": 10,
        "make": "Honda",
        "model": "Civic",
        "year": 2020,
        "plate": "ABC-123",
        "user": {
            "id": 10,
            "username": "shumail",
            "email": "shumail@example.com"
        }
    }
}
```

---

## 📅 Booking Module

### 1. Get Bookings (with optional date filter)
- **URL:** `/api/bookings/?from=2025-07-01&to=2025-07-10`
- **Method:** `GET`
- **Response:**
```json
{
    "status": 1,
    "message": "Bookings fetched successfully",
    "data": [
        {
            "id": 21,
            "vehicle": {
                "id": 11,
                "make": "Toyota",
                "model": "Corolla",
                "year": 2020,
                "plate": "ABC-123",
                "user": {
                    "id": 10,
                    "username": "shumail",
                    "email": "shumail@example.com"
                }
            },
            "start_date": "2025-07-10",
            "end_date": "2025-07-12",
            "created_at": "2025-07-10T14:37:58.483819Z"
        }
    ]
}
```

---

### 2. Create Booking
- **URL:** `/api/bookings/`
- **Method:** `POST`
- **Body:**
```json
{
  "vehicle_id": 11,
  "start_date": "2025-07-10",
  "end_date": "2025-07-12"
}

```
- **Response:**
```json
{
    "status": 1,
    "message": "Booking created successfully",
    "data": {
        "id": 21,
        "vehicle": {
            "id": 11,
            "make": "Toyota",
            "model": "Corolla",
            "year": 2020,
            "plate": "ABC-123",
            "user": {
                "id": 10,
                "username": "shumail",
                "email": "shumail@example.com"
            }
        },
        "start_date": "2025-07-10",
        "end_date": "2025-07-12",
        "created_at": "2025-07-10T14:37:58.483819Z"
    }
}
```

---
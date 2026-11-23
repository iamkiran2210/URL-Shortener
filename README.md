# Shortly — URL Shortener API

A URL shortener API built with **FastAPI, PostgreSQL, and Redis**. Shortly generates compact, unique short URLs using a Redis-backed counter and Base62 encoding, while PostgreSQL handles user accounts and URL persistence.

## Features

- **URL Shortening:** Transform long URLs into compact, shareable links.
- **Redis Counter:** Generate unique numeric identifiers using Redis.
- **Base62 Encoding:** Convert numeric identifiers into short, URL-friendly codes.
- **Duplicate URL Detection:** Check whether a URL already exists before generating a new short code.
- **User Authentication:** Register and authenticate users.
- **PostgreSQL Persistence:** Store user accounts and URL mappings.
- **URL Redirection:** Resolve short codes to their original destinations.
- **Protected Endpoints:** Secure URL creation and user profile access through Bearer authentication.

## Tech Stack

| Technology | Purpose |
|---|---|
| Python | Backend development |
| FastAPI | REST API framework |
| PostgreSQL | Persistent storage for users and URLs |
| Redis | Atomic counter for generating unique IDs |
| Base62 | Numeric ID encoding into short codes |
| Pydantic | Request validation and data schemas |

## Architecture

Shortly uses Redis for ID generation and PostgreSQL for persistent data storage.

### URL Generation Workflow

When a user submits a long URL:

1. The user sends a URL creation request to the FastAPI backend.
2. The backend checks whether the URL already exists.
3. If the URL exists, its existing short code can be reused.
4. Otherwise, Redis generates the next unique numeric ID using a counter.
5. The numeric ID is encoded into Base62.
6. The generated short code and original URL are stored in PostgreSQL.
7. The API returns the shortened URL information.

### Base62 Encoding

Base62 uses 62 characters to represent numeric identifiers:

```text
0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ
```

Instead of using a long numeric identifier directly, Base62 converts it into a shorter representation.

For example:

```text
Numeric ID  →  Base62 Encoded ID

1           →  1
10          →  a
61          →  Z
62          →  10
```

This provides compact, deterministic short codes for generated IDs.

### URL Redirection Workflow

When someone accesses a shortened URL:

1. The backend receives the short code.
2. It searches PostgreSQL for the corresponding URL mapping.
3. If the mapping exists, the original URL is retrieved.
4. The application redirects the user to the original destination.

### Database Responsibilities

**Redis**
- Maintains the numeric counter.
- Generates unique sequential identifiers.
- Provides atomic counter operations.

**PostgreSQL**
- Stores registered users.
- Stores URLs created by users.
- Maintains the relationship between users and their URLs.
- Stores original URLs and their corresponding short codes.

## Getting Started

### Prerequisites

- Python 3.10+
- PostgreSQL
- Redis
- Git

### Installation

**1. Clone the repository**

```bash
git clone <your-repository-url>
cd shortly
```

**2. Create a virtual environment**

```bash
python -m venv .venv
```

Activate it:

```bash
# Linux / macOS
source .venv/bin/activate

# Windows
.venv\Scripts\activate
```

**3. Install dependencies**

```bash
pip install -r requirements.txt
```

**4. Configure environment variables**

Create a `.env` file in the project root.

Configure your PostgreSQL connection, Redis connection, and other application settings according to your implementation.

**5. Start PostgreSQL and Redis**

Ensure both services are running and accessible to the application.

**6. Run the application**

```bash
uvicorn app.main:app --reload
```

The API will be available at:

```text
http://localhost:8000
```

> Adjust the Uvicorn import path if your application entry point differs.

## API Documentation

### Authentication

| Method | Endpoint | Description | Authentication |
|---|---|---|---|
| POST | `/auth/register` | Register a new user | Not required |
| POST | `/auth/login` | Authenticate a user | Not required |
| GET | `/user/me` | Get current user details | Required |

### URL Management

| Method | Endpoint | Description | Authentication |
|---|---|---|---|
| POST | `/urls/` | Create a shortened URL | Required |
| GET | `/urls/?short_code={code}` | Retrieve URL using short code | Not specified |

## API Usage

### 1. Register a User

**Request**

```http
POST /auth/register
Content-Type: application/json
```

```json
{
  "username": "kiran",
  "password": "your_password"
}
```

**Response — 200 OK**

```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "username": "kiran",
  "created_at": "2026-11-23T10:30:00Z"
}
```

### 2. Login

**Request**

```http
POST /auth/login
Content-Type: application/json
```

```json
{
  "username": "kiran",
  "password": "your_password"
}
```

**Response — 200 OK**

```json
{
  "message": "Login successful",
  "access_token": "<access_token>",
  "refresh_token": "<refresh_token>"
}
```

### 3. Get Current User

**Request**

```http
GET /user/me
Authorization: Bearer <access_token>
```

**Response — 200 OK**

```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "username": "kiran",
  "created_at": "2026-11-23T10:30:00Z"
}
```

### 4. Shorten a URL

**Request**

```http
POST /urls/
Authorization: Bearer <access_token>
Content-Type: application/json
```

```json
{
  "long_url": "https://www.example.com/articles/this-is-a-very-long-url"
}
```

**Response — 200 OK**

```json
{
  "long_url": "https://www.example.com/articles/this-is-a-very-long-url",
  "short_code": "aB12xY",
  "created_at": "2026-11-23T10:35:00Z"
}
```

### 5. Retrieve a URL

**Request**

```http
GET /urls/?short_code=aB12xY
```

The backend resolves the short code to its original URL and redirects the client to the destination.

## Authentication

Shortly uses HTTP Bearer authentication for protected endpoints.

Include the access token in the Authorization header:

```http
Authorization: Bearer <access_token>
```

Protected endpoints:

- `GET /user/me`
- `POST /urls/`

## Interactive API Documentation

FastAPI provides interactive API documentation.

Once the server is running:

| Documentation | URL |
|---|---|
| Swagger UI | http://localhost:8000/docs |
| ReDoc | http://localhost:8000/redoc |
| OpenAPI JSON | http://localhost:8000/openapi.json |

## Project Structure

```text
shortly/
│
├── app/
│   ├── main.py
│   └── ...
│
├── .env
├── requirements.txt
└── README.md
```

*Update this structure to match the actual repository layout.*

## Error Handling

| Status Code | Meaning |
|---|---|
| 200 | Request successful |
| 401 | Authentication required or invalid credentials |
| 403 | Access forbidden |
| 404 | Resource not found |
| 422 | Request validation error |
| 500 | Internal server error |

**Shortly** — Turning long URLs into short, shareable links.

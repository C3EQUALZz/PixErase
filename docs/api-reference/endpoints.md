# API Endpoints

The PixErase API provides a RESTful interface for OSINT operations, image processing, and user management. All endpoints are versioned under `/v1`.

## Base URL

- **Development**: `http://localhost:8080/api`
- **Staging/Production**: `http://<host>/api`

## Authentication

Most endpoints require authentication via JWT token stored in HTTP-only cookies. The token is automatically sent with each request after successful login.

## Endpoints

### **Healthcheck**

#### `GET /v1/healthcheck/`

- **Description**: Checks the API's health status.
- **Authentication**: Not required
- **Response**:
  ```json
  { "message": "ok", "status": "success" }
  ```
- **Status**: 200 OK

### **Index**

#### `GET /v1/`

- **Description**: Returns a welcome message.
- **Authentication**: Not required
- **Response**:
  ```json
  { "message": "Hello there! Welcome to API" }
  ```
- **Status**: 200 OK

### Authentication

#### `POST /v1/auth/signup/`

- **Description**: Registers a new user account.
- **Authentication**: Not required
- **Request Body**:
  ```json
  {
    "email": "john.smith@example.com",
    "name": "John Smith",
    "password": "super-puper-password-123"
  }
  ```
- **Response**:
  ```json
  {
    "id": "0c8ba68a-299d-42d9-aca6-5b4056d3fd0f"
  }
  ```
- **Status**: 201 Created, 400 Bad Request, 409 Conflict, 422 Unprocessable Entity

#### `POST /v1/auth/login/`

- **Description**: Authenticates a user and creates a session. Sets JWT access token in HTTP-only cookies.
- **Authentication**: Not required
- **Request Body**:
  ```json
  {
    "email": "john.smith@example.com",
    "password": "super-puper-password-123"
  }
  ```
- **Response**: None (sets cookie)
- **Status**: 204 No Content, 401 Unauthorized, 403 Forbidden, 404 Not Found, 422 Unprocessable Entity

#### `POST /v1/auth/logout/`

- **Description**: Terminates the current user session.
- **Authentication**: Required
- **Response**: None
- **Status**: 204 No Content, 401 Unauthorized

#### `GET /v1/auth/me/`

- **Description**: Returns the current authenticated user's information.
- **Authentication**: Required
- **Response**: See Read User Response
- **Status**: 200 OK, 401 Unauthorized, 404 Not Found

### User Management

#### `GET /v1/user/`

- **Description**: Retrieves a paginated list of users with sorting and filtering.
- **Authentication**: Required
- **Query Parameters**:
  - `limit` _(optional)_: Number of results (default: 20, min: 1).
  - `offset` _(optional)_: Pagination offset (default: 0, max: 100).
  - `sorting_field` _(optional)_: Field to sort by - `email` or `name` (default: `email`).
  - `sorting_order` _(optional)_: Sort order - `ASC` or `DESC` (default: `DESC`).
- **Response**:
  ```json
  {
    "users": [
      {
        "id": "75079971-fb0e-4e04-bf07-ceb57faebe84",
        "email": "user1@example.com",
        "name": "User One",
        "role": "user"
      }
    ]
  }
  ```
- **Status**: 200 OK, 401 Unauthorized, 403 Forbidden

#### `GET /v1/user/id/{user_id}/`

- **Description**: Retrieves a user by ID.
- **Authentication**: Required
- **Path Parameters**:
  - `user_id`: User identifier (UUID).
- **Response**: See Read User Response
- **Status**: 200 OK, 401 Unauthorized, 403 Forbidden, 404 Not Found

#### `POST /v1/user/`

- **Description**: Creates a new user (admin only).
- **Authentication**: Required (Admin)
- **Request Body**:
  ```json
  {
    "email": "ilovejava23@gmail.com",
    "name": "Egoryan Grishkov",
    "password": "SuperBobratus",
    "role": "admin"
  }
  ```
- **Response**:
  ```json
  {
    "id": "08bde6f0-06c7-43f2-ab5d-d60ca062c5b5"
  }
  ```
- **Status**: 201 Created, 400 Bad Request, 401 Unauthorized, 403 Forbidden, 409 Conflict, 422 Unprocessable Entity

#### `PATCH /v1/user/name/`

- **Description**: Updates the current user's name.
- **Authentication**: Required
- **Request Body**:
  ```json
  {
    "name": "super-bagratus"
  }
  ```
- **Response**: None
- **Status**: 204 No Content, 400 Bad Request, 401 Unauthorized, 422 Unprocessable Entity

#### `PATCH /v1/user/email/`

- **Description**: Updates the current user's email address.
- **Authentication**: Required
- **Request Body**:
  ```json
  {
    "email": "super-bagratus2013@gmail.com"
  }
  ```
- **Response**: None
- **Status**: 204 No Content, 400 Bad Request, 401 Unauthorized, 409 Conflict, 422 Unprocessable Entity

#### `PATCH /v1/user/password/`

- **Description**: Updates the current user's password.
- **Authentication**: Required
- **Request Body**:
  ```json
  {
    "password": "new-secure-password-123"
  }
  ```
- **Response**: None
- **Status**: 204 No Content, 400 Bad Request, 401 Unauthorized, 422 Unprocessable Entity

#### `DELETE /v1/user/id/{user_id}/`

- **Description**: Deletes a user by ID.
- **Authentication**: Required (Admin)
- **Path Parameters**:
  - `user_id`: User identifier (UUID).
- **Response**: None
- **Status**: 204 No Content, 401 Unauthorized, 403 Forbidden, 404 Not Found

#### `PATCH /v1/user/id/{user_id}/grant-admin/`

- **Description**: Grants admin role to a user (super_admin only).
- **Authentication**: Required (Super Admin)
- **Path Parameters**:
  - `user_id`: User identifier (UUID).
- **Response**: None
- **Status**: 204 No Content, 401 Unauthorized, 403 Forbidden, 404 Not Found

#### `PATCH /v1/user/id/{user_id}/revoke-admin/`

- **Description**: Revokes admin role from a user (super_admin only).
- **Authentication**: Required (Super Admin)
- **Path Parameters**:
  - `user_id`: User identifier (UUID).
- **Response**: None
- **Status**: 204 No Content, 401 Unauthorized, 403 Forbidden, 404 Not Found

#### `PATCH /v1/user/id/{user_id}/activate/`

- **Description**: Activates a user account (admin only).
- **Authentication**: Required (Admin)
- **Path Parameters**:
  - `user_id`: User identifier (UUID).
- **Response**: None
- **Status**: 204 No Content, 401 Unauthorized, 403 Forbidden, 404 Not Found

### Image Processing

#### `POST /v1/image/`

- **Description**: Uploads and creates a new image.
- **Authentication**: Required
- **Request**: `multipart/form-data` with `image` file
- **Response**:
  ```json
  {
    "image_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890"
  }
  ```
- **Status**: 201 Created, 400 Bad Request, 401 Unauthorized, 422 Unprocessable Entity

#### `GET /v1/image/id/{image_id}/`

- **Description**: Retrieves an image by ID (returns image binary data).
- **Authentication**: Required
- **Path Parameters**:
  - `image_id`: Image identifier (UUID).
- **Response**: Image binary data with appropriate `Content-Type` header
- **Status**: 200 OK, 401 Unauthorized, 404 Not Found

#### `DELETE /v1/image/id/{image_id}/`

- **Description**: Deletes an image by ID.
- **Authentication**: Required
- **Path Parameters**:
  - `image_id`: Image identifier (UUID).
- **Response**: None
- **Status**: 204 No Content, 401 Unauthorized, 404 Not Found

#### `GET /v1/image/id/{image_id}/exif/`

- **Description**: Retrieves EXIF metadata from an image.
- **Authentication**: Required
- **Path Parameters**:
  - `image_id`: Image identifier (UUID).
- **Response**: See Read Image EXIF Response in Data Models
- **Status**: 200 OK, 401 Unauthorized, 404 Not Found

#### `PATCH /v1/image/id/{image_id}/rotate/`

- **Description**: Rotates an image by specified angle (asynchronous task).
- **Authentication**: Required
- **Path Parameters**:
  - `image_id`: Image identifier (UUID).
- **Request Body**:
  ```json
  {
    "angle": 90
  }
  ```
- **Response**:
  ```json
  {
    "task_id": "rotate_image:75079971-fb0e-4e04-bf07-ceb57faebe84"
  }
  ```
- **Status**: 202 Accepted, 400 Bad Request, 401 Unauthorized, 404 Not Found, 422 Unprocessable Entity

#### `PATCH /v1/image/id/{image_id}/grayscale/`

- **Description**: Converts an image to grayscale (asynchronous task).
- **Authentication**: Required
- **Path Parameters**:
  - `image_id`: Image identifier (UUID).
- **Response**:
  ```json
  {
    "task_id": "grayscale_image:75079971-fb0e-4e04-bf07-ceb57faebe84"
  }
  ```
- **Status**: 202 Accepted, 401 Unauthorized, 404 Not Found

#### `PATCH /v1/image/id/{image_id}/upscale/`

- **Description**: Upscales an image using AI or Nearest Neighbour algorithm (asynchronous task).
- **Authentication**: Required
- **Path Parameters**:
  - `image_id`: Image identifier (UUID).
- **Request Body**:
  ```json
  {
    "algorithm": "AI",
    "scale": 4
  }
  ```
- **Response**:
  ```json
  {
    "task_id": "upscale_image:75079971-fb0e-4e04-bf07-ceb57faebe84"
  }
  ```
- **Status**: 202 Accepted, 400 Bad Request, 401 Unauthorized, 404 Not Found, 422 Unprocessable Entity

#### `PATCH /v1/image/id/{image_id}/remove-background/`

- **Description**: Removes background from an image (asynchronous task).
- **Authentication**: Required
- **Path Parameters**:
  - `image_id`: Image identifier (UUID).
- **Response**:
  ```json
  {
    "task_id": "remove_background_image:75079971-fb0e-4e04-bf07-ceb57faebe84"
  }
  ```
- **Status**: 202 Accepted, 401 Unauthorized, 404 Not Found

#### `PATCH /v1/image/id/{image_id}/compress/`

- **Description**: Compresses an image (asynchronous task).
- **Authentication**: Required
- **Path Parameters**:
  - `image_id`: Image identifier (UUID).
- **Request Body**:
  ```json
  {
    "quality": 85
  }
  ```
- **Response**:
  ```json
  {
    "task_id": "compress_image:75079971-fb0e-4e04-bf07-ceb57faebe84"
  }
  ```
- **Status**: 202 Accepted, 400 Bad Request, 401 Unauthorized, 404 Not Found, 422 Unprocessable Entity

### Internet Protocol / OSINT

#### `GET /v1/ip/ping/`

- **Description**: Pings an IP address or hostname.
- **Authentication**: Required
- **Query Parameters**:
  - `destination_address`: Target IP address or hostname (required).
  - `timeout` _(optional)_: Ping timeout in seconds (default: 4.0, min: 0.1).
  - `packet_size` _(optional)_: Packet size in bytes (default: 56, min: 56).
  - `ttl` _(optional)_: Time to live (min: 1).
- **Response**: See Ping Response in Data Models
- **Status**: 200 OK, 400 Bad Request, 401 Unauthorized, 408 Request Timeout, 500 Internal Server Error

#### `GET /v1/ip/info/`

- **Description**: Retrieves geolocation and network information for an IP address.
- **Authentication**: Required
- **Query Parameters**:
  - `destination_address`: Target IP address (required).
- **Response**: See Read IP Info Response in Data Models
- **Status**: 200 OK, 400 Bad Request, 401 Unauthorized, 404 Not Found

#### `GET /v1/ip/analyze-domain/`

- **Description**: Analyzes a domain for DNS records, subdomains, and HTTP title.
- **Authentication**: Required
- **Query Parameters**:
  - `domain`: Target domain name or IP address (required).
  - `timeout`: Analysis timeout in seconds (required, min: 0.1).
- **Response**: See Analyze Domain Response in Data Models
- **Status**: 200 OK, 400 Bad Request, 401 Unauthorized, 408 Request Timeout, 422 Unprocessable Entity

#### `POST /v1/ip/scan-ports/single/`

- **Description**: Scans a single port on a target host.
- **Authentication**: Required
- **Request Body**:
  ```json
  {
    "target": "192.168.1.1",
    "port": 80,
    "timeout": 1.0
  }
  ```
- **Response**: See Port Scan Response in Data Models
- **Status**: 200 OK, 400 Bad Request, 401 Unauthorized, 408 Request Timeout, 500 Internal Server Error

#### `POST /v1/ip/scan-ports/multiple/`

- **Description**: Scans multiple ports on a target host concurrently.
- **Authentication**: Required
- **Request Body**:
  ```json
  {
    "target": "192.168.1.1",
    "ports": [80, 443, 22, 5432],
    "timeout": 1.0,
    "max_concurrent": 100
  }
  ```
- **Response**: See Port Scan Summary Response in Data Models
- **Status**: 200 OK, 400 Bad Request, 401 Unauthorized, 408 Request Timeout, 500 Internal Server Error

#### `POST /v1/ip/scan-ports/range/`

- **Description**: Scans a range of ports on a target host.
- **Authentication**: Required
- **Request Body**:
  ```json
  {
    "target": "192.168.1.1",
    "start_port": 1,
    "end_port": 1000,
    "timeout": 1.0,
    "max_concurrent": 100
  }
  ```
- **Response**: See Port Scan Summary Response in Data Models
- **Status**: 200 OK, 400 Bad Request, 401 Unauthorized, 408 Request Timeout, 422 Unprocessable Entity, 500 Internal Server Error

#### `POST /v1/ip/scan-ports/common/`

- **Description**: Scans common ports (well-known service ports) on a target host.
- **Authentication**: Required
- **Request Body**:
  ```json
  {
    "target": "192.168.1.1",
    "timeout": 1.0,
    "max_concurrent": 100
  }
  ```
- **Response**: See Port Scan Summary Response in Data Models
- **Status**: 200 OK, 400 Bad Request, 401 Unauthorized, 408 Request Timeout, 500 Internal Server Error

### Task Management

#### `GET /v1/task/id/{task_id}/`

- **Description**: Retrieves the status of an asynchronous task.
- **Authentication**: Required
- **Path Parameters**:
  - `task_id`: Task identifier in format `{operation_type}:{uuid}` (e.g., `rotate_image:75079971-fb0e-4e04-bf07-ceb57faebe84`).
- **Response**: See Read Task Response in Data Models
- **Status**: 200 OK, 400 Bad Request, 401 Unauthorized, 404 Not Found, 422 Unprocessable Entity

## Swagger UI

Interactive API documentation is available at:

- **Development**: http://localhost:8080/api/docs
- **Production**: http://<host>/api/docs

See [Data Models](data-models.md) for detailed request/response schemas.
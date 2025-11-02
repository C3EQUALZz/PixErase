# Data Models

The PixErase API uses structured data models for requests and responses, defined in `src/pix_erase/domain` entities and `src/pix_erase/presentation/http/v1/routes` schemas.

## Entities

### User

- **Location**: `src/pix_erase/domain/user/entities/user.py`
- **Fields**:
  - `id` (UUID): Unique identifier (UserID).
  - `email` (UserEmail): User email address (must be valid format, unique in system).
  - `name` (Username): User display name (5–255 characters).
  - `hashed_password` (HashedPassword): Bcrypt-hashed password.
  - `role` (UserRole, optional): User role - `user`, `admin`, or `super_admin` (default: `user`).
  - `is_active` (bool, optional): Account activation status (default: `True`).
  - `images` (list[ImageID], optional): List of associated image IDs (default: `[]`).
  - `created_at` (datetime): Entity creation timestamp.
  - `updated_at` (datetime): Entity last update timestamp.

### Image

- **Location**: `src/pix_erase/domain/image/entities/image.py`
- **Fields**:
  - `id` (UUID): Unique identifier (ImageID).
  - `data` (bytes): Raw image binary data.
  - `width` (ImageSize): Image width in pixels (must be positive).
  - `height` (ImageSize): Image height in pixels (must be positive).
  - `name` (ImageName): Image filename (non-empty, no Cyrillic characters).
  - `created_at` (datetime): Entity creation timestamp.
  - `updated_at` (datetime): Entity last update timestamp.

### InternetDomain

- **Location**: `src/pix_erase/domain/internet_protocol/entities/internet_domain.py`
- **Fields**:
  - `id` (UUID): Unique identifier (DomainID).
  - `domain_name` (DomainName): Validated domain name (RFC 1123 compliant).
  - `dns_records` (DnsRecords, optional): Cached DNS records (A, AAAA, MX, NS, TXT, CNAME, SOA).
  - `subdomains` (list[DomainName], optional): List of discovered subdomains (default: `[]`).
  - `title` (str, optional): HTTP title extracted from domain.
  - `is_analyzed` (bool, optional): Analysis completion flag (default: `False`).
  - `created_at` (datetime): Entity creation timestamp.
  - `updated_at` (datetime): Entity last update timestamp.

## Value Objects

Value objects enforce validation rules at the domain level:

### Username (`src/pix_erase/domain/user/values/user_name.py`):

- **Length**: 5–255 characters.
- **Rules**: Cannot be empty or whitespace-only.
- **Errors**: `UserAccountNameCantBeEmptyError`, `TooBigUserAccountNameError`.

### UserEmail (`src/pix_erase/domain/user/values/user_email.py`):

- **Format**: Valid email address format (regex + `parseaddr` validation).
- **Rules**: Must match email pattern (e.g., `user@example.com`).
- **Errors**: `WrongUserAccountEmailFormatError`.

### ImageName (`src/pix_erase/domain/image/values/image_name.py`):

- **Rules**: Non-empty, cannot contain Cyrillic characters.
- **Errors**: `BadImageNameError`.

### ImageSize (`src/pix_erase/domain/image/values/image_size.py`):

- **Range**: Must be positive integer (> 0).
- **Errors**: `BadImageSizeError`.

### DomainName (`src/pix_erase/domain/internet_protocol/values/domain_name.py`):

- **Format**: RFC 1123 compliant domain name.
- **Rules**: 
  - Total length up to 253 characters.
  - Each label (part between dots) can be 1–63 characters.
  - Can contain letters, digits, and hyphens.
  - Hyphens cannot be at the beginning or end of a label.
  - Must have at least one TLD with minimum 2 characters.
- **Errors**: `InvalidDomainNameError`.

### UserRole (`src/pix_erase/domain/user/values/user_role.py`):

- **Values**: `"user"`, `"admin"`, `"super_admin"`.
- **Rules**: `super_admin` role is not assignable or changeable by users.

## API Schemas

### Sign Up Request

```json
{
  "email": "john.smith@example.com",
  "name": "John Smith",
  "password": "super-puper-password-123"
}
```

### Sign Up Response

```json
{
  "id": "0c8ba68a-299d-42d9-aca6-5b4056d3fd0f"
}
```

### Create User Request

```json
{
  "email": "ilovejava23@gmail.com",
  "name": "Egoryan Grishkov",
  "password": "SuperBobratus",
  "role": "admin"
}
```

### Read User Response

```json
{
  "id": "75079971-fb0e-4e04-bf07-ceb57faebe84",
  "email": "tiji-hiyosi44@mail.ru",
  "name": "Egorutine",
  "role": "admin"
}
```

### Create Image Response

```json
{
  "image_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890"
}
```

### Analyze Domain Response

```json
{
  "domain_id": "b2c3d4e5-f6a7-8901-bcde-f12345678901",
  "domain_name": "example.com",
  "dns_records": {
    "A": ["93.184.216.34"],
    "AAAA": ["2606:2800:220:1:248:1893:25c8:1946"],
    "MX": ["10 mail.example.com"],
    "NS": ["ns1.example.com", "ns2.example.com"],
    "TXT": ["v=spf1 include:_spf.example.com ~all"],
    "CNAME": [],
    "SOA": ["ns1.example.com admin.example.com 2023010101 3600 1800 604800 86400"]
  },
  "subdomains": ["www.example.com", "mail.example.com"],
  "title": "Example Domain",
  "created_at": "2024-01-01T12:00:00Z",
  "updated_at": "2024-01-01T12:00:00Z"
}
```

#### Port Scan Request

```json
{
  "target": "192.168.1.1",
  "port": 80,
  "timeout": 1.0
}
```

#### Port Scan Response

```json
{
  "port": 80,
  "status": "open",
  "response_time": 0.05,
  "service": "http",
  "error_message": null,
  "scanned_at": "2024-01-01T12:00:00Z"
}
```

#### Port Scan Multiple Request

```json
{
  "target": "192.168.1.1",
  "ports": [80, 443, 22, 5432],
  "timeout": 1.0,
  "max_concurrent": 100
}
```

#### Port Scan Range Request

```json
{
  "target": "192.168.1.1",
  "start_port": 1,
  "end_port": 1000,
  "timeout": 1.0,
  "max_concurrent": 100
}
```

#### Port Scan Common Request

```json
{
  "target": "192.168.1.1",
  "timeout": 1.0,
  "max_concurrent": 100
}
```

#### Port Scan Summary Response

```json
{
  "target": "192.168.1.1",
  "port_range": "1-1000",
  "total_ports": 1000,
  "open_ports": 3,
  "closed_ports": 997,
  "filtered_ports": 0,
  "scan_duration": 45.2,
  "started_at": "2024-01-01T12:00:00Z",
  "completed_at": "2024-01-01T12:00:45Z",
  "success_rate": 0.995,
  "results": [
    {
      "port": 80,
      "status": "open",
      "response_time": 0.05,
      "service": "http",
      "error_message": null,
      "scanned_at": "2024-01-01T12:00:00Z"
    },
    {
      "port": 443,
      "status": "open",
      "response_time": 0.08,
      "service": "https",
      "error_message": null,
      "scanned_at": "2024-01-01T12:00:01Z"
    }
  ]
}
```

### Task Management

#### Read Task Response

```json
{
  "status": "success",
  "description": "Image processing completed successfully"
}
```

**Task Status Values:**
- `"success"`: Task completed successfully
- `"failure"`: Task failed with error
- `"started"`: Task has started processing
- `"retrying"`: Task is being retried after failure
- `"processing"`: Task is currently being processed

> [!NOTE]
> For other schemas see `Swagger`
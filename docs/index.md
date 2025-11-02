# PixErase Documentation

Welcome to the documentation for the **PixErase**, my scientific research work for university.  

## Project Overview

PixErase is an OSINT (Open Source Intelligence) platform for digital image analysis and network reconnaissance. 
The platform provides tools for processing images, analyzing network infrastructure, and gathering publicly available information through various internet protocols.

Built using Robert Martin's (Uncle Bob) Clean Architecture principles, the project emphasizes dependency inversion, modularity, and separation of concerns.

### Key Features

- **Image Processing**: Compression, format conversion, watermark removal, background extraction, and EXIF metadata analysis.
- **Network Reconnaissance**: Port scanning, IP address analysis, domain investigation, and certificate transparency monitoring.
- **RESTful API** powered by FastAPI.
- **Clean Architecture** for scalable and maintainable code.
- **Dependency Injection** using the Dishka framework.
- **Database** integration with PostgreSQL and SQLAlchemy.
- **Observability** with Prometheus, Grafana, Loki, and Tempo.
- **CI/CD** pipelines using GitHub Actions.
- **Comprehensive testing** with Pytest and coverage reports.

## Getting Started

To start using the PixErase, follow the [Quick Start](getting-started/quick-start.md) guide to set up the project locally or deploy it using Docker.

## Repository

- **Source**: [GitHub](https://github.com/C3EQUALZz/PixErase)
- **License**: [MIT](license.md)
- **Author**: Danil Kovalev ([GitHub](https://github.com/C3EQUALZz))

---

Explore the documentation to learn about the [Architecture](architecture/backend/overview.md), [API Reference](api-reference/endpoints.md), and [Development](development/testing.md) processes.
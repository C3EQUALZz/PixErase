# Installation

This guide covers the prerequisites and installation steps for the PixErase.

## Prerequisites

- **Docker**: For containerized deployment
- **Git**: For cloning the repository

## Installation Steps

1. **Clone the Repository**:

   ```bash
   git clone https://github.com/C3EQUALZz/PixErase
   cd PixErase
   ```

2. **Set Up Environment**:

   Create .env file and copy-paste all data from .env.dist

3. **Docker Setup**:
    
   To run the full stack with Docker
   
   ```bash
   just up
   ```

   This starts all services defined in docker-compose.prod.yaml, including the API, database, and observability tools.
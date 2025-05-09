# Payment Gateway System

A complete payment processing system with:
- **FastAPI backend** (payment-gateway)
- **Laravel frontend** (payment-gateway-client)

## 🚀 Features

### API (FastAPI)
- Payment initiation with status simulation (Pending/Success/Failed)
- Transaction status checking
- MySQL database integration
- Docker containerization
- Rate limiting

### Client (Laravel)
- Payment initiation form
- Transaction status viewer
- Tailwind CSS styling
- Docker containerization

## 📦 Prerequisites

- Docker 20.10+
- Docker Compose 2.0+
- Python 3.9+ (for API development)
- PHP 8.1+ (for client development)

## 🛠️ Deployment

### Single-Command Setup (Production)

```bash
git clone https://github.com/kagsburg/payment-gateway
cd payment-gateway-client
docker-compose up --build -d
````
## Service Access

| Service          | URL                          | Port Mapping              |
|------------------|------------------------------|---------------------------|
| **Client App**   | http://localhost:8001        | Host 8001 → Container 80  |
| **API Docs**     | http://localhost:8000/docs   | Host 8000 → Container 8000|
| **MySQL**        | Available internally only    | Host 3306 → Container 3306|
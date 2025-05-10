# Payment Gateway System

A complete payment processing system with:
- **FastAPI backend** (payment-gateway)
- **Laravel frontend** (payment-gateway-client)

## Features

### API (FastAPI  + MySQL)
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

### Single-Command Setup (Dev)

```bash
git clone https://github.com/kagsburg/payment-gateway
````
```bash
cd payment-gateway
````
```bash
docker-compose up -d
````
This single command docker-compose up -d  will:

- **Build and start all containers** (Laravel client + FastAPI + MySQL)
- **Automatically pull/publish all dependencies**
- **Set up network connections** between services

## Service Access

| Service          | URL                          | Port Mapping              |
|------------------|------------------------------|---------------------------|
| **Client App**   | http://localhost:8001        | Host 8001 → Container 80  |
| **API Endpoint** | http://localhost:8083/       | Host 8083 → Container 8000|
| **MySQL**        | Available internally only    | Host 3308 → Container 3306|
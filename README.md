# MicroMarket-

MicroMarket- is a modern and flexible platform for creating and managing online markets and stores. The project includes a user registration system, product management, and security features using JWT tokens. It provides a convenient interface for both sellers and buyers, as well as the ability to integrate with payment systems and third-party services.

Description
MicroMarket- is a project that allows the creation of online stores with product and user management functionality. The project includes the following key features:

User Registration with email and password.
JWT Token Authentication for user login and secure access.
Product Management (adding, updating, deleting products).
Product Search by name or slug.
Security: All key operations are protected with modern authentication and authorization methods.
Multiple Database Support: The system supports both the main and test databases for isolating tests.
Technology Stack
Backend: FastAPI, Pydantic
Database: PostgreSQL
Authentication: JWT
Containerization: Docker, Docker Compose
Testing: Pytest
CI/CD: GitHub Actions
Installation and Setup

Clone the repository:
  git clone https://github.com/your_project/MicroMarket-.git
  cd MicroMarket-

Ensure that you have Docker and Docker Compose installed on your machine.
To start the containers for the app and the database, run:
  docker-compose up -d

This will create and start the containers for your project and database.

To stop the containers, use:
  docker-compose down

Usage
After successfully starting the project, you can access the API at http://localhost:8000.
Use a client like Postman or cURL to interact with the API.

Development
  Install dependencies:
    poetry install
  Run the server:
    uvicorn main:app --reload


Contributing
Fork this repository.
Create a new branch (git checkout -b feature-feature_name).
Make your changes.
Open a pull request

# ✅ FastAPI To-Do List Backend

A high-performance backend for a To-Do list application, built with FastAPI, SQLAlchemy, and Pydantic.

---

## 🚀 Project Description

This repository contains the complete backend logic for a feature-rich To-Do application. It is built using **FastAPI**, a modern, fast (high-performance) web framework for building APIs with Python. The application handles task management and user authentication, using **SQLAlchemy** to communicate with a **SQLite** database and **Pydantic** models to ensure all data is valid and well-structured. This project is a perfect example of a clean, modular, and scalable Python backend.

---

## ✨ Key Features

* **Full CRUD for Tasks**: Complete API endpoints to Create, Read, Update, and Delete to-do items.
* **User Authentication**: A dedicated module to handle secure user registration and login.
* **SQLAlchemy ORM**: Uses the powerful SQLAlchemy ORM for elegant and efficient database operations.
* **Pydantic Data Validation**: Leverages Pydantic schemas for robust data validation, serialization, and documentation.
* **High-Performance API**: Built with **FastAPI**, providing asynchronous speed and automatic interactive API documentation (via Swagger UI).
* **SQLite Database**: Uses a simple and lightweight file-based SQLite database (`todos.db`).
* **Modular Architecture**: Well-organized project structure with separate modules for database, models, schemas, and authentication.

---

## 💻 Technology Stack

* **Web Framework**: **FastAPI**
* **Database ORM**: **SQLAlchemy**
* **Data Validation**: **Pydantic**
* **Database**: **SQLite**
* **Language**: **Python**
* **ASGI Server**: **Uvicorn** (for running the application)

---

## ⚙️ Setup and Installation

To get this project running locally on your machine, follow these steps:

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/your-username/Todo-python-backend.git](https://github.com/your-username/Todo-python-backend.git)
    cd Todo-python-backend/backend
    ```

2.  **Create a virtual environment and install dependencies:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    pip install -r requirements.txt
    ```

3.  **Run the application:**
    * The application is served using Uvicorn, an ASGI server.
    ```bash
    uvicorn main:app --reload
    ```

4.  **Access the API Documentation:**
    * Once the server is running, you can access the interactive Swagger UI documentation in your browser to test the API endpoints:
    * **http://127.0.0.1:8000/docs******

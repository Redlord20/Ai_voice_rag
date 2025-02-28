# Ai_voice_rag

# FastAPI Setup Guide

This guide will help you set up a Python virtual environment, install dependencies, and run a FastAPI application on both macOS and Windows.

## Prerequisites

- Python (>=3.8) installed
- pip installed (comes with Python)
- Virtual environment module (`venv`) available

---

## 1. Creating a Virtual Environment

### **On macOS and Linux**

Open a terminal and run the following commands:

```bash
# Navigate to your project folder
cd /path/to/your/project

# Create a virtual environment
python3 -m venv venv

# Activate the virtual environment
source venv/bin/activate
```

### **On Windows**

Open Command Prompt or PowerShell and run:

```powershell
# Navigate to your project folder
cd C:\path\to\your\project

# Create a virtual environment
python -m venv venv

# Activate the virtual environment (Command Prompt)
venv\Scripts\activate

# OR (PowerShell)
venv\Scripts\Activate.ps1
```

---

## 2. Installing Dependencies

Once the virtual environment is activated, install all required dependencies using:

```bash
pip install -r requirements.txt
```

Make sure your `requirements.txt` includes:

```
fastapi
uvicorn
```

You can generate `requirements.txt` from an existing environment using:

```bash
pip freeze > requirements.txt
```

---

## 3. Running the FastAPI Application

After installing dependencies, start your FastAPI application using Uvicorn:

```bash
uvicorn main:app --reload
```

- `main` refers to the Python file `main.py` where your FastAPI app instance is created.
- `app` is the FastAPI instance inside `main.py`.
- `--reload` enables automatic reloading for development.

---

## 4. Testing the API

Once the server is running, open your browser or use a tool like `curl` or Postman to test the API.

- **Interactive API docs:** [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---

## 5. Deactivating the Virtual Environment

When done, deactivate the virtual environment:

```bash
deactivate
```

---

Now you're all set to develop and run FastAPI applications on macOS and Windows! 🚀


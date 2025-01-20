#  Restaurant System - FastAPI & React Application

This project is a full-stack application built using **FastAPI** (backend), **React** (frontend), and **SQLite** (database). Follow the steps below to set up and run the application on a new machine.

---

## Prerequisites

Ensure you have the following installed on your machine:
- Python 3.8 or later
- Node.js and npm (for managing the React frontend)
- Git (for cloning the repository)

---

## Setup Instructions

### 1. Clone the Repository
```bash
git clone <repository-url>
cd <repository-folder>
```

### 2. Backend Setup (FastAPI)
1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install the required Python packages:
   ```bash
   pip install -r requirements.txt
   ```

4. Start the FastAPI server:
   ```bash
   uvicorn main:app --reload
   ```

   The server will be available at: `http://127.0.0.1:8000`

---

### 3. Frontend Setup (React)
1. Navigate to the frontend directory:
   ```bash
   cd ../frontend
   ```

2. Install the required npm packages:
   ```bash
   npm install
   ```

3. Start the React development server:
   ```bash
   npm start
   ```

   The frontend will be available at: `http://localhost:3000`

---

## Accessing the Application
1. **Frontend**: Open your browser and navigate to `http://localhost:3000`.
2. **API Docs**: Visit the FastAPI interactive documentation at `http://127.0.0.1:8000/docs`.

---

## Troubleshooting
- Ensure the backend server (`uvicorn`) is running before starting the frontend.
- Check your database connection if there are issues with data retrieval.
- Run `npm audit fix` in the frontend directory to resolve dependency warnings.

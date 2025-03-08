# User Management System

This project consists of a CRUD application for user management, developed with Vue.js for the frontend, Flask for the backend, and MongoDB as the database.

## Project Structure

- `backend/`: Contains the Flask API
- `frontend/`: Contains the Vue.js application
- `parser.py`: Script to import data from the JSON file to MongoDB
- `udata.json`: Sample data for import

## Prerequisites

- Python 3.8+
- Node.js 14+
- MongoDB

## Setup

### 1. Configure MongoDB

- Install MongoDB
- Start the MongoDB service
- The database will be automatically created by the import script

### 2. Configure the Backend

```bash
cd backend
pip install -r requirements.txt
```

### 3. Configure the Frontend

```bash
cd frontend
npm install
```

## Execution

### 1. Import Data

Run the import script to load the initial data:

```bash
python parser.py
```

### 2. Start the Backend

```bash
cd backend
python app.py
```

The Flask server will be available at `http://localhost:5000`.

### 3. Start the Frontend

```bash
cd frontend
npm run serve
```

The Vue.js application will be available at `http://localhost:8080`.

## Features

- User listing in a table with sorting
- Detailed user view
- Creation of new users
- Editing existing users
- User deletion (with confirmation) 
#!/bin/bash

# Start backend
cd backend
source venv/bin/activate
uvicorn app.main:app --reload --port 8000 &

# Start frontend
cd ../frontend
npm start 
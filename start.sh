#!/bin/bash
# Start FastAPI on port 8000
uvicorn main:app --host 0.0.0.0 --port 8000 &

# Start Streamlit on the port Cloud Run expects ($PORT defaults to 8080)
streamlit run app.py --server.port=${PORT:-8080} --server.address=0.0.0.0

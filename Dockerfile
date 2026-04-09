FROM python:3.12-slim
ENV PYTHONUNBUFFERED True
WORKDIR /app
COPY . ./
RUN pip install fastapi uvicorn streamlit google-cloud-firestore google-cloud-aiplatform pydantic
RUN chmod +x start.sh
CMD ["./start.sh"]

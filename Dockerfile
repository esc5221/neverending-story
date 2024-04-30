FROM python:3.12-slim

WORKDIR /app

COPY server.py .
EXPOSE 8000

# Command to run the server
CMD ["python", "server.py"]
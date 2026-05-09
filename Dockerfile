FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Copy master knowledge base into the runtime input location
RUN cp -r knowledge/. inputs/knowledge/

CMD ["python", "main.py"]

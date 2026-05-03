FROM python:3.13-slim

WORKDIR /app

# Install system dependencies (if needed for psycopg2)
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8087

# Run migrations (if using Flask-Migrate) then start the app
CMD ["sh", "-c", "flask db upgrade || echo 'No migrations found, skipping...' && flask run --host=0.0.0.0 --port=8087"]
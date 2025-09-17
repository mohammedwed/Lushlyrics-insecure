FROM python:3.13.5-slim

# ─── ENVIRONMENT SETTINGS ─────────────────────────────────────────────
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# ─── SET WORKING DIRECTORY ────────────────────────────────────────────
WORKDIR /app

# ─── INSTALL SYSTEM DEPENDENCIES ──────────────────────────────────────
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    libjpeg-dev \
    zlib1g-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# ─── INSTALL PYTHON DEPENDENCIES ──────────────────────────────────────
RUN pip install --upgrade pip
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ─── COPY PROJECT FILES ───────────────────────────────────────────────
COPY . .

# ─── COLLECT STATIC FILES ─────────────────────────────────────────────
RUN python manage.py collectstatic --noinput

# ─── EXPOSE PORT FOR GUNICORN ─────────────────────────────────────────
EXPOSE 8000

# ─── START DJANGO APP WITH GUNICORN ───────────────────────────────────
CMD ["gunicorn", "youtify.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3"]

### Stage 1: Build the frontend ###
FROM node:20-alpine AS frontend-build
WORKDIR /frontend
COPY src/frontend/package.json src/frontend/package-lock.json ./
RUN npm ci
COPY src/frontend ./
RUN npm run build

### Stage 2: Build Python dependencies (needs a compiler for psycopg2 etc.) ###
FROM python:3.11-slim AS python-build
RUN apt-get update && \
    apt-get install -y --no-install-recommends build-essential libpq-dev && \
    rm -rf /var/lib/apt/lists/*
COPY requirements.txt /requirements.txt
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir --prefix=/install -r /requirements.txt

### Stage 3: Final runtime image (no Node, no compiler) ###
FROM python:3.11-slim
LABEL authors="bastianlobe"
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Install Nginx web server + runtime lib for psycopg2
RUN apt-get update && \
    apt-get install -y --no-install-recommends nginx gettext libpq5 && \
    rm -rf /var/lib/apt/lists/*

COPY --from=python-build /install /usr/local

# Create a directory for the Django project
WORKDIR /HelloMeals

### Copy project files ###
COPY nginx.conf /etc/nginx/sites-available/default
COPY scripts scripts
COPY src src

# Create a directory for static files
RUN mkdir /static

# Move the built frontend into nginx's web root
COPY --from=frontend-build /frontend/dist/ /usr/share/nginx/html/

# Expose port 6753 for the container
EXPOSE 6753

# Run the boot.sh script when the container starts
ENTRYPOINT ["scripts/boot.sh"]

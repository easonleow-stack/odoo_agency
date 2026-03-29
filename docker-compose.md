version: "3.8"

# ─────────────────────────────────────────────────────────────────
#  Ads On Marketing — Odoo 18 Full-Stack Stack
#  Services: PostgreSQL 15 · Odoo 18 · Nginx · Certbot (SSL)
# ─────────────────────────────────────────────────────────────────

services:

  # ── 1. PostgreSQL Database ──────────────────────────────────────
  db:
    image: postgres:15-alpine
    container_name: odoo_db
    restart: unless-stopped
    environment:
      POSTGRES_USER: ${DB_USER:-odoo}
      POSTGRES_PASSWORD: ${DB_PASSWORD:?DB_PASSWORD is required}
      POSTGRES_DB: postgres
    volumes:
      - postgres_data:/var/lib/postgresql/data
    networks:
      - odoo_net
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U ${DB_USER:-odoo}"]
      interval: 10s
      timeout: 5s
      retries: 5

  # ── 2. Odoo 18 Application ──────────────────────────────────────
  odoo:
    image: odoo:18.0
    container_name: odoo_app
    restart: unless-stopped
    depends_on:
      db:
        condition: service_healthy
    ports:
      - "8069:8069"   # Main web interface
      - "8072:8072"   # Long-polling (live chat / real-time updates)
    environment:
      HOST: db
      PORT: 5432
      USER: ${DB_USER:-odoo}
      PASSWORD: ${DB_PASSWORD:?DB_PASSWORD is required}
    volumes:
      - odoo_data:/var/lib/odoo                          # Odoo filestore
      - ./custom_addons:/mnt/extra-addons                # Your custom modules
      - ./odoo.conf:/etc/odoo/odoo.conf:ro               # Odoo config
    networks:
      - odoo_net
    command: odoo --config /etc/odoo/odoo.conf

  # ── 3. Nginx Reverse Proxy ──────────────────────────────────────
  nginx:
    image: nginx:1.25-alpine
    container_name: odoo_nginx
    restart: unless-stopped
    depends_on:
      - odoo
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx/nginx.conf:/etc/nginx/nginx.conf:ro
      - certbot_certs:/etc/letsencrypt:ro
      - certbot_webroot:/var/www/certbot:ro
    networks:
      - odoo_net

  # ── 4. Certbot (SSL — run once to obtain certificate) ──────────
  #  Usage:  docker compose run --rm certbot
  certbot:
    image: certbot/certbot:latest
    container_name: odoo_certbot
    volumes:
      - certbot_certs:/etc/letsencrypt
      - certbot_webroot:/var/www/certbot
    command: >
      certonly --webroot
      --webroot-path=/var/www/certbot
      --email ${ADMIN_EMAIL:?ADMIN_EMAIL is required}
      --agree-tos --no-eff-email
      -d ${DOMAIN:?DOMAIN is required}
    profiles:
      - ssl   # Only runs when: docker compose --profile ssl run certbot

# ─────────────────────────────────────────────────────────────────
#  Named Volumes
# ─────────────────────────────────────────────────────────────────
volumes:
  postgres_data:
  odoo_data:
  certbot_certs:
  certbot_webroot:

# ─────────────────────────────────────────────────────────────────
#  Network
# ─────────────────────────────────────────────────────────────────
networks:
  odoo_net:
    driver: bridge

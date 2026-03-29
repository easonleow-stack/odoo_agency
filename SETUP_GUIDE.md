# Ads On Marketing — Odoo 18 Full-Stack Setup Guide

Database Name
odoo_agency
Email
odoo
Password
odoo

## What You're Building

| Layer | Technology | Purpose |
|---|---|---|
| Database | PostgreSQL 15 | Stores all Odoo data |
| Backend | Odoo 18 (Community) | CRM, Task Tracker, Sales, Live Chat |
| Reverse Proxy | Nginx | HTTPS, routing, caching |
| SSL | Let's Encrypt / Certbot | Free HTTPS certificate |
| Container | Docker Compose | Runs everything together |
| Server | Ubuntu 22.04 VPS | Hosts it all online |

---

## STEP 1 — Get a Server (VPS)

### Recommended: DigitalOcean
**Why**: Simple control panel, reliable, good for beginners, one-click Ubuntu setup.

**Recommended Droplet for Odoo 18:**
- Plan: **Basic — Regular** → **4 GB RAM / 2 vCPU / 80 GB SSD**
- Cost: ~**USD $24/month** (~RM 110/month)
- Region: **Singapore** (closest to Malaysia, low latency)
- OS: **Ubuntu 22.04 LTS**

Sign up at: https://www.digitalocean.com
> Use the $200 free credit promo for new accounts — gives you ~8 months free.

**Cheaper alternative: Contabo VPS S**
- 4 vCPU / 4 GB RAM for ~€5.50/month (~RM 28/month)
- Sign up at: https://contabo.com
- Slightly slower support, but excellent value for budget setups.

---

## STEP 2 — Get a Domain Name

### Recommended: Namecheap
1. Go to https://www.namecheap.com
2. Search for your domain (e.g. `adsonmarketing.com.my` or `agencyboard.com.my`)
3. `.com.my` costs ~**RM 50/year** (requires Malaysian business registration)
4. `.com` costs ~**USD $12/year** (~RM 55/year, no requirements)

### Point Domain to Your Server
After buying the domain:
1. In Namecheap → **Advanced DNS** settings
2. Add an **A Record**:
   - Host: `@` (root domain)
   - Value: your server's IP address
   - TTL: Automatic
3. Add another **A Record**:
   - Host: `www`
   - Value: same server IP
4. Changes take up to 24 hours to propagate (usually faster)

---

## STEP 3 — Set Up the Server

SSH into your new server from your computer:

```bash
ssh root@YOUR_SERVER_IP
```

### Install Docker & Docker Compose

```bash
# Update system
apt update && apt upgrade -y

# Install Docker
curl -fsSL https://get.docker.com | bash

# Install Docker Compose plugin
apt install docker-compose-plugin -y

# Verify
docker --version
docker compose version
```

### Create a Non-Root User (Security Best Practice)

```bash
adduser odoo_admin
usermod -aG sudo odoo_admin
usermod -aG docker odoo_admin
su - odoo_admin
```

---

## STEP 4 — Upload Your Project to the Server

### Option A — Use Git (Recommended)

```bash
# On your server
git clone https://github.com/YOUR_USERNAME/odoo-agency.git
cd odoo-agency
```

> First push your `odoo-agency/` folder to a **private** GitHub repo.
> Do NOT include your `.env` file in the repo — it contains passwords.

### Option B — Use SCP (copy files directly)

```bash
# On your LOCAL computer (Windows: use WinSCP app)
scp -r ./odoo-agency odoo_admin@YOUR_SERVER_IP:~/odoo-agency
```

---

## STEP 5 — Configure Environment Variables

```bash
cd ~/odoo-agency

# Create your .env file from the example
cp .env.example .env
nano .env
```

Fill in your actual values:

```env
DB_USER=odoo
DB_PASSWORD=YourVeryStrongPassword123!
DOMAIN=crm.adsonmarketing.com.my
ADMIN_EMAIL=eason@adsonmarketing.com.my
```

**Also update these files:**
- `odoo.conf` → change `admin_passwd` to something secure
- `nginx/nginx.conf` → replace `YOUR_DOMAIN` with your actual domain (3 places)

---

## STEP 6 — Start Odoo (HTTP first, before SSL)

Start without Nginx (to test Odoo works):

```bash
# Start just DB + Odoo
docker compose up -d db odoo

# Check logs
docker compose logs -f odoo
```

Visit `http://YOUR_SERVER_IP:8069` — you should see the Odoo setup screen.

### Create your first database:
1. Go to `http://YOUR_SERVER_IP:8069/web/database/manager`
2. Fill in:
   - Master Password: (from `odoo.conf` → `admin_passwd`)
   - Database Name: `ads_on_agency`
   - Email: `admin@adsonmarketing.com.my`
   - Password: (create a strong admin password)
   - Language: English
   - Country: Malaysia
3. Click **Create Database** — wait 2-3 minutes

---

## STEP 7 — Activate Your Custom Module

1. Log in to Odoo with your admin credentials
2. Go to **Settings → Activate Developer Mode** (URL: add `?debug=1`)
3. Go to **Apps → Update Apps List**
4. Search for **Agency Task Tracker**
5. Click **Install**

You should now see **Agency Board** in the top navigation menu.

---

## STEP 8 — Enable SSL with HTTPS

Once your domain DNS is pointing to your server:

```bash
# Start Nginx in HTTP-only mode first
docker compose up -d nginx

# Request SSL certificate
docker compose --profile ssl run --rm certbot

# Restart Nginx with SSL
docker compose restart nginx
```

Visit `https://YOUR_DOMAIN` — it should load Odoo over HTTPS!

---

## STEP 9 — Enable Odoo Modules

In Odoo **Settings → Apps**, install:

| Module | Purpose |
|---|---|
| CRM | Sales pipeline, leads, opportunities |
| Project | Project/campaign management |
| Discuss | Internal team messaging |
| Live Chat | Website visitor chat widget |
| Invoicing | Client invoice creation |
| Email Marketing | Campaign email blasts |

---

## STEP 10 — Routine Maintenance

### Start / Stop the stack
```bash
docker compose up -d      # Start everything
docker compose down        # Stop everything
docker compose restart     # Restart
```

### View logs
```bash
docker compose logs -f odoo    # Follow Odoo logs
docker compose logs -f db      # Follow database logs
```

### Backup the database
```bash
# Create a database dump
docker compose exec db pg_dump -U odoo ads_on_agency > backup_$(date +%Y%m%d).sql

# Restore from backup
docker compose exec -T db psql -U odoo ads_on_agency < backup_20260329.sql
```

### Update Odoo (when a new version drops)
```bash
docker compose pull odoo
docker compose up -d odoo
```

### Renew SSL Certificate (every 90 days — automate this!)
```bash
docker compose --profile ssl run --rm certbot renew
docker compose restart nginx
```

Add to crontab (`crontab -e`) for automatic renewal:
```
0 3 1 * * cd ~/odoo-agency && docker compose --profile ssl run --rm certbot renew && docker compose restart nginx
```

---

## Project File Structure

```
odoo-agency/
├── docker-compose.yml          ← Runs all services
├── odoo.conf                   ← Odoo configuration
├── .env.example                ← Template for secrets (copy → .env)
├── nginx/
│   └── nginx.conf              ← HTTPS proxy config
└── custom_addons/
    └── agency_tracker/         ← Your custom Odoo module
        ├── __manifest__.py     ← Module metadata
        ├── __init__.py
        ├── models/
        │   └── agency_task.py  ← Task data model
        ├── views/
        │   ├── agency_task_views.xml  ← Kanban, List, Form views
        │   └── menu.xml               ← App menu items
        ├── security/
        │   └── ir.model.access.csv    ← User permissions
        └── static/src/
            ├── css/tracker.css        ← Custom styles
            └── js/tracker.js          ← Frontend JS patches
```

---

## Cost Summary (Monthly)

| Item | Cost |
|---|---|
| DigitalOcean VPS (4GB) | ~RM 110/month |
| Domain name (.com.my) | ~RM 4/month (~RM 50/year) |
| SSL certificate | FREE (Let's Encrypt) |
| Odoo 18 Community | FREE (open source) |
| **Total** | **~RM 114/month** |

> Odoo Enterprise (paid) adds modules like accounting, payroll, eSign.
> Community edition is fully functional for agency internal operations.

---

## Next Steps (Future Expansion)

- **Live Chat** — Enable the `im_livechat` module, embed the widget on your Odoo website
- **Client Portal** — Clients log in to view their proposals and pay invoices online
- **Stripe/PayPal Payments** — Add via Odoo's Payment Acquirer settings
- **Mobile App** — Odoo has official iOS/Android apps that connect to your server
- **Email Automation** — Set up automated follow-up emails in CRM

---

*Generated by Claude for Ads On Marketing Sdn Bhd — March 2026*

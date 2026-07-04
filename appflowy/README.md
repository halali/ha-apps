# Home Assistant Add-on: AppFlowy

Self-hosted **AppFlowy Cloud** — an open-source, privacy-first alternative to
Notion. This add-on packages the whole AppFlowy Cloud stack into a single
Home Assistant add-on so you can run your own backend for the AppFlowy desktop
and mobile apps.

## What's inside

This is an **all-in-one** add-on. It bundles and orchestrates (via supervisord)
every service AppFlowy Cloud needs:

| Service | Role |
|---------|------|
| PostgreSQL 16 + pgvector | Primary database |
| Redis | Realtime collaboration cache |
| MinIO | S3-compatible object storage |
| GoTrue | Authentication (email + admin user) |
| AppFlowy Cloud API | Core backend + WebSocket sync |
| AppFlowy Worker | Background imports & notifications |
| nginx | Gateway / reverse proxy |

> ⚠️ **Heavy add-on.** The full stack uses roughly **2–4 GB RAM**. Run it on a
> capable host (x86-64 / amd64 only).

## Installation

1. Add the repository `https://github.com/halali/ha-apps` in the HA Add-on Store.
2. Install **AppFlowy**.
3. Set **`APPFLOWY_BASE_URL`** in the configuration (see below) — this is required.
4. Start the add-on and watch the log until every service reports ready
   (first start takes a while: it initialises the database and pulls the
   storage bucket into shape).

## Configuration

```yaml
APPFLOWY_BASE_URL: http://192.168.1.10:9080   # REQUIRED — how clients reach this add-on
GOTRUE_ADMIN_EMAIL: you@example.com
GOTRUE_ADMIN_PASSWORD: choose-a-strong-password
GOTRUE_DISABLE_SIGNUP: false
GOTRUE_MAILER_AUTOCONFIRM: true               # true = no SMTP needed, accounts auto-confirmed
RUST_LOG: info
TZ: Europe/Bratislava
```

### `APPFLOWY_BASE_URL` — important

AppFlowy generates auth redirects, WebSocket URLs and presigned storage links
against this value, so it **must be the exact URL your clients use to reach the
add-on** — typically `http://<home-assistant-ip>:9080`. If you put AppFlowy
behind your own reverse proxy / domain with HTTPS, set it to that public URL
(e.g. `https://appflowy.example.com`) and forward the port there.

### Optional SMTP (for email confirmation / invites)

```yaml
GOTRUE_MAILER_AUTOCONFIRM: false
SMTP_HOST: smtp.example.com
SMTP_PORT: 587
SMTP_USER: apikey
SMTP_PASSWORD: your-password
SMTP_FROM: appflowy@example.com
```

## Connecting a client

1. Install the [AppFlowy app](https://appflowy.com/download) (desktop or mobile).
2. Go to **Settings → Cloud Settings → Self-hosted Cloud**.
3. Enter your `APPFLOWY_BASE_URL` (e.g. `http://192.168.1.10:9080`).
4. Sign up / sign in.

The HA sidebar button opens a small landing page that shows your server URL and
a link to download the app. The pre-configured admin account
(`GOTRUE_ADMIN_EMAIL` / `GOTRUE_ADMIN_PASSWORD`) can sign in from the app too.

## External Port

- `9080/tcp` — AppFlowy gateway: web console, REST API and realtime WebSocket.

## Data & secrets

- All data (PostgreSQL, MinIO objects, Redis) is stored under
  `/addon_configs/appflowy` and survives restarts and updates.
- Auth/JWT, database and object-storage secrets are generated on first start and
  saved to `/addon_configs/appflowy/secrets.env`. Keep a backup — losing them
  makes existing data unreadable.

## Notes & limitations

- **amd64 only** — the bundled AppFlowy binaries are published for x86-64.
- The browser-based UI — the **admin console** (`admin_frontend`, a Next.js app)
  and the standalone **web editor** (`appflowy_web`) — plus the optional **AI**
  and **search** services are not bundled. Document editing is done through the
  AppFlowy desktop/mobile apps; AI features stay disabled.
- HA **Ingress** shows a status/landing page rather than an app, because AppFlowy
  is served from its own base URL. Use the external port / `APPFLOWY_BASE_URL`.

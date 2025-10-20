# dev_hub: my personal website

This is a website that will serve as a personal hub for public projects and apps I want to share.
I want this to replace my old personal website.

# Environment variables

The application needs the following environment variables based on this env file example:

```
PORTFOLIO_DJANGO_SECRET=secret_example
PORTFOLIO_DEBUG=true
PORTFOLIO_ALLOWED_HOSTS=localhost,127.0.0.1
DOMAIN=localhost
PORTFOLIO_PORT=8000
PORTFOLIO_SSL_LIVE_DIR=./.certs/live/localhost
PORTFOLIO_SSL_ARCHIVE_DIR=./.certs/archive/localhost
PORTFOLIO_SSL_KEYS_DIR=./.certs/keys
```

# Generate Local Certs for Full Local Deployment

To deploy a "productionalized" version of the app locally (with a nginx webserver for serving static content and forwarding requests to the application's gunicorn server), you should first generate local self-signed certs:

```bash
chmod +x scripts/generate_local_certs.sh
./scripts/generate_local_certs.sh
```

# Build and Run The Application

First, ensure you have a .env file setup as shown previously. Feel free to change the secret.

```bash
docker compose up -d --build
```
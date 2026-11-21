# Cloudilio documentation

Guides for putting your app online with Cloudilio, exported from [https://cloudilio.com/docs](https://cloudilio.com/docs).

- [Quickstart](quickstart.md): Create an app from a template, a .zip, GitHub or the AI builder, and publish it.
- [Build, fix and deploy with AI](ai.md): Deploy with AI (drop files and the AI publishes them), building from a description, Fix with AI, Cloudilio credits and using your own ChatGPT or Claude key.
- [Build with Claude](claude.md): Connect Claude to Cloudilio (the MCP connector at /mcp) and build apps from a chat.
- [Python apps](python.md): Flask, Django, FastAPI, Streamlit and scripts: detection, start commands, Python versions.
- [Node.js apps](nodejs.md): Express, Next.js and other Node.js servers: start scripts, lock files, Node.js versions.
- [Your own Dockerfile](dockerfile.md): Any other language: what the node enforces and what a Dockerfile can't do.
- [Static sites](static-sites.md): HTML sites and Vite, React or Vue builds, _redirects and _headers, public build settings.
- [System packages](system-packages.md): Debian packages a Python app needs, in packages.txt.
- [Run a command](commands.md): One-off commands such as database migrations, and commands before each publish.
- [Background workers](background-workers.md): A second process beside the web app, for slow jobs.
- [Databases](databases.md): An app's own PostgreSQL or MySQL database, found through DATABASE_URL and backed up daily.
- [Redis](redis.md): An app's own private Redis for caches, job queues and sessions, found through REDIS_URL.
- [Saving data](storage.md): APP_DATA_DIR, SQLite, backups and the read-only filesystem.
- [Secrets and settings](secrets-and-settings.md): Environment variables, secrets and preview values.
- [Your own domain](domains.md): Connecting a domain with DNS records, and HTTPS.
- [Command line and API](cli-and-api.md): The cloudilio command-line tool, access tokens and the REST API at /api/v1, for scripts and CI.

For AI assistants, [platform-guide.md](../platform-guide.md) has every rule in one file.

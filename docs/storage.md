# Persistent Storage & Volume Architecture

*This page is also on the website: [https://cloudilio.com/docs/storage](https://cloudilio.com/docs/storage)*

## Dedicated NVMe Volume at /app/data

Standard container filesystems reset when a new revision deploys. Cloudilio provides a persistent host mount at `/app/data`. Data placed in this directory survives application updates, restarts, and crashes.

Need a database server rather than files? Add a [PostgreSQL or MySQL database](databases.md) or [Redis](redis.md) of your app's own on its Data page. Both are backed up with this folder.

## How Persistent Storage Works

The execution node binds a dedicated host folder to `/app/data` inside the application container. The container process runs under user ID 1000. Cloudilio sets filesystem permissions to allow write access without root credentials.

### Directory separation

**/app (Ephemeral Workspace)**

Contains source code, templates, and installed virtual environment packages. Cloudilio replaces this directory whenever you deploy a new commit or ZIP release.

**/app/data (Durable Mount)**

Contains databases (SQLite, DuckDB), user uploads, and persistent state files. Cloudilio retains this directory across every code revision.

## SQLite Database Configuration Examples

Point your connection string to `/app/data`. Here are configurations for popular Python libraries:

1. Python Native sqlite3:

```
import os, sqlite3
db_dir = os.environ.get("APP_DATA_DIR", "/app/data")
db_path = os.path.join(db_dir, "production.db")
conn = sqlite3.connect(db_path)
```

2. SQLAlchemy URI:

```
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:////app/data/app.db"
```

3. Django settings.py:

```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': '/app/data/db.sqlite3',
    }
}
```

## Node.js Apps and Other Languages

Every kind of app gets the same folder, and the path in the `APP_DATA_DIR` environment variable. Read it there rather than writing the path out.

```
// Node.js
const dataDir = process.env.APP_DATA_DIR || "data";
const dbPath = require("path").join(dataDir, "app.db");
// Go
dbPath := filepath.Join(os.Getenv("APP_DATA_DIR"), "app.db")
```

- The rest of the app's files are read-only while it runs. Use `/tmp` for files you don't need to keep; it's cleared on each restart.
- An app built from [your own Dockerfile](dockerfile.md) runs as user 1000 and can write to `/app/data` whatever its `USER` says. A `VOLUME` in the Dockerfile isn't allowed; save files here instead.
- A [static site](static-sites.md) runs no code, so it saves nothing on the server.
- Need a full database server? Add a [PostgreSQL or MySQL database](databases.md) of your app's own. It's included in every backup, beside the files here.
- When your app's [Redis](redis.md) is on, it saves its data in a hidden `.redis` folder here. That folder counts toward your storage and is included in backups. Leave it to Redis.

## Data Backups & Archival

Developers can export their complete persistent volume at any time. Navigate to your application overview page in the control panel and click **Backup** in the persistent storage card. Cloudilio packs the directory into a compressed `.tar.gz` archive and delivers the file directly through the browser.

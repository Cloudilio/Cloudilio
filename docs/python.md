# Framework Runtimes & Startup Configurations

*This page is also on the website: [https://cloudilio.com/docs/frameworks](https://cloudilio.com/docs/frameworks)*

## Supported Frameworks & Execution Commands

Cloudilio inspects code repositories during build phases. The analyzer identifies entry points and automatically prepares the runtime server. Developers can override default commands in the application settings panel.

A Node.js app, such as Express or Next.js, runs on Node.js: see [Node.js apps](nodejs.md). A website with no server code, made of HTML, CSS and JavaScript or built with React, Vue or Vite, is served as a [static site](static-sites.md). Any other language builds with [your own Dockerfile](dockerfile.md).

WSGI MICROSERVICE

## Flask (3.0+)

Cloudilio runs Flask applications using Gunicorn with two worker processes. The platform injects the assigned host port via the `PORT` environment variable.

**DEFAULT EXECUTION COMMAND**

```
gunicorn --bind 0.0.0.0:$PORT --workers 2 app:app
```

FILE DETECTION RULES:

- Detects `app.py`, `application.py`, or `wsgi.py`.
- Looks for an `app` or `application` instance.
- Supports application factory functions like `create_app()`.

RECOMMENDED PACKAGES:

flask>=3.0.0 
 gunicorn>=22.0.0

FULL STACK

## Django (5.0+)

When Cloudilio finds `manage.py`, the build agent runs database migrations automatically before serving web traffic.

**DEFAULT EXECUTION COMMAND**

```
python manage.py migrate --noinput && gunicorn <project>.wsgi:application --bind 0.0.0.0:$PORT
```

SQLITE DATABASE PATH:

Configure your `DATABASES` setting in `settings.py` to point to `/app/data/db.sqlite3`. Files in `/app/data` persist across restarts and code updates.

ALLOWED_HOSTS CONFIGURATION:

ALLOWED_HOSTS = ['*'] # Or your assigned subdomain

ASGI ASYNC

## FastAPI

FastAPI powers asynchronous APIs and WebSockets. Cloudilio executes FastAPI applications using Uvicorn.

**DEFAULT EXECUTION COMMAND**

```
uvicorn main:app --host 0.0.0.0 --port $PORT
```

FASTAPI SNIPPET (main.py):

```
from fastapi import FastAPI
app = FastAPI(title="Service API")
@app.get("/health")
def health():
    return {"status": "ok"}
```

STANDALONE PROCESS

## General Python (Workers & Bots)

Cloudilio runs general Python programs including job queues, Discord bots, scheduled scrapers, and custom HTTP servers. Celery and RQ queues can use your app's own [Redis](redis.md).

**DEFAULT EXECUTION COMMAND**

```
python main.py  # Or python app.py / worker.py
```

DAEMON SUPERVISION:

Cloudilio monitors the process lifecycle. If the script crashes or encounters an unhandled exception, the supervisor logs the traceback and triggers an immediate alert.

DATA INTERFACE

## Streamlit

Cloudilio supports data visualization and machine learning dashboards built with Streamlit.

**DEFAULT EXECUTION COMMAND**

```
streamlit run app.py --server.port $PORT --server.address 0.0.0.0 --server.headless true
```

## Python versions

Apps can run on Python 3.14, 3.13, 3.12, 3.11, 3.10. New apps start on 3.14, the newest. An app keeps its version until you change it, so a new release of Python never changes an app that already works.

- To change the version, open your app's page, go to **Advanced settings**, choose a version and publish again.
- You can also name the version in your project. Put `3.12` in a file called `.python-version`, or `python-3.12` in a file called `runtime.txt`. Cloudilio reads it when you create the app.
- If a package fails to install on the newest version, it may not support that version yet. Choose an older version and publish again.

## System packages

Some Python packages need programs that pip can't install. Examples are ffmpeg for video, Tesseract for reading text in images and Chromium for browser automation. List them in a file called `packages.txt` next to your `requirements.txt`, one per line. Cloudilio installs them when it builds your app.

**EXAMPLE PACKAGES.TXT**

```
# Video and audio
ffmpeg
# Reading text in images, for pytesseract
tesseract-ocr
# Browser automation, for Selenium
chromium
chromium-driver
```

The [system packages guide](system-packages.md) explains how to find package names, check the publish log and fix common errors.

## Apps that take a while to start

When you publish, Cloudilio starts the new version next to the live one and waits for it to answer. Only then does it switch visitors over. By default, it waits up to one minute. If the new version isn't ready in time, publishing stops, and the version that's live now stays live.

Apps that load a machine learning model, a large data file or a big cache when they start can need longer. Open your app's page, go to **Advanced settings** and change **Time allowed to start** to 2 or 5 minutes. If your app crashes while it starts, Cloudilio stops waiting at once and shows the app's last output in the publish log.

## Databases, Redis and saved files

- **SQLite** works out of the box: keep the file in `/app/data`, which is kept across publishes and backed up daily. See [Saving data](storage.md).
- **PostgreSQL or MySQL.** Add a database of your app's own on the Data page and read `DATABASE_URL`, with `psycopg2-binary` or `PyMySQL` in `requirements.txt`. It's backed up with your files. See [Databases](databases.md).
- **Redis** for Celery, RQ, caching or sessions: turn it on on the Data page and read `REDIS_URL`. See [Redis](redis.md).

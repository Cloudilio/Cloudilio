# Put your first Python app online

*This page is also on the website: [https://cloudilio.com/docs](https://cloudilio.com/docs)*

## Three steps, a few minutes

This guide is for people bringing their own code. Want the setup done for you? Create an app and choose **Deploy with AI**: drop your files, and the AI fixes, previews and publishes them (see [Build, fix and deploy with AI](ai.md)). Don't have any code? Choose **Describe it** or **Use a template** instead, and skip all of this.

Publishing a Node.js app, such as Express or Next.js? See [Node.js apps](nodejs.md). A website made only of HTML, CSS and JavaScript, or a React, Vue or Vite project? See [Static sites](static-sites.md).

## Step 1. Prepare Your Project Files

Place your Python code in a directory with a standard dependency manifest. Cloudilio supports `requirements.txt`, `Pipfile`, and `pyproject.toml`.

```
# Example directory layout
my-python-app/
├── app.py                  # Entry point file
├── requirements.txt        # Pinned Python dependencies
└── data/                   # Local assets (optional)
```

Here is a minimal Flask application in `app.py`:

```
# app.py
import os
from flask import Flask, jsonify
app = Flask(__name__)
@app.route("/")
def home():
    return jsonify({
        "status": "online",
        "platform": "Cloudilio",
        "port": os.environ.get("PORT", "8000")
    })
if __name__ == "__main__":
    port = int(os.environ.get("PORT", "8000"))
    app.run(host="0.0.0.0", port=port)
```

Add the necessary packages to `requirements.txt`:

```
flask==3.0.3
gunicorn==22.0.0
```

Not a Python app? Cloudilio recognises these too, from the files in your project:

| Your project has | Cloudilio runs it as | Guide |
|---|---|---|
| `package.json` with a `start` script, or Express, Next.js and similar | A Node.js app, started with `npm start` | [Node.js apps](nodejs.md) |
| `index.html`, or a Vite, React or Vue project with a `build` script | A static site, served as files | [Static sites](static-sites.md) |
| A `Dockerfile` (Go, Ruby, PHP, Java, Rust and others) | An app built from your Dockerfile | [Your own Dockerfile](dockerfile.md) |

Every kind of app should listen on port 8000 (in `PORT`) and keep its saved files in `/app/data` (in `APP_DATA_DIR`). An app that listens on its own port, such as 3000 or 8080, still works: Cloudilio finds the port and sends visitors there.

## Step 2. Create Your Application in Cloudilio

Sign in and press **New app**. If you're bringing code, choose one of these:

| Deployment Source | Description | Ideal For |
|---|---|---|
| Source ZIP Upload | Upload a .zip of your project, up to 2 GB. It starts uploading as soon as you choose or drop it, with a progress bar, so pressing Create and publish doesn't wait for it. | Instant deployments and local testing. |
| Built-In Starters | Start from a working template: Flask, Django, FastAPI, Streamlit, Express, a React app, a static website, a Go app and more. | New projects and proof of concepts. |
| GitHub Repository | Link a public or private GitHub repository branch. See [Deploy from GitHub](github.md). | Continuous delivery and team workflows. |

## Step 3. Deploy and Inspect Runtime Output

The platform triggers the build pipeline immediately upon submission. The deployment worker executes the following steps:

1. **Security Inspection:** The worker unpacks files and checks paths against directory traversal attempts.
2. **Runtime Detection:** The worker identifies the framework from dependencies and entry files.
3. **Container Assembly:** The worker builds a secure image running under user ID 1000.
4. **Process Launch:** The worker launches the process and mounts `/app/data` for persistent storage.
5. **Edge Verification:** The worker sends an HTTP probe to the health check endpoint.

**LIVE ENDPOINT ROUTING**

Cloudilio assigns a subdomain formatted as `https://<app-slug>.apps.cloudilio.com`. When running on a public node, the edge router provisions an automatic Let's Encrypt certificate.

## Add a database if your app needs one

A small app can keep its data in a SQLite file in `/app/data`. When it needs a database server, open the app's **Data** page and add a PostgreSQL or MySQL database of its own, or turn on Redis for caching and job queues. Your code reads `DATABASE_URL` or `REDIS_URL` after you publish again, and everything is backed up every day with your files.

[PostgreSQL and MySQL](databases.md) [Redis](redis.md) [Files and SQLite](storage.md)

### Next Steps

Explore framework specifics or configure persistent databases:

[Framework Runtimes](python.md) [Persistent Storage](storage.md) [Secrets Management](secrets-and-settings.md) [Node.js Apps](nodejs.md) [Static Sites](static-sites.md) [Your Own Dockerfile](dockerfile.md) [Databases](databases.md) [Redis](redis.md)

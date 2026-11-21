<!-- The guide Claude's Cloudilio connector reads, also at https://cloudilio.com/llms-full.txt -->

# Working with Cloudilio

1. list_apps to find the app, or create_app for a new one (it starts empty).
2. For an existing app, list_files and read_file before changing anything. Keep the app in its own language and
   framework (get_status says what kind of app it is) unless the person asks to change it.
3. write_files with each file's complete contents (up to 50 files a call). delete_file removes one.
4. preview, then get_status every 20 to 30 seconds until the preview is running or has failed. A first build can
   take a few minutes (installing packages, an npm build).
5. check_page on / and the pages you changed. If anything fails, get_errors, fix the cause, preview again.
6. Tell the person the preview is ready (get_status gives its link). Publish only when they say so: publish and
   rollback change what visitors see.
7. Secrets: set_secret, or ask the person to add them in the dashboard. Never put secret values in files.
8. Domains: connect_domain returns the DNS records the person adds; call it again afterwards to finish.
9. A project that's already on the person's computer, or too big to send file by file, goes up faster with the
   cloudilio command-line tool (docs at /docs/cli): cloudilio preview APP ./folder --wait, then cloudilio publish APP.
   It needs an access token from their Account page.

# Rules every app follows

- Cloudilio works out the kind of app from its files and sets it up: requirements.txt or .py files (Python),
  package.json with a start script (Node.js), index.html (a static website) or a Dockerfile (any other language).
  Don't add Dockerfiles, Procfiles or start scripts to Python, Node.js or static apps.
- A web app listens on the port in the PORT environment variable (8000), on all addresses (0.0.0.0). An app that
  listens on a fixed port of its own (above 1023) also works: Cloudilio finds it from the app's output, a
  Dockerfile's EXPOSE or app.listen(8080) in Node.js code, and sends visitors there. New code should use PORT.
- The filesystem is read-only. An app can write only to /tmp (small, held in memory, cleared on restart) and the
  folder named by APP_DATA_DIR (/app/data), which survives restarts and publishes and is backed up daily. Keep
  databases (SQLite), uploads and anything else the app saves there.
- Apps run as user 1000 with no Linux capabilities, so they can't bind a port below 1024 or become root.
- Each app has a memory limit from its owner's plan (get_status shows it); static sites get 128 MB.
  Avoid heavy packages, such as machine-learning libraries, unless they're needed.
- Settings and secrets reach the app as environment variables (os.environ in Python, process.env in Node.js).
  APP_ID, APP_SLUG and PORT are set too.
- The app is public on the internet. Never put secrets in code, and don't build features that collect passwords
  or payment details for other services.
- A preview has its own copy of the app's saved data and the same secrets, unless the person gave previews
  different values. Nothing a preview does reaches the live app.
- For data that outgrows SQLite, add the app's own PostgreSQL or MySQL database with manage_database. The app reads
  DATABASE_URL after its next publish (for SQLAlchemy with MySQL, change mysql:// to mysql+pymysql://). Run
  migrations as a release command. It's backed up daily with the app's files. The server is shared, so queries
  are stopped after 2 minutes and a MySQL database turns read-only when it reaches the plan's storage; keep
  queries indexed and connection pools small (about 5).
- For caches, job queues (Celery, RQ, BullMQ) or sessions, turn on the app's own Redis with manage_redis instead
  of an outside service. The app reads REDIS_URL after its next publish; a preview gets an empty Redis of its own.
  Its memory comes out of the app's. Static sites can't have one.

# Python apps

- Python 3.10 to 3.14; new apps get 3.14.
- Supported: Flask, Django, FastAPI and Streamlit, other WSGI or ASGI apps, and plain scripts or bots. For a new
  app, prefer Streamlit for dashboards and data tools, FastAPI for APIs and Flask for multi-page websites.
- List every package in requirements.txt (or pyproject.toml), one per line with a lower bound, such as
  flask>=3.0. Include gunicorn for Flask and Django and uvicorn for FastAPI. Packages come from PyPI.
- Entry files Cloudilio finds: app.py (Flask app object called app, or a Streamlit script), main.py (FastAPI app
  object called app), a Django project with manage.py. Streamlit settings go in .streamlit/config.toml.
- Debian packages a Python package needs (for example libpq for psycopg2) go in packages.txt, one per line.
- A bot or worker with no web page still runs: Cloudilio checks that its process keeps running instead.

# Node.js apps (Express, Next.js or any Node.js server)

- Node.js 24 or 22; new apps get 24. .nvmrc or "engines" in package.json can ask
  for one of these.
- package.json needs a "start" script that starts the server, and a "build" script if the app needs building
  (Next.js: "build": "next build", "start": "next start"). List every package the code uses in dependencies.
- The server listens on process.env.PORT on 0.0.0.0, and keeps saved files under process.env.APP_DATA_DIR.
- Cloudilio installs with the project's package manager (npm, pnpm or Yarn), from its lock file when there is one
  (package-lock.json, pnpm-lock.yaml or yarn.lock). You can't update a lock file, and an install fails when
  package.json and the lock file disagree. Avoid adding or changing packages; when you must, delete the lock file
  and tell the person: each publish then installs the newest versions package.json allows, until they add a fresh
  lock file from their computer.
- Development servers (vite, react-scripts start, next dev) aren't servers for visitors: a project whose start
  script runs one, and that has a "build" script, is built and served as a static website instead.
- Don't add requirements.txt or .py files to a Node.js app.

# Static websites

- A project is a static site when it has an index.html and no Python or Node.js server: no .py files, no
  requirements.txt, no package.json start script that runs a server. Cloudilio serves its files itself; they
  start in seconds and use almost no memory.
- Write index.html at the top with styles.css and app.js beside it. about.html answers /about and 404.html is
  shown for missing pages. _redirects and _headers files (Netlify style) are supported.
- A Vite, React, Vue or Svelte project with a "build" script in package.json is built on each publish, and the
  folder it makes (dist, build or out) is served. Prefer plain HTML, CSS and JavaScript unless the person wants a
  framework or the project already uses one.
- A static site can't keep secrets or save data on the server: everything in its files is public. Its build gets
  only the secrets named for the browser (VITE_, REACT_APP_, NEXT_PUBLIC_ and similar), which end up public too.
- Files whose names start with a dot (.env, .git) are never served.

# Apps built from their own Dockerfile (any other language: Go, Ruby, PHP, Java, Rust...)

- The project's Dockerfile at the top level builds and starts the app. Its CMD starts a server on port 8000 (the
  PORT environment variable), or on the port its EXPOSE line names.
- Whatever USER says, the app runs as user 1000 with a read-only filesystem: it can write to /tmp and
  APP_DATA_DIR (/app/data). Make sure user 1000 can read the app's files.
- Refused: VOLUME (use APP_DATA_DIR); ADD with a URL, a git address or a variable (download with RUN curl or
  wget, which run inside the build); ONBUILD, and base images that have ONBUILD steps; BuildKit-only syntax
  (RUN --mount, heredocs); images named by ID or variable, or from a registry on a private address; an escape=
  line. Images over 5 GB are refused.
- The build gets no secrets (build arguments stay in the image's history); the app gets them when it runs.
- A project with both a Dockerfile and Python or Node.js files is set up as Python or Node.js; the person can
  switch it to the Dockerfile in the app's Advanced settings.

# Common errors and what to do

- "stopped while it was starting" with a traceback or stack trace: the app crashed on start. Fix what the error
  names, such as a missing package (add it to requirements.txt or package.json) or a bad import.
- "didn't answer" or a health check timeout: the server isn't listening on 0.0.0.0, on PORT (8000) or a port
  Cloudilio could find, or it takes longer than its start time. Check the start command and the host and port the code binds.
- Read-only file system, EROFS or permission denied when writing: write under APP_DATA_DIR or /tmp instead.
- npm ERR! ... lock file out of sync, or "npm ci can only install packages when your package.json and
  package-lock.json are in sync": see the lock file rule in the node topic.
- "Cannot find module": the package is missing from dependencies, or the start script points at the wrong file.
- ModuleNotFoundError or No module named: the package is missing from requirements.txt, or the import path is wrong.
- "The build ran out of memory": the build needs less memory, such as fewer pages built at once or smaller
  dependencies. Builds have a fixed memory limit the app can't raise.
- "The server couldn't save the built image" or a Docker storage error: a problem on Cloudilio's side, not in the
  app. Preview or publish again.
- Connection refused, ENOTFOUND or "Name or service not known" for redis: Redis is off, or the app hasn't been
  published since it was turned on. manage_redis with action status says which.
- "OOM command not allowed when used memory > 'maxmemory'": Redis is full and set to refuse writes. Make it
  bigger, set keys to expire, or use allkeys-lru if it's only a cache.
- "Our servers are full": Cloudilio has no room for the app right now; tell the person and try later.
- A 404 at / on a static site: there's no index.html in the folder being served (for a built site, the build's
  output folder).
- Always read get_errors and the end of the build log in get_status before changing code; change one thing at a
  time and preview again.

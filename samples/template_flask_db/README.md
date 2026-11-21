# Guestbook: a Flask form that saves to a database

- `app.py` serves the page and saves each entry to SQLite.
- The database lives in `APP_DATA_DIR`, which Cloudilio keeps across deploys and restarts.
- Change `templates/index.html` to restyle it, or add fields to the form and the `entries` table.

Previews get their own copy of the data, so trying changes never touches real entries.

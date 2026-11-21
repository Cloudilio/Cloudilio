# Feedback board: an Express app

- `server.js` is the app: a page in `public/` and a JSON API at `/api/notes`.
- Cloudilio starts it with `npm start` and sets `PORT`; the app listens there.
- Notes are saved in `APP_DATA_DIR`, the folder Cloudilio keeps across publishes and restarts. Everything
  else in the app is read-only while it runs.

To run it on your computer: `npm install`, then `npm start`, and open http://localhost:3000.

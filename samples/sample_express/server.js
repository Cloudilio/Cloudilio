// A feedback board: visitors leave a note, everyone sees the latest ones.
// Cloudilio starts it with `npm start` and sets PORT, so the app listens there.
// Notes are saved in APP_DATA_DIR, the one folder Cloudilio keeps across publishes and restarts.
const express = require("express");
const fs = require("fs");
const path = require("path");

const app = express();
const PORT = process.env.PORT || 3000;
const DATA_DIR = process.env.APP_DATA_DIR || path.join(__dirname, "data");
const NOTES_FILE = path.join(DATA_DIR, "notes.json");
const MAX_NOTES = 200;

fs.mkdirSync(DATA_DIR, { recursive: true });

function loadNotes() {
  try {
    return JSON.parse(fs.readFileSync(NOTES_FILE, "utf8"));
  } catch {
    return [];
  }
}

function saveNotes(notes) {
  // Write to a new file, then swap it in, so a crash mid-write never leaves half a file
  const temporary = NOTES_FILE + ".tmp";
  fs.writeFileSync(temporary, JSON.stringify(notes.slice(0, MAX_NOTES), null, 2));
  fs.renameSync(temporary, NOTES_FILE);
}

app.use(express.json({ limit: "10kb" }));
app.use(express.urlencoded({ extended: false, limit: "10kb" }));
app.use(express.static(path.join(__dirname, "public")));

// The JSON API, for the page and anything else that wants the notes
app.get("/api/notes", (req, res) => {
  res.json(loadNotes());
});

app.post("/api/notes", (req, res) => {
  const name = String(req.body.name || "").trim().slice(0, 60) || "Someone";
  const text = String(req.body.text || "").trim().slice(0, 500);
  if (!text) {
    return res.status(400).json({ error: "Write a note first." });
  }
  const note = { name, text, at: new Date().toISOString() };
  saveNotes([note, ...loadNotes()]);
  res.status(201).json(note);
});

app.listen(PORT, () => {
  console.log(`Feedback board listening on port ${PORT}`);
});

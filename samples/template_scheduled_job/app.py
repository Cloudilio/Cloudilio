"""A status page for the scheduled job: when it last ran and what it found."""
import json
import os

from flask import Flask, render_template_string

DATA_DIR = os.environ.get("APP_DATA_DIR", os.path.join(os.path.dirname(os.path.abspath(__file__)), "data"))
RUNS_FILE = os.path.join(DATA_DIR, "runs.json")

app = Flask(__name__)

PAGE = """<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Scheduled job</title>
<style>
 body { font-family: system-ui, sans-serif; max-width: 44rem; margin: 2rem auto; padding: 0 1rem; color: #1f2937; }
 table { width: 100%; border-collapse: collapse; } td, th { text-align: left; padding: .4rem; border-bottom: 1px solid #e5e7eb; }
 .muted { color: #6b7280; }
</style></head><body>
<h1>Scheduled job</h1>
<p class="muted">Cloudilio runs <code>python job.py</code> every hour (change it on the Scheduled Tasks tab).
Each run is listed here, newest first.</p>
{% if runs %}
<table><tr><th>When</th><th>Took</th><th>Result</th></tr>
{% for run in runs %}<tr><td>{{ run.at }}</td><td>{{ run.seconds }} s</td><td><code>{{ run.result }}</code></td></tr>{% endfor %}
</table>
{% else %}<p>No runs yet. Use "Run now" on the Scheduled Tasks tab to try it.</p>{% endif %}
</body></html>"""


@app.route("/")
def index():
    try:
        with open(RUNS_FILE) as f:
            runs = json.load(f)
    except (OSError, ValueError):
        runs = []
    return render_template_string(PAGE, runs=runs)

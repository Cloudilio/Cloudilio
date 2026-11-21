# Scheduled job

- `job.py` is the job. Cloudilio runs `python job.py` every hour; change the schedule, or run it now,
  on the Scheduled Tasks tab.
- `app.py` is a small page listing each run.
- Results are saved in `APP_DATA_DIR`, which Cloudilio keeps across deploys.

Replace `run()` in `job.py` with your own work.

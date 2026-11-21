# Background workers

*This page is also on the website: [https://cloudilio.com/docs/background-workers](https://cloudilio.com/docs/background-workers)*

## Do slow work beside your website

A background worker is a second program that runs all the time next to your website, from the same code. Your pages hand it slow jobs, such as sending email or building reports, and answer visitors right away.

## Step 1. Add a worker to your project

Your project needs a program that keeps running and takes jobs from a queue. A job queue library gives you one. Huey is a good first choice, because it keeps its queue in a SQLite file and needs no other service. Add `huey` to your `requirements.txt` and create this file.

**TASKS.PY**

```
import os
from huey import SqliteHuey

huey = SqliteHuey(filename=os.path.join(os.environ.get("APP_DATA_DIR", "."), "jobs.db"))

@huey.task(retries=3, retry_delay=60)
def send_welcome_email(address):
    ...  # the slow work goes here
```

Call `send_welcome_email(address)` from your website's code. The call returns at once, and the worker does the work. Keep the queue file in the data folder, as shown, so your website and your worker share it.

## Step 2. Publish your app

Publish the new version. The worker runs the published version of your code, so your app must be published before a worker can start.

## Step 3. Enter the worker command

Open your app and go to the **Tasks** page. In the **Background worker** card, enter the command that starts your worker and press **Save**.

| Library | Worker command |
|---|---|
| Huey | `huey_consumer.py tasks.huey --workers 2` |
| Huey with Django | `python manage.py run_huey` |
| Django Q2 | `python manage.py qcluster` |
| Celery | `celery -A tasks worker --loglevel=INFO --concurrency=2` |
| Your own script | `python worker.py` |

Celery, RQ and BullMQ need a Redis server. Turn on your app's own [Redis](redis.md) on the Data page, and the worker and the website both find it through `REDIS_URL`. For RQ, the worker command is `rq worker --url $REDIS_URL`.

## Step 4. Check that it runs

The worker starts within a few seconds, and the card shows **Running**. Open the **Logs** page to see its output. Lines from the worker start with `[worker]`.

**LOGS**

```
[worker] Huey consumer started with 2 thread
[worker] Sent the welcome email to ada@example.com
```

## How workers run

| Topic | What happens |
|---|---|
| Code and packages | The worker runs the same published version as your website. |
| Secrets | The worker gets every secret from the Secrets page. |
| Saved data | The worker shares your website's data folder, `/app/data`. |
| Memory and CPU | The worker has its own limits: half your website's memory and processor, and at least 256 MB of memory. A heavy job can't take memory from your pages. |
| Your plan's apps | A worker doesn't count as one of your plan's apps. |
| Number of workers | Each app can have one worker. Use the library's own option, such as `--workers 4`, to run more jobs at once. |
| Internet | The worker can call other services. Nothing on the internet can reach the worker. |

## When the worker restarts

- **You publish a new version.** The worker restarts on the new version after it goes live.
- **You change a secret or the worker command.** The worker restarts with the new values.
- **You press Restart.** The website and the worker both restart.
- **The worker crashes.** Cloudilio starts it again by itself.
- **You stop the app.** The worker stops too, and starts again with the app.

Before a restart, Cloudilio asks the worker to stop and waits 10 seconds. Celery uses that time to finish the job in hand. Huey stops at once, and the job it was running does not finish. Keep each job short, write jobs that are safe to run twice, and record finished work in your own database so you can queue missed work again.

## Worker or scheduled task

Use a worker when your website creates the work, such as an email after each signup. Use a scheduled task when the clock creates the work, such as a report every morning. A scheduled task starts, does its job and ends. A worker never ends.

## Workers in Node.js and Other Languages

A worker can be any program in your project that keeps running. Enter the command that starts it, the same way.

| Your app | Worker command |
|---|---|
| Node.js, a file that loops over jobs | `node worker.js` |
| Node.js, a script in package.json | `npm run worker` |
| Ruby with Sidekiq or Good Job, in your own Dockerfile | `bundle exec good_job start` |
| Go, a second program in the image | `/worker` |

- Keep the queue in a file in `APP_DATA_DIR`, such as a SQLite database, so the website and the worker share it.
- An app built from [your own Dockerfile](dockerfile.md) runs the worker command through its `ENTRYPOINT`, if it has one, as `docker run` does.
- [Static sites](static-sites.md) run no code, so they have no workers.

## Fix common problems

The card says "Keeps stopping"

The worker ends soon after it starts. Open the Logs page and read the lines that start with `[worker]`. The usual causes are a typing mistake in the command, a package missing from `requirements.txt` and a script that finishes instead of looping.

The worker runs, but jobs never start

The website and the worker must use the same queue. Check that the queue file is in `/app/data`. A file saved anywhere else is not shared.

"database is locked" errors

Your website and your worker write to the same SQLite database. Turn on WAL mode and set a timeout of 30 seconds when you open the database. Keep each write short.

The worker restarts in the middle of long jobs

It may be reaching its memory limit. Process large files in pieces, lower the number of worker threads or move to a plan with more memory.

"The server that runs your app has no room for a worker right now"

A worker needs memory of its own on the server that runs your app. Contact support, and we'll make room.

Our post [How to Run Background Jobs in Python Without Redis](https://cloudilio.com/posts/python-background-jobs-without-redis) builds a complete queue with Huey and SQLite, step by step. When you outgrow it, the [Redis guide](redis.md) shows Celery and BullMQ.

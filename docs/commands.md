# Run a command

*This page is also on the website: [https://cloudilio.com/docs/commands](https://cloudilio.com/docs/commands)*

## Run something once in your app

Some jobs happen once, by hand. Examples are updating the database, creating an admin user and fixing a batch of records. The **Run a command** box runs one command with your app's code, packages, secrets and saved data, and shows you what it printed.

## Step 1. Publish your app

Commands run in the published version of your app. An app that has never been published has nothing to run them in. They get the same secrets as your app, including `DATABASE_URL` for your app's own [database](databases.md) and `REDIS_URL` for its [Redis](redis.md), so migrations reach the right database.

## Step 2. Type the command

Open your app and go to the **Tasks** page. Type the command under **Run a command**, the way you would in a terminal. The buttons under the box fill in common commands for your framework.

| To do this | Run this |
|---|---|
| Apply Django database changes | `python manage.py migrate` |
| Create a Django admin user | `python manage.py createsuperuser --noinput --username admin --email you@example.com` |
| Apply Flask-Migrate database changes | `flask db upgrade` |
| Run a script from your project | `python scripts/fix_prices.py` |
| List the files your app has saved | `ls -la /app/data` |
| See installed packages | `pip list` |
| Apply Prisma database changes (Node.js) | `npx prisma migrate deploy` |
| Run a Node.js script from your project | `node scripts/fix-prices.js` |
| See installed Node.js packages | `npm ls --depth=0` |
| Run a Rails task (your own Dockerfile) | `bin/rails db:migrate` |

## Step 3. Pick a time limit and press Run

Choose how long the command may run: 1 minute, 5 minutes, 15 minutes or 1 hour. Cloudilio stops the command when the time is up. Then press **Run**. The page shows a spinner and updates by itself when the command finishes.

## Step 4. Read the result

You see everything the command printed, how long it took and one of three results.

- **Finished** means the command ended normally.
- **Failed** means the command reported an error. The page shows its exit code, and the output usually says what went wrong.
- **Stopped** means it ran out of time. You still see what it printed before that.

Each app keeps its last 20 commands. Open **Earlier commands** to read any of them again, with the time and the person who ran it.

## How commands run

- **Beside your app.** Each command runs in a temporary copy of your app. Your website keeps running while it works.
- **With your app's settings.** The command gets the same code, packages, secrets and memory limit as your app.
- **On your real data.** The command reads and writes the same data folder, `/app/data`. Create a backup on the Data & backups page before a command that changes or deletes data.
- **Only the data folder keeps changes.** Files written anywhere else disappear when the command ends.
- **One at a time.** An app runs one command at a time. Wait for it to finish before you start the next.
- **Owners and developers only.** People with view-only access can't run commands.

## Commands can't ask questions

A command has no keyboard attached, so it can't wait for you to type an answer. Pass every answer as an option or a secret. For Django, add `--noinput`.

To create a Django admin user, add a secret named `DJANGO_SUPERUSER_PASSWORD` on the Secrets page. Then run this command, and delete the secret afterwards.

**CREATE AN ADMIN USER**

```
python manage.py createsuperuser --noinput --username admin --email you@example.com
```

## Run two commands in a row

The box runs one program. Shell symbols such as `&&`, `|` and `>` don't work by themselves. To use them, give the whole line to a shell.

**TWO COMMANDS**

```
sh -c "python manage.py migrate && python manage.py clearsessions"
```

## Which tool to use

| Tool | When it runs | Where to find it |
|---|---|---|
| Run a command | Once, when you press Run | Tasks page |
| Run before each publish | Every publish, before the new version goes live | Overview page, Advanced settings |
| Scheduled task | On a timetable | Tasks page |
| [Background worker](background-workers.md) | All the time | Tasks page |

## Commands for Each Kind of App

- **Python and Node.js apps** run commands with the app's packages installed, so `python`, `pip`, `node`, `npm` and `npx` work as on your computer.
- **Apps built from [your own Dockerfile](dockerfile.md)** run commands in their image, through its `ENTRYPOINT` if it has one. A minimal image, such as distroless, may have no shell, so commands like `ls` aren't there.
- **[Static sites](static-sites.md)** are only files, so they have no commands to run.

## Fix common problems

"Publish the app first"

Publish your app once. After that, the box works.

"A command is still running"

Wait for the current command to finish or reach its time limit. Then run the next one.

"That command has a quote that is never closed"

Every `"` or `'` needs a partner. Check the command for a missing quote.

The command stops with an error about input, or runs until its time limit

It is waiting for an answer nobody can type. Add the option that skips questions, such as `--noinput` or `--yes`.

"No such file or directory"

The command runs in your project's main folder. Give paths from there, such as `python scripts/fix_prices.py`. Use `ls` to see what is in the folder.

The command was force-stopped with exit code 137

It used more memory than your plan allows. Process records in smaller batches, or move to a plan with more memory.

Our post [How to Run One-Off Commands in a Deployed Python App](https://cloudilio.com/posts/run-one-off-commands-deployed-python-app) has more examples and six habits for working safely on live data.

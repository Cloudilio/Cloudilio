# Command Line Tool and API

*This page is also on the website: [https://cloudilio.com/docs/cli](https://cloudilio.com/docs/cli)*

## Deploy and manage apps from your terminal, scripts and CI

The `cloudilio` command-line tool puts a folder online with one command, and the REST API behind it lets any script or CI pipeline do the same. Changes go through a private preview first, just as they do in the dashboard, so your live app keeps working until you publish.

## Step 1. Make an access token

Open the **Access tokens** section of your [Account settings](https://cloudilio.com/account/). Give the token a name, such as *my laptop* or *GitHub Actions*, choose what it can do and when it expires, and press **Create token**. Copy it straight away, because Cloudilio shows it only once and keeps only a scrambled copy.

- **Full access** can preview, publish and roll back apps, change their secrets and start or stop them.
- **Read only** can list apps and read their status, versions, logs and secret names, and nothing else.
- A token has the same role you have on each app. If you're a viewer on someone else's app, your token can only look at it.
- No token can delete an app, change your plan or manage your team. Those stay in the dashboard.
- Tokens stop working on the date they expire (30 days, 90 days or a year), or as soon as you delete them.

## Step 2. Install the tool

The tool is a single file that needs only Python 3.8 or newer, which macOS and Linux usually have already. On macOS or Linux, run this to download it and put it on your path.

**MACOS AND LINUX**

```
curl -fsSL https://cloudilio.com/cli/cloudilio.py -o cloudilio && chmod +x cloudilio && sudo mv cloudilio /usr/local/bin/
```

On Windows, [download the file](https://cloudilio.com/cli/cloudilio.py), save it as `cloudilio.py` and run it with `python cloudilio.py` in place of `cloudilio`. The file you download already knows your dashboard's address.

## Step 3. Log in

**LOG IN**

```
cloudilio login
```

Paste your token when it asks. The tool checks it, then saves it in `~/.config/cloudilio/config.json`, a file only your user can read. `cloudilio logout` removes it.

## Step 4. Preview, then publish

Create the app in the dashboard first. After that, use the name in its address (for `my-shop.apps.cloudilio.com`, that's `my-shop`), or run `cloudilio apps` to list them all.

**TRY YOUR CHANGES IN A PRIVATE PREVIEW**

```
cloudilio preview my-shop ./my-shop --wait
```

This zips the folder, uploads it and builds a preview, showing the build as it goes. Your live app doesn't change. When it's ready the tool prints a link, which opens for anyone signed in to Cloudilio who can see the app. The upload replaces the app's files, and the files it replaces are kept in the app's file history. Cloudilio works out the kind of app again, so a project that changed language is set up for its new one.

**MAKE IT LIVE**

```
cloudilio publish my-shop --wait
```

If something goes wrong after publishing, `cloudilio rollback my-shop` puts the version before back online. `cloudilio versions my-shop` lists earlier versions, and `cloudilio rollback my-shop VERSION` goes back to a particular one.

For an app connected to GitHub, push your code as usual and use `cloudilio preview my-shop --branch my-branch` to preview a branch. Leave out `--branch` to preview the tracked branch.

## Every command

| Command | What it does |
|---|---|
| cloudilio apps | Lists your apps with their status and address. |
| cloudilio status APP | Shows whether the app is running, its latest publish and its preview. |
| cloudilio preview APP [FOLDER] [--branch B] [--wait] | Uploads the folder, if given, and builds a private preview. |
| cloudilio publish APP [--wait] | Makes the app's current files live. |
| cloudilio deploy APP [FOLDER] [--wait] | Uploads and publishes in one step, with no preview. Useful in CI after your own tests pass. |
| cloudilio rollback APP [VERSION] [--wait] | Publishes an earlier version again. |
| cloudilio versions APP | Lists recent publishes and their version IDs. |
| cloudilio logs APP [--stream runtime\|build\|all] | Shows the app's output and build logs. |
| cloudilio start \| stop \| restart APP | Starts, stops or restarts the live app. |
| cloudilio env list APP | Lists the names of the app's secrets. Values are never shown. |
| cloudilio env set APP NAME=value ... | Sets secrets. Publish afterwards to use them. |
| cloudilio env unset APP NAME ... | Removes secrets. |
| cloudilio database status APP | Whether the app has a [database](databases.md), and its size. |
| cloudilio database add APP --engine mysql | Adds a PostgreSQL (the default) or MySQL database and sets `DATABASE_URL`. |
| cloudilio database delete APP | Drops the database and everything in it. |
| cloudilio redis status APP | Whether the app's [Redis](redis.md) is on, and how full it is. |
| cloudilio redis on APP --size 64 | Turns Redis on, or changes it. Add `--when-full allkeys-lru` for a cache. |
| cloudilio redis clear APP | Deletes every key. Redis stays on. |
| cloudilio redis off APP | Turns Redis off and deletes its data. |

The tool never uploads `.env`, `.env.local` or other `.local` settings files, installed packages (`node_modules`, `venv`, `.venv`), version control (`.git`), caches or symbolic links. Set secrets with `cloudilio env set` instead. Other hidden files that builds read, such as `.npmrc`, `.babelrc` or `.env.production`, are uploaded with your project. A folder can be up to 2 GB once zipped.

## Using it in CI

In a CI pipeline, skip `cloudilio login` and set two environment variables instead. Keep the token in your CI's secret store.

**GITHUB ACTIONS STEP**

```
- name: Deploy to Cloudilio
  env:
    CLOUDILIO_URL: https://cloudilio.com
    CLOUDILIO_TOKEN: ${{ secrets.CLOUDILIO_TOKEN }}
  run: |
    curl -fsSL https://cloudilio.com/cli/cloudilio.py -o cloudilio
    python3 cloudilio deploy my-shop . --wait
```

With `--wait`, the command exits with an error when the build or start fails, so the pipeline fails too. For an app connected to GitHub you usually don't need this: Cloudilio can publish on every push by itself.

## The REST API

The tool uses a plain JSON API you can call from any language. Send the token in the `Authorization` header. `{app}` is the app's address name or its ID.

**EXAMPLE REQUEST**

```
curl -H "Authorization: Bearer $CLOUDILIO_TOKEN" https://cloudilio.com/api/v1/apps
```

| Request | What it does |
|---|---|
| GET /api/v1/apps | Apps you can see. |
| GET /api/v1/apps/{app} | Status, address and latest publish. |
| GET /api/v1/apps/{app}/preview | The preview's status, link, error and build log. |
| POST /api/v1/apps/{app}/preview | Builds a preview. Send a zip as the multipart field `archive` to replace the files first, or `branch` for a GitHub app. |
| POST /api/v1/apps/{app}/publish | Publishes the current files. |
| POST /api/v1/apps/{app}/deploy | Uploads `archive`, if sent, and publishes straight away. |
| POST /api/v1/apps/{app}/rollback | Publishes an earlier version: JSON `{"version": "ID"}`, or the one before if left out. |
| GET /api/v1/apps/{app}/deployments | Recent publishes. |
| GET /api/v1/apps/{app}/deployments/{id} | One publish, with its build log. |
| GET /api/v1/apps/{app}/logs?stream=all | Logs: `all`, `runtime` or `build`. |
| GET /api/v1/apps/{app}/env | Secret names. Values are never returned. |
| PUT /api/v1/apps/{app}/env | Sets a secret: JSON `{"key": "NAME", "value": "..."}`. |
| DELETE /api/v1/apps/{app}/env/{name} | Removes a secret. |
| GET /api/v1/apps/{app}/database | The app's database: its kind, size and the secrets it sets. |
| POST /api/v1/apps/{app}/database | Adds one: JSON `{"engine": "postgres"}` or `"mysql"`. Owner only. |
| DELETE /api/v1/apps/{app}/database | Drops it and everything in it. Owner only. |
| GET /api/v1/apps/{app}/redis | The app's Redis: on or off, its size, memory used and keys. |
| PUT /api/v1/apps/{app}/redis | Turns Redis on or changes it: JSON `{"size_mb": 64, "eviction_policy": "noeviction"}`. Owner only. |
| POST /api/v1/apps/{app}/redis/clear | Deletes every key. |
| DELETE /api/v1/apps/{app}/redis | Turns Redis off and deletes its data. Owner only. |
| POST /api/v1/apps/{app}/start, /stop, /restart | Starts, stops or restarts the live app. |

Errors come back as JSON with an `error` message. Each token can make 600 requests every 10 minutes. Preview, publish, deploy and rollback answer `202` while the build carries on, so check the status afterwards.

## Keeping tokens safe

- Use a separate token for each computer or pipeline, so you can delete one without breaking the others.
- Choose **Read only** for anything that only needs to watch, such as a status page.
- The Account page shows when each token was last used. Delete any you don't recognise.
- Tokens made before Cloudilio's rename start with `pyh_` and keep working until they expire. New ones start with `cld_`.

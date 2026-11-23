# Deploy from GitHub

*This page is also on the website: [https://cloudilio.com/docs/github](https://cloudilio.com/docs/github)*

## Host your app straight from its GitHub repository

Link a repository and a branch, and Cloudilio publishes the latest code on that branch. It works with public and private repositories, for Python, Node.js, static sites and apps with their own Dockerfile. You keep working in Git as usual, and each publish fetches a fresh copy of the branch.

## Connect a repository

1. Press **New app** and choose **From GitHub**.
2. Paste the repository link, such as `https://github.com/your-name/your-app`. Use the link to the repository itself, not to a file or a folder inside it.
3. Enter the **Branch**, or leave it empty to use the repository's main branch, whatever it's called.
4. For a private repository, paste an **Access token**. See [Private repositories](github.md#private-repositories-and-access-tokens).
5. Name your app and press **Create and publish**. Cloudilio fetches the branch, works out what kind of app it is and publishes it.

To link an app you already have, or change its repository, branch or token, open the app's **Data & backups** tab (**GitHub** for a static site). Clear the repository link and save to disconnect it.

## Private repositories and access tokens

Cloudilio needs a token to read a private repository. A fine-grained personal access token with the least access works best.

1. On GitHub, open **Settings**, then **Developer settings**, **Personal access tokens** and **Fine-grained tokens**, and press **Generate new token**.
2. Under **Repository access**, choose **Only select repositories** and pick the app's repository.
3. Under **Permissions**, set **Contents** to **Read-only**. Cloudilio needs nothing else.
4. Choose when it expires, generate it and paste it into the **Access token** field.

**STORED ENCRYPTED**

Cloudilio encrypts the token and never shows it again. The field says *Saved*. Enter a new token there to replace it.

**WHEN IT EXPIRES**

Publishing fails with *We couldn't get the code* once the token expires. Generate a new one and paste it in. Your live app keeps running in the meantime.

## Publish your latest code

Push your changes to the linked branch, then press **Publish again** on the app. Every publish fetches the branch fresh, builds it and swaps it in once it starts.

- **Restart doesn't fetch new code.** It starts the version that's already running again. Use **Publish again** after a push, and after changing a secret.
- **Push first, then publish.** A publish takes its copy of the branch the moment it starts. If you press Publish while a push is still on its way, that publish builds the code from before the push. Publish once more when the push is done.
- **A failed publish leaves the last working version running.** If your change doesn't build or start, visitors keep seeing the previous version. The **History** tab shows the failure and the **Logs** tab shows why.

## Publish on every push

A GitHub webhook can tell Cloudilio about each push, so the app publishes itself.

1. On the app's **Data & backups** tab (**GitHub** for a static site), find **Publish automatically**. Copy the link and press **Make a secret**. Copy the secret straight away, because Cloudilio shows it only once.
2. In the repository on GitHub, open **Settings**, then **Webhooks**, and press **Add webhook**.
3. Paste the link as the **Payload URL**, set **Content type** to `application/json` and paste the secret into **Secret**.
4. Choose **Just the push event** and press **Add webhook**. GitHub sends a test ping, which should show a green tick.
- Only pushes to the linked branch publish. Pushes to other branches are ignored.
- Cloudilio checks GitHub's signature on every delivery, so nobody without the secret can trigger a publish.
- A webhook can publish up to 30 times in 10 minutes. After that it waits a few minutes.
- Lost the secret? Press **Make a new secret** and paste the new one into the webhook. The old secret stops working.

A CI job such as GitHub Actions can call the same link with the header `Authorization: Bearer <secret>` instead, for example to publish only after your tests pass. The [command line and API](cli-and-api.md) guide has a ready-made step.

## Preview another branch

Open **Preview** on the app and pick any branch of the repository. Cloudilio builds it at its own private address beside the live app, so you can try a change before you merge it. The live app isn't touched. From the command line, run `cloudilio preview my-app --branch my-branch`.

## What gets published from the repository

- **The files on the branch, at its latest commit.** Git history and the `.git` folder are left out.
- **No `.env` file.** Local settings files are never published, and they shouldn't be in a repository anyway. Put the values on the app's **Secrets** tab, where you can paste a whole `.env` file at once. See [Secrets and settings](secrets-and-settings.md).
- **No symbolic links.** Cloudilio removes them, so commit real files instead.
- **Size limits.** A repository can hold up to 4 GB and 10,000 files, and fetching it must finish within 90 seconds.

## Editing a GitHub app's files

For an app linked to GitHub, the repository is the source of truth. Each publish replaces the app's files with the branch, so a change made in the dashboard's **Files** tab is gone after the next publish. Make changes in the repository and push them. For the same reason, [Fix with AI](ai.md) and [Claude](claude.md) can't edit a GitHub app's files.

## Fixing common GitHub deploy problems

### "The repository has no main branch"

Older repositories often call their main branch `master`. The message names the right branch. Enter it as the branch, or leave the branch empty.

### "We couldn't get the code from the branch"

Check the repository link and the branch name for typos. If the repository is private, the token may be missing, expired, or limited to other repositories. Make a new one as in [Private repositories](github.md#private-repositories-and-access-tokens).

### It works on my computer but shows 400 Bad Request or "Host is not trusted"

Some apps answer only on `localhost`. On Cloudilio, visitors arrive at your app's own address, such as `my-app.apps.cloudilio.com`, or your own domain. Add those addresses to the app's list of allowed hosts, ideally read from a secret, so your computer keeps working too:

- **Flask 3.1 and later**: `TRUSTED_HOSTS`.
- **Django**: `ALLOWED_HOSTS`.
- **Express and other Node.js servers**: any host check or `allowedHosts` setting in your code.

```
# Flask: the hosted addresses come from a secret, and this computer is the default
hosts = os.environ.get("TRUSTED_HOSTS", "localhost,127.0.0.1")
app.config["TRUSTED_HOSTS"] = [h.strip() for h in hosts.split(",") if h.strip()]
```

Enter just the address in the secret, with no `https://` and no trailing `/`. When you connect another domain later, add it there and publish again.

### Forms expire, or people get logged out at random

This happens when the app makes a new secret key each time it starts, for example with `secrets.token_hex()` when no key is set. Every publish then logs everyone out. Cloudilio's usual start command for a Python app runs two workers, and each makes its own key, so a form signed by one worker fails in the other. Set the key as a secret, such as `SECRET_KEY`, with a long random value. You can make one with `python3 -c "import secrets; print(secrets.token_hex(32))"`.

### The app doesn't start, or the address never answers

Your app must listen on `0.0.0.0` at the port in `PORT`, not on `127.0.0.1`. The [Python](python.md) and [Node.js](nodejs.md) guides show the start command for each framework.

### I pushed a fix, but the app still shows the old error

The app is still running the old code. Check that you pushed to the linked branch, then press **Publish again**. Restart doesn't fetch new code. If you pressed Publish before the push reached GitHub, publish once more. In the **Logs** tab, a line number from your old code is a sign the new version isn't running yet.

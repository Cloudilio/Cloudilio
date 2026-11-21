# Node.js apps

*This page is also on the website: [https://cloudilio.com/docs/nodejs](https://cloudilio.com/docs/nodejs)*

## Publish an Express, Next.js or other Node.js app

Upload a Node.js project and Cloudilio installs its packages, runs its build and starts it with `npm start`. It works with Express, Next.js, Fastify, Koa, NestJS, Nuxt, Remix and plain Node.js servers.

## What your project needs

- **A `package.json`** that lists every package the app uses in `dependencies`. Add your lock file (`package-lock.json`, `pnpm-lock.yaml` or `yarn.lock`) so every publish installs the same versions. You can leave out `node_modules`.
- **A `start` script**, such as `"start": "node server.js"`. Without one, Cloudilio starts the file in `main`, or `server.js`, `app.js` or `index.js`.
- **Listen on `process.env.PORT`.** Cloudilio sets it to 8000. `app.listen(process.env.PORT || 3000)` works here and on your computer. An app that always listens on its own port, such as 3000 or 8080, still works: when it doesn't answer on 8000, Cloudilio finds the port it uses from its output and code, and sends visitors there.

**SERVER.JS**

```
const express = require("express");
const app = express();
app.get("/", (req, res) => res.send("Hello from Cloudilio"));
app.listen(process.env.PORT || 3000);
```

To see one working first, choose the **Express app** template on the New app page.

## What happens when you publish

1. Packages are installed with npm, pnpm or yarn, whichever matches your lock file. They're installed again only when `package.json` or the lock file changes, so publishing a code change is quicker. Yarn 2 and later install a `node_modules` folder here instead of using Plug'n'Play, so every start command finds its packages.
2. If `package.json` has a `build` script, it runs. TypeScript, Next.js and similar builds happen here.
3. The app starts with its start command and must answer within the time allowed to start. Only then does it replace the version that's live.

Apps run on Node.js 24. To use 22 instead, choose it under **Advanced settings**, or name it before you create the app in `.nvmrc` or in `engines` in `package.json`, such as `"node": "22.x"`.

Packages with native code, such as `bcrypt`, `better-sqlite3` and `sharp`, are compiled during the build. Packages that need a system library list it in `packages.txt`, as described in [System packages](system-packages.md).

## Next.js

- A Next.js app runs as a server with `next start`, so server components, API routes, middleware and pages that regenerate (ISR) all work.
- With `output: 'standalone'` in `next.config`, only the small server Next.js builds goes online, started with `node server.js`. The app is the same, but about half the size, so it publishes and starts faster. We recommend it.
- With `output: 'export'` in `next.config`, it's published as a [static site](static-sites.md) instead, which starts in seconds and uses almost no memory.
- Settings named `NEXT_PUBLIC_` are written into the pages while they're built, so set them on the **Secrets** page before you publish.
- Builds get 2 GB of memory. Most apps build well within it. If a large app runs out, the publish log says so; leave out what the build doesn't need, or contact us.

## Secrets, saved files and the rest

- **Secrets.** Your app reads them with `process.env`, for example `process.env.DATABASE_URL`. The build gets them too, as it would on your computer.
- **Saved files.** Keep anything your app saves in the folder named by `process.env.APP_DATA_DIR`. It's kept across publishes and restarts and backed up every day. The app's own files are read-only while it runs, and `/tmp` is cleared on each restart.
- **Database changes.** Put a command such as `npx prisma migrate deploy` in **Run before each publish** under Advanced settings.
- **Memory.** Cloudilio sets `NODE_OPTIONS` so Node.js keeps its memory within your plan's limit and cleans up before reaching it. Options you set yourself in `NODE_OPTIONS` are kept, and a `--max-old-space-size` of your own takes the place of Cloudilio's.
- **Background workers and commands.** Run a queue worker beside the app, such as `node worker.js`, from the **Tasks** tab, where you can also run one-off commands.
- **A database.** Add a [PostgreSQL or MySQL database](databases.md) on the Data page. Prisma, `pg` and `mysql2` all read `process.env.DATABASE_URL`.
- **Redis.** For BullMQ queues, caches or sessions, turn on your app's own [Redis](redis.md) on the Data page and connect with `process.env.REDIS_URL`.

## Fix common problems

The app starts but never answers

Cloudilio already tries the port the app says it listens on, so check that it listens on all addresses (`0.0.0.0`), not `localhost`, and on a port above 1023. Using `process.env.PORT` avoids both problems, and makes publishing a few seconds faster.

"This app has no start command"

Add a `start` script to `package.json`, or set the start command under Advanced settings.

"The build ran out of memory"

The build used more than its 2 GB. This mostly happens with large Next.js apps. Remove packages the app no longer uses, then publish again, or contact us.

"EROFS: read-only file system"

The app tried to write next to its code. Write to the folder in `APP_DATA_DIR` instead, or to `/tmp` for files you don't need to keep.

A package is missing when the app starts

It's probably installed on your computer but not listed in `package.json`. Run `npm install the-package` and upload the project again with the new `package.json` and lock file.

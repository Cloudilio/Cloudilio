# Static sites

*This page is also on the website: [https://cloudilio.com/docs/static-sites](https://cloudilio.com/docs/static-sites)*

## Publish a website made of HTML, CSS and JavaScript

A static site is only files: pages, styles, scripts and images. Cloudilio serves them as they are, with no server code. A static site starts in seconds and is given 128 MB of memory, of which serving files uses about 15 MB. Sites made with React, Vue or Vite work too: Cloudilio builds them each time you publish.

## Upload a site

Make a .zip of your site and upload it on the **New app** page. Cloudilio looks for `index.html`, your home page, in the top folder of the .zip. If it isn't there, it looks in a folder called `dist`, `build`, `out`, `public`, `site`, `_site` or `www`, and serves the first one that has it.

To see one working first, choose a template on the New app page: **Static website** is a small café site made of HTML, CSS and JavaScript, and **React app** is a task board built with React and Vite.

A project with any Python file or a `requirements.txt` is set up as a Python app instead. To publish a site, leave those out.

## Sites made with React, Vue or Vite

Upload the project itself, with its `package.json`. You can leave out the `node_modules` folder: Cloudilio installs the packages again. When `package.json` has a `build` script, each publish:

1. Installs the packages your lock file lists, with npm, pnpm or yarn, whichever matches the lock file.
2. Runs the build script.
3. Serves the folder the build made: `dist` (Vite and Vue), `build` (Create React App), `out` (Next.js with `output: 'export'`) or `dist/<project>/browser` (Angular).

Packages are installed again only when `package.json` or the lock file changes. Publishing after a change to your code alone skips that step, so it's much faster.

Builds use Node.js 24. To use 22 instead, choose it under **Advanced settings** on your app's page, or put the version in a file called `.nvmrc` before you create the app.

You can also upload the built folder alone, such as `dist`. Then nothing is built, and the files are served as they are.

If your site is somewhere else, set **Folder to publish** under Advanced settings, for example `dist/my-app/browser` or `site/public`. Leave it empty and Cloudilio finds the folder for you.

## Pages and addresses

- `/about` opens `about.html`, or `about/index.html` if that's how your files are laid out.
- Add a `404.html` and it's shown for any address that doesn't exist.
- Without a `404.html`, Cloudilio treats the site as a single-page app: an address that isn't a file opens `index.html`, so links handled by React Router or Vue Router work when someone opens them directly. Addresses that end in a file type, such as `/logo.png`, still say not found.
- Files whose names start with a dot, such as `.env` or `.git`, are never served.
- Visitors' browsers check pages for changes on every visit, so a new version shows up straight away. In a built site, files whose names include a hash of their contents, such as Vite's `/assets/index-CdpyoHQK.js`, are kept for a year, since a change gives them a new name.
- Every response tells browsers not to guess file types (`X-Content-Type-Options: nosniff`) and to send only your site's address to other sites (`Referrer-Policy: strict-origin-when-cross-origin`).

## Redirects and headers

Add a `_redirects` or `_headers` file next to your `index.html`, written the way Netlify and Cloudflare Pages read them. In a project built with npm, put them in the `public` folder. Neither file is ever served.

**_REDIRECTS**

```
# Moved pages: 301 unless you give another status
/old-page      /new-page
/blog/*        /posts/:splat    302
/news/:year/:slug   /articles/:slug
# Show a page at another address, keeping the address
/help/*        /index.html      200
# ! applies the rule even when a file exists at the address
/pricing       /plans           301!
```

**_HEADERS**

```
/*
  X-Frame-Options: DENY
/downloads/*
  Content-Disposition: attachment
```

- Statuses 200, 301, 302, 303, 307, 308 and 404 work. Redirects to another site work; showing another site's page with 200 doesn't.
- Rules with conditions, such as countries or languages, are skipped. So are values with quotes, braces, backslashes or backticks. The **While publishing** log lists each skipped line.
- Your headers come after Cloudilio's, so the same header in `_headers` replaces Cloudilio's value.

## What a static site can't do

- **Keep secrets.** Everything in a site's files reaches every visitor's browser, including the [settings a build puts in](https://cloudilio.com#build-settings). Never put a private API key in a static site.
- **Save data on the server.** A form can send its entries to another service, or the browser can keep them for one visitor. To store entries yourself, build a Python or Node.js app instead.
- **Run background workers.** There's no server process to run beside the site.
- **Use a database or Redis.** Nothing in a static site runs to connect to one. Build a Python or Node.js app when you need a [database](databases.md) or [Redis](redis.md).

## Settings for the build

A site built with npm often needs a setting while it's built, such as the address of its API. Add it on your app's **Secrets** page with the name your build tool expects, then publish. Each publish gives the build every setting whose name starts with one of these:

| Starts with | Used by |
|---|---|
| `VITE_` | Vite, including React and Vue projects made with it |
| `REACT_APP_` | Create React App |
| `NEXT_PUBLIC_` | Next.js |
| `VUE_APP_` | Vue CLI |
| `PUBLIC_` | Astro and SvelteKit |
| `NUXT_PUBLIC_`, `GATSBY_`, `EXPO_PUBLIC_` | Nuxt, Gatsby and Expo |

- Your code reads them as usual, for example `import.meta.env.VITE_API_URL` in a Vite project.
- A setting on the Secrets page wins over the same name in a `.env` file in your project.
- The build writes these values into your site's files, so every visitor can read them. The Secrets page marks each one **Public, in the build**. Use them for addresses and public keys, such as a Supabase anon key, never for private keys.
- Secrets with any other name never reach a static site or its build, or the server that serves it.

## Fix common problems

"No index.html was found"

Your home page must be called `index.html`, in the top folder or one of the folders listed under Upload a site.

"package.json has no build script"

The app is set to be built with npm. Add a `build` script, or under **Advanced settings** change the type of app to website files.

"None of the folders dist, build or out has an index.html"

The build worked but wrote the site somewhere else. Set **Folder to publish** under Advanced settings to the folder it made.

"Next.js builds a static site only when next.config sets output: 'export'"

Add `output: 'export'` to your `next.config` file. To keep features that need a server, such as API routes, publish it as a [Node.js app](nodejs.md#nextjs) instead: upload it without `output: 'export'`.

"This app's server needs an update before it can build static sites"

The server your app runs on hasn't been updated for static sites yet. Try again a little later, and contact us if it keeps happening.

The build fails while installing packages

Your lock file may not match `package.json`. Run `npm install` on your computer and upload the project again with the new `package-lock.json`. The **While publishing** view on your app's **Logs** tab shows the exact error.

The page is blank after publishing

Open your browser's developer console. A file that won't load usually means the build expected the site at another address: in a Vite config, set `base` to `/`.

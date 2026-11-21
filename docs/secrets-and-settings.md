# Environment Variables & Cryptographic Secrets

*This page is also on the website: [https://cloudilio.com/docs/environment](https://cloudilio.com/docs/environment)*

## Secure Ingestion & 256-Bit Fernet Encryption

Cloudilio encrypts credentials, database URIs, and third-party tokens at rest using symmetric 256-bit Fernet keys. The platform decrypts values only in memory when spawning container processes.

## Adding Variables in the Control Panel

Open the **Environment** tab on any application. Enter the variable key in uppercase format along with the plaintext secret. Cloudilio stores the ciphertext in the database.

**AUTOMATIC RUNTIME INJECTION**

The container agent reads your encrypted keys, decodes the secrets, and passes them to your app as ordinary environment variables, whatever language it's written in.

**REVISION SAFETY**

Altering environment variables triggers a prompt to deploy a new revision. Existing containers keep their original values until you deploy the update.

## Bulk Importing .env Files

Developers can import existing environment files with a single operation. Click **Bulk Import .env** in the environment view and paste standard configuration text:

```
# Paste this format into the bulk importer
DEBUG=False
SECRET_KEY=9f83ac01bc8e4112
DATABASE_URL=sqlite:////app/data/app.db
STRIPE_API_KEY=sk_live_51M0...
```

The parser automatically skips comments starting with `#`, trims whitespace, and strips wrapping quotation marks.

## Reading Variables in Python Code

Use standard library methods to access injected variables:

```
import os
api_key = os.environ.get("STRIPE_API_KEY")
debug_mode = os.environ.get("DEBUG", "False").lower() == "true"
```

## Reading Variables in Other Languages

```
// Node.js
const apiKey = process.env.STRIPE_API_KEY;
// Go
apiKey := os.Getenv("STRIPE_API_KEY")
# Ruby
api_key = ENV["STRIPE_API_KEY"]
// PHP
$apiKey = getenv("STRIPE_API_KEY");
```

- **Node.js apps** also get every setting while they're built, as they would on your computer, because Next.js and similar tools read some while building. See [Node.js apps](nodejs.md).
- **Apps built from your own Dockerfile** get their settings only when they run, never while they're built: build arguments end up in the image's history. See [Your own Dockerfile](dockerfile.md).

## Settings Cloudilio sets for you

- `PORT` (8000), `APP_ID`, `APP_SLUG` and `APP_DATA_DIR` (`/app/data`) are set for every app.
- When you add a [database](databases.md), Cloudilio saves `DATABASE_URL` on the Secrets tab for you, and for MySQL also `MYSQL_HOST`, `MYSQL_PORT`, `MYSQL_USER`, `MYSQL_PASSWORD` and `MYSQL_DATABASE`. You can give previews a different `DATABASE_URL`.
- When your app's [Redis](redis.md) is on, it also gets `REDIS_URL`, `REDIS_HOST`, `REDIS_PORT` and `REDIS_PASSWORD`. They replace any secrets of yours with the same names, and a preview gets values for its own Redis.
- A preview gets `PYHOST_PREVIEW=1`, so your code can tell it isn't the live app.

## Settings for static sites

A static site has no server to read secrets. A site built with npm, such as a Vite or React project, gets the settings whose names start with `VITE_`, `REACT_APP_`, `NEXT_PUBLIC_` and similar while it's built, and those become public. See [Settings for the build](static-sites.md#build-settings).

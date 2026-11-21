# Databases

*This page is also on the website: [https://cloudilio.com/docs/databases](https://cloudilio.com/docs/databases)*

## Give your app a PostgreSQL or MySQL database

Many apps start with SQLite, a database in a single file, and that works well on Cloudilio. When you need a full database server, add a PostgreSQL or MySQL database of your app's own. No other app can reach it, your app finds it through the `DATABASE_URL` secret, and it's backed up every day with your saved files.

## Step 1. Add the database

Open your app and go to the **Data** page. In the **Database** card, choose PostgreSQL or MySQL and press **Add**. Choose PostgreSQL unless your code was written for MySQL or MariaDB.

| Secret | What it holds |
|---|---|
| `DATABASE_URL` | Everything needed to connect, such as `postgresql://user:password@host:5432/name` or `mysql://user:password@host:3306/name`. |
| `MYSQL_HOST`, `MYSQL_PORT`, `MYSQL_USER`, `MYSQL_PASSWORD`, `MYSQL_DATABASE` | For MySQL only, for libraries that want the parts apart. |
| `MYSQL_SSL_MODE`, `MYSQL_SSL_CA` | For MySQL, when the database server only accepts encrypted connections: the mode (such as `REQUIRED`) and the server's certificate. See [Encrypted connections](https://cloudilio.com#encrypted). |

## Step 2. Publish your app

The secrets are saved straight away, and your app reads them the next time it's published. Create your tables as part of each publish: put your migration command, such as `flask db upgrade`, `python manage.py migrate` or `npx prisma migrate deploy`, in **Run before each publish** under Advanced settings.

## Step 3. Connect from your code

### Flask with SQLAlchemy

Add `Flask-SQLAlchemy` and a driver to `requirements.txt`: `psycopg2-binary` for PostgreSQL or `PyMySQL` for MySQL. SQLAlchemy names the MySQL driver in the address, so change the start of it.

```
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

url = os.environ.get("DATABASE_URL", "sqlite:///local.db")
if url.startswith("mysql://"):
    url = url.replace("mysql://", "mysql+pymysql://", 1)

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = url
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {"pool_pre_ping": True}
db = SQLAlchemy(app)
```

### Django

Add `dj-database-url` and a driver (`psycopg2-binary` or `mysqlclient`) to `requirements.txt`.

```
import dj_database_url

DATABASES = {"default": dj_database_url.config(conn_max_age=60)}
```

### Node.js

Prisma reads `DATABASE_URL` as it is: set `provider` to `"postgresql"` or `"mysql"` in `schema.prisma`. Without an ORM, use `pg` or `mysql2`.

```
// PostgreSQL
const { Pool } = require("pg");
const pool = new Pool({ connectionString: process.env.DATABASE_URL });

// MySQL
const mysql = require("mysql2/promise");
const db = mysql.createPool(process.env.DATABASE_URL);
```

## Encrypted connections

Some database servers only accept encrypted connections. When yours does, Cloudilio sets things up so your app's connection is encrypted too, and a new MySQL database's login is refused if it tries to connect without encryption. That keeps its password and data private on the network.

- **PostgreSQL:** `DATABASE_URL` ends in `?sslmode=require`, which every PostgreSQL driver understands. Nothing to change.
- **MySQL with Django or Prisma:** they encrypt by themselves when the server asks. Nothing to change.
- **MySQL with PyMySQL or mysql2:** these only encrypt when told to. Check for `MYSQL_SSL_MODE`, as below.

```
# Flask-SQLAlchemy with PyMySQL
import os, ssl

options = {"pool_pre_ping": True}
mode, ca = os.environ.get("MYSQL_SSL_MODE"), os.environ.get("MYSQL_SSL_CA")
if mode:
    context = ssl.create_default_context(cadata=ca) if ca else ssl.create_default_context()
    # With the server's certificate, check it; also check its name only in VERIFY_IDENTITY mode
    context.check_hostname = bool(ca) and mode == "VERIFY_IDENTITY"
    if not ca:
        context.verify_mode = ssl.CERT_NONE
    options["connect_args"] = {"ssl": context}
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = options
```

```
// Node.js with mysql2
const mysql = require("mysql2/promise");
const { MYSQL_SSL_MODE: mode, MYSQL_SSL_CA: ca } = process.env;
const ssl = !mode ? undefined
  : !ca ? { rejectUnauthorized: false }
  : mode === "VERIFY_IDENTITY" ? { ca }
  : { ca, checkServerIdentity: () => undefined };
const db = mysql.createPool({ uri: process.env.DATABASE_URL, ssl });
```

Backups always use the same encryption as the server asks for.

## Backups and restores

- **Every backup includes the database.** The daily backup, and any you make yourself, holds a copy of the database beside your app's saved files, both from the same moment. The backups list marks them *Files and database*.
- **A restore puts both back.** Your database and saved files return to the moment the backup was made. Tables created since then are removed. If the database can't be restored, nothing changes.
- **Downloads include it.** A downloaded backup has the database as a compressed SQL file in its `database` folder, which you can load into any PostgreSQL or MySQL server.
- **Backups made before you added the database** hold only files. Restoring one of those leaves the database as it is.

## How it runs

| Topic | What happens |
|---|---|
| Who can reach it | Only your app's own login, which can use only its own database. It isn't on the internet. |
| Storage | The database's size counts toward your plan's storage, beside your saved files and backups. Usage shows it. |
| When it's full | A MySQL database that grows to your plan's storage turns read-only, and you get an email. Your app can still read, delete rows and drop tables, so it keeps working while you make room. Emptying or dropping tables frees space straight away; deleted rows free it only once the table is rebuilt. It takes new data again within a few minutes of going under 95% of the limit, or straight away on a plan with more storage. A full database can't load a backup until it has room. |
| Long queries | The database server is shared, so a query still running after 2 minutes is stopped and your app gets an error for it. The connection stays open. The Data page counts stopped queries. An index on the columns you search by usually makes a slow query quick. |
| Encryption | New MySQL databases accept only encrypted connections when the server supports them, which DigitalOcean's do. See [Encrypted connections](https://cloudilio.com#encrypted) for the settings your code may need. |
| Previews | Previews use the same database as the live app. To keep a preview away from live data, give `DATABASE_URL` a different preview value on the Secrets tab. |
| Connections | Each database allows 20 connections at once. Keep your connection pool small, such as 5, so a publish, which briefly runs the old and new app together, stays well under it. |
| One per app | Each app can have one database: PostgreSQL or MySQL. |
| Static sites | Static sites can't have a database, because nothing in them runs to connect to it. |

## Delete it

**Delete database** on the Data page drops the database and everything in it, and removes its secrets. Backups made before then still hold copies. From a terminal, `cloudilio database status`, `cloudilio database add --engine mysql` and `cloudilio database delete` do the same; see the [command line guide](cli-and-api.md).

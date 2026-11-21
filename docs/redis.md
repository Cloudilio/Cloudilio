# Redis

*This page is also on the website: [https://cloudilio.com/docs/redis](https://cloudilio.com/docs/redis)*

## Give your app its own Redis

Redis is a fast store that keeps data in memory. Apps use it to cache slow pages, to queue jobs for a background worker and to keep people signed in. On Cloudilio each app gets its own Redis server. No other app can reach it, and your app finds it through the `REDIS_URL` secret.

## Step 1. Turn on Redis

Open your app and go to the **Data** page. In the **Redis** card, pick a size and what should happen when Redis is full, then press **Turn on Redis**.

- **Size.** Redis takes its memory from your app's own, so your plan's price doesn't change. On a plan with 256 MB per app, a 64 MB Redis leaves your app 192 MB. Redis can use up to half your app's memory.
- **Refuse new writes** when full. Best for job queues and sessions: nothing is ever dropped, and writes fail until there's room. This is the default.
- **Drop the least-used keys** when full. Best for a cache: the keys used least recently make room for new ones.

## Step 2. Publish your app

Redis starts within a few seconds. Your app gets `REDIS_URL` the next time it's published, so press **Publish now** in the Redis card. A background worker picks it up on its own.

| Secret | What it holds |
|---|---|
| `REDIS_URL` | Everything needed to connect, such as `redis://:password@redis:6379/0`. Most libraries take this. |
| `REDIS_HOST`, `REDIS_PORT` | `redis` and `6379`, for libraries that want them apart. |
| `REDIS_PASSWORD` | The password, made for you. Redis always asks for it. |

While Redis is on, Cloudilio sets these for you. A `REDIS_URL` of your own on the Secrets page is replaced.

## Step 3. Use it from your code

Read the address from `REDIS_URL`. Never write the password into your code.

### Python with redis-py

Add `redis` to your `requirements.txt`.

```
import os
import redis

r = redis.Redis.from_url(os.environ["REDIS_URL"])
r.set("greeting", "hello", ex=3600)  # kept for an hour
print(r.get("greeting"))
```

### A job queue with Celery or RQ

Point the queue at Redis, then run its worker as your app's [background worker](background-workers.md).

```
import os
from celery import Celery

app = Celery("tasks", broker=os.environ["REDIS_URL"], backend=os.environ["REDIS_URL"])

# Worker command: celery -A tasks worker --concurrency 2
```

With RQ, the worker command is `rq worker --url $REDIS_URL`.

### Node.js with ioredis

Run `npm install ioredis`. The redis package works too: `createClient({ url: process.env.REDIS_URL })`.

```
const Redis = require("ioredis");

const redis = new Redis(process.env.REDIS_URL);
await redis.set("greeting", "hello", "EX", 3600);
console.log(await redis.get("greeting"));
```

### A job queue with BullMQ

```
const { Queue, Worker } = require("bullmq");
const IORedis = require("ioredis");

const connection = new IORedis(process.env.REDIS_URL, { maxRetriesPerRequest: null });
const emails = new Queue("emails", { connection });

// In your background worker:
new Worker("emails", async (job) => { /* send it */ }, { connection });
```

BullMQ needs **Refuse new writes**, so its jobs are never dropped.

## How Redis runs

| Topic | What happens |
|---|---|
| Who can reach it | Only your app, its background worker and its scheduled tasks. It sits on a private network of its own, and it isn't on the internet. |
| Saved data | Redis writes its data to disk every second, in a hidden `.redis` folder inside your app's data folder. It's kept when you publish or restart, counts toward your storage and is included in your backups. |
| Memory | Redis keeps about 70% of its size for your data. The rest covers Redis itself while it saves. |
| Previews | A preview gets an empty Redis of its own, with its own password. It can never change the live data. |
| Stopping your app | Redis stops with your app and starts again with it, with its data. |
| Static sites | Static sites can't use Redis, because nothing in them runs to connect to it. |
| Version | Redis 7.4. |

## Clear it, resize it or turn it off

- **Clear all data** deletes every key within a few seconds. Redis stays on, and your app keeps running.
- **Change size or what happens when it's full** restarts Redis with the new settings in a few seconds, keeping its data.
- **Turn off Redis** removes the server and deletes its data. Publish your app afterwards so it stops looking for `REDIS_URL`.
- From a terminal, `cloudilio redis status`, `cloudilio redis on`, `cloudilio redis clear` and `cloudilio redis off` do the same. See the [command line guide](cli-and-api.md).

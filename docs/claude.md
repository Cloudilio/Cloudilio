# Build with Claude

*This page is also on the website: [https://cloudilio.com/docs/claude](https://cloudilio.com/docs/claude)*

## Build and publish your app from a chat with Claude

Connect Cloudilio to Claude once. After that, you can ask Claude for an app in a normal chat. Claude writes the app, shows you a private preview and puts it online when you say yes.

## Step 1. Copy your connector address

Your connector address is the link Claude uses to reach your Cloudilio account. You can also copy it from the **Claude** section of your [Account settings](https://cloudilio.com/account/#claude).

**CONNECTOR ADDRESS**

```
https://cloudilio.com/mcp
```

## Step 2. Add Cloudilio to Claude

In Claude on the web or the desktop app, open **Settings**, then **Connectors**, and choose **Add custom connector**. Name it Cloudilio, paste the address and save. The connector then works in the Claude phone apps too.

In Claude Code, run this command in your terminal instead.

**CLAUDE CODE**

```
claude mcp add --transport http cloudilio https://cloudilio.com/mcp
```

Free Claude accounts can add one custom connector. On a Team or Enterprise plan, an owner of the organization may need to add it first.

## Step 3. Sign in and allow

Claude opens a Cloudilio page. Sign in with your usual email and password. The next page lists what Claude will be able to do. Press **Allow**, and Claude takes you back to the chat.

## Step 4. Ask for your app

Say what you want in plain words, and mention Cloudilio so Claude knows where to put it. Claude creates the app, builds a preview and checks that its pages open. It tells you when the preview is ready. The live app changes only after you say yes.

| You want to | Ask Claude |
|---|---|
| Make a new app | Build a booking page for my dog-walking business on Cloudilio. |
| Change an app you have | On my Cloudilio app bakery-orders, add a field for allergies. |
| Find out why an app fails | My Cloudilio app shop shows an error. Find out why and fix it. |
| Undo a bad update | Put my app shop back to the version from yesterday. |
| Use your own domain | Connect www.mybakery.com to my app bakery-orders. |

## What Claude can do

- **See your apps.** Claude sees your apps and apps others shared with you, with their files and status.
- **Create apps and change files.** New apps count toward the number your plan includes. File changes don't reach visitors until you publish.
- **Build previews.** Previews are private links beside your live app. Claude gives you a link to open them.
- **Publish and go back.** Claude asks you in the chat before it publishes or puts back an earlier version.
- **Read errors.** Claude sees only the error lines from your app's output. Email addresses, passwords, keys, card numbers and IP addresses are hidden first.
- **Save secrets.** Claude can save an API key for your app. The key then passes through your chat, so you may prefer to add it yourself on the **Secrets** page.
- **Connect domains.** Claude lists the two DNS records to add, then checks them for you.
- **Add a database.** Claude can give your app its own [PostgreSQL or MySQL database](databases.md) and write the code that uses it. Only an app's owner can add or delete one, and Claude asks you before deleting it.
- **Set up Redis.** When your app needs a cache or a job queue, Claude can turn on its own [Redis](redis.md) and write the code that uses it. Only an app's owner can turn Redis on or off, and Claude asks you before clearing it or turning it off.

## What Claude can't do

- Delete apps
- Change your account, plan or billing
- Change apps someone shared with you to view only
- Edit the files of an app that publishes from GitHub. Change those in the repository

## Disconnect Claude

Open [Account settings](https://cloudilio.com/account/#claude) and press **Disconnect** beside the connection. Claude loses access straight away. A connection also ends by itself after 30 days without use. Your activity feed lists everything Claude published, rolled back or added.

## Fix common problems

Claude doesn't use Cloudilio

Check that Cloudilio is switched on for the chat in Claude's connectors menu. Then mention Cloudilio in your message.

"This account is using all the apps its plan includes"

Ask Claude to change an app you already have, or delete an app you no longer need in your dashboard.

"This account doesn't have a plan yet"

Your account needs a plan before it can create apps.

The preview keeps saying it is getting ready

A first preview takes a minute or two while Cloudilio installs your app's packages. Ask Claude to check again.

Claude asks you to sign in again

The connection ended, after 30 days without use or because it was disconnected. Sign in again from Claude.

Our post [How to Deploy an App Built with Claude and Host It Online](https://cloudilio.com/posts/build-and-publish-web-app-from-claude-chat) walks through a whole app, start to finish.

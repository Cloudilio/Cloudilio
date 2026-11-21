# Build, fix and deploy with AI

*This page is also on the website: [https://cloudilio.com/docs/ai](https://cloudilio.com/docs/ai)*

## Let the AI build your app, fix it or put it online for you

Cloudilio has an AI that works on your app's files. It can build a new app from a description, publish an app you already have, and fix a publish or an app that stopped working. You don't need an AI account to start: every account comes with Cloudilio credits.

## Three ways to use the AI

| What you want | Where to start | What the AI does |
|---|---|---|
| Publish code you already have | **New app**, then **Deploy with AI** | Reads your files, fixes what stops them running, previews the app, publishes it and checks it's live |
| A new app from an idea | **New app**, then **Describe it** | Writes the app and tries it in a private preview. You publish when you're happy |
| Fix a failed publish or a broken app | The **Fix with AI** button beside the error | Reads the error and the logs, fixes the cause and tries it again |

## Deploy with AI, step by step

Deploy with AI is for code that came from somewhere else: an app ChatGPT or Claude wrote, a project from a freelancer, or files on your computer that you've never put online. It handles the setup a host normally asks of you.

1. Open **New app** and choose **Deploy with AI**.
2. Drag your files onto the page. You can drop single files, whole folders, .zip files or any mix of them, up to 2 GB in all. Folders a server never needs, such as `node_modules`, `.git` and `.venv`, are left out for you. Any .zip files are unpacked where you dropped them.
3. Give the app a name and press **Create and deploy with AI**.
4. The builder page opens. The AI looks through the files and fixes whatever would stop them running here, such as a missing `requirements.txt` or `package.json` entry, a missing start script or files saved in the wrong folder. It changes as little as it can and keeps the app in its own language.
5. It tries the app in a private preview, fixes any error and tries again.
6. Once the preview runs, it publishes the app, opens its home page to check it works and tells you what it changed. If a publish fails, it reads the error and tries again.

You can watch each step as it happens, open every file it changed and undo any of it. If your app needs a key the AI can't make up, such as a Stripe or OpenAI key, it asks you to add it on the **Secrets** page.

## Cloudilio credits

Every account gets Cloudilio credits for building and deploying with AI, so you can try it without signing up anywhere else. Credits are for the life of your account. They don't reset each month.

Beside each chat, a bar shows how much of your credits you've used, as a percentage. When the bar is full, the AI stops and tells you how to carry on with your own key. Fixes from the **Fix with AI** button are free and don't use your credits.

## Use your own ChatGPT or Claude key

You can add your own key at any time, before or after your credits run out. The AI then runs on your own account, OpenAI (the company behind ChatGPT) or Anthropic (the company behind Claude) bills you directly at their prices, and Cloudilio adds nothing on top.

1. Get an API key from [OpenAI](https://platform.openai.com/api-keys) or [Anthropic](https://console.anthropic.com/settings/keys). An API key is separate from a ChatGPT Plus or Claude Pro subscription.
2. Open [Account, AI keys](https://cloudilio.com/account/#ai-keys), paste the key and press **Connect**. Cloudilio checks it works, then stores it encrypted.
3. New chats now run on your key. Your remaining credits stay for later.

To switch back and forth, use **Pay for new chats with** beside the chat, and choose **Cloudilio credits** or **My own key**. Switching starts a new chat, and your app's files stay as they are. Deploy with AI has the same choice on the New app page when you have both.

With your own key, the chat shows what it has cost so far at your provider's list prices, and you can set a limit so it stops at an amount you choose. Setting a monthly budget in your OpenAI or Anthropic account is also a good idea.

## What the AI can and can't do

- It reads and writes your app's files, builds previews, reads your app's logs and opens its pages.
- It publishes only in Deploy with AI. Everywhere else, your live app changes only when you press **Publish**.
- It can't see your secrets' values, add a database or Redis, or change your plan. When an app needs a database, it tells you to add one on the app's **Data** page.
- It works with apps you upload, not apps linked to GitHub, because each publish from GitHub would replace its changes.

## If something goes wrong

### The AI stopped and says my credits are used

Add your own ChatGPT or Claude key in Account, AI keys, then choose **My own key** beside the chat.

### The AI couldn't get my app live

It says what's still wrong in its last message. Reply in the chat with anything it asked for, such as a missing secret, or ask it to try again. The publish log on the app's **History** page has the full error.

### I don't like a change it made

Press **Restore files from before this** under your message in the chat, then publish again. Every version of every file is also kept on the app's **Files** page.

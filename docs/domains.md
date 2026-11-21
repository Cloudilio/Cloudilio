# Custom Domains & Edge TLS Routing

*This page is also on the website: [https://cloudilio.com/docs/domains](https://cloudilio.com/docs/domains)*

## Domain Configuration & Automatic SSL

Cloudilio routes web traffic through an edge reverse proxy powered by Caddy. The proxy obtains and renews TLS certificates from Let's Encrypt or ZeroSSL without manual maintenance.

## Step 1: Add your domain

Open your app, go to the **Web address** tab, type your domain under **Use your own domain** and press **Connect domain**. It can be a whole domain (`example.com`), a `www` address (`www.example.com`) or any other subdomain (`shop.example.com`).

Leave **also send visitors who add or leave out www to it** ticked. Whichever address you enter is the main one, and the other forwards to it, keeping the rest of the address:

- Enter `www.example.com`: `example.com/menu` forwards to `www.example.com/menu`.
- Enter `example.com`: `www.example.com/menu` forwards to `example.com/menu`.

It's offered for a whole domain and its `www` address, not for other subdomains such as `shop.example.com`. You can turn it on or off later from the **Web address** tab.

## Step 2: Add the records at your domain company

Sign in where you bought the domain (for example GoDaddy, Namecheap, Porkbun or Cloudflare) and open its DNS settings. The **Web address** tab shows each record with copy buttons. You need two, plus a third when the other address (with or without `www`) forwards:

| What it does | Type | Name | Value |
|---|---|---|---|
| 1. Point it here: a subdomain such as `www` or `shop` | CNAME | `www` | `your-app.apps.cloudilio.com` |
| 1. Point it here: a whole domain such as `example.com` | A | `@` | The address shown on the tab |
| 2. Prove it's yours | TXT | `_platform-challenge.www` (or `_platform-challenge` for a whole domain) | `pythonhost-verify=…`, shown on the tab |
| 3. Point the other address here (if forwarding is on) | A | `@` for `example.com`, or `www` for `www.example.com` | The address shown on the tab |

The ownership record stops anyone else from connecting your domain to their app, even if it used to point here. If your domain company already has a record with the same name, such as a parking page, replace it.

## Step 3: Check and connect

Press **See current settings** to see what's in place. Once it says **Both records are in place**, press **Check and connect**. Your app opens at the domain, and the padlock (https) is set up automatically within a minute or two. The forwarding address gets its own padlock once its record points here.

**AUTOMATIC RENEWALS**

Certificates renew automatically before they expire. There's nothing to set up or remember.

## Troubleshooting Domain Verification

- **Changes take a while:** new records usually show up within a few minutes, sometimes a few hours. Press **See current settings** to check.
- **Still waiting after Check and connect:** the ownership (TXT) record isn't visible yet. Check its name: most domain companies add your domain to the end automatically, so type `_platform-challenge.www`, not the whole address.
- **Cloudflare Proxy Status:** If you manage DNS in Cloudflare, set proxy status to *DNS Only* (grey cloud) during initial verification so Caddy can reach the ACME challenge server directly.
- **CAA Records:** Confirm that your domain does not have CAA records blocking Let's Encrypt or ZeroSSL.

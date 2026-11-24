# Verify one Betterloop pageview on localhost

Use the ready-to-copy test page in a new Free Betterloop project. You need Python 3.

<details>
<summary>Watch the 15-second setup walkthrough</summary>

![Betterloop setup walkthrough. Copy the local test page, start the local server, open the page and check that Setup reports Connected.](assets/betterloop-first-pageview.gif)

</details>

1. [Set up monitoring](https://betterloopai.com/signup/from-install-guide) or sign in to your own starter project. Open **Setup**.
2. Under **Drop in the snippet**, expand **Try the snippet on localhost**. Use **Copy local test page** and save the complete contents as `betterloop-setup-test.html` in an empty folder.
3. Open a terminal in that folder. Use **Copy local server command** or run the command below.

   ```sh
   python3 -m http.server 8765 --bind 127.0.0.1
   ```
4. If Setup asks you to add an allowed origin, open **Settings** and append `http://127.0.0.1:8765` to the existing comma-separated list under **Allowed origins**. Save and allow up to 15 seconds for the change.
5. Choose **Open the local test page** in Setup. Leave it open for a few seconds, then return to Setup and look for **Connected. Events received.** The test page uses your project’s event allowance.

If you added an allowed origin for this test, remove only that entry when you finish. If your project is already connected or Setup does not offer the local check, [verify the snippet on your deployed site](https://betterloopai.com/docs/install#verify).

The pageview comes from the test page. Confirm a second pageview from your actual site before relying on its monitoring. If Setup is still waiting, use the [install troubleshooting steps](https://betterloopai.com/docs/install#verify). Stop the local server with Ctrl+C.

<details>
<summary>Build the HTML page manually</summary>

Use this option if your project allows `http://127.0.0.1:8765` and you prefer to paste your own snippet. From **Drop in the snippet**, copy the script and paste it where marked. Save this file as `betterloop-pageview-test.html`.

```html
<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <title>Betterloop pageview test</title>
    <!-- Paste the script from your Betterloop Setup tab here. -->
  </head>
  <body>
    <h1>Betterloop pageview test</h1>
  </body>
</html>
```

Run the same Python command above and open `http://127.0.0.1:8765/betterloop-pageview-test.html`. The first pageview should show in Setup. To inspect it, open the browser’s Network panel on the test page before reloading. Look for a `POST /api/ingest` response of HTTP 200 with `{"ok":true}`.

</details>

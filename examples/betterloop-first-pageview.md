# Verify one Betterloop pageview on localhost

Use a local HTML page to check that your Betterloop snippet sends a pageview. You need Python 3 and a Free Betterloop project.

1. [Set up monitoring](https://betterloopai.com/signup/from-install-guide) or sign in to your own starter project. Open **Setup** and copy the script under **Drop in the snippet**. If your existing project only accepts traffic from your production site, follow the [deployed-site check](https://betterloopai.com/docs/install#verify) there.
2. Save this as `betterloop-pageview-test.html` in a folder for this exercise. Paste your own snippet where the comment indicates.

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

3. Open a terminal in that folder and run:

```sh
python3 -m http.server 8765 --bind 127.0.0.1
```

4. Open `http://127.0.0.1:8765/betterloop-pageview-test.html` and leave that tab visible for a few seconds. Return to **Setup** and look for **Connected. Events received.** To inspect the new event, open the browser’s Network panel on the test page before reloading it. `POST /api/ingest` should return HTTP 200 with `{"ok":true}`.

The recorded pageview is the local test page. To start measuring your real site, place the project’s snippet on that site and open it once to check the installation there. If Setup still shows **Waiting for your first event**, use the [install troubleshooting steps](https://betterloopai.com/docs/install#verify). Stop the local server with Ctrl+C when you finish.

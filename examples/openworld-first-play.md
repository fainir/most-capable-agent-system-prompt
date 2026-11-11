# Test a browser game's first click when Three.js fails to load

OpenWorld’s built-in demo game runs inside an iframe. The title screen originally displayed **Click or press anything to start** before its JavaScript module loaded. If the module failed, the screen kept showing that prompt and the controls never became ready. [OpenWorld startup change](https://github.com/fainir/open-world/pull/19)

## Wait for the game to be ready

Render a status message, a hidden native Start button and a hidden Retry button. Give the module script the `ow-base-module` ID so the error handler can recognize its failure.

```html
<p id="ow-base-status" role="status">Loading game…</p>
<button type="button" id="ow-base-play" hidden>Start game</button>
<button type="button" id="ow-base-retry" hidden>Retry</button>
```

Install the handlers before starting the module. Capture load errors while Start is hidden. On failure, update the message and reveal Retry. Retry reloads the iframe document. On the ready event, hide the status and reveal Start.

```js
const status = document.getElementById('ow-base-status');
const play = document.getElementById('ow-base-play');
const retry = document.getElementById('ow-base-retry');

window.addEventListener('error', event => {
  if (play.hidden && (event.target?.id === 'ow-base-module' || event instanceof ErrorEvent)) {
    status.textContent = 'The game could not load.';
    retry.hidden = false;
  }
}, true);

document.addEventListener('ow-base-ready', () => {
  status.hidden = true;
  retry.hidden = true;
  play.hidden = false;
}, { once: true });

retry.addEventListener('click', event => {
  event.stopPropagation();
  location.reload();
});
```

After the scene and controls are initialized, dispatch `document.dispatchEvent(new Event('ow-base-ready'))` from the module. Add `if (document.getElementById('ow-base-play').hidden) return;` at the top of `startGame` so old entry points honor the same gate. Put the Start button inside the overlay whose click handler calls `startGame`. Remove the document-wide start-on-keydown listener. Enter and Space activate the focused button. Touch users see **Tap to play**.

The linked patch also stops button events from reaching the game’s input handlers. It applies the change to the known demo template and keeps the existing iframe sandbox. [Startup patch](https://github.com/fainir/open-world/pull/19/files)

## Verify failure, recovery and first play

Use Playwright with Google Chrome installed. Save this as `first-play.mjs` in a project with `playwright` and run `node first-play.mjs`. It aborts the first Three.js request. Retry loads it again. The final assertion checks for the game’s controls after pressing Start.

```js
import assert from 'node:assert/strict';
import { chromium } from 'playwright';

const browser = await chromium.launch({
  channel: 'chrome',
  args: ['--enable-unsafe-swiftshader'],
});

try {
  const page = await browser.newPage({ viewport: { width: 1440, height: 812 } });
  page.setDefaultTimeout(45000);
  const three = 'https://cdn.jsdelivr.net/npm/three@*/build/three.module.js';
  await page.route(three, route => route.abort('failed'), { times: 1 });
  await page.goto('https://open-world.gg/', { waitUntil: 'commit' });
  
  const game = page.frameLocator('#ow-game');
  const retry = game.getByRole('button', { name: 'Retry', exact: true });
  const start = game.getByRole('button', { name: /start game|tap to play/i });
  
  await retry.waitFor({ state: 'visible' });
  assert.equal(await start.isVisible(), false);
  
  await retry.click();
  await start.waitFor({ state: 'visible' });
  await start.press('Enter');
  await game.locator('#overlay').waitFor({ state: 'hidden' });
  await game.locator('#bottom-bar').waitFor({ state: 'visible' });
} finally {
  await browser.close();
}
```

The full check also holds the module request open to verify that **Loading game…** stays visible. It tests Retry and first play with touch at 375px and keyboard at 1440px. A separate contrast fix sets the loading and error text to white, which the test also checks. [Full browser check](https://github.com/fainir/open-world/blob/main/qa/check-game-startup.mjs) · [Contrast fix](https://github.com/fainir/open-world/pull/20)

Open the live demo to see the normal loading and Start states. [Live OpenWorld game](https://open-world.gg/?utm_source=github&utm_medium=readme&utm_campaign=openworld-first-play)

*AI generated this guide from the linked source and verified browser tests.*

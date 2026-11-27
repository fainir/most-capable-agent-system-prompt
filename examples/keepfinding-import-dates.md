# Check the dates in a KeepFinding import

Try a small export in a guest library before moving your bookmarks. Use a fresh signed-out browser session for each sample.

| Export | Test file | Saved date in the file |
| --- | --- | --- |
| Pocket | [Pocket CSV](pocket-test.csv) | 2025-11-01 UTC |
| Raindrop | [Raindrop CSV](raindrop-dates-test.csv) | 2024-03-01 UTC |
| Browser bookmarks | [Bookmarks HTML](browser-bookmark-date-test.html) | 2024-02-15 UTC |

1. Open a sample file in GitHub. On desktop, choose **Download raw file**. On a phone, open **Edit and raw actions** and choose **Download**.
2. In a signed-out browser, open the matching [Pocket importer](https://keepfind.ing/pocket?utm_source=github&utm_medium=readme&utm_campaign=mcasp-bookmark-date-check), [Raindrop importer](https://keepfind.ing/raindrop?utm_source=github&utm_medium=readme&utm_campaign=mcasp-bookmark-date-check) or [browser bookmarks importer](https://keepfind.ing/?import=1&utm_source=github&utm_medium=readme&utm_campaign=mcasp-bookmark-date-check).
3. On Pocket or Raindrop, select the import button for that service. Choose the sample file in the import panel. The preview should recognize the format and show one link. The HTML sample should also show the **Reading** folder and the date from the file.
4. Choose **Import 1 link** to save the sample. Close Settings and find the sample in **All saved**. Compare the card’s **Saved** age with the date in the table. These samples should show an age in years. Reload and confirm the sample and its **Saved** label are the same.

If the preview looks right, choose your own export from the same import panel and review the preview before saving it. Browser bookmark exports use the HTML format. [Export bookmarks from Chrome](https://support.google.com/chrome/answer/96816?hl=en) · [Export bookmarks from Firefox](https://support.mozilla.org/en-US/kb/export-firefox-bookmarks-to-backup-or-transfer).

# Verify an English and Korean Astro cutover

Use this exercise before switching a bilingual static site to a new host. Keep a list of the old public URLs and the exact final URLs you intend to serve. This fictional cutover keeps both article slugs.

| Language | Final path |
| --- | --- |
| English | `/blog/api-document` |
| Korean | `/blog/api-document-ko` |

In the rendered HTML, each final page has its own canonical URL. Both pages list both final URLs as `hreflang` alternates, including their own. Build that list from the translations you actually publish. When a post has just one published language, this example omits translation alternates. In Astro, check the paths your routing configuration generates before using them in metadata. [Google's localized page guidance](https://developers.google.com/search/docs/specialty/international/localized-versions) · [Astro's locale routing](https://docs.astro.build/en/guides/internationalization/).

## Run the fixture

From the repository root, run the six checks. They cover a complete alternate group, a missing self-link, a Korean page pointing its canonical at English, an unpublished alternate, a duplicated locale suffix, and an extra redirect. [Python fixture](astro-bilingual-cutover.py).

```sh
python3 -I examples/astro-bilingual-cutover.py -v
```

## Check your preview

Set `legacy` to an old public URL you control, then repeat for the other language and each legacy host. The first command prints the original URL, its response status and its destination. The second follows at most one redirect and prints the final status and URL.

```sh
legacy='https://legacy.example.test/blog/api-document-ko'
curl --silent --show-error --max-time 15 --output /dev/null \
  --write-out '%{url_effective} %{http_code} %{redirect_url}\n' "$legacy"
curl --fail --silent --show-error --max-time 15 --location --max-redirs 1 \
  --output /dev/null --write-out '%{http_code} %{url_effective}\n' "$legacy"
```

For this fixture, expect one permanent `301` to the same Korean slug on the new host, followed by `200`. Compare the final page's canonical and alternate URLs with your published map. Spot-check the English page the same way. [Google's site migration checklist](https://developers.google.com/search/docs/crawling-indexing/site-move-with-url-changes).

Run a free Betterloop report on one public preview URL to see the canonical it detects. When the site is live, open the same checker with the deployed URL. [Run the website check](https://betterloopai.com/check/from-agent-readme).

For recurring monitoring across several sites, the Pro comparison shows the current project limits and price. [See the monitoring plans](https://betterloopai.com/pricing/from-readme).

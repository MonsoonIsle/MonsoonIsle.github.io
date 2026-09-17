# Monsoon Isle website

Static HTML/CSS site for GitHub Pages. No build step, external fonts or site analytics. English and Chinese are independent static pages under /en/ and /zh/. The root redirects to /en/. Language links open the equivalent page, and the URL always determines the language. No JavaScript or browser storage is required.

- English home: https://monsoonisle.github.io/en/
- Chinese home: https://monsoonisle.github.io/zh/
- English privacy policy (Google Play): https://monsoonisle.github.io/en/games/the-arrow/privacy/
- Chinese privacy policy: https://monsoonisle.github.io/zh/games/the-arrow/privacy/

## Preview

Run `python -m http.server 8080` from this directory and visit http://localhost:8080/.

## Publish

Commit and push to the branch configured in Settings → Pages. This change has not been pushed automatically.

## Release checklist

- Confirmed developer name: Monsoon Isle. Public privacy and support contact: aquark314@gmail.com.
- Verify Firebase retention settings, target age and final distributed SDK configuration.
- Current game source integrates AdMob and Firebase Analytics; its old offline privacy text in data/settings_content.gd and docs/legal/privacy-policy.md needs updating before release.
- Keep the Play Data safety declaration and in-game privacy text consistent with this page.
- The website does not implement in-game SDK consent; verify required consent for release regions separately.

## Add another game

Add matching pages under en/games/<game-slug>/privacy/ and zh/games/<game-slug>/privacy/. Add a game card to each language homepage, matching language links, canonical and hreflang links, and update sitemap.xml.

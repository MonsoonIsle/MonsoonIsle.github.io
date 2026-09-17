# Monsoon Isle website

Static HTML/CSS site for GitHub Pages. No build step, external fonts, JavaScript or site analytics.

- Home: https://monsoonisle.github.io/
- The Arrow privacy policy: https://monsoonisle.github.io/games/the-arrow/privacy/

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

Add games/<game-slug>/privacy/index.html and a card on index.html. Use stable directory URLs, and update sitemap.xml.

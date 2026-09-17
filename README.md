# Monsoon Isle website

Static HTML/CSS site for GitHub Pages. No build step, external fonts or site analytics. English and Chinese are independent static pages under /en/ and /zh/. The root redirects to /en/. Language links open the equivalent page, and the URL always determines the language. No JavaScript or browser storage is required.

- English home: https://monsoonisle.github.io/en/
- Chinese home: https://monsoonisle.github.io/zh/
- English privacy policy (Google Play): https://monsoonisle.github.io/en/games/the-arrow/privacy/
- Chinese privacy policy: https://monsoonisle.github.io/zh/games/the-arrow/privacy/

## Preview

Run `python -m http.server 8080` from this directory and visit http://localhost:8080/.

## Publish

Commit and push to the branch configured in Settings → Pages.

## Release checklist

- Confirmed developer name: Monsoon Isle. Public privacy and support contact: aquark314@gmail.com.
- Apply and verify the agreed 2-month Analytics retention policy in the console; align the store target audience with ages 13 and over and verify the final distributed SDK configuration.
- Current game source integrates AdMob and Firebase Analytics; its old offline privacy text in data/settings_content.gd and docs/legal/privacy-policy.md needs updating before release.
- Keep the Play Data safety declaration and in-game privacy text consistent with this page.
- The website does not implement in-game SDK consent; verify required consent for release regions separately.

## Privacy policy maintenance

The English and Chinese policies cover The Arrow, support correspondence, and this GitHub Pages website. Keep their numbered sections, data practices, dates, and links synchronized. The policy distinguishes local saves from analytics events, explains SDK data handling and deletion limits, and provides a privacy request contact. It does not claim an in-game consent screen or analytics switch is implemented.

Confirmed product decisions:

- Target audience: users aged 13 and over; the game is not directed to children under 13. The store's 3+ content rating is separate from this target audience. Ages 13–17 may still require additional protections under local law and Google Play policies.
- Planned release regions: Southeast Asia and Europe/Americas (东南亚和欧美). The public policy does not need a country-by-country availability list; exact store distribution settings determine which regional requirements must be implemented.
- Retention policy: 2 months for applicable Firebase/Google Analytics user-level and event-level data. This is a policy decision, not confirmation of a console change. It does not set a 2-month limit for aggregate reports, AdMob data, local records or support messages.

Before publishing the policy with a game release, complete these implementation checks:

- Match the actual Play Console target audience selections and marketing to the intended 13+ audience. Check protections for younger teens by release country; a 13+ audience does not automatically remove all obligations concerning minors. Do not claim an age gate or child-directed SDK safeguards exist without verifying the implementation.
- Review the actual country distribution settings internally. For personalized AdMob ads in the EEA, UK and Switzerland, implement Google's required certified CMP/TCF flow (for example, the appropriate Google UMP flow), alongside any other legally required consent and withdrawal controls. Review applicable US state and Southeast Asian privacy requirements for the selected countries. A regional rights paragraph does not implement these controls.
- Check the final build's consent flow and withdrawal controls. On September 17, 2026, the sibling `TheArrow` source includes consent APIs in the AdMob plugin, but no game-side calls to display/manage consent were found; Firebase collection is enabled by build configuration without a player-facing opt-out. Policy wording does not implement these controls.
- In the linked Google Analytics property under Admin → Data retention, set the applicable user/event retention to **2 months**, turn **Reset user data on new activity off** so user identifiers are not renewed by fresh activity, and save and verify the settings before publishing the 2-month statement. These console changes have not been performed or verified in this task. Google's scheduled deletion cycle still applies. Check exports or linked services and document any separate retention; do not infer console settings from SDK code or apply this duration to AdMob.
- The developer does not separately retain raw gameplay analytics on self-operated servers. This does not mean no retention: the current client persists installation identifiers and an event queue in a local `.analytics.cfg` file, Google hosts analytics and advertising data, and support emails remain subject to their own retention criteria. Keep the public policy consistent if exports or additional storage are introduced.
- Confirm that Monsoon Isle and the contact details identify the operator consistently with the store listing; add legal identity, address or regional representative details if required for the release territories.
- Replace the outdated offline-only text in the game's `data/settings_content.gd` and `docs/legal/privacy-policy.md`, and reconcile the Play Data safety form with the final SDK behavior.

Editorial references (reviewed September 17, 2026): [Easybrain](https://easybrain.com/privacy) for coverage and organization, and [Chroma Blocks](https://atomnyx.com/chroma-blocks-privacy.html) for direct language. Their product features, age limits and consent mechanisms are not evidence of The Arrow's practices. Technical and disclosure references: [Google Play User Data](https://support.google.com/googleplay/android-developer/answer/10144311), [AdMob data disclosure](https://developers.google.com/admob/android/privacy/play-data-disclosure), [Firebase privacy](https://firebase.google.com/support/privacy), [Analytics retention](https://support.google.com/analytics/answer/7667196), [GitHub Pages visitor logging](https://docs.github.com/en/pages/getting-started-with-github-pages/what-is-github-pages), and [ICO privacy information guidance](https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/individual-rights/the-right-to-be-informed/what-privacy-information-should-we-provide/).

## Add another game

Add matching pages under en/games/<game-slug>/privacy/ and zh/games/<game-slug>/privacy/. Add a game card to each language homepage, matching language links, canonical and hreflang links, and update sitemap.xml.

# Monsoon Isle website

Static HTML/CSS site for GitHub Pages. No build step, external fonts or site analytics. The site is English-only for an international audience. The homepage and game privacy policies live under /en/ to preserve existing public links. The root redirects to /en/. No JavaScript or browser storage is required.

- English home: https://monsoonisle.github.io/en/
- English privacy policy (Google Play): https://monsoonisle.github.io/en/games/the-arrow/privacy/

## The Cube privacy draft

`en/games/the-cube/privacy/index.html` is the September 30, 2026 review draft for
The Cube's next Android release. It has no effective date, is marked
`noindex,nofollow`, and is excluded from `sitemap.xml`. Its homepage card links to
a draft. This section supersedes the September 29 development-only snapshot;
normal gameplay now has defined interstitial and optional rewarded-revive
placements. The Cube uses no banners.

The policy describes separate, default-off usage statistics and Crashlytics
(Java/NDK) sharing, the limited gameplay-event fields, withdrawal controls,
AdMob/UMP, local saves, provider processing and deletion limits. It does not
claim that Java/NDK reporting captures every GDScript error or that Firebase
console delivery, release configuration or legal compliance has been verified.

Before treating this as the effective policy:

- Confirm The Cube's actual target age groups and regional age/consent handling.
  No age restriction or store rating has been inferred from another product.
- Verify and record the Analytics retention duration and reset-on-new-activity
  setting for project `the-cube-63905`. No duration is assumed. Google's
  documented Crashlytics retention is a separate provider practice.
- Match the distributed build to the event definitions and separate privacy
  switches; verify off-by-default behavior, withdrawal/restart behavior and
  controlled Analytics/Crashlytics delivery in the project's console.
- Verify production interstitial and rewarded ad-unit formats and UMP messages.
  Endless shows at most one interstitial at ordinary game-over, with a 60-second
  skip after rewarded revival; challenges count three first-time completions,
  excluding replays; either mode allows at most two rewarded revives per attempt.
- Replace review notes with verified facts and set an effective date before
  removing draft labels/robots restrictions and adding the canonical URL to the
  sitemap. Keep the game's policy link and Play Data safety declaration aligned.
  A push to a branch does not itself establish that GitHub Pages published it.

The intended policy URL is
https://monsoonisle.github.io/en/games/the-cube/privacy/.
For a local preview, run the server below and open
http://localhost:8080/en/games/the-cube/privacy/.

### The Cube app-ads.txt

The root `app-ads.txt` adds this authorized direct-seller entry for the supplied
AdMob publisher account; it is not an app ID or an ad-unit ID:

```text
google.com, pub-8551268736492401, DIRECT, f08c47fec0942fa0
```

Format and root placement follow [AdMob's setup instructions](https://support.google.com/admob/answer/9363762?hl=en)
and [Google's seller-entry example](https://support.google.com/admanager/answer/9422161?hl=en).
Do not replace or remove other publishers' existing lines during future updates.
After publishing, check https://monsoonisle.github.io/app-ads.txt and the store's
developer-website domain, then verify crawl status in AdMob. A valid local file
does not establish public availability, AdMob verification or ad serving.

### The Cube verification

Check policy section links, duplicate IDs, canonical/robots metadata, local
assets and the homepage's Cube link. Serve the repository and check the policy,
homepage, stylesheet and `/app-ads.txt` return HTTP 200. In a browser, check the
policy at 320, 390, 768 and 1280 CSS pixels for horizontal overflow, readable
headings, visible focus and working section navigation. Review `git diff` to
ensure other products and shared styles are untouched.

Validation on September 30, 2026: `git diff --check` passed; a Python HTML parser
resolved all 22 local policy links/assets and checked 14 unique IDs, canonical,
draft robots metadata and the homepage's Cube link. Local HTTP checks returned
200 for the homepage, Cube policy, stylesheet, Cube image and plain-text
`app-ads.txt`. Headless Chrome via the existing Playwright installation passed
all four widths, section navigation and visible keyboard focus, with no page
errors. The 390 px and 1280 px screenshots were visually reviewed. The homepage
and README text outside this Cube section were verified byte-identical to HEAD.
These are local checks; public availability and provider-console verification
remain separate release checks.

Official disclosure references, reviewed September 30, 2026:
[Mobile Ads data](https://developers.google.com/admob/android/privacy/play-data-disclosure),
[UMP controls](https://developers.google.com/admob/android/privacy),
[Firebase privacy and Crashlytics retention](https://firebase.google.com/support/privacy),
[Crashlytics collection controls](https://firebase.google.com/docs/reference/android/com/google/firebase/crashlytics/FirebaseCrashlytics),
and [Analytics retention settings](https://support.google.com/analytics/answer/7667196).
These documents do not verify The Cube's console settings or replace validation
against the SDK versions and features in the final build.

## Preview

Run `python -m http.server 8080` from this directory and visit http://localhost:8080/.

## Publish

Commit and push to the branch configured in Settings → Pages.

## Release checklist

The following existing checklist and confirmed decisions apply to **The Arrow**.

- Confirmed developer name: Monsoon Isle. Public privacy and support contact: aquark314@gmail.com.
- Apply and verify the agreed 2-month Analytics retention policy in the console; align the store target audience with ages 13 and over and verify the final distributed SDK configuration.
- Current game source integrates AdMob and Firebase Analytics; its old offline privacy text in data/settings_content.gd and docs/legal/privacy-policy.md needs updating before release.
- Keep the Play Data safety declaration and in-game privacy text consistent with this page.
- The website does not implement in-game SDK consent; verify required consent for release regions separately.

## Privacy policy maintenance

The English privacy policy covers The Arrow, support correspondence, and this GitHub Pages website. Keep its data practices, dates, and links up to date. The policy distinguishes local saves from analytics events, explains SDK data handling and deletion limits, and provides a privacy request contact. It does not claim an in-game consent screen or analytics switch is implemented.

Confirmed product decisions:

- Target audience: users aged 13 and over; the game is not directed to children under 13. The store's 3+ content rating is separate from this target audience. Ages 13–17 may still require additional protections under local law and Google Play policies.
- Planned release regions: Southeast Asia and Europe/Americas. The public policy does not need a country-by-country availability list; exact store distribution settings determine which regional requirements must be implemented.
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

Add an English policy under en/games/<game-slug>/privacy/. Add a game card to en/index.html, set the canonical URL for the new policy, and update sitemap.xml.

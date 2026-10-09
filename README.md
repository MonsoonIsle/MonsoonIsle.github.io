# Monsoon Isle website

Static HTML/CSS site for GitHub Pages. No build step, external fonts or site analytics. The site is English-only for an international audience. The homepage and game privacy policies live under /en/ to preserve existing public links. The root redirects to /en/. No JavaScript or browser storage is required.

- English home: https://monsoonisle.github.io/en/
- English privacy policy (Google Play): https://monsoonisle.github.io/en/games/the-arrow/privacy/

## The Cube privacy policy

`en/games/the-cube/privacy/index.html` is The Cube's effective privacy policy,
effective **September 30, 2026**, last updated **October 3, 2026**. It covers
Android versions, including test versions, support correspondence and this
website. The public policy URL is
https://monsoonisle.github.io/en/games/the-cube/privacy/.
The Cube privacy and support contact is **mengjingchanyu@gmail.com**.
The Arrow and the general website contact remain unchanged. The policy's effective
date does not mean the game has launched publicly or that every feature is available
in every build.

The policy reflects the following verified source and console facts:

- Production uses one Google UMP form explicitly describing ads, Firebase gameplay
  statistics and Crashlytics stability reports. Agree to all permits the three
  together; Choose separately and No thanks retain independent purpose choices.
  Own purposes use consent: device storage (1), advertising measurement (7), content
  measurement (8), services development (10). Statistics require 1+8, app ad events
  also require 7, and crash reporting for stability improvement requires 1+10.
  Native settings may turn either optional service off; silent refresh cannot
  re-enable it. Invalid or interrupted consent records keep optional collection off.
  Turning statistics off resets local Analytics. Turning diagnostics off requests
  deletion of unsent reports, with full SDK disabling at next launch; transmitted
  or in-progress reports cannot be recalled. Development retains test choices.
- Gameplay Analytics uses a fixed field set: app/build context, mode, level,
  outcomes, scores, revives, a per-attempt identifier and ad outcomes/error codes.
  Separate event-deduplication IDs stay local. Custom events do not contain saved
  games, names, emails, free-text errors or a custom user ID; this does not mean
  SDK data or crash reports are anonymous. Analytics advertising consent
  categories remain denied independently of AdMob choices.
- Production enables owned AdMob placements for ordinary supported phones after
  UMP permission; fill still depends on Google, readiness and network. No age-test
  prompt appears in production. Development/closed-test modes retain test operator
  restrictions, and emulators receive SDK test ads. No banners; placements remain
  game-boundary interstitials and optional rewarded revives. Refusal preserves
  permitted limited-ad requests without enabling optional Firebase sharing.
- The intended audience is 13+. Adult test confirmation does not verify the age
  of all players or establish protections for a general 13+ advertising rollout.
- On September 30, 2026, the Firebase project `the-cube-63905` was verified as
  linked to Analytics property `556274805` and Android stream `15861889930`
  (`com.tesselox.game`). The console showed **2 months for event data**, **14
  months for user data**, and **Reset user data on new activity enabled**. The
  policy describes renewal of user-identifier retention and Google's monthly
  deletion cycle. These settings were inspected, not changed. They do not set
  retention for standard aggregate reports, AdMob, Crashlytics or support email.
- The Cube's English European UMP message was published and its published status
  read back on September 30, 2026. It targets the EEA, UK and Switzerland and
  offers Consent, Do not consent and Manage options. The vendor list is available
  in the message; the policy does not hard-code its size. Account-wide Consent
  Mode and supplier settings were not changed. Console publication does not
  itself verify delivery on a device. The existing non-debuggable Android test
  build subsequently received the three-button Cube form on an isolated emulator;
  reject, reopen and consent returned to settings with both telemetry switches off.
  Actual rewarded/interstitial display and physical-device checks remain pending.

Before a broader game release, match the distributed build, in-game notice and
Play Data safety form to this policy; verify the first-use choices, withdrawal,
Analytics/Crashlytics delivery and advertising flow on a device. Confirm the
store audience, distribution countries, required protections for minors and
regional notices, plus any required operator/representative details. The current
adult-only test restriction does not implement those broader release controls.
Keep these implementation checks separate from the policy's effective status.

### The Cube app-ads.txt

The root `app-ads.txt` includes this authorized direct-seller entry for the
supplied AdMob publisher account; it is not an app ID or an ad-unit ID:

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

Check section links, duplicate IDs, canonical metadata, effective date, both
contact addresses and absence of draft/noindex wording. Check the homepage's
Cube link and the sitemap entry. Serve the repository and check the policy,
homepage, stylesheet and `/app-ads.txt` return HTTP 200. In a browser, check the
policy at 320, 390, 768 and 1280 CSS pixels for horizontal overflow, readable
headings, visible focus and working section navigation. Review `git diff` to
ensure The Arrow and shared styles are untouched. After publishing, verify the
public policy and homepage; a branch push alone is not proof of deployment.

Content validation on September 30, 2026: `git diff --check` passed. A Python
HTML-parser check confirmed balanced markup, 14 unique IDs, 13 policy sections,
22 local link/asset references, the canonical URL, effective date, both contacts
and the verified retention values. The Arrow policy and README content outside
this Cube section were byte-identical to the pre-change `HEAD`. Browser checks at
320, 390, 768 and 1280 CSS pixels showed no horizontal overflow; local resource
requests returned HTTP 200, section links worked and keyboard focus was visible.
The 390 px and 1280 px views were visually reviewed. Public deployment and
ad-display checks remain separate from these content checks.

Official disclosure references, reviewed September 30, 2026:
[Next-Gen Mobile Ads data](https://developers.google.com/admob/android/next-gen/privacy/play-data-disclosure),
[UMP controls](https://developers.google.com/admob/android/privacy),
[European message choices and vendor lists](https://support.google.com/admob/answer/10114014?hl=en),
[Firebase privacy and Crashlytics retention](https://firebase.google.com/support/privacy),
[Crashlytics collection controls](https://firebase.google.com/docs/reference/android/com/google/firebase/crashlytics/FirebaseCrashlytics),
[Analytics retention settings](https://support.google.com/analytics/answer/7667196),
[Google transfer mechanisms](https://policies.google.com/privacy/frameworks),
and [ICO privacy-notice guidance](https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/individual-rights/the-right-to-be-informed/what-privacy-information-should-we-provide/).
These sources explain provider practices; local source review and the recorded
console observations support the product-specific statements. They do not
certify legal compliance or prove device delivery of every service.

The existing release checklist below continues to apply to The Arrow.

## Preview

Run `python -m http.server 8080` from this directory and visit http://localhost:8080/.

## Publish

Commit and push to the branch configured in Settings → Pages.

## Release checklist

- Confirmed developer name: Monsoon Isle. Public privacy and support contact: aquark314@gmail.com.
- Apply and verify the agreed 2-month Analytics retention policy in the console; align the store target audience with ages 13 and over and verify the final distributed SDK configuration.
- The Arrow source integrates AdMob, Firebase Analytics, UMP consent controls and optional Firebase Crashlytics. Its in-game privacy text in `data/settings_content.gd`, `docs/legal/privacy-policy.md` and this website policy were aligned on October 9, 2026, including advertising measurement and independent crash sharing.
- Keep the Play Data safety declaration and in-game privacy text consistent with this page.
- The website does not implement in-game SDK consent; verify required consent for release regions separately.

## Privacy policy maintenance

The English privacy policy covers The Arrow, support correspondence, and this GitHub Pages website. Keep its data practices, dates, and links up to date. The policy distinguishes local saves from analytics events, explains SDK data handling and deletion limits, and provides a privacy request contact. It describes the implemented Privacy choices entry, Share gameplay analytics and independent Share crash reports switches, and records the policy update date.

Confirmed product decisions:

- Target audience: users aged 13 and over; the game is not directed to children under 13. The store's 3+ content rating is separate from this target audience. Ages 13–17 may still require additional protections under local law and Google Play policies.
- Planned release regions: all regions except mainland China. The public policy does not need a country-by-country availability list; exact store distribution settings determine which regional requirements must be implemented.
- Retention policy: 2 months for applicable Firebase/Google Analytics user-level and event-level data. This is a policy decision, not confirmation of a console change. It does not set a 2-month limit for aggregate reports, AdMob data, local records or support messages. Crashlytics has a separate provider retention period of 90 days before deletion begins; native minidumps are temporary processing data.
- Google Ads: the developer currently has no Ads account and plans to link it after the app is published, before paid acquisition. Client measurement capability does not mean an account is linked or a campaign is running. The policy discloses the data uses supported by the release; account linking and actual attribution remain separate operational steps.
- Crash sharing: off by default and independent of gameplay analytics. Automatic upload stays off; enabling takes effect after restart and eligible reports are submitted on a later launch. Disabling invalidates the current session, even if sharing is re-enabled before restart; unauthorized pending reports are queued for deletion on a subsequent launch. Already submitted or in-transit reports cannot be recalled.

Before publishing the policy with a game release, complete these implementation checks:

- Match the actual Play Console target audience selections and marketing to the intended 13+ audience. Check protections for younger teens by release country; a 13+ audience does not automatically remove all obligations concerning minors. Do not claim an age gate or child-directed SDK safeguards exist without verifying the implementation.
- Review the actual country distribution settings internally. For personalized AdMob ads in the EEA, UK and Switzerland, implement Google's required certified CMP/TCF flow (for example, the appropriate Google UMP flow), alongside any other legally required consent and withdrawal controls. Review applicable US state and Southeast Asian privacy requirements for the selected countries. A regional rights paragraph does not implement these controls.
- Check the final build's consent flow and withdrawal controls. The October 9, 2026 release candidate retains the UMP cold-launch update, required forms, `canRequestAds()` advertising gate and Settings privacy entry. Firebase advertising storage, advertising user data and advertising personalization now follow their respective UMP signals; unknown or unconfigured purposes stay denied, and turning off Share gameplay analytics denies all Firebase purposes. This replaces the earlier statement that Analytics advertising-ID collection is always disabled. AdMob retains its separate consent processing.
- Device evidence on October 9, 2026: a Xiaomi 14 kept collection disabled during a Google consent-server timeout, then received the non-applicable-region status after network recovery. Turning analytics off disabled the Firebase advertising purposes and retained progress. Four QA diagnostic types were generated and submitted, and the developer confirmed seeing Crashlytics test reports in the console. A Google test rewarded ad produced the standard `ad_impression` with USD and a zero test value. These checks do not establish European-region consent/refusal behavior, every cloud diagnostic frame, or real paid attribution and revenue reconciliation.
- In the linked Google Analytics property under Admin → Data retention, set the applicable user/event retention to **2 months**, turn **Reset user data on new activity off** so user identifiers are not renewed by fresh activity, and save and verify the settings before publishing the 2-month statement. These console changes have not been performed or verified in this task. Google's scheduled deletion cycle still applies. Check exports or linked services and document any separate retention; do not infer console settings from SDK code or apply this duration to AdMob.
- The developer does not separately retain raw gameplay analytics on self-operated servers. This does not mean no retention: the current client persists installation identifiers and an event queue in a local `.analytics.cfg` file, Google hosts analytics and advertising data, and support emails remain subject to their own retention criteria. Keep the public policy consistent if exports or additional storage are introduced.
- Confirm that Monsoon Isle and the contact details identify the operator consistently with the store listing; add legal identity, address or regional representative details if required for the release territories.
- Keep the game's `data/settings_content.gd` and `docs/legal/privacy-policy.md` synchronized with this policy; all three describe the new controls as of October 9, 2026. Reconcile the Play Data safety form with the final SDK behavior, including crash diagnostics, identifiers and advertising measurement. Local source and policy updates do not confirm store declarations or public website deployment.
- The Arrow and The Cube use the existing publisher `pub-8551268736492401`; the root `app-ads.txt` already contains its direct-seller entry. No duplicate line is needed. Verify the public file and AdMob crawl status separately.
- After the Play listing is publicly accessible, add its verified download link to the homepage. Do not label the game publicly released based only on a local AAB export or upload.

Website validation on October 9, 2026: the eight added or changed disclosure paragraphs match the game policy; all 12 section anchors are unique and resolve, and local links and assets return HTTP 200. Browser checks at 320, 390, 768 and 1280 CSS pixels passed without horizontal overflow, with working section navigation and visible keyboard focus. The 390 px and 1280 px screenshots were reviewed. The Cube policy, its README section, shared styles, homepage and app-ads.txt were unchanged. Public deployment and Play declarations remain separate checks.

Editorial references (reviewed September 17, 2026): [Easybrain](https://easybrain.com/privacy) for coverage and organization, and [Chroma Blocks](https://atomnyx.com/chroma-blocks-privacy.html) for direct language. Their product features, age limits and consent mechanisms are not evidence of The Arrow's practices. Technical and disclosure references: [Google Play User Data](https://support.google.com/googleplay/android-developer/answer/10144311), [AdMob data disclosure](https://developers.google.com/admob/android/privacy/play-data-disclosure), [Firebase privacy](https://firebase.google.com/support/privacy), [Analytics retention](https://support.google.com/analytics/answer/7667196), [GitHub Pages visitor logging](https://docs.github.com/en/pages/getting-started-with-github-pages/what-is-github-pages), and [ICO privacy information guidance](https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/individual-rights/the-right-to-be-informed/what-privacy-information-should-we-provide/).

## Add another game

Add an English policy under en/games/<game-slug>/privacy/. Add a game card to en/index.html, set the canonical URL for the new policy, and update sitemap.xml.

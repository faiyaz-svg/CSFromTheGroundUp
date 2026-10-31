# Mobile development

Cheat sheet for the chapter. Lessons: [Mobile platforms: native and cross-platform](01-mobile-platforms-native-and-cross-platform.md), [PWAs, offline and push](02-pwas-offline-and-push.md).

## Key terms

| Term | Meaning | Lesson |
|---|---|---|
| iOS, Android | The two mobile platforms; Swift and Kotlin are their main languages | [1](01-mobile-platforms-native-and-cross-platform.md) |
| Native app | Built with the platform's own language and UI toolkit (SwiftUI, Jetpack Compose) | [1](01-mobile-platforms-native-and-cross-platform.md) |
| Cross-platform framework | One codebase, apps for both platforms (React Native with Expo, Flutter) | [1](01-mobile-platforms-native-and-cross-platform.md) |
| Foreground, background | The user is using the app, or has switched away; a background app can be killed | [1](01-mobile-platforms-native-and-cross-platform.md) |
| Runtime permission | User consent requested when a feature is first needed | [1](01-mobile-platforms-native-and-cross-platform.md) |
| Release track | Stage of testing in a store (TestFlight, Play internal, closed, open, production) | [1](01-mobile-platforms-native-and-cross-platform.md) |
| OTA update | Replaces JavaScript and assets without a store release; cannot change native code | [1](01-mobile-platforms-native-and-cross-platform.md) |
| PWA | A website that can be installed and work offline | [2](02-pwas-offline-and-push.md) |
| Web app manifest | JSON file with name, icons, `start_url`, `display` | [2](02-pwas-offline-and-push.md) |
| Service worker | Background script that handles `fetch`, `push` and other events | [2](02-pwas-offline-and-push.md) |
| Cache Storage | Browser store of request and response pairs managed by scripts | [2](02-pwas-offline-and-push.md) |
| Offline-first | Local copy is primary, sync to the server later | [2](02-pwas-offline-and-push.md) |
| Sync conflict | Two devices change the same record while offline | [2](02-pwas-offline-and-push.md) |
| Push service | Browser vendor's server that delivers push messages | [2](02-pwas-offline-and-push.md) |

## Choosing an approach

| Approach | Strong when | Cost |
|---|---|---|
| Native | Heavy graphics, new platform features at once | Two codebases |
| React Native + Expo | React team, standard screens | Sometimes a native module |
| Flutter | Identical custom look on both platforms | Dart, own widgets |
| Responsive web or PWA | Content, forms, internal tools, no store | Limited device access, weaker on iOS |

## Facts as of 2026

- Canada mobile OS share, September 2026: iOS about 65%, Android about 35% ([StatCounter](https://gs.statcounter.com/os-market-share/mobile/canada)).
- TestFlight: up to 100 internal and 10,000 external testers ([Apple](https://developer.apple.com/testflight/)).
- New personal Google Play accounts: closed test with 12 testers for 14 continuous days before production ([Google](https://support.google.com/googleplay/android-developer/answer/14151465)).
- React Native 0.88 and Expo SDK 58 were current in October 2026.
- Web Push on iOS needs a web app added to the Home Screen and a permission request from a tap ([WebKit](https://webkit.org/blog/13878/web-push-for-web-apps-on-ios-and-ipados/)).

## App lifecycle

| State | React Native `AppState` | Do |
|---|---|---|
| Foreground | `active` | Normal work |
| Switching | `inactive` (iOS only) | Pause sensitive work |
| Background | `background` | Save the user's work |
| Killed | no callback | Restore state on next start |

## PWA installability (Chromium)

1. Manifest linked with `<link rel="manifest" href="manifest.json">`.
2. `name` or `short_name`, `start_url`, `display`, and icons of 192 px and 512 px.
3. HTTPS, or `localhost` in development.
4. A service worker is needed for offline use, not for installing.

## Service worker lifecycle

| Event | When | Use for |
|---|---|---|
| `install` | Once per new version | `cache.addAll([...])` |
| `activate` | Old worker's pages are gone | Delete old caches, `clients.claim()` |
| `fetch` | Every request from a controlled page | `event.respondWith(...)` |
| `push` | A push message arrives | `showNotification(...)` |

## Caching strategies

| Strategy | Order | Good for |
|---|---|---|
| Cache first | Cache, then network | App shell, versioned files |
| Network first | Network, then cache | Fresh data with an offline fallback |
| Stale-while-revalidate | Cache now, refresh in the background | Lists, avatars |
| Network only | Network | Payments, must-be-current data |

## Rules

1. Change the cache name when the cached files change, and delete old caches in `activate`.
2. Store `response.clone()`, return the original (a body is read once).
3. Ask for permissions after a user action, in context.
4. Do not promise an over-the-air fix for native code or permission changes.
5. Replay offline writes when the page opens as well as through Background Sync.

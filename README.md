# adn-build-server

Free public build backend for the **Adn Building APK** Android app. A Cloudflare Worker relay receives a zipped project, stores it as a private *draft* release, and triggers the `build-apk` GitHub Actions workflow. The workflow auto-detects the project type, builds an APK, signs it, and attaches `app.apk` to that draft release, where the relay picks it up.

Supported: Web/HTML (WebView wrapper) · Native Android (Gradle, Java/Kotlin) · Flutter · Capacitor · Cordova · React Native (bare, with `android/`). Python/Kivy and other types get a clear bilingual error.

Security: the untrusted build job has no secrets, a read-only token, and no saved git credentials. Signing happens in a separate job on a fresh runner. Uploaded zips live only in draft releases (visible only to the repo owner) and are deleted after 6 hours by `cleanup-old-jobs`.

Secrets (optional; without them each build uses a one-time key): `SIGNING_KEYSTORE_B64`, `SIGNING_PASSWORD`, `SIGNING_ALIAS`.

Licenses: this repo – MIT. Actions used: actions/checkout, setup-java, setup-node, upload/download-artifact (MIT); gradle/actions (MIT); subosito/flutter-action (MIT). Tools: Gradle (Apache-2.0), Flutter (BSD-3), Capacitor (MIT), Cordova (Apache-2.0).

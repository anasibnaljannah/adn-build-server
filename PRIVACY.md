# Privacy Policy — Adn Building APK / سياسة الخصوصية

_Last updated: 22 October 2026 · Developer: Anas30 · Contact: anasibnaljannah@gmail.com_

[English](#english) · [العربية](#العربية)

---

## English

This policy covers the Android app **Adn Building APK** (package `com.xqvrtmzk.n7plb`) and its public build service (the relay at `https://adn-build-relay.anasibnaljannah.workers.dev` and the GitHub repository `anasibnaljannah/adn-build-server`).

### 1. Summary
- No account, no registration, no analytics, no advertising, no tracking SDKs, no crash reporting.
- The app sends data **only** when you press "Convert": your chosen project zip (and, if you enable it, your signing key) goes to the build service to produce your APK.
- Uploaded files are temporary and deleted automatically.

### 2. Data the app sends
| Data | When | Purpose |
|---|---|---|
| The project `.zip` you pick (max 50 MB) and its file name | When you tap Convert | Build an APK from it |
| Optional: your signing keystore, its password and alias | Only if "Sign with my key" is ON | Sign the APK with your own key |
| Technical connection data (IP address, user-agent, request time) | Every request | Unavoidably processed by the network providers below to deliver the request |

The app does not read your contacts, location, device identifiers, or any other files. It does not send anything in the background.

### 3. Where data is processed
1. **Cloudflare Workers** (Cloudflare, Inc.) — the relay receives the upload over HTTPS and forwards it to GitHub. The relay does not keep its own copy or log file contents. If your signing key is included, the relay encrypts it with AES-256-GCM before forwarding.
2. **GitHub** (GitHub, Inc. / Microsoft) — the zip is stored as an asset of a **draft (non-public) release** in the repository, and a **GitHub Actions** workflow builds and signs the APK on GitHub-hosted runners. The resulting APK is attached to the same draft release so the app can download it.
3. **DNS fallback** — if your network cannot resolve the relay's hostname, the app asks a DNS-over-HTTPS resolver (Cloudflare `1.1.1.1` and then Google `dns.google`) for that hostname only.

These providers may process data in the United States or other countries under their own privacy policies (cloudflare.com/privacypolicy, docs.github.com/site-policy/privacy-policies).

### 4. Retention and deletion
- Your zip, the build output, and the built APK live in a draft release that is **deleted automatically about 6 hours** after creation (an hourly cleanup job, so up to ~7 hours).
- Intermediate build artifacts inside GitHub Actions expire after **1 day** at most.
- Your encrypted signing key (if sent) is **deleted from the release immediately before signing** (and also on failure); the decrypted copy exists only on a short-lived, single-use runner that is destroyed after the job.
- Workflow run logs (which never contain file contents or key secrets) are kept by GitHub according to its default log retention.
- On your device: the built APK is saved to your Downloads folder; your settings and optional generated key are stored in the app's private storage. Uninstalling the app or clearing its data removes them (except files you saved to Downloads).

### 5. Sharing
We do not sell, rent, or share your data with anyone except the infrastructure providers named above, strictly to run the build. We do not inspect your projects except where needed to investigate abuse or comply with law.

### 6. Security
All transfers use HTTPS. Uploaded drafts are visible only to the repository owner. No method is 100% secure; do not upload projects containing secrets you cannot afford to expose (API keys, passwords).

### 7. Children
The app is not directed at children under 13 and does not knowingly collect their data.

### 8. Your rights
Because we hold no account or profile about you, and uploads delete themselves within hours, there is usually nothing to access or erase. You may still email us to ask for deletion of a specific job early, or with any privacy question.

### 9. Changes
We may update this policy; the "Last updated" date will change and the current version is always at this URL.

### 10. Contact
Anas30 — anasibnaljannah@gmail.com

---

## العربية

تغطي هذه السياسة تطبيق أندرويد **Adn Building APK** (الحزمة `com.xqvrtmzk.n7plb`) وخدمة البناء العامة التابعة له (الوسيط `https://adn-build-relay.anasibnaljannah.workers.dev` ومستودع GitHub ‏`anasibnaljannah/adn-build-server`).

### ١. الخلاصة
- لا حساب ولا تسجيل، ولا تحليلات، ولا إعلانات، ولا أدوات تتبّع، ولا تقارير أعطال.
- لا يرسل التطبيق أي بيانات **إلا** عند ضغطك "تحويل": يُرسَل ملف المشروع المضغوط الذي تختاره (ومفتاح التوقيع إن فعّلت ذلك) إلى خدمة البناء لإنتاج ملف APK.
- الملفات المرفوعة مؤقتة وتُحذف تلقائياً.

### ٢. البيانات التي يرسلها التطبيق
| البيانات | متى | الغرض |
|---|---|---|
| ملف ‎.zip‎ الذي تختاره (حتى 50 ميغابايت) واسمه | عند ضغط "تحويل" | بناء APK منه |
| اختياري: ملف مفتاح التوقيع وكلمة مروره واسمه المستعار | فقط إذا فعّلت "التوقيع بمفتاحي" | توقيع التطبيق بمفتاحك |
| بيانات اتصال تقنية (عنوان IP، نوع العميل، وقت الطلب) | مع كل طلب | تعالجها شبكات المزوّدين أدناه حتماً لإيصال الطلب |

لا يقرأ التطبيق جهات الاتصال أو الموقع أو معرّفات الجهاز أو أي ملفات أخرى، ولا يرسل شيئاً في الخلفية.

### ٣. أين تُعالَج البيانات
١. **Cloudflare Workers** (شركة Cloudflare) — يستقبل الوسيط الملف عبر HTTPS ويمرّره إلى GitHub دون الاحتفاظ بنسخة منه أو تسجيل محتواه. وإن أُرسل مفتاح توقيع يُشفَّر بـ AES-256-GCM قبل تمريره.
٢. **GitHub** (شركة GitHub / مايكروسوفت) — يُحفظ الملف كمرفق في **إصدار مسودّة غير عام** داخل المستودع، ويبني سير عمل **GitHub Actions** التطبيق ويوقّعه على خوادم GitHub، ثم يُرفق ملف APK بالمسودّة نفسها ليُنزّله التطبيق.
٣. **احتياط DNS** — إذا تعذّر على شبكتك حلّ اسم نطاق الوسيط، يستعلم التطبيق عنه وحده عبر DNS-over-HTTPS من Cloudflare ‏(1.1.1.1) ثم Google ‏(dns.google).

قد يعالج هؤلاء المزوّدون البيانات في الولايات المتحدة أو دول أخرى وفق سياسات خصوصيتهم.

### ٤. مدة الاحتفاظ والحذف
- يبقى ملفك المضغوط وناتج البناء وملف APK في مسودّة إصدار **تُحذف تلقائياً بعد نحو 6 ساعات** من إنشائها (مهمة تنظيف كل ساعة، أي 7 ساعات كحدّ أقصى تقريباً).
- الملفات الوسيطة داخل GitHub Actions تنتهي صلاحيتها خلال **يوم واحد** كحدّ أقصى.
- مفتاح التوقيع المشفّر (إن أُرسل) **يُحذف من المسودّة مباشرةً قبل التوقيع** (وكذلك عند الفشل)، والنسخة المفكوكة لا توجد إلا على خادم مؤقت يُستخدم مرة واحدة ثم يُتلف.
- سجلات تشغيل سير العمل (ولا تحتوي محتوى الملفات ولا أسرار المفاتيح) تحتفظ بها GitHub وفق مدتها الافتراضية.
- على جهازك: يُحفظ ملف APK في مجلد التنزيلات، وتُحفظ الإعدادات والمفتاح المُنشأ اختيارياً في التخزين الخاص بالتطبيق، وتُزال بإلغاء التثبيت أو مسح البيانات (عدا ما حفظته في التنزيلات).

### ٥. المشاركة
لا نبيع بياناتك ولا نؤجّرها ولا نشاركها مع أحد سوى مزوّدي البنية المذكورين وفقط لتنفيذ البناء. لا نطّلع على مشاريعك إلا عند الحاجة للتحقيق في إساءة استخدام أو الامتثال للقانون.

### ٦. الأمان
كل عمليات النقل عبر HTTPS، والمسودّات مرئية لمالك المستودع فقط. لا توجد وسيلة آمنة 100%؛ فلا ترفع مشاريع تحتوي أسراراً لا تحتمل كشفها (مفاتيح API أو كلمات مرور).

### ٧. الأطفال
التطبيق غير موجّه للأطفال دون 13 عاماً ولا يجمع بياناتهم عن علم.

### ٨. حقوقك
لا نحتفظ بأي حساب أو ملف تعريفي عنك، والملفات تُحذف ذاتياً خلال ساعات، فلا يوجد عادةً ما يُطلب الوصول إليه أو حذفه. ويمكنك مراسلتنا لطلب حذف مهمة معيّنة مبكراً أو لأي استفسار.

### ٩. التعديلات
قد نحدّث هذه السياسة، وسيتغيّر "تاريخ آخر تحديث"، والنسخة الحالية متاحة دائماً على هذا الرابط.

### ١٠. التواصل
Anas30 — anasibnaljannah@gmail.com

#!/usr/bin/env python3
"""Adn Build (GitHub Actions edition). Usage:
  build.py detect <zip> <workdir>      -> prints project type, writes <workdir>/root.txt
  build.py build  <workdir> <name> <out.apk>   (unsigned)
  build.py sign   <in.apk> <out.apk>
Signing: env KEYSTORE (path), KS_PASS, KS_ALIAS. Licensed MIT."""
import os, re, sys, json, html, shutil, secrets, string, zipfile, subprocess
from pathlib import Path

MAX_UNZIPPED = 200 * 1024 * 1024; MAX_FILES = 5000
HERE = Path(__file__).resolve().parent
ANDROID_HOME = os.environ.get("ANDROID_HOME") or os.environ.get("ANDROID_SDK_ROOT", "")
ERR = {
 "kivy": "Python/Kivy projects are not supported yet. / مشاريع Python/Kivy غير مدعومة حاليًا.",
 "unknown": "Unsupported project: no index.html, Android Gradle, Flutter, React Native, Cordova or Capacitor project found. Desktop/server code cannot run as an Android app. / مشروع غير مدعوم: لم يتم العثور على مشروع ويب أو أندرويد أو Flutter أو React Native أو Cordova أو Capacitor. شيفرات سطح المكتب أو الخوادم لا تعمل كتطبيق أندرويد.",
}

def fail(msg):
    Path("error.txt").write_text(msg[:600], encoding="utf-8"); print("ERROR:", msg); sys.exit(1)

def safe_extract(zp, dest):
    total = 0; root = dest.resolve()
    with zipfile.ZipFile(zp) as z:
        infos = z.infolist()
        if len(infos) > MAX_FILES: fail("too many files in zip")
        for info in infos:
            t = (dest / info.filename).resolve()
            if root != t and root not in t.parents: fail("unsafe path in zip (zip-slip)")
            if (info.external_attr >> 16) & 0o170000 == 0o120000: fail("symlinks not allowed in zip")
            total += info.file_size
            if total > MAX_UNZIPPED: fail("unzipped project too large")
            if info.is_dir(): t.mkdir(parents=True, exist_ok=True); continue
            t.parent.mkdir(parents=True, exist_ok=True)
            with z.open(info) as s, open(t, "wb") as d: shutil.copyfileobj(s, d)

def files(src):
    return [p for p in src.rglob("*") if p.is_file() and not any(x in p.parts for x in ("__MACOSX", "node_modules", "build", ".gradle"))]
def shallow(fs, pred):
    c = [p for p in fs if pred(p)]
    return min(c, key=lambda p: len(p.parts)) if c else None
def rd(p): return p.read_text(errors="ignore")

def detect(src):
    fs = files(src)
    pub = shallow(fs, lambda p: p.name == "pubspec.yaml")
    if pub and "flutter" in rd(pub): return "flutter", pub.parent
    cap = shallow(fs, lambda p: p.name.startswith("capacitor.config."))
    if cap: return "capacitor", cap.parent
    cfg = shallow(fs, lambda p: p.name == "config.xml" and "widget" in rd(p)[:2000])
    if cfg: return "cordova", cfg.parent
    pkg = shallow(fs, lambda p: p.name == "package.json")
    if pkg and '"react-native"' in rd(pkg): return "react-native", pkg.parent
    st = shallow(fs, lambda p: p.name in ("settings.gradle", "settings.gradle.kts"))
    if st and any("com.android.application" in rd(p) for p in st.parent.rglob("build.gradle*")): return "android", st.parent
    if shallow(fs, lambda p: p.name == "buildozer.spec") or any("kivy" in rd(p) for p in [p for p in fs if p.suffix == ".py"][:200]): return "kivy", None
    idx = shallow(fs, lambda p: p.name.lower() == "index.html")
    if idx: return "web", idx.parent
    return "unknown", None

def run(cmd, cwd, timeout=1500):
    print("$", " ".join(map(str, cmd)), flush=True)
    r = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, timeout=timeout)
    print(r.stdout[-6000:]); print(r.stderr[-6000:], file=sys.stderr)
    return r
def why(r):
    t = r.stderr + "\n" + r.stdout
    m = re.search(r"What went wrong:\s*(.{0,350})", t, re.S)
    return (m.group(1) if m else t.strip()[-350:]).strip() or "unknown error"

def gradle(proj):
    w = proj / "gradlew"
    if w.exists(): w.chmod(0o755); return ["./gradlew"]
    return ["gradle"]
# Speed: skip lint/tests, parallel workers + build cache; configuration cache only for our own template.
FAST_FLAGS = ["--no-daemon", "-q", "--parallel", "--build-cache", "-x", "lint", "-x", "test"]

def run_gradle(proj, template=False):
    (proj / "local.properties").write_text(f"sdk.dir={ANDROID_HOME}\n")
    last = None
    for task in ("assembleRelease", "assembleDebug"):
        extra = ["--configuration-cache"] if template else []
        r = run(gradle(proj) + [task] + FAST_FLAGS + extra, proj)
        apks = list(proj.rglob("build/outputs/apk/**/*.apk"))
        if r.returncode == 0 and apks: return sorted(apks, key=lambda p: ("universal" not in p.name, len(p.name)))[0]
        last = r
    fail("gradle build failed: " + why(last))

def rand_pkg():
    l = string.ascii_lowercase
    return "com.x" + "".join(secrets.choice(l) for _ in range(7)) + "." + secrets.choice(l) + "".join(secrets.choice(l + string.digits) for _ in range(5))

def web_project(web, name, work):
    pkg = rand_pkg(); proj = work / "proj"; shutil.copytree(HERE / "template", proj)
    pp = proj / "app/src/main/java" / pkg.replace(".", "/"); pp.parent.mkdir(parents=True, exist_ok=True)
    shutil.move(str(proj / "app/src/main/java/PKGPATH"), str(pp))
    for f in [proj / "app/build.gradle", pp / "MainActivity.java"]: f.write_text(f.read_text().replace("__PKG__", pkg))
    (proj / "app/src/main/res/values").mkdir(parents=True, exist_ok=True)
    n = html.escape(name).replace("'", "\\'").replace("@", "\\@").replace("?", "\\?")
    (proj / "app/src/main/res/values/strings.xml").write_text(f'<resources><string name="app_name">{n}</string></resources>', encoding="utf-8")
    shutil.copytree(web, proj / "app/src/main/assets/www")
    return proj

def npm_install(root):
    r = run(["npm", "ci" if (root / "package-lock.json").exists() else "install", "--no-audit", "--no-fund"], root)
    if r.returncode != 0: fail("npm install failed: " + why(r))

def build(kind, root, name, work):
    if kind == "web": return run_gradle(web_project(root, name, work), template=True)
    if kind == "android": return run_gradle(root)
    if kind == "flutter":
        r = run(["flutter", "build", "apk", "--release", "--target-platform", "android-arm,android-arm64" ], root)
        apk = root / "build/app/outputs/flutter-apk/app-release.apk"
        if r.returncode != 0 or not apk.exists(): fail("flutter build failed: " + why(r))
        return apk
    if kind == "react-native":
        if not (root / "android").exists(): fail("React Native project has no android/ folder (run 'npx expo prebuild' first)")
        npm_install(root); return run_gradle(root / "android")
    if kind == "capacitor":
        npm_install(root)
        if "build" in json.loads((root / "package.json").read_text()).get("scripts", {}): run(["npm", "run", "build"], root)
        if not (root / "android").exists():
            r = run(["npx", "cap", "add", "android"], root)
            if r.returncode != 0: fail("capacitor add android failed: " + why(r))
        r = run(["npx", "cap", "sync", "android"], root)
        if r.returncode != 0: fail("capacitor sync failed: " + why(r))
        return run_gradle(root / "android")
    if kind == "cordova":
        if (root / "package.json").exists(): npm_install(root)
        run(["npx", "--yes", "cordova@12", "platform", "add", "android"], root)
        r = run(["npx", "--yes", "cordova@12", "build", "android", "--release", "--", "--packageType=apk"], root)
        apks = list((root / "platforms/android").rglob("build/outputs/apk/**/*.apk"))
        if not apks: fail("cordova build failed: " + why(r))
        return apks[0]
    fail(ERR.get(kind, ERR["unknown"]))

def sign(apk, out):
    bt = sorted((Path(ANDROID_HOME) / "build-tools").iterdir())[-1]
    al = out.with_suffix(".aligned.apk")
    subprocess.run([str(bt / "zipalign"), "-f", "-p", "4", str(apk), str(al)], check=True)
    r = subprocess.run([str(bt / "apksigner"), "sign", "--ks", os.environ["KEYSTORE"], "--ks-key-alias", os.environ.get("KS_ALIAS", "srv"),
                        "--ks-pass", "env:KS_PASS", "--out", str(out), str(al)], capture_output=True, text=True)
    if r.returncode != 0: fail("signing failed: " + r.stderr[-200:])
    al.unlink(missing_ok=True)

def app_name(fn):
    n = re.sub(r"\.zip$", "", Path(fn or "app").name, flags=re.I)
    return re.sub(r"[_\-]+", " ", n).strip()[:40] or "Web App"

if __name__ == "__main__":
    if sys.argv[1] == "sign":
        sign(Path(sys.argv[2]), Path(sys.argv[3]).resolve()); print("signed"); sys.exit(0)
    if sys.argv[1] == "detect":
        zp, work = Path(sys.argv[2]), Path(sys.argv[3]); src = work / "src"; src.mkdir(parents=True, exist_ok=True)
        if not zipfile.is_zipfile(zp): fail("not a valid zip file")
        safe_extract(zp, src); kind, root = detect(src)
        (work / "root.txt").write_text(str(root or "")); (work / "kind.txt").write_text(kind)
        print(kind)
        if kind in ("kivy", "unknown"): fail(ERR[kind])
    else:
        work, name, out = Path(sys.argv[2]), sys.argv[3], Path(sys.argv[4])
        kind = (work / "kind.txt").read_text(); root = Path((work / "root.txt").read_text())
        apk = build(kind, root, app_name(name), work); shutil.copy(apk, out); print("OK (unsigned)", out)

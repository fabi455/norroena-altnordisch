# Norrœna – Altnordisch lernen ⚔️

Eine kostenlose deutschsprachige Offline-Lern-App für Altwestnordisch – mit **8 Lektionen**, **96 Vokabeleinträgen**, **32 Satzbeispielen**, Karteikarten, Quiz, Lernfortschritt und **127 synthetischen Hörbeispielen**.

> **Aussprache-Hinweis:** Die Tonbeispiele werden mit einer computergenerierten **modernen isländischen Stimme** erzeugt. Sie sind eine Annäherung für das Training, **keine authentische Rekonstruktion historischer altnordischer Aussprache**.

## 📱 Android-APK direkt herunterladen

1. [**Actions öffnen**](https://github.com/fabi455/norroena-altnordisch/actions/workflows/android-apk.yml).
2. **Android APK – Norroena** wählen. Ist kein erfolgreicher Durchlauf vorhanden, **Run workflow** anklicken (gegebenenfalls GitHub Actions für das Repository erlauben).
3. Den erfolgreichen Durchlauf öffnen; unter **Artifacts** **Norroena-Android-APK** herunterladen.
4. ZIP auf dem Smartphone entpacken, `app-debug.apk` antippen und die Installation von Apps aus dieser Quelle erlauben.

Die APK ist eine **Debug-Version** für persönliche Nutzung, keine signierte Play-Store-Release-Version. Sie läuft ab Android 7.0 (API 24), benötigt keine Netzwerkberechtigung und speichert den Lernfortschritt auf dem Gerät.

## 🌐 Web-App

Die Dateien `index.html`, `app.js`, `style.css` und `content.js` sind eine eigenständige Web-App ohne externe Frameworks. Für Tonbeispiele müssen Audios im Ordner `audio/` erzeugt werden. Über einen Webserver kann die Web-App genutzt werden; ein Service Worker hält bereits geladene Inhalte offline verfügbar. In der Android-App werden alle Audios mit eingebaut.

```bash
sudo apt-get install espeak ffmpeg
python3 tools/generate_audio.py
python3 -m http.server 8000
```

Danach im Browser `http://localhost:8000` öffnen.

## Aufbau

- `content.js`: Lernstoff und Satzbeispiele
- `app.js`: Lektionen, Quiz, Karteikarten und Lernfortschritt
- `style.css`: Gestaltung für Smartphone und Desktop
- `android/`: Android-WebView-App mit lokalen Assets
- `tools/generate_audio.py`: erzeugt aus dem Lernstoff die MP3-Dateien
- `.github/workflows/android-apk.yml`: baut und veröffentlicht die APK als GitHub-Actions-Artefakt

**Datenschutz:** keine Konten, kein Tracking, keine Werbung; Fortschritt wird lokal gespeichert.

Bei Änderung von `main` wird der Android-Build erneut gestartet. APK-Artifacts sind zeitlich begrenzt verfügbar; `Run workflow` erstellt bei Bedarf eine neue.

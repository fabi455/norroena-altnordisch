# Norrœna – Altnordisch lernen ⚔️

Eine kostenlose deutschsprachige Offline-Lern-App für Altwestnordisch – mit **8 Lektionen**, **96 Vokabeleinträgen**, **32 Satzbeispielen**, Karteikarten, Quiz, Lernfortschritt und **128 natürlich klingenden, synthetischen Hörbeispielen**.

> **Aussprache-Hinweis:** Die Tonbeispiele werden mit einer neuronalen **modernen isländischen Männerstimme Gunnar** erzeugt. Sie sind eine Annäherung für das Training, **keine authentische Rekonstruktion historischer altnordischer Aussprache**.

## 📱 Android-APK direkt herunterladen

1. [**Actions öffnen**](https://github.com/fabi455/norroena-altnordisch/actions/workflows/android-apk.yml).
2. **Android APK – Norroena** wählen. Ist kein erfolgreicher Durchlauf vorhanden, **Run workflow** anklicken (gegebenenfalls GitHub Actions für das Repository erlauben).
3. Den erfolgreichen Durchlauf öffnen; unter **Artifacts** **Norroena-1.1-Neural-APK** herunterladen.
4. ZIP auf dem Smartphone entpacken, `app-debug.apk` antippen und die Installation von Apps aus dieser Quelle erlauben.

Die APK ist eine **Debug-Version** für persönliche Nutzung, keine signierte Play-Store-Release-Version. Sie läuft ab Android 7.0 (API 24), benötigt keine Netzwerkberechtigung und speichert den Lernfortschritt auf dem Gerät.

## 🌐 Web-App

Die Dateien `index.html`, `app.js`, `style.css` und `content.js` sind eine eigenständige Web-App ohne externe Frameworks. Für Tonbeispiele müssen Audios im Ordner `audio/` erzeugt werden. Über einen Webserver kann die Web-App genutzt werden; ein Service Worker hält bereits geladene Inhalte offline verfügbar. In der Android-App werden alle Audios mit eingebaut.

```bash
python3 -m pip install edge-tts==7.3.1
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

## Version 1.1 – natürlicher klingende Hörbeispiele

Die bisherige eSpeak-Stimme wurde durch die isländische **Neuralstimme Gunnar** (`is-IS-GunnarNeural`) ersetzt. Alle 128 Wörter und Sätze erhalten neue synthetische MP3-Hörbeispiele. Beim Erstellen der App wird die Neuralstimme online abgefragt; danach sind sämtliche Audiodateien **offline in der Android-App** enthalten. Die Stimme klingt flüssiger und weniger mechanisch, spricht aber **modernes Isländisch**, nicht das historisch rekonstruierte Altnordisch. Die Clips eignen sich als Hörhilfe und enthalten möglicherweise Fehler bei alten Wortformen. Der Build bricht bei einer unerreichbaren Sprachsynthese ab, statt alte eSpeak-Aufnahmen zu übernehmen.

**Update-Hinweis:** Die APK ist für den Eigengebrauch mit einer Debug-Signatur signiert. Falls sich Version 1.1 nicht über Version 1.0 installieren lässt, vor dem Deinstallieren unter *Einstellungen → Sicherung exportieren* den Lernfortschritt sichern und anschließend in der neuen App importieren. Der Datenspeicherschlüssel `norroena-progress-v1` bleibt gleich.

# Norrœna 1.2 – Altnordisch lernen ⚔️

Eine kostenlose deutschsprachige Offline-Lern-App für **Altwestnordisch**. Mit **16 Lektionen**, **192 Vokabeln**, **64 Beispielsätzen**, adaptiven Lernrunden, Karteikarten, Quiz, Lernfortschritt und **255 verschiedenen Gunnar-Neural-MP3-Hörproben**. Zwei Übungen aus den ursprünglichen Lektionen teilen sich die identische Audio-ID; insgesamt sind es **256 Lernkarten**.

## Neu in Version 1.2

- **Acht zusätzliche Lektionen** zu Reisen & Richtungen, Tieren & Wildnis, Haus & Gegenständen, Essen & Trinken, Körper & Leben, Handlungen & Verben, Recht & Gemeinschaft sowie Göttern & Sagas.
- **„Mein Lernpfad“** empfiehlt automatisch die nächste passende Lektion.
- Mit **„Kann ich“** und **„Noch üben“** steuerst du die Wiederholung. Fehlende Quizkenntnisse werden ebenfalls in der Auswahl berücksichtigt; richtig gelernte Wörter kommen mit zunehmendem Abstand erneut.
- Pro Lernrunde werden bis zu zwölf gerade passende Wörter und Sätze ausgewählt.
- Über das **„Mehr“-Menü** in der unteren Android-Navigation erreichst du auch Aussprache, Fortschritt und Einstellungen.
- **Alle bisherigen Lektionen und Kennungen bleiben erhalten**, ebenso der Fortschrittsschlüssel `norroena-progress-v1`. Beim Import einer alten Sicherung werden neue Lernstatistiken ergänzt.

Die Auswertung erfolgt offline und ohne Konto. Der Lernpfad bewertet keine gesprochenen Aufnahmen, sondern nur Antworten und Selbsteinschätzungen.

## Hörproben

Die Android-App enthält nach erfolgreichem Build **255 synthetische MP3-Dateien** mit der modernen isländischen Neuralstimme **Gunnar** (`is-IS-GunnarNeural`). Die 127 alten Hörproben werden aus der geprüften Norrœna-1.1-APK übernommen, 128 neue mit derselben Stimme erzeugt.

**Aussprache-Hinweis:** Das ist eine natürlich klingende moderne isländische Aussprache-Annäherung, **keine authentische Rekonstruktion altnordischer Sprache zur Wikingerzeit**. Wörter mit historischen Lauten oder ungewöhnlichen Flexionsformen können abweichend ausgesprochen werden. Die Audio-Erzeugung läuft einmalig beim Build über einen externen Dienst; fertige Android-App und alle MP3s funktionieren offline.

## Android-APK herunterladen

1. [GitHub Actions für Norrœna öffnen](https://github.com/fabi455/norroena-altnordisch/actions/workflows/android-apk.yml).
2. Den erfolgreichen Lauf „**Norroena 1.2 – 16 Lektionen, adaptiv, Gunnar-Neural**“ öffnen.
3. Unter **Artifacts** `Norroena-1.2-Adaptiv-Gunnar-Android` herunterladen.
4. ZIP entpacken und die APK auf einem Android-Smartphone ab Android 7.0 installieren.

Der GitHub-Debug-APK-Build ist ein Test-Build, keine Play-Store-Version. Debug-APKs aus unterschiedlichen GitHub-Läufen können unterschiedliche Signaturzertifikate haben.

**Vor dem Update sichern:** In der bisher installierten App unter **Einstellungen → Sicherung exportieren** den Lernstand als JSON-Datei speichern. Wenn Android die neue APK wegen anderer Signatur nicht über die vorherige App installiert, nach der Sicherung die alte Installation entfernen, Norrœna 1.2 installieren und die JSON-Sicherung importieren. **Nicht deinstallieren, wenn keine Sicherung vorhanden ist und der Lernstand wichtig ist.**

## Inhalt, Sprachform und Quellen

Die Lektionen verwenden vereinfachte normalisierte **altwestnordische Schriftformen**. Die neu ergänzten Lernbeispiele sind zum Üben kurzer Satzmuster zusammengestellt und keine Zitate aus mittelalterlichen Originaltexten.

Sprachliche Orientierung:
- University of Texas at Austin: [Old Norse Online](https://lrc.la.utexas.edu/eieol_toc/norol)
- Universität Kopenhagen: [Dictionary of Old Norse Prose (ONP)](https://nors.ku.dk/english/research/arnamagnaean/a-dictionary-of-old-norse-prose/)

Altnordische Wortformen, Bedeutungsunterschiede und historisch korrekte Flexion sind komplex; die App ersetzt kein wissenschaftliches Wörterbuch.

## Eigenständig bauen

Voraussetzungen: Java 17, Android SDK 35, Gradle 8.9, Python 3.12 und Internetverbindung bei der Audio-Erzeugung.

```bash
python3 -m pip install edge-tts==7.3.1
python3 tools/generate_audio.py --part 0 --parts 1 --reused audio --output generated
# Generierte MP3-Dateien in den Ordner audio/ übernehmen
cd android && gradle --no-daemon :app:assembleDebug
```

Automatisch erzeugt die GitHub-Actions-Pipeline alle 128 neuen MP3s in 16 parallelen Gruppen und kombiniert sie mit den 127 ursprünglich geprüften Dateien. Sie verweigert einen unvollständigen Build.

## Struktur und Datenschutz

- `content.js` und `content.json`: 16 Lektionen mit 256 Karten (255 verschiedene MP3-IDs)
- `adaptive.js`: Wiederholungsplan, Schwierigkeitsgewichtung und Lernempfehlungen
- `app.js`, `style.css`, `index.html`: Offline-Oberfläche
- `tools/restore_gunnar.py`: Vorhandene Gunnar-Audiodateien mit ihrem Ursprungstext prüfen
- `tools/generate_audio.py`: Zusätzliche isländische Neural-Hörproben
- `android/` und `.github/workflows/android-apk.yml`: Android-Projekt und automatischer APK-Build

Kein Nutzerkonto, keine Werbung und keine Verfolgung. Der Lernfortschritt bleibt in `localStorage` auf dem Gerät.


# Tankpreise Hohenwutzen für Home Assistant

Benutzerdefinierte Integration, Version 1.0.1. Für die Tankstelle am **Polenmarkt Hohenwutzen**. Andere Tankstellen im Ort, insbesondere die separate SB Tank oder AB-Tankstellen, sind nicht enthalten.

## Installation

1. ZIP entpacken.
2. Den Ordner `custom_components/hohenwutzen_fuel` in das Konfigurationsverzeichnis von Home Assistant kopieren. Das Ergebnis muss `/config/custom_components/hohenwutzen_fuel/manifest.json` sein. Vorhandene andere Integrationen nicht überschreiben.
3. Home Assistant vollständig neu starten.
4. **Einstellungen → Geräte & Dienste → Integration hinzufügen → Tankpreise Hohenwutzen** öffnen und bestätigen. Falls die Integration nicht erscheint, die Browserseite vollständig neu laden.
5. Die drei Sensoren anschließend über **Dashboard bearbeiten → Karte hinzufügen → Entitäten** auswählen. Unter der Integration findest du ihre tatsächlichen Entitätsnamen. Eine YAML-Konfiguration ist nicht notwendig.

Kein API-Schlüssel, kein Konto und keine zusätzlichen Python-Pakete erforderlich. Die Integration wird manuell installiert; dieses ZIP ist kein bereits veröffentlichtes HACS-Repository.

## Enthaltene Sensoren

| Sensor | Einheit / Inhalt |
|---|---|
| Super E10 | EUR/L |
| Super Plus | EUR/L |
| Diesel | EUR/L |
| Letzter erfolgreicher Abruf | Zeitstempel, als Diagnoseentität |

Die erste Abfrage erfolgt bei der Einrichtung. Danach werden alle drei Preise gemeinsam alle **5 Minuten** abgerufen. Eine sofortige Aktualisierung ist über die Home-Assistant-Aktion `homeassistant.update_entity` für einen Preissensor möglich. Der normale Intervall lässt sich bei Bedarf in `const.py` über `UPDATE_MINUTES` ändern; anschließend neu starten.

## Datenquelle und Grenzen

Quelle: https://www.hohenwutzen.de/tanken/

Die Betreiberseite veröffentlicht Super, Plus und Diesel als tagesaktuelle Preise pro Liter in Euro. Die Sortenzuordnung Super E10 / Super Plus folgt den Angaben auf derselben Seite. Es handelt sich um Webseitenabfragen, nicht um einen offiziellen Live-API-Zugang. Der Abrufzeitpunkt gibt an, wann Home Assistant die Seite erfolgreich gelesen hat; er sagt nicht, wann der Betreiber den Preis geändert hat. Maßgeblich bleibt der Preis an der Zapfsäule.

Fehlen Preise oder schlägt eine Abfrage fehl, meldet die Integration die Sensoren als nicht verfügbar und versucht es bei folgenden Abfragen erneut. Bei einem Fehler beim ersten Start übernimmt Home Assistant die Einrichtungswiederholung. Es werden keine Beispielpreise oder Suchmaschinenwerte als aktuelle Preise eingesetzt.

Änderungen am Seitenaufbau können eine Anpassung von `parser.py` erfordern. Eine bereits bestehende gleichnamige Integration sollte vor dem Kopieren gesichert werden.

## Prüfstatus

Python-Syntax, JSON-Dateien und sechs Offline-Tests für Preisauswertung, HTML-Varianten und Fehlerfälle geprüft. Die Testdaten sind aus dem öffentlich abgerufenen Seitentext nachgebildet. Der direkte Abruf des Original-HTML war aus der Entwicklungsumgebung gesperrt. Deshalb sind weder die Verarbeitung des aktuellen Original-HTML noch der Betrieb in einer echten Home-Assistant-Instanz live verifiziert. Empfohlen ist eine aktuelle Home-Assistant-Core-Version; eine Mindestversion wurde nicht praktisch ermittelt.

Falls nach Installation keine Daten erscheinen: **Einstellungen → System → Protokolle** öffnen, nach `hohenwutzen_fuel` suchen und den Fehlertext zur Anpassung weitergeben.

Tests lokal: `python3 -m unittest discover -s tests -v`

## Entfernen

Integration unter Geräte & Dienste löschen. Anschließend bei Bedarf den Ordner `custom_components/hohenwutzen_fuel` entfernen und Home Assistant neu starten.

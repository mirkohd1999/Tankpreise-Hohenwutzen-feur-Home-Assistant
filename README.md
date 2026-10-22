# ⛽ Tankpreise Hohenwutzen für Home Assistant

Eine benutzerdefinierte Home-Assistant-Integration für die Kraftstoffpreise der Tankstelle am Polenmarkt Hohenwutzen.

Die Integration liest die veröffentlichten Preise von hohenwutzen.de aus und fragt sie automatisch alle 5 Minuten ab.

## Funktionen

- Einzelne Sensoren für Super E10, Super Plus und Diesel in EUR/L
- Zusätzlicher Sensor für den letzten erfolgreichen Abruf
- Einrichtung über die Home-Assistant-Oberfläche
- Kein API-Schlüssel erforderlich
- Sensoren für Dashboards und eigene Automationen nutzbar
- Kein Konto und keine zusätzlichen Python-Pakete erforderlich.

| Sensor | Einheit / Inhalt |
|---|---|
| Super E10 | EUR/L |
| Super Plus | EUR/L |
| Diesel | EUR/L |
| Letzter erfolgreicher Abruf | Zeitstempel, als Diagnoseentität |

## Installation über HACS

1. In HACS das Menü **Benutzerdefinierte Repositories** öffnen.
2. Als Repository `https://github.com/mirkohd1999/Tankpreise-Hohenwutzen-feur-Home-Assistant` eintragen und als Typ **Integration** auswählen.
3. **Tankpreise Hohenwutzen** suchen und herunterladen. Ohne veröffentlichte Releases die aktuelle Standardbranch `main` auswählen.
4. Home Assistant neu starten.
5. Unter **Einstellungen → Geräte & Dienste → Integration hinzufügen** nach **Tankpreise Hohenwutzen** suchen und bestätigen.

Bei einer früheren HACS-Fehlermeldung die Repository-Informationen in HACS erneut laden und den aktuellen Stand herunterladen. Der alte Commit `26771f6` enthält noch keine HACS-Metadaten.

## Manuelle Installation

1. Repository herunterladen und entpacken.
2. Den Ordner custom_components/hohenwutzen_fuel nach /config/custom_components/ kopieren.
3. Home Assistant neu starten.
4. Unter Einstellungen → Geräte & Dienste → Integration hinzufügen nach Tankpreise Hohenwutzen suchen.
5. Einrichtung bestätigen und die Sensoren zum Dashboard hinzufügen.

## Datenquelle

Die Preise stammen von der Betreiberseite des Polenmarkts Hohenwutzen. Ein Abruf alle fünf Minuten bedeutet nicht, dass der Betreiber die Preise ebenso häufig aktualisiert. Maßgeblich ist der Preis an der Zapfsäule.

Bei Abruf- oder Auswertungsfehlern werden die Sensoren als nicht verfügbar angezeigt. Änderungen am Aufbau der Quellseite können eine Anpassung der Integration erfordern.

## Entwicklungsstand

Version 1.0.2 – experimentell.

Sechs Offline-Tests für die Preisauswertung bestanden. Der Live-Abruf und der Betrieb in einer echten Home-Assistant-Instanz sind noch nicht verifiziert. Die Repository-Metadaten sind für die Installation als benutzerdefiniertes HACS-Repository vorbereitet. Ein Installationstest in HACS steht noch aus.

Dieses Projekt ist eine unabhängige Community-Entwicklung und steht in keiner offiziellen Verbindung zum Tankstellenbetreiber.

Fehlerberichte und Verbesserungsvorschläge sind über GitHub Issues willkommen.

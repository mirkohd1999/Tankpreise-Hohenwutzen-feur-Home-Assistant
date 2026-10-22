# ⛽ Tankpreise Hohenwutzen für Home Assistant

Eine benutzerdefinierte Home-Assistant-Integration für die Kraftstoffpreise der Tankstelle am Polenmarkt Hohenwutzen.

Die Integration liest die veröffentlichten Preise von hohenwutzen.de aus und fragt sie automatisch alle 5 Minuten ab.

## Funktionen

- Einzelne Sensoren für Super E10, Super Plus und Diesel in EUR/L
- Zusätzlicher Sensor für den letzten erfolgreichen Abruf
- Einrichtung über die Home-Assistant-Oberfläche
- Kein API-Schlüssel erforderlich
- Sensoren für Dashboards und eigene Automationen nutzbar
- Kein API-Schlüssel, kein Konto und keine zusätzlichen Python-Pakete erforderlich. Die Integration wird manuell installiert; dieses ZIP ist kein bereits veröffentlichtes HACS-Repository.

| Sensor | Einheit / Inhalt |
|---|---|
| Super E10 | EUR/L |
| Super Plus | EUR/L |
| Diesel | EUR/L |
| Letzter erfolgreicher Abruf | Zeitstempel, als Diagnoseentität |

## Installation

1. Repository herunterladen und entpacken.
2. Den Ordner custom_components/hohenwutzen_fuel nach /config/custom_components/ kopieren.
3. Home Assistant neu starten.
4. Unter Einstellungen → Geräte & Dienste → Integration hinzufügen nach Tankpreise Hohenwutzen suchen.
5. Einrichtung bestätigen und die Sensoren zum Dashboard hinzufügen.

## Datenquelle

Die Preise stammen von der Betreiberseite des Polenmarkts Hohenwutzen. Ein Abruf alle fünf Minuten bedeutet nicht, dass der Betreiber die Preise ebenso häufig aktualisiert. Maßgeblich ist der Preis an der Zapfsäule.

Bei Abruf- oder Auswertungsfehlern werden die Sensoren als nicht verfügbar angezeigt. Änderungen am Aufbau der Quellseite können eine Anpassung der Integration erfordern.

## Entwicklungsstand

Version 1.0.1 – experimentell.

Sechs Offline-Tests für die Preisauswertung bestanden. Der Live-Abruf und der Betrieb in einer echten Home-Assistant-Instanz sind noch nicht verifiziert. Eine HACS-Installation wird derzeit nicht angeboten.

Dieses Projekt ist eine unabhängige Community-Entwicklung und steht in keiner offiziellen Verbindung zum Tankstellenbetreiber.

Fehlerberichte und Verbesserungsvorschläge sind über GitHub Issues willkommen.

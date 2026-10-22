# ⛽ Tankpreise Hohenwutzen für Home Assistant

Die Kraftstoffpreise der Tankstelle am **Polenmarkt Hohenwutzen** direkt in Home Assistant – automatisch alle **5 Minuten**, wahlweise in **Euro oder Złoty**.

**Ab Home Assistant 2025.12.0 · Einrichtung über die Oberfläche · Kein Konto oder API-Schlüssel nötig**

## Funktionen

| Entität | Anzeige |
|---|---|
| Super E10 | EUR/L oder PLN/L |
| Super Plus | EUR/L oder PLN/L |
| Diesel | EUR/L oder PLN/L |
| Tankstelle | Geöffnet / Geschlossen, Symbol `mdi:store` |
| Letzter erfolgreicher Abruf | Zeitstempel als Diagnoseentität |

Alle Sensoren lassen sich in Dashboards und Automationen verwenden. Zusätzliche Python-Pakete sind nicht erforderlich.

## Installation

### Über HACS

1. In HACS **Benutzerdefinierte Repositories** öffnen.
2. Diese Adresse mit dem Typ **Integration** hinzufügen:

   ```text
   https://github.com/mirkohd1999/Tankpreise-Hohenwutzen-feur-Home-Assistant
   ```

3. **Tankpreise Hohenwutzen** suchen und die neueste veröffentlichte Version herunterladen.
4. Home Assistant neu starten.
5. Unter **Einstellungen → Geräte & Dienste → Integration hinzufügen** nach **Tankpreise Hohenwutzen** suchen und das gewünschte Profil wählen.

### Manuell

Den Ordner `custom_components/hohenwutzen_fuel` aus dem Repository nach `/config/custom_components/` kopieren. Anschließend Home Assistant neu starten und die Integration wie oben hinzufügen.

**Updates:** In HACS aktualisieren und Home Assistant neu starten.

## Sprache und Währung

Ab Version **1.1.0** stehen zwei Profile zur Auswahl:

| Profil | Sensornamen | Preise |
|---|---|---|
| Deutsch → Euro (€) | Deutsch | Originalpreise in EUR/L |
| Polski → Złoty (zł) | Polnisch | Umgerechnete Preise in PLN/L |

**Umstellen:** Einstellungen → Geräte & Dienste → Tankpreise Hohenwutzen → **Konfigurieren**. Nach dem Speichern lädt die Integration automatisch neu. Bestehende Installationen bleiben zunächst bei Deutsch/Euro.

EUR und PLN verwenden getrennte Preisentitäten, damit ihre Verläufe nicht vermischt werden. Nach einem Wechsel die neuen Sensoren im Dashboard und in Automationen auswählen. Alte Preisentitäten können als nicht verfügbar bestehen bleiben; beim Zurückwechseln auf EUR werden die bisherigen Sensoren wiederverwendet.

Die Sprache der Home-Assistant-Oberfläche und von **Geöffnet/Geschlossen** folgt weiterhin dem persönlichen Benutzerprofil. Einrichtungsdialoge sind auf Deutsch, Polnisch und Englisch verfügbar.

### Automatische PLN-Umrechnung

**PLN-Preis = Europreis × PLN pro EUR**, gerundet auf zwei Dezimalstellen.

Der Referenzkurs stammt aus Tabelle A der [polnischen Nationalbank NBP](https://api.nbp.pl/en.html). Im PLN-Profil wird er stündlich abgerufen; die Kraftstoffpreise weiterhin alle fünf Minuten. Es gilt der zuletzt veröffentlichte Kurs, der an Wochenenden und Feiertagen älter sein kann.

> PLN-Werte sind umgerechnete Vergleichspreise. Sie entsprechen nicht zwingend dem Złoty-Zahlpreis oder Umrechnungskurs der Tankstelle.

Die Sensorattribute enthalten Originalpreis, Wechselkurs, Kursdatum, Quelle und `converted: true`. Scheitert die Kursabfrage, sind nur die PLN-Preise nicht verfügbar; der nächste Versuch erfolgt nach fünf Minuten. Im EUR-Profil wird kein Wechselkurs abgefragt.

## Datenquelle und Öffnungsstatus

Preise und Öffnungsangaben stammen von [hohenwutzen.de](https://www.hohenwutzen.de/tanken/). Die Abfrage alle fünf Minuten bedeutet nicht, dass der Betreiber seine Angaben ebenso häufig aktualisiert. **Maßgeblich ist der Preis an der Zapfsäule.**

Der Öffnungssensor wertet ausschließlich eindeutige Angaben im Abschnitt **Tankstelle** aus: `24/7 geöffnet` ergibt **Geöffnet**, eine ausdrückliche Schließungsangabe hat Vorrang. Öffnungszeiten des Polenmarkts oder Shops werden nicht übernommen.

Der Status beruht auf der Webseite; dort nicht veröffentlichte kurzfristige Schließungen sind nicht erkennbar. Fehlende oder widersprüchliche Angaben führen zu **nicht verfügbar**. Bei einem Fehler der Preisabfrage werden die zugehörigen Entitäten ebenfalls nicht verfügbar. Änderungen am Seitenaufbau können Anpassungen erfordern.

## Projektstatus und Hilfe

**Version 1.1.0:** HACS Validation, Hassfest und 30 Offline-Tests für die Erweiterung bestanden. Der Betrieb und die Profilumstellung in Home Assistant wurden vom Nutzer als funktionierend zurückgemeldet; eine umfassende Prüfung verschiedener Installationen steht aus.

Fehler oder Ideen? Bitte ein [GitHub Issue](https://github.com/mirkohd1999/Tankpreise-Hohenwutzen-feur-Home-Assistant/issues) erstellen.

Unabhängiges Community-Projekt ohne offizielle Verbindung zum Tankstellenbetreiber. Veröffentlicht unter der [MIT-Lizenz](LICENSE).

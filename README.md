# ⛽ Tankpreise Hohenwutzen für Home Assistant

[![Version](https://img.shields.io/github/v/release/mirkohd1999/Tankpreise-Hohenwutzen-feur-Home-Assistant?label=Version&color=orange)](https://github.com/mirkohd1999/Tankpreise-Hohenwutzen-feur-Home-Assistant/releases/latest)
[![Lizenz: MIT](https://img.shields.io/github/license/mirkohd1999/Tankpreise-Hohenwutzen-feur-Home-Assistant?label=Lizenz&color=green)](LICENSE)
[![Home Assistant](https://img.shields.io/badge/Home_Assistant-2025.12.0%2B-41BDF5)](https://www.home-assistant.io/)

**Die Tankpreise vom Polenmarkt Hohenwutzen direkt auf deinem Dashboard.**

Super E10, Super Plus und Diesel im Blick behalten, den veröffentlichten Öffnungsstatus anzeigen und Preise für eigene Automationen nutzen. Die Integration ruft die Betreiber-Webseite automatisch alle **5 Minuten** ab. Sensornamen und Währung wählst du unabhängig voneinander: **Deutsch, Polski oder English** mit **Euro oder Złoty**.

[![Open HACS Repository on My Home Assistant](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=mirkohd1999&repository=Tankpreise-Hohenwutzen-feur-Home-Assistant&category=integration)

*Kein Konto, kein API-Schlüssel und keine zusätzlichen Python-Pakete erforderlich.*

## Inhalt

- [Funktionen](#funktionen)
- [Installation](#installation)
- [Sprache und Währung](#sprache-und-währung)
- [Datenquelle und Öffnungsstatus](#datenquelle-und-öffnungsstatus)
- [Hilfe und Projektstatus](#hilfe-und-projektstatus)

## Funktionen

| Sensor | Anzeige |
|---|---|
| Super E10 | Preis in EUR/L oder PLN/L |
| Super Plus | Preis in EUR/L oder PLN/L |
| Diesel | Preis in EUR/L oder PLN/L |
| Tankstelle | Geöffnet / Geschlossen mit `mdi:store` |
| Letzter erfolgreicher Abruf | Zeitstempel als Diagnoseentität |

Alle Entitäten lassen sich in Dashboards und Automationen verwenden.

## Installation

**Voraussetzung:** Home Assistant **2025.12.0 oder neuer**. Für die folgenden HACS-Wege muss HACS bereits installiert sein.

### Direkt über HACS

1. Auf den **Open HACS Repository**-Button oben klicken oder in HACS nach **Tankpreise Hohenwutzen** suchen.
2. Die neueste veröffentlichte Version herunterladen.
3. Home Assistant neu starten.
4. Unter **Einstellungen → Geräte & Dienste → Integration hinzufügen** nach **Tankpreise Hohenwutzen** suchen.
5. Sprache und Währung auswählen und die Einrichtung abschließen.

### Alternative: Benutzerdefinierte Repositories

Falls die Integration in deiner HACS-Suche noch nicht erscheint:

1. **HACS** öffnen und im Menü **⋮ → Benutzerdefinierte Repositories** auswählen.
2. Diese Repository-Adresse eintragen:

   ```text
   https://github.com/mirkohd1999/Tankpreise-Hohenwutzen-feur-Home-Assistant
   ```

3. Als Typ **Integration** auswählen und das Repository hinzufügen.
4. Nach **Tankpreise Hohenwutzen** suchen und die neueste veröffentlichte Version herunterladen.
5. Home Assistant neu starten.
6. Unter **Einstellungen → Geräte & Dienste → Integration hinzufügen** die Integration einrichten.

### Manuell ohne HACS

1. Den Quellcode der [neuesten Veröffentlichung](https://github.com/mirkohd1999/Tankpreise-Hohenwutzen-feur-Home-Assistant/releases/latest) herunterladen und entpacken.
2. Den Ordner `custom_components/hohenwutzen_fuel` nach `/config/custom_components/` kopieren.
3. Home Assistant neu starten und die Integration unter **Geräte & Dienste** hinzufügen.

**Updates:** Über HACS aktualisieren und Home Assistant neu starten. Bei manueller Installation den Integrationsordner durch die neue Version ersetzen und anschließend neu starten.

## Sprache und Währung

| Einstellung | Auswahl |
|---|---|
| Sprache der Sensoren | Deutsch / Polski / English |
| Preiswährung | Euro (EUR/L) / Złoty (PLN/L) |

Alle **sechs Kombinationen** sind möglich – zum Beispiel deutsche Sensornamen mit Złoty-Preisen.

**Ändern:** Einstellungen → Geräte & Dienste → Tankpreise Hohenwutzen → **Konfigurieren**. Nach dem Speichern lädt die Integration automatisch neu. Bisherige Einstellungen werden übernommen; ein reiner Sprachwechsel behält dieselben Entitäten und Preisverläufe.

Beim **Währungswechsel** die passenden Preisentitäten im Dashboard und in Automationen auswählen. EUR und PLN verwenden getrennte Entitäten, damit ihre Verläufe nicht vermischt werden. Alte Entitäten können als nicht verfügbar bestehen bleiben; beim Zurückwechseln auf EUR werden die bisherigen Sensoren wiederverwendet.

Die Sprache der Home-Assistant-Oberfläche und von **Geöffnet/Geschlossen** folgt deinem persönlichen Benutzerprofil. Einrichtungsdialoge sind auf Deutsch, Polnisch und Englisch verfügbar.

### Umrechnung in Złoty

**PLN-Preis = Europreis × PLN pro EUR**, gerundet auf zwei Dezimalstellen.

Der Referenzkurs stammt aus Tabelle A der [polnischen Nationalbank NBP](https://api.nbp.pl/en.html). Im PLN-Modus wird er stündlich abgerufen; Kraftstoffpreise weiterhin alle fünf Minuten. An Wochenenden und Feiertagen kann der zuletzt veröffentlichte Kurs älter sein.

> PLN-Werte sind rechnerische Vergleichspreise. Sie entsprechen nicht zwingend dem Złoty-Zahlpreis oder Umrechnungskurs der Tankstelle.

Sensorattribute zeigen Originalpreis, Wechselkurs, Kursdatum, Quelle und `converted: true`. Scheitert die Kursabfrage, sind nur die PLN-Preise nicht verfügbar; ein erneuter Versuch folgt nach fünf Minuten. Im EUR-Modus erfolgt kein NBP-Abruf.

## Datenquelle und Öffnungsstatus

Die Angaben stammen von [hohenwutzen.de](https://www.hohenwutzen.de/tanken/). Die Abfrage alle fünf Minuten bedeutet nicht, dass der Betreiber seine Angaben ebenso häufig aktualisiert. **Maßgeblich ist der Preis an der Zapfsäule.**

Der Öffnungssensor berücksichtigt eindeutige Angaben im Abschnitt **Tankstelle**: `24/7 geöffnet` ergibt **Geöffnet**, eine ausdrückliche Schließungsangabe hat Vorrang. Öffnungszeiten von Polenmarkt oder Shop werden nicht übernommen.

Kurzfristige Schließungen sind nur erkennbar, wenn sie auf der Webseite stehen. Fehlende oder widersprüchliche Angaben führen zu **nicht verfügbar**. Bei Fehlern der Preisabfrage werden auch die zugehörigen Entitäten nicht verfügbar. Änderungen am Seitenaufbau können Anpassungen erfordern.

## Hilfe und Projektstatus

HACS Validation, Hassfest und **35 Offline-Tests** für Version 1.3.0 bestanden. Die Tests decken alle sechs Sprach-/Währungskombinationen ab. Der erfolgreiche Betrieb in Home Assistant wurde vom Nutzer bestätigt; dies ist keine umfassende Prüfung aller Installationsvarianten.

Fehler gefunden oder eine Idee? Erstelle ein [GitHub Issue](https://github.com/mirkohd1999/Tankpreise-Hohenwutzen-feur-Home-Assistant/issues) und beschreibe dein Anliegen.

---

Unabhängiges Community-Projekt ohne offizielle Verbindung zum Tankstellenbetreiber. Veröffentlicht unter der [MIT-Lizenz](LICENSE).

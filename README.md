# ⛽ Tankpreise Hohenwutzen für Home Assistant

Eine benutzerdefinierte Home-Assistant-Integration für die Kraftstoffpreise der Tankstelle am Polenmarkt Hohenwutzen.

Die Integration liest die veröffentlichten Preise von hohenwutzen.de aus und fragt sie automatisch alle 5 Minuten ab.

## Funktionen

- Einzelne Sensoren für Super E10, Super Plus und Diesel in EUR/L
- Binärer Sensor für die Tankstelle: geöffnet oder geschlossen laut Betreiber-Webseite
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
| Tankstelle (binärer Sensor) | Geöffnet / Geschlossen laut Betreiber-Webseite |

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

Version 1.1.0 – experimentell.

30 Offline-Tests für Preise, Öffnungsstatus, Anzeigeprofile, Kursumrechnung und Kursabrufe bestanden. Der Live-Abruf und der Betrieb in einer echten Home-Assistant-Instanz sind noch nicht verifiziert. Die Repository-Metadaten sind für die Installation als benutzerdefiniertes HACS-Repository vorbereitet. Ein Installationstest in HACS steht noch aus.

Dieses Projekt ist eine unabhängige Community-Entwicklung und steht in keiner offiziellen Verbindung zum Tankstellenbetreiber.

Fehlerberichte und Verbesserungsvorschläge sind über GitHub Issues willkommen.

## Öffnungsstatus der Tankstelle

Ab Version 1.0.3 gibt es zusätzlich einen binären Sensor **Tankstelle** mit der Geräteklasse `opening`. Home Assistant zeigt ihn als **Geöffnet** (`on`) oder **Geschlossen** (`off`) an. Er gehört zum bestehenden Gerät und wird zusammen mit den Preisen alle fünf Minuten aktualisiert, ohne zusätzlichen HTTP-Abruf. Nach einem Update Home Assistant neu starten; danach erscheint die neue Entität automatisch.

Ausgewertet wird nur der Abschnitt **Tankstelle** auf der Betreiberseite. Aktuell nennt dieser `24/7 geöffnet`; daraus folgt **Geöffnet**. Eine dort veröffentlichte ausdrückliche Angabe `geschlossen` hat Vorrang vor den regulären Öffnungszeiten. Die Öffnungszeiten des Polenmarkts oder die Erwähnung eines 24h-Shops werden nicht als Tankstellenstatus übernommen.

Der Sensor zeigt **keinen direkt gemessenen Live-Betriebsstatus**. Kurzfristige Schließungen, die nicht auf der Seite stehen, sind nicht erkennbar. Fehlen eindeutige Angaben, werden widersprüchliche Angaben erkannt oder misslingt der Abruf, ist der Status **nicht verfügbar** statt fälschlich „Geschlossen“. Andere Zeitpläne als die ausdrücklich erkannten Angaben werden nicht geraten. Die vorhandene Preisabfrage muss weiterhin erfolgreich sein.

Prüfung der Erweiterung: Offline-Tests für Öffnung, Schließung, unbekannte und widersprüchliche Angaben sowie die vorhandenen Preistests. Kein Live-Test in Home Assistant.

Der binäre Sensor **Tankstelle** verwendet das Ladensymbol `mdi:store` für beide Zustände. Die Anzeige **Geöffnet/Geschlossen** bleibt erhalten. Die Symbolfarbe bestimmt das Home-Assistant-Theme bzw. die Dashboard-Karte.

## Lizenz

Dieses Projekt steht unter der [MIT-Lizenz](LICENSE).

## Automatische Prüfungen

Der Workflow **Validate** führt HACS Validation ohne deaktivierte Prüfungen, Hassfest und die Offline-Tests bei Pushes und Pull Requests aus. Die Aufnahme in den offiziellen HACS-Katalog ist erst nach erfolgreichen Prüfungen, einem anschließenden Release und der Freigabe durch das HACS-Team abgeschlossen. Bis dahin wird das Repository als benutzerdefiniertes Repository hinzugefügt.

## Deutsch / Euro oder Polski / Złoty

Ab Version 1.1.0 wird bei der Einrichtung das Profil gewählt:

| Auswahl | Sensornamen | Preise |
|---|---|---|
| Deutsch → Euro (€) | Deutsch | EUR/L, Originalpreis der Betreiberseite |
| Polski → Złoty (zł) | Polnisch | PLN/L, aus dem Europreis umgerechnet |

Bestehende Installationen bleiben automatisch bei Deutsch / EUR. Unter **Einstellungen → Geräte & Dienste → Tankpreise Hohenwutzen → Konfigurieren** kann das Profil geändert werden. Die Integration lädt sich danach neu; sie muss nicht gelöscht werden. Die Sprache der Home-Assistant-Oberfläche und die Übersetzung von Geöffnet/Geschlossen richten sich weiterhin nach der Sprache im persönlichen Home-Assistant-Profil. Für die Einrichtungs- und Optionsdialoge sind Deutsch, Polnisch und Englisch enthalten.

Der PLN-Wert berechnet sich aus **Europreis × PLN pro EUR**. Der Referenzkurs kommt aus Tabelle A der [polnischen Nationalbank NBP](https://api.nbp.pl/en.html) und wird bei gewähltem PLN-Profil stündlich abgerufen; die Kraftstoffpreise werden weiterhin alle fünf Minuten aktualisiert. Die NBP liefert den zuletzt veröffentlichten Kurs, keinen Echtzeit-Devisenkurs. Insbesondere an Wochenenden oder Feiertagen kann das Kursdatum älter sein. PLN/L wird auf zwei Dezimalstellen gerundet.

In den Attributen der PLN-Preissensoren stehen `original_price_eur`, `pln_per_eur`, `exchange_rate_date`, `exchange_rate_source` und `converted: true`. Es handelt sich um einen rechnerischen Vergleichswert, nicht um einen von der Tankstelle veröffentlichten Złoty-Zahlpreis oder deren eigenen Umrechnungskurs.

Kann der NBP-Kurs beim ersten Abruf oder der nächsten stündlichen Aktualisierung nicht geladen werden, werden nur die PLN-Preise nicht verfügbar. Es gibt keinen erfundenen Ersatzkurs und keinen stillen Rückfall auf EUR. Öffnungsstatus und Zeitstempel bleiben bei erfolgreichem Webseitenabruf nutzbar; der Kursabruf wird bei der nächsten Fünf-Minuten-Abfrage erneut versucht. Im EUR-Profil erfolgt kein NBP-Abruf.

PLN-Preissensoren erhalten eigene eindeutige IDs mit dem Suffix `_pln`. Die bisherigen EUR-IDs bleiben erhalten. Nach einem Währungswechsel müssen die neuen Preissensoren einmal im Dashboard bzw. in Automationen ausgewählt werden; die bisherigen Preisentitäten können als nicht verfügbar bestehen bleiben. Beim Zurückwechseln auf EUR werden die ursprünglichen Sensoren wiederverwendet. Dadurch werden die Preisverläufe unterschiedlicher Währungen nicht vermischt.

Für Version 1.1.0 wird Home Assistant ab 2025.12.0 benötigt (OptionsFlowWithReload). Der Betrieb in einer echten Home-Assistant-Instanz bleibt noch praktisch zu prüfen.

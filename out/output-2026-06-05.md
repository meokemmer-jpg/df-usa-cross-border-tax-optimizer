# df-usa-cross-border-tax-optimizer — Output [CRUX-MK]
*Autonom aktiviert 2026-06-05T17:22:25.087575+00:00 | ollama-local/qwen2.5:14b-instruct*

# DF-USA-Cross-Border-Tax-Optimizer [CRUX-MK]

## Mission: USA-Markt-Expansion

### Dokumentierte Spezifikation:

**Ziel:** Entwicklung eines Mock-Calculators zur Berechnung der Steuerfolge
Steuerfolgen im Rahmen des Deutschland-USA Doppelbesteuerungsabkommens (DBA
(DBA) und der US-Sekundären Steuerregel 883 Carve-Out für Hoteloperationen.
Hoteloperationen. Der Fokus liegt auf der Wegzugssteuer- und Quellensteuero
Quellensteueroptimierung.

### Technische Stack-Begründung:

- **Steuer-DBA:** Deutschland-USA DBA, insbesondere Artikel 7 (Einkommen au
aus Vermögenswerten), 10 (Dividenden) und 12 (Zinsen).
- **Sec-883-Carve-Out:** Spezielle Vereinbarungen für US-Hotelbetriebe unte
unter Berücksichtigung der Cape Coral E2 Visa Regelung.
- **K_0:** Erste Kompilierung zur Wegzugssteuer und Quellensteueroptimierun
Quellensteueroptimierung ohne realen Steuerrechner, nur Modell-Berechnungs-
Modell-Berechnungs-Estimates.
- **Sandbox-Default:** Keine Realzeit-Tax-Kalkulation, sondern strukturiert
strukturierte Modellestimates.
- **Anwalt-API-Stub:** Nicht-LLM Validierungs-Schicht zur späteren Integrat
Integration mit LexVance.

### CRUX-Bindung:

- **K_0:** Direkte Verarbeitung von Steuerfragen (Wegzugssteuer, Sec-883, Q
Quellensteuer).
- **Q_0:** Familien-Vermögens-Stabilität durch klare und präzise Steuerverw
Steuerverwaltung.
- **I_min:** Bereitstellung einer tax-calculating Struktur basierend auf de
den DBA Artikel 7/10/12.
- **W_0:** Vermeidung von Fehlentwicklungen durch die Nutzung eines Mock-De
Mock-Defaults.

### Datenklassen und Umgebungsvariablen:

Die DF verwendet eine Dataclass `TaxQuery` um Steueranfragen zu strukturier
strukturieren, einschließlich Feldern wie `query_id`, `query_type`, `locati
`location_preference`, `duration_nights`, und anderen relevante Information
Informationen. Die Umgebungsvariablen `DF_103_REAL_BOOKING_ENABLED`, `DF_10
`DF_103_REAL_LLM_ENABLED` und `PHRONESIS_TICKET` werden zur Kontrolle der r
realen Buchungsfunktionalität und LLM-Validierung verwendet.

### Mock-Kalkulationsbeispiel:

Eine Beispiel-Berechnung könnte folgendermaßen strukturiert sein:
```python
class TaxQuery:
    def __init__(self, query_id: str, query_type: QueryType, location_prefe
location_preference: Optional[str], duration_nights: int):
        self.query_id = query_id
        self.query_type = query_type
        self.location_preference = location_preference
        self.duration_nights = duration_nights

# Beispiel-Aufruf
tax_query = TaxQuery(query_id="12345", query_type=QueryType.INCOME, locatio
location_preference=None, duration_nights=7)
```

Diese Klasse ermöglicht es uns, Steueranfragen zu standardisieren und die B
Berechnung von Steuerfolgen basierend auf dem DBA-Artikel 7/10/12 durchzufü
durchzuführen. Der Fokus liegt darauf, sicherzustellen, dass jede Anfrage k
korrekt interpretiert wird, um falsche Steuervorstellungen zu vermeiden.

### Kompilierung und Tests:

- **Kompilation:** Der Prozess basiert auf der Dokumentation des aktuellen 
Codezustands durch AST-Evidenz.
- **Tests:** 10 Iterationen zur Erkennung von Backbone-Orchestration, Attri
Attribution, Identity, Operations, Data-Quality, Resilience und mehr.

### Zusammenfassung:

Die Dark Factory `df-usa-cross-border-tax-optimizer` entwickelt einen Mock-
Mock-Steuerrechner, der die DBA Artikel 7/10/12 sowie die Sec-883 Carve-Out
Carve-Outs für US-Hoteloperationen berücksichtigt. Der Schwerpunkt liegt au
auf der Wegzugssteuer und Quellensteueroptimierung mit einer späteren Integ
Integration zur Nicht-LLM Validierung via LexVance.

Diese Initiative trägt direkt zur Steuerfolgen-Planung bei, welche eine ent
entscheidende Rolle für die familienweite Vermögensstabilität spielt.
# 📌 Empfehlung zur Vorgangsreferenz in XIMA Formcycle Workflows (`HWG-WF-02`)

> **Dokumenttyp:** Technische & verwaltungsfachliche Empfehlung  
> **Kontext:** XIMA Formcycle Governance-Standard (HWG Ludwigshafen) – Regel `HWG-WF-02`  
> **Erstellt am:** 30.10.2026  

---

## 1. Ausgangslage & Problemstellung

Die Governance-Regel **`HWG-WF-02`** fordert für automatisierte Workflow-E-Mails (z. B. Eingangsbestätigungen via `FC_EMAIL`) eine eindeutige Vorgangsreferenz in Betreff oder Textkörper, um Nachvollziehbarkeit und Auffindbarkeit nach DIN EN ISO 9241-110 (Erwartungskonformität und Aufgabenangemessenheit) sicherzustellen.

In bestehenden Formular-Workflows und Dokumentationen taucht häufig der Platzhalter **`[%$PROJECT_ALIAS%]`** auf. Es stellt sich die verwaltungsfachliche Frage:
> **Sollte in der Remediation weiterhin `[%$PROJECT_ALIAS%]` empfohlen werden, oder ausschließlich `[%$RECORD_ID%]` bzw. `[%$ID%]`?**

---

## 2. Technischer Unterschied der Platzhalter in XIMA Formcycle

| Platzhalter | Typ | Bedeutung in Formcycle | Eignung als Fallnummer |
| :--- | :--- | :--- | :--- |
| **`[%$PROJECT_ALIAS%]`** | Statisch | Der systemweite **Projekt-Alias / Formularname** (z. B. `antrag_sprints`, `form_20952_2`, `auslagenerstattung`). | ❌ **Nein.** Alle Einreichungen desselben Formulars erhalten exakt denselben String. |
| **`[%$RECORD_ID%]`** bzw. **`[%$ID%]`** | Dynamisch | Die fortlaufende, **eindeutige Datensatz-ID** in der Formcycle-Datenbank (z. B. `1042`, `1043`). |  **Ja.** Jede einzelne Antragsabsendung erhält eine unverwechselbare Ticketnummer. |
| **`[%$UUID%]`** | Dynamisch | Globale 36-stellige UUID des Vorgangs. | ⚠️ Technisch eindeutig, für Endanwender am Telefon jedoch zu sperrig. |

---

## 3. Verwaltungspraktische Bewertung

### A. Warum `PROJECT_ALIAS` alleine unzureichend ist
Wenn ein E-Mail-Betreff lediglich lautet:
> `Betreff: Eingang Ihres Antrags (antrag_sprints)`

hat weder die antragstellende Person noch die Sachbearbeitung im Dekanat / ZFK eine verwertbare Referenz. Ruft die antragstellende Person im Prüfungsamt oder der Drittmittelabteilung an, muss die Sachbearbeitung zeitaufwendig nach Nachname, Datum oder E-Mail-Adresse suchen.

### B. Warum `RECORD_ID` die echte Ticketnummer ist
Lautet der Betreff hingegen:
> `Betreff: Eingang Ihres Antrags [Vorgang #1042]`

kann die Sachbearbeitung die Ziffer `1042` direkt in die Suchmaske des Formcycle-Postfachs eingeben und öffnet binnen einer Sekunde den konkreten Vorgang.

### C. Warum `PROJECT_ALIAS` im Ist-Bestand toleriert wird
In der empirischen Vollerhebung der HWG-Formulare (Kapitel 3) wurde festgestellt, dass einige Entwickler zumindest `[%$PROJECT_ALIAS%]` eingebunden haben, um dem Empfänger die Antragsart zu verdeutlichen. Daher prüft die AST-Engine (`test_rule_engine.py`) tolerant:
```python
alias_tokens = ("%$project_alias%", "%$record_id%", "%$vorgang", "[%$id%]")
```
Dadurch wird ein Formular im Ist-Bestand nicht sofort mit einem Fehler abgestraft, wenn es zumindest den Formularnamen dynamisch referenziert.

---

## 4. Leitlinien & Best-Practice-Empfehlung

Für künftige Formulare und als Richtschnur für Formularverantwortliche der HWG gilt:

### 1. In der Remediation: `RECORD_ID` im Fokus
In Handlungsanweisungen (Remediation) für neue oder zu überarbeitende Formulare sollte primär **`[%$RECORD_ID%]`** (bzw. **`[%$ID%]`**) als die **einzige echte Vorgangsnummer** kommuniziert werden.

### 2. Die verwaltungsfachliche Ideallösung: Kombination aus beidem
Die professionellste Betreffzeile für automatisierte E-Mails kombiniert Formularart und laufende Nummer:

```text
Betreff: [[%$PROJECT_ALIAS%] # [%$RECORD_ID%]] Eingang Ihres Antrags
```

**Konkretes Ausgabebeispiel:**
```text
Betreff: [Antrag-Sprints #1042] Eingang Ihres Förderantrags
```

**Vorteile:**
1. **Für Antragstellende:** Sofortige Erkennbarkeit, um welches Anliegen es sich handelt, inklusive verbindlicher Belegnummer für Rückfragen.
2. **Für Sachbearbeitende:** Eindeutige Vorgangszuordnung im Formcycle-Postfach und klare Sortierung im zentralen E-Mail-Client (z. B. Outlook/Thunderbird).

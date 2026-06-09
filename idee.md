Gute Wahl. Hier ist die komplette Projektstruktur:

---

## Bewerbungs-Tracker – Projektübersicht

### Datenmodell (eine Bewerbung)

```
id, firma, stelle, ort, datum, status, techstack, antwort, notizen
```

Status-Werte z.B.: `beworben → einladung → interview → angebot → abgelehnt`

---

### Projektstruktur

```
bewerbungs-tracker/
├── backend/
│   ├── main.py          # FastAPI App + Routen
│   ├── database.py      # SQLite Verbindung
│   ├── models.py        # Pydantic Modelle
│   └── requirements.txt
└── frontend/
    ├── index.html
    ├── style.css
    └── app.js           # fetch() API-Calls
```

---

### Backend – die 5 Endpunkte

| Methode | Route | Was passiert |
|--------|-------|--------------|
| `GET` | `/bewerbungen` | Alle Einträge laden |
| `GET` | `/bewerbungen/{id}` | Eine Bewerbung laden |
| `POST` | `/bewerbungen` | Neue Bewerbung anlegen |
| `PUT` | `/bewerbungen/{id}` | Bewerbung komplett ersetzen |
| `PATCH` | `/bewerbungen/{id}` | Nur Status/Antwort aktualisieren |
| `DELETE` | `/bewerbungen/{id}` | Bewerbung löschen |

---

### Lernschritte – in dieser Reihenfolge

**Tag 1–2: Backend Grundgerüst**
- SQLite Tabelle anlegen mit `database.py`
- Pydantic Modell definieren (das ist FastAPIs Art, Daten zu validieren)
- `GET` und `POST` implementieren und mit den automatischen Docs testen (`/docs` – das ist einer der größten Vorteile von FastAPI)

**Tag 3: Restliche Endpunkte**
- `PUT`, `PATCH`, `DELETE` hinzufügen
- Bewusst den Unterschied zwischen `PUT` (alles ersetzen) und `PATCH` (nur ein Feld ändern) verstehen – das ist eine klassische Interview-Frage

**Tag 4–5: Frontend**
- Einfache HTML-Tabelle die per `fetch()` die Daten lädt
- Formular zum Hinzufügen
- Status-Dropdown zum direkten Aktualisieren per `PATCH`

**Tag 6: Feinschliff**
- Fehlerbehandlung (was passiert bei ungültiger ID?)
- CORS konfigurieren (wirst du brauchen, sobald Frontend und Backend separat laufen)

---

### Was du dabei lernst – und im Interview sagen kannst

- REST-Prinzipien praktisch angewendet
- Datenbankanbindung ohne ORM (erstmal raw SQL – lehrreich) oder mit SQLAlchemy
- Pydantic für Datenvalidierung
- Async-Grundlagen durch FastAPI
- DOM-Manipulation und fetch() im Frontend
- CORS – warum es existiert und wie man es löst

---

### Mein Tipp zum Start

Fang **nicht** mit dem Frontend an. Bau zuerst das Backend komplett und teste alles über `/docs` – FastAPI generiert dir automatisch eine interaktive API-Oberfläche. Das Frontend ist dann fast nur noch Darstellung.

Willst du, dass ich dir den Starter-Code für `main.py` und `database.py` schreibe?
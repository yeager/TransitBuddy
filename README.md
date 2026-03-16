# TransitBuddy - Reseplanerare

Enkel reseplanerare med stora, tydliga steg-för-steg-instruktioner.
Designad för att vara lättanvänd, särskilt för personer med kognitiva funktionshinder.

## Funktioner

- Välj start- och slutplats från dropdown-menyer
- Tydliga steg-för-steg-instruktioner med ikoner
- Stora, lättlästa texter
- Svenska som huvudspråk
- Sparade rutter i JSON-format

## Installation

### Krav

- Python 3.8+
- PyGObject (GTK4 + libadwaita)

### Installera beroenden

**Ubuntu/Debian:**
```bash
sudo apt install python3-gi python3-gi-cairo gir1.2-gtk-4.0 gir1.2-adw-1
```

**Fedora:**
```bash
sudo dnf install python3-gobject gtk4 libadwaita
```

**Arch:**
```bash
sudo pacman -S python-gobject gtk4 libadwaita
```

### Installera appen

```bash
pip install .
```

### Kör direkt

```bash
python -m transitbuddy.main
```

## Användning

1. Välj var du vill resa **från**
2. Välj var du vill resa **till**
3. Tryck på **SÖK RESA**
4. Följ instruktionerna steg för steg

## Anpassa rutter

Rutter sparas i `~/.config/transitbuddy/routes.json`. Du kan redigera denna fil för att lägga till egna rutter.

## Licens

MIT

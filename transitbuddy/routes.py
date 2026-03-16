"""Hårdkodade rutter för TransitBuddy."""

import json
import os
from transitbuddy.i18n import _

# Standardrutter - enkla exempelrutter i Stockholm
DEFAULT_ROUTES = [
    {
        "from": "Kungsträdgården",
        "to": "Gamla Stan",
        "steps": [
            {"type": "walk", "instruction": "Gå till hållplats Kungsträdgården", "detail": "Ca 2 minuters promenad"},
            {"type": "metro", "instruction": "Ta Tunnelbana 🟢 Linje 19 mot Hagsätra", "detail": "1 stopp"},
            {"type": "exit", "instruction": "Kliv av vid Gamla Stan", "detail": "Du är framme! 🎉"},
        ],
    },
    {
        "from": "Centralen",
        "to": "Södermalm (Medborgarplatsen)",
        "steps": [
            {"type": "walk", "instruction": "Gå till T-Centralen", "detail": "Följ skyltarna till tunnelbanan"},
            {"type": "metro", "instruction": "Ta Tunnelbana 🟢 Linje 19 mot Hagsätra", "detail": "2 stopp"},
            {"type": "exit", "instruction": "Kliv av vid Medborgarplatsen", "detail": "Du är framme! 🎉"},
        ],
    },
    {
        "from": "Centralen",
        "to": "Djurgården",
        "steps": [
            {"type": "walk", "instruction": "Gå till hållplats Centralstationen", "detail": "Gå ut genom huvudingången"},
            {"type": "bus", "instruction": "Ta Buss 67 mot Blockhusudden", "detail": "Ca 15 minuter"},
            {"type": "exit", "instruction": "Kliv av vid Djurgårdsbron", "detail": "Du är framme! 🎉"},
        ],
    },
    {
        "from": "Gamla Stan",
        "to": "Kungsträdgården",
        "steps": [
            {"type": "walk", "instruction": "Gå till hållplats Gamla Stan", "detail": "Ca 3 minuters promenad"},
            {"type": "metro", "instruction": "Ta Tunnelbana 🟢 Linje 19 mot Kungsträdgården", "detail": "1 stopp"},
            {"type": "exit", "instruction": "Kliv av vid Kungsträdgården", "detail": "Du är framme! 🎉"},
        ],
    },
    {
        "from": "Södermalm (Medborgarplatsen)",
        "to": "Centralen",
        "steps": [
            {"type": "walk", "instruction": "Gå till Medborgarplatsen tunnelbana", "detail": "Följ skyltarna"},
            {"type": "metro", "instruction": "Ta Tunnelbana 🟢 Linje 17 mot Åkeshov", "detail": "2 stopp"},
            {"type": "exit", "instruction": "Kliv av vid T-Centralen", "detail": "Du är framme! 🎉"},
        ],
    },
    {
        "from": "Centralen",
        "to": "Odenplan",
        "steps": [
            {"type": "walk", "instruction": "Gå till T-Centralen", "detail": "Följ skyltarna till gröna linjen"},
            {"type": "metro", "instruction": "Ta Tunnelbana 🟢 Linje 17 mot Åkeshov", "detail": "Eller linje 18/19"},
            {"type": "metro", "instruction": "Byt till Tunnelbana 🔵 Linje 10 vid Fridhemsplan", "detail": "Följ skyltarna"},
            {"type": "exit", "instruction": "Kliv av vid Odenplan", "detail": "Du är framme! 🎉"},
        ],
    },
]


def get_saved_routes_path():
    """Returnera sökväg till sparade rutter."""
    config_dir = os.path.join(os.path.expanduser("~"), ".config", "transitbuddy")
    os.makedirs(config_dir, exist_ok=True)
    return os.path.join(config_dir, "routes.json")


def load_routes():
    """Ladda rutter från fil eller returnera standardrutter."""
    path = get_saved_routes_path()
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return DEFAULT_ROUTES


def save_routes(routes):
    """Spara rutter till JSON-fil."""
    path = get_saved_routes_path()
    with open(path, "w", encoding="utf-8") as f:
        json.dump(routes, f, ensure_ascii=False, indent=2)


def find_route(from_place, to_place):
    """Hitta en rutt baserat på från/till."""
    routes = load_routes()
    from_lower = from_place.lower().strip()
    to_lower = to_place.lower().strip()
    for route in routes:
        if from_lower in route["from"].lower() and to_lower in route["to"].lower():
            return route
    return None


def get_all_places():
    """Returnera alla unika platser."""
    routes = load_routes()
    places = set()
    for route in routes:
        places.add(route["from"])
        places.add(route["to"])
    return sorted(places)

"""TransitBuddy - Huvudapplikation."""

import sys

import gi
from transitbuddy.i18n import _

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
from gi.repository import Adw, Gtk, Pango  # noqa: E402

from transitbuddy.routes import find_route, get_all_places  # noqa: E402


class TransitBuddyApp(Adw.Application):
    """Huvudapplikation för TransitBuddy."""

    def __init__(self):
        super().__init__(application_id="se.transitbuddy.app")
        self.connect("activate", self.on_activate)

    def on_activate(self, app):
        self.win = TransitBuddyWindow(application=app)
        self.win.present()


class TransitBuddyWindow(Adw.ApplicationWindow):
    """Huvudfönster."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.set_title("TransitBuddy - Reseplanerare")
        self.set_default_size(420, 700)

        # Huvudlayout
        self.main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        self.set_content(self.main_box)

        # Headerbar
        header = Adw.HeaderBar()
        title = Adw.WindowTitle(title=_("TransitBuddy", subtitle=_("Your travel planner")
        header.set_title_widget(title)
        self.main_box.append(header)

        # Scrollad vy för innehåll
        scroll = Gtk.ScrolledWindow(vexpand=True)
        self.main_box.append(scroll)

        content = Gtk.Box(
            orientation=Gtk.Orientation.VERTICAL,
            spacing=16,
            margin_top=16,
            margin_bottom=16,
            margin_start=16,
            margin_end=16,
        )
        scroll.set_child(content)

        # Välkomsttext
        welcome = Gtk.Label(label=_("Where do you want to go?")
        welcome.add_css_class("title-1")
        content.append(welcome)

        # Från-fält
        from_label = Gtk.Label(label=_("FROM:"), xalign=0
        from_label.add_css_class("heading")
        content.append(from_label)

        self.from_dropdown = Gtk.DropDown()
        self._setup_dropdown(self.from_dropdown)
        content.append(self.from_dropdown)

        # Till-fält
        to_label = Gtk.Label(label=_("TILL:", xalign=0)
        to_label.add_css_class("heading")
        content.append(to_label)

        self.to_dropdown = Gtk.DropDown()
        self._setup_dropdown(self.to_dropdown)
        content.append(self.to_dropdown)

        # Sök-knapp
        search_btn = Gtk.Button(label=_("🔍 SEARCH TRAVEL")
        search_btn.add_css_class("suggested-action")
        search_btn.add_css_class("pill")
        search_btn.set_margin_top(8)
        search_btn.connect("clicked", self.on_search)
        content.append(search_btn)

        # Resultat-sektion
        self.result_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        self.result_box.set_margin_top(16)
        content.append(self.result_box)

        # Ladda CSS
        self._load_css()

    def _setup_dropdown(self, dropdown):
        """Konfigurera dropdown med platser."""
        places = get_all_places()
        string_list = Gtk.StringList()
        for place in places:
            string_list.append(place)
        dropdown.set_model(string_list)

        # Gör dropdown större med factory
        factory = Gtk.SignalListItemFactory()
        factory.connect("setup", self._on_dropdown_setup)
        factory.connect("bind", self._on_dropdown_bind)
        dropdown.set_factory(factory)

    @staticmethod
    def _on_dropdown_setup(_factory, list_item):
        label = Gtk.Label(xalign=0)
        label.set_margin_top(8)
        label.set_margin_bottom(8)
        label.set_margin_start(8)
        label.set_margin_end(8)
        label.add_css_class("body")
        list_item.set_child(label)

    @staticmethod
    def _on_dropdown_bind(_factory, list_item):
        label = list_item.get_child()
        item = list_item.get_item()
        label.set_label(item.get_string())

    def _load_css(self):
        """Ladda anpassad CSS för stora, tydliga element."""
        css = b"""
        .step-card {
            padding: 16px;
            border-radius: 12px;
            background: @card_bg_color;
        }
        .step-instruction {
            font-size: 18px;
            font-weight: bold;
        }
        .step-detail {
            font-size: 14px;
            color: @dim_label_color;
        }
        .step-icon {
            font-size: 28px;
        }
        .result-header {
            font-size: 20px;
            font-weight: bold;
        }
        """
        provider = Gtk.CssProvider()
        provider.load_from_data(css)
        Gtk.StyleContext.add_provider_for_display(
            self.get_display(), provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )

    def on_search(self, _button):
        """Sök efter en resa."""
        # Rensa gamla resultat
        while child := self.result_box.get_first_child():
            self.result_box.remove(child)

        from_item = self.from_dropdown.get_selected_item()
        to_item = self.to_dropdown.get_selected_item()
        if not from_item or not to_item:
            return

        from_place = from_item.get_string()
        to_place = to_item.get_string()

        if from_place == to_place:
            self._show_message("⚠️ Du har valt samma plats!")
            return

        route = find_route(from_place, to_place)
        if not route:
            self._show_message("😔 Tyvärr hittades ingen resa.\nFörsök med andra platser!")
            return

        # Visa resultatheader
        header = Gtk.Label(label=f"📍 {from_place} → {to_place}", xalign=0, wrap=True)
        header.add_css_class("result-header")
        self.result_box.append(header)

        sep = Gtk.Separator()
        self.result_box.append(sep)

        # Visa varje steg
        for i, step in enumerate(route["steps"], 1):
            card = self._create_step_card(i, step)
            self.result_box.append(card)

    def _create_step_card(self, number, step):
        """Skapa ett steg-kort."""
        icons = {"walk": "🚶", "metro": "🚇", "bus": "🚌", "tram": "🚊", "exit": "📍"}
        icon = icons.get(step["type"], "➡️")

        frame = Gtk.Frame()
        frame.add_css_class("step-card")

        box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=12)
        box.set_margin_top(8)
        box.set_margin_bottom(8)
        box.set_margin_start(8)
        box.set_margin_end(8)
        frame.set_child(box)

        # Ikon
        icon_label = Gtk.Label(label=icon)
        icon_label.add_css_class("step-icon")
        box.append(icon_label)

        # Text
        text_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=4)
        text_box.set_hexpand(True)
        box.append(text_box)

        # Stegnummer + instruktion
        instr = Gtk.Label(
            label=f"Steg {number}: {step['instruction']}",
            xalign=0,
            wrap=True,
            wrap_mode=Pango.WrapMode.WORD_CHAR,
        )
        instr.add_css_class("step-instruction")
        text_box.append(instr)

        # Detaljer
        if step.get("detail"):
            detail = Gtk.Label(label=step["detail"], xalign=0, wrap=True)
            detail.add_css_class("step-detail")
            text_box.append(detail)

        return frame

    def _show_message(self, text):
        """Visa ett meddelande i resultatrutan."""
        label = Gtk.Label(label=text, wrap=True)
        label.add_css_class("title-2")
        self.result_box.append(label)


def main():
    """Starta applikationen."""
    app = TransitBuddyApp()
    return app.run(sys.argv)


if __name__ == "__main__":
    main()

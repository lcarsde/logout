#!/usr/bin/env python3

import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk


css = b'''
.button {
    min-height: 38px;
    font-family: 'Ubuntu Condensed', sans-serif;
    font-weight: 600;
    font-size: 18px;
    color: #000;
    text-shadow: none;
    outline-style: none;
    border-radius: 25px;
    border-width: 0;
    box-shadow: none;
    padding: 2px 20px;
    margin: 0;
}
.button--f90 {
    background-color: #f90;
    background: #f90; /* for Ubuntu */
}
.button--c9c {
    background-color: #c9c;
    background: #c9c; /* for Ubuntu */
}
.button--99c {
    background-color: #99c;
    background: #99c; /* for Ubuntu */
}
.button--c66 {
    background-color: #c66;
    background: #c66; /* for Ubuntu */
}
.button--fc9 {
    background-color: #fc9;
    background: #fc9; /* for Ubuntu */
}
.button--99f {
    background-color: #99f;
    background: #99f; /* for Ubuntu */
}
.button--f96 {
    background-color: #f96;
    background: #f96; /* for Ubuntu */
}
.button--c69 {
    background-color: #c69;
    background: #c69; /* for Ubuntu */
}
.category {
    font-family: 'Ubuntu Condensed', sans-serif;
    font-weight: 600;
    font-size: 24px;
    color: #f90;
}
.line-end {
    min-width: 20px;
    background-color: #99F;
    background: #99F; /* for Ubuntu */
    outline-style: none;
    border-width: 0;
    box-shadow: none;
    padding: 0;
    margin: 0;
}
.line-end--left {
    border-radius: 20px 0 0 20px;
}
.line-end--right {
    border-radius: 0 20px 20px 0;
}
.window {
    background-color: #000;
}
'''


class LcarsdeLogout(Gtk.Window):
    """
    lcarsde logout main window
    """

    def __init__(self):
        Gtk.Window.__init__(self, title="Logout")

        self.css_provider = Gtk.CssProvider()
        self.css_provider.load_from_data(css)

        self.scroll_container = Gtk.ScrolledWindow()
        self.scroll_container.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)

        self.app_container = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)

        self.setup_buttons()

        self.scroll_container.add(self.app_container)
        self.add(self.scroll_container)
        self.connect('size-allocate', self.view_changed)

        self.get_style_context().add_class("window")
        self.get_style_context().add_provider(self.css_provider, Gtk.STYLE_PROVIDER_PRIORITY_USER)

    def view_changed(self, widget, event, data=None):
        adj = self.scroll_container.get_vadjustment()
        adj.set_value(0)

    def setup_buttons(self):
        self.create_button("Shutdown", None, "c66")
        self.create_button("Reboot", None, "f96")
        self.create_button("Suspend", None, "c9c")
        self.create_button("Lock Screen", None, "99c")
        self.create_button("Logout", None, "f96")

    def create_button(self, label, handler, color):
        button = Gtk.Button(label=label)
#        button.connect("clicked", handler)
        button.set_alignment(1, 1)
        button.get_style_context().add_class("button")
        button.get_style_context().add_class("button--{}".format(color))
        button.get_style_context().add_provider(self.css_provider, Gtk.STYLE_PROVIDER_PRIORITY_USER)
        self.app_container.add(button)


if __name__ == "__main__":
    win = LcarsdeLogout()
    win.connect("destroy", Gtk.main_quit)
    win.show_all()
    Gtk.main()

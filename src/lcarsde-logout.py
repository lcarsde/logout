#!/usr/bin/env python3
import gi
import psutil
import os
import subprocess
from multiprocessing import Process

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gio, GLib

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
.button--f96 {
    background-color: #f96;
    background: #f96; /* for Ubuntu */
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
        handler = LcarsdeLogout.get_handler("Stop", "PowerOff")
        if handler is not None:
            self.create_button("Shutdown", handler, "c66")

        handler = LcarsdeLogout.get_handler("Restart", "Reboot")
        if handler is not None:
            self.create_button("Reboot", handler, "f96")

        handler = LcarsdeLogout.get_handler("Suspend", "Suspend")
        if handler is not None:
            self.create_button("Suspend", handler, "c9c")

        handler = LcarsdeLogout.get_handler("Hibernate", "Hibernate")
        if handler is not None:
            self.create_button("Hibernate", handler, "c9c")

        if LcarsdeLogout.is_lock_screen_available():
            self.create_button("Lock Screen", LcarsdeLogout.lock_screen, "99c")

        self.create_button("Logout", LcarsdeLogout.logout, "f96")

    def create_button(self, label, handler, color):
        button = Gtk.Button(label=label)
        button.connect("clicked", lambda w: handler())
        button.set_alignment(1, 1)
        button.get_style_context().add_class("button")
        button.get_style_context().add_class("button--{}".format(color))
        button.get_style_context().add_provider(self.css_provider, Gtk.STYLE_PROVIDER_PRIORITY_USER)
        self.app_container.add(button)

    @staticmethod
    def get_proxy(name, object_path, interface_name):
        bus = Gio.bus_get_sync(Gio.BusType.SYSTEM, None)
        return Gio.DBusProxy.new_sync(bus, Gio.DBusProxyFlags.NONE, None, name, object_path, interface_name, None)

    @staticmethod
    def is_method_available(proxy, method_name):
        try:
            result = proxy.call_sync(method_name, None, Gio.DBusCallFlags.NONE, 100, None)
        except GLib.GError:
            return False
        return result[0] == 'yes'

    @staticmethod
    def is_console_kit_method_available(method_name):
        """
        :param method_name: Stop or Restart
        """
        proxy = LcarsdeLogout.get_proxy('org.freedesktop.ConsoleKit', '/org/freedesktop/ConsoleKit/Manager',
                                        'org.freedesktop.ConsoleKit.Manager')

        return LcarsdeLogout.is_method_available(proxy, method_name)

    @staticmethod
    def run_console_kit_method(method_name):
        """
        :param method_name: Stop or Restart
        """
        proxy = LcarsdeLogout.get_proxy('org.freedesktop.ConsoleKit', '/org/freedesktop/ConsoleKit/Manager',
                                        'org.freedesktop.ConsoleKit.Manager')

        proxy.call_sync(method_name, None, Gio.DBusCallFlags.NONE, 100, None)

    @staticmethod
    def is_systemd_method_available(method_name):
        """
        :param method_name: PowerOff, Reboot, Suspend or Hibernate
        """
        proxy = LcarsdeLogout.get_proxy('org.freedesktop.login1', '/org/freedesktop/login1',
                                        'org.freedesktop.login1.Manager')

        return LcarsdeLogout.is_method_available(proxy, method_name)

    @staticmethod
    def run_systemd_method(method_name):
        """
        :param method_name: PowerOff, Reboot, Suspend or Hibernate
        """
        proxy = LcarsdeLogout.get_proxy('org.freedesktop.login1', '/org/freedesktop/login1',
                                        'org.freedesktop.login1.Manager')

        parameter = GLib.Variant.new_tuple(GLib.Variant.new_boolean(True))
        proxy.call_sync(method_name, parameter, Gio.DBusCallFlags.NONE, 100, None)

    @staticmethod
    def get_handler(console_kit_method, systemd_method):
        """
        :param console_kit_method: method name for action via ConsoleKit
        :param systemd_method: method name for action via SystemD
        :return: handler for calling the action or None, if action is not available
        """
        if LcarsdeLogout.is_console_kit_method_available("Can" + console_kit_method):
            return lambda: LcarsdeLogout.run_console_kit_method(console_kit_method)

        elif LcarsdeLogout.is_systemd_method_available("Can" + systemd_method):
            return lambda: LcarsdeLogout.run_systemd_method(systemd_method)

        else:
            return None

    @staticmethod
    def is_lock_screen_available():
        return any(
            os.access(os.path.join(path, "xdg-screensaver"), os.X_OK)
            for path in os.environ["PATH"].split(os.pathsep)
        )

    @staticmethod
    def lock_screen():
        p = Process(target=lambda c: subprocess.Popen(c), args=("xdg-screensaver", "lock",))
        p.start()

    @staticmethod
    def logout():
        """
        Terminate lcarswm.kexe.
        """
        for process in psutil.process_iter():
            if process.name() == "lcarswm.kexe":
                process.terminate()
                break


if __name__ == "__main__":
    win = LcarsdeLogout()
    win.connect("destroy", Gtk.main_quit)
    win.show_all()
    Gtk.main()

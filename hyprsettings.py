import sys
import gi
import subprocess
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
from gi.repository import Gtk, Adw, Pango

title_str = "hyprsettings "

class MainWindow(Gtk.ApplicationWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Setup the UI and styling
        self.setup_ui()
        self.setup_style()

    def setup_ui(self):
        """Set up the user interface."""
        self.box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=20)
        self.set_child(self.box)

        # Create and configure the header bar
        self.header_bar = Gtk.HeaderBar()
        self.header_bar.set_show_title_buttons(True)
        self.set_titlebar(self.header_bar)
        self.set_title(title_str)

        # Create and configure the label for Privacy Settings
        self.label = Gtk.Label(label="<big><b>Privacy Settings</b></big>")
        self.label.set_margin_top(20)
        self.label.set_margin_bottom(5)
        self.label.set_margin_start(50)
        self.label.set_halign(Gtk.Align.START)
        self.label.set_use_markup(True)

        # Create and configure the description label
        self.description_label = Gtk.Label(label="Manage privacy settings, such as clipboard and command history.")
        self.description_label.set_margin_bottom(5)
        self.description_label.set_halign(Gtk.Align.START)
        self.description_label.set_margin_start(50)

        # Create and configure the Clipboard button
        self.clipboard_button = Gtk.Button(label="Clear Clipboard History")
        self.clipboard_button.set_margin_top(5)
        self.clipboard_button.set_margin_start(50)
        self.clipboard_button.set_margin_end(50)
        self.clipboard_button.set_size_request(200, 50)
        self.clipboard_button.set_halign(Gtk.Align.START)
        self.clipboard_button.connect('clicked', self.on_clipboard_button_clicked)
        
        # Create and configure the Command history button
        self.history_button = Gtk.Button(label="Clear Command History")
        self.history_button.set_margin_top(5)
        self.history_button.set_margin_start(50)
        self.history_button.set_margin_end(50)
        self.history_button.set_margin_bottom(50)
        self.history_button.set_size_request(200, 50)
        self.history_button.set_halign(Gtk.Align.START)
        self.history_button.connect('clicked', self.on_history_button_clicked)

        # Add widgets to the box
        self.box.append(self.label)
        self.box.append(self.description_label)
        self.box.append(self.clipboard_button)
        self.box.append(self.history_button)

        # Set the window's default size
        self.set_default_size(600, 300)

    def setup_style(self):
        """Set up the application style."""
        app = self.get_application()
        style_manager = app.get_style_manager()
        style_manager.set_color_scheme(Adw.ColorScheme.PREFER_DARK)

    def on_clipboard_button_clicked(self, button):
        """Handle clipboard button click event by showing a confirmation dialog."""
        dialog = Gtk.MessageDialog(
            transient_for=self,
            modal=True,
            message_type=Gtk.MessageType.QUESTION,
            buttons=Gtk.ButtonsType.YES_NO,
            text="Are you sure you want to clear the clipboard history?",
        )
        dialog.connect("response", self.on_clipboard_dialog_response)
        dialog.present()

    def on_history_button_clicked(self, button):
        """Handle history button click event by showing a confirmation dialog."""
        dialog = Gtk.MessageDialog(
            transient_for=self,
            modal=True,
            message_type=Gtk.MessageType.QUESTION,
            buttons=Gtk.ButtonsType.YES_NO,
            text="Are you sure you want to clear the command history?",
        )
        dialog.connect("response", self.on_history_dialog_response)
        dialog.present()

    def on_clipboard_dialog_response(self, dialog, response_id):
        """Handle the clipboard dialog response event."""
        if response_id == Gtk.ResponseType.YES:
            self.clear_clipboard_history()
        dialog.destroy()

    def on_history_dialog_response(self, dialog, response_id):
        """Handle the history dialog response event."""
        if response_id == Gtk.ResponseType.YES:
            self.clear_command_history()
        dialog.destroy()

    def clear_clipboard_history(self):
        """Clear the clipboard history using the 'cliphist wipe' command."""
        try:
            subprocess.run(['cliphist', 'wipe'], check=True)
            print("Clipboard history cleared")
        except subprocess.CalledProcessError as e:
            print(f"An error occurred: {e}")

    def clear_command_history(self):
        """Clear the command history using the 'history -cw' command."""
        try:
            subprocess.run(['history', '-cw'], check=True, shell=True)
            print("Command history cleared")
        except subprocess.CalledProcessError as e:
            print(f"An error occurred: {e}")

class MyApp(Adw.Application):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.connect('activate', self.on_activate)

    def on_activate(self, app):
        """Activate the application by creating and presenting the main window."""
        self.win = MainWindow(application=app)
        self.win.present()

def main():
    """Main function to run the application."""
    app = MyApp(application_id="com.example.GtkApplication")
    app.run(sys.argv)

if __name__ == "__main__":
    main()

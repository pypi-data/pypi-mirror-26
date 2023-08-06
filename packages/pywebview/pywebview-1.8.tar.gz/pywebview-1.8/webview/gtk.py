"""
(C) 2014-2016 Roman Sirokov and contributors
Licensed under BSD license

http://github.com/r0x0r/pywebview/
"""
import sys
import threading
import logging
from uuid import uuid1
from webview.localization import localization
from webview import _escape_string, OPEN_DIALOG, FOLDER_DIALOG, SAVE_DIALOG

logger = logging.getLogger(__name__)

import gi
gi.require_version('Gtk', '3.0')
gi.require_version('Gdk', '3.0')
gi.require_version('WebKit', '3.0')

from gi.repository import Gtk as gtk
from gi.repository import Gdk
from gi.repository import GLib as glib
from gi.repository import WebKit as webkit

class BrowserView:
    instance = None

    def __init__(self, title, url, width, height, resizable, fullscreen, min_size,
                 confirm_quit, background_color, webview_ready):
        BrowserView.instance = self

        self.webview_ready = webview_ready
        self.is_fullscreen = False
        self._js_result_semaphore = threading.Semaphore(0)

        glib.threads_init()
        window = gtk.Window(title=title)

        if resizable:
            window.set_size_request(min_size[0], min_size[1])
            window.resize(width, height)
        else:
            window.set_size_request(width, height)

        window.set_resizable(resizable)
        window.set_position(gtk.WindowPosition.CENTER)

        # Set window background color
        style_provider = gtk.CssProvider()
        style_provider.load_from_data(
            'GtkWindow {{ background-color: {}; }}'.format(background_color).encode()
        )
        gtk.StyleContext.add_provider_for_screen(
            Gdk.Screen.get_default(),
            style_provider,
            gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )

        scrolled_window = gtk.ScrolledWindow()
        window.add(scrolled_window)

        self.window = window

        if confirm_quit:
            self.window.connect('delete-event', self.on_destroy)
        else:
            self.window.connect('delete-event', self.close_window)

        self.webview = webkit.WebView()
        self.webview.connect('notify::visible', self.on_webview_ready)
        self.webview.connect('document-load-finished', self.on_load_finish)
        self.webview.props.settings.props.enable_default_context_menu = False
        self.webview.props.opacity = 0.0
        scrolled_window.add(self.webview)
        window.show_all()

        if url is not None:
            self.webview.load_uri(url)

        if fullscreen:
            self.toggle_fullscreen()

    def close_window(self, *data):
        self.window.destroy()
        while gtk.events_pending():
            gtk.main_iteration()
        gtk.main_quit()

    def on_destroy(self, widget=None, *data):
        dialog = gtk.MessageDialog(parent=self.window, flags=gtk.DialogFlags.MODAL & gtk.DialogFlags.DESTROY_WITH_PARENT,
                                          type=gtk.MessageType.QUESTION, buttons=gtk.ButtonsType.OK_CANCEL,
                                          message_format=localization['global.quitConfirmation'])
        result = dialog.run()
        if result == gtk.ResponseType.OK:
            self.close_window()
        else:
            dialog.destroy()
            return True

    def on_webview_ready(self, arg1, arg2):
        self.webview_ready.set()

    def on_load_finish(self, webview, webframe):
        # Show the webview if it's not already visible
        if not webview.props.opacity:
            glib.idle_add(webview.set_opacity, 1.0)

    def show(self):
        gtk.main()

    def destroy(self):
        self.window.emit('delete-event', Gdk.Event())

    def toggle_fullscreen(self):
        if self.is_fullscreen:
            self.window.unfullscreen()
        else:
            self.window.fullscreen()

        self.is_fullscreen = not self.is_fullscreen

    def create_file_dialog(self, dialog_type, directory, allow_multiple, save_filename):
        if dialog_type == FOLDER_DIALOG:
            gtk_dialog_type = gtk.FileChooserAction.SELECT_FOLDER
            title = localization["linux.openFolder"]
            button = gtk.STOCK_OPEN
        elif dialog_type == OPEN_DIALOG:
            gtk_dialog_type = gtk.FileChooserAction.OPEN
            if allow_multiple:
                title = localization['linux.openFiles']
            else:
                title = localization['linux.openFile']

            button = gtk.STOCK_OPEN
        elif dialog_type == SAVE_DIALOG:
            gtk_dialog_type = gtk.FileChooserAction.SAVE
            title = localization['global.saveFile']
            button = gtk.STOCK_SAVE

        dialog = gtk.FileChooserDialog(title, self.window, gtk_dialog_type,
                                       (gtk.STOCK_CANCEL, gtk.ResponseType.CANCEL, button, gtk.ResponseType.OK))

        dialog.set_select_multiple(allow_multiple)
        dialog.set_current_folder(directory)

        if dialog_type == SAVE_DIALOG:
            dialog.set_current_name(save_filename)

        response = dialog.run()

        if response == gtk.ResponseType.OK:
            file_name = dialog.get_filenames()
        else:
            file_name = None

        dialog.destroy()

        return file_name

    def get_current_url(self):
        uri = self.webview.get_uri()
        return uri

    def load_url(self, url):
        self.webview.load_uri(url)

    def load_html(self, content, base_uri):
        self.webview.load_string(content, 'text/html', 'utf-8', base_uri)

    def evaluate_js(self, script):
        def _evaluate_js():
            self.webview.execute_script(code)
            self._js_result_semaphore.release()

        unique_id = uuid1().hex

        # Backup the doc title and store the result in it with a custom prefix
        code = 'oldTitle{0} = document.title; document.title = eval("{1}");'.format(unique_id, _escape_string(script))

        glib.idle_add(_evaluate_js)
        self._js_result_semaphore.acquire()

        # Restore document title and return
        _js_result = self.webview.get_title()
        code = 'document.title = oldTitle{0};'.format(unique_id)
        glib.idle_add(self.webview.execute_script, code)
        return _js_result


def create_window(title, url, width, height, resizable, fullscreen, min_size,
                  confirm_quit, background_color, webview_ready):
    browser = BrowserView(title, url, width, height, resizable, fullscreen,
                          min_size, confirm_quit, background_color, webview_ready)
    browser.show()


def destroy_window():
    def _destroy_window():
        BrowserView.instance.close_window()
    glib.idle_add(_destroy_window)


def toggle_fullscreen():
    def _toggle_fullscreen():
        BrowserView.instance.toggle_fullscreen()
    glib.idle_add(_toggle_fullscreen)


def get_current_url():
    return BrowserView.instance.get_current_url()


def load_url(url):
    def _load_url():
        BrowserView.instance.load_url(url)
    glib.idle_add(_load_url)


def load_html(content, base_uri):
    def _load_html():
        BrowserView.instance.load_html(content, base_uri)
    glib.idle_add(_load_html)


def create_file_dialog(dialog_type, directory, allow_multiple, save_filename):
    file_name_semaphore = threading.Semaphore(0)
    file_names = []

    def _create():
        result = BrowserView.instance.create_file_dialog(dialog_type, directory, allow_multiple, save_filename)
        if result is None:
            file_names.append(None)
        else:
            result = map(unicode, result) if sys.version < '3' else result
            file_names.append(tuple(result))
        
        file_name_semaphore.release()

    glib.idle_add(_create)
    file_name_semaphore.acquire()

    return file_names[0]


def evaluate_js(script):
    return BrowserView.instance.evaluate_js(script)

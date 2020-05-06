from cefpython3 import cefpython as cef
try:
    import tkinter as tk
except ImportError:
    import Tkinter as tk
import sys
import platform
import folium

# Fix for PyCharm hints warnings
WindowUtils = cef.WindowUtils()

# Platforms
WINDOWS = (platform.system() == "Windows")
LINUX = (platform.system() == "Linux")
MAC = (platform.system() == "Darwin")

# Constants
# Tk 8.5 doesn't support png images
IMAGE_EXT = ".png" if tk.TkVersion > 8.5 else ".gif"


def main():
    sys.excepthook = cef.ExceptHook  # To shutdown all CEF processes on error
    root = tk.Tk()
    app = MainFrame(root)
    # Tk must be initialized before CEF otherwise fatal error (Issue #306)
    cef.Initialize()
    app.mainloop()
    cef.Shutdown()


class MainFrame(tk.Frame):

    def __init__(self, root):
        self.result_frame = None
        self.map_frame = None
        self.button1 = None
        self.button2 = None
        self.map = None

        # Root
        root.geometry("1000x600")

        # MainFrame
        tk.Frame.__init__(self, root)
        self.master.title("Datasets Manager")
        self.master.protocol("WM_DELETE_WINDOW", self.on_close)
        self.master.bind("<Configure>", self.on_configure)

        # Sections
        self.lower = tk.PanedWindow(self, orient=tk.HORIZONTAL)
        self.lower.pack(fill=tk.BOTH, expand=1, side=tk.BOTTOM)
        self.left = tk.Frame(self.lower)
        self.lower.add(self.left, minsize=200)

        # MessageFrame
        self.message_frame = tk.LabelFrame(self, height=100)
        self.message_frame.pack(fill=tk.X, side=tk.BOTTOM)
        self.message_frame.propagate(0)
        self.label = tk.Label(self.message_frame, text="Some description here!")
        self.label.place(relx=.5, rely=.5, anchor="center")

        # MenuFrame
        self.menu_frame = tk.LabelFrame(self.left, width=700, height=100)
        self.menu_frame.pack(fill=tk.X)
        self.menu_frame.grid_propagate(0)
        self.main_menu()

        # ResultFrame
        self.result_frame = BrowserFrame(self.left)
        self.left.bind("<Configure>", self.on_configure)
        self.result_frame.pack(fill=tk.BOTH, expand=1)

        # MapFrame
        self.map_frame = BrowserFrame(self.lower)
        self.lower.bind("<Configure>", self.on_configure)
        self.lower.add(self.map_frame, minsize=200)

        # Pack MainFrame
        self.pack(fill=tk.BOTH, expand=tk.YES)

    def main_menu(self):
        self.button1 = tk.Button(self.menu_frame, text="Test Map", command=self.function_1)
        self.button1.grid(row=0, column=0)
        self.button2 = tk.Button(self.menu_frame, text="Test Table", command=self.function_2)
        self.button2.grid(row=0, column=1)

    def on_configure(self, _):
        if self.result_frame:
            self.result_frame.on_configure()
        if self.map_frame:
            self.map_frame.on_configure()

    def on_close(self):
        if self.result_frame:
            self.result_frame.clear_browser_references()
        if self.map_frame:
            self.map_frame.clear_browser_references()
        self.master.destroy()

    def function_1(self):
        self.map = folium.Map(location=[40.738, -73.98], zoom_start=12)
        self.map_frame.set_html(self.map.get_root().render())

    def function_2(self):
        if self.result_frame:
            self.result_frame.set_url('data:text/html;base64,PHRhYmxlIGJvcmRlcj0iMSIgY2xhc3M9ImRhdGFmcmFtZSI+CiAgPHRoZWFkPgogICAgPHRyIHN0eWxlPSJ0ZXh0LWFsaWduOiByaWdodDsiPgogICAgICA8dGg+PC90aD4KICAgICAgPHRoPm5hbWU8L3RoPgogICAgICA8dGg+aW5zdHJ1Y3Rpb25zPC90aD4KICAgICAgPHRoPnNlcnZpbmdzPC90aD4KICAgICAgPHRoPmNvdXJzZTwvdGg+CiAgICAgIDx0aD5zZWFzb248L3RoPgogICAgPC90cj4KICA8L3RoZWFkPgogIDx0Ym9keT4KICAgIDx0cj4KICAgICAgPHRoPjA8L3RoPgogICAgICA8dGQ+Q2hpY2tlbiBTYW5kd2ljaDwvdGQ+CiAgICAgIDx0ZD5TcHJlYWQgbWF5b25uYWlzZSBvbiBhIHNsaWNlIG9mIGJyZWFkLiBQbGFjZSBjaGlja2VuIG9uIHRvcCwgYWRkIGEgc2Vjb25kIHNsaWNlIG9mIGJyZWFkIG9uIHRvcCBvZiB0aGF0LjwvdGQ+CiAgICAgIDx0ZD4xPC90ZD4KICAgICAgPHRkPkVudHJlZTwvdGQ+CiAgICAgIDx0ZD5TcHJpbmc8L3RkPgogICAgPC90cj4KICAgIDx0cj4KICAgICAgPHRoPjE8L3RoPgogICAgICA8dGQ+SGFtIFNhbmR3aWNoPC90ZD4KICAgICAgPHRkPlNwcmVhZCBtdXN0YXJkIG9uIHR3byBzbGljZXMgb2YgYnJlYWQuIFBsYWNlIGhhbSBhbmQgY2hlZXNlIGJldHdlZW4gdGhlbS48L3RkPgogICAgICA8dGQ+MTwvdGQ+CiAgICAgIDx0ZD5FbnRyZWU8L3RkPgogICAgICA8dGQ+RmFsbDwvdGQ+CiAgICA8L3RyPgogICAgPHRyPgogICAgICA8dGg+MjwvdGg+CiAgICAgIDx0ZD5GcmVuY2ggRnJpZXM8L3RkPgogICAgICA8dGQ+U2xpY2UgcG90YXRvZXMgYW5kIGZyeSB0aGVtLjwvdGQ+CiAgICAgIDx0ZD4zPC90ZD4KICAgICAgPHRkPlNpZGU8L3RkPgogICAgICA8dGQ+QWxsPC90ZD4KICAgIDwvdHI+CiAgICA8dHI+CiAgICAgIDx0aD4zPC90aD4KICAgICAgPHRkPkdhcmRlbiBTYWxhZDwvdGQ+CiAgICAgIDx0ZD5Bc3NlbWJsZSBpbmdyZWRpZW50cyBpbiBhIGJvd2wgYW5kIHRvc3MgdGhlbSB0b2dldGhlci48L3RkPgogICAgICA8dGQ+ODwvdGQ+CiAgICAgIDx0ZD5TaWRlPC90ZD4KICAgICAgPHRkPkFsbDwvdGQ+CiAgICA8L3RyPgogICAgPHRyPgogICAgICA8dGg+NDwvdGg+CiAgICAgIDx0ZD5IYW1idXJnZXI8L3RkPgogICAgICA8dGQ+Rm9ybSBncm91bmQgYmVlZiBpbnRvIHBhdHRpZXMuIENvb2sgcGF0dGllcyB0byBvcmRlci4gUGxhY2UgcGF0dGllcyBvbiBidW4uIFNlcnZlIG9wZW4gZmFjZTwvdGQ+CiAgICAgIDx0ZD4xPC90ZD4KICAgICAgPHRkPkVudHJlZTwvdGQ+CiAgICAgIDx0ZD5BbGw8L3RkPgogICAgPC90cj4KICAgIDx0cj4KICAgICAgPHRoPjU8L3RoPgogICAgICA8dGQ+UHVtcGtpbiBQaWU8L3RkPgogICAgICA8dGQ+UG91ciBwaWUgZmlsbGluZyBpbnRvIHBpZSBjcnVzdC4gQmFrZSBhdCBhbiBhcHByb3ByaWF0ZSB0ZW1wZXJhdHVyZSB1bnRpbCBkb25lLjwvdGQ+CiAgICAgIDx0ZD44PC90ZD4KICAgICAgPHRkPkRlc3NlcnQ8L3RkPgogICAgICA8dGQ+RmFsbDwvdGQ+CiAgICA8L3RyPgogICAgPHRyPgogICAgICA8dGg+NjwvdGg+CiAgICAgIDx0ZD5JY2UgQ3JlYW0gU3VuZGFlPC90ZD4KICAgICAgPHRkPlNjb29wIGljZSBjcmVhbSBpbnRvIGRpc2gsIGFuZCBhZGQgY2hvY29sYXRlIHNhdWNlLjwvdGQ+CiAgICAgIDx0ZD4xPC90ZD4KICAgICAgPHRkPkRlc3NlcnQ8L3RkPgogICAgICA8dGQ+U3ByaW5nPC90ZD4KICAgIDwvdHI+CiAgICA8dHI+CiAgICAgIDx0aD43PC90aD4KICAgICAgPHRkPk1pbGtzaGFrZTwvdGQ+CiAgICAgIDx0ZD5BZGQgaWNlIGNyZWFtIGFuZCBtaWxrIHRvIGJsZW5kZXIsIGFuZCBibGVuZCB1bnRpbCBzbW9vdGguIFNlcnZlIGluIGEgdGFsbCBnbGFzcy48L3RkPgogICAgICA8dGQ+MjwvdGQ+CiAgICAgIDx0ZD5EZXNzZXJ0PC90ZD4KICAgICAgPHRkPkFsbDwvdGQ+CiAgICA8L3RyPgogICAgPHRyPgogICAgICA8dGg+ODwvdGg+CiAgICAgIDx0ZD5IYW0gYW5kIE1hc2hlZCBQb3RhdG9lczwvdGQ+CiAgICAgIDx0ZD5Sb2FzdCBoYW0gaW4gb3ZlbiB1bnRpbCBob3QuIEJvaWwgcG90YXRvZXMgdW50aWwgZG9uZSwgdGhlbiBtYXNoIGFuZCBhZGQgbWlsayB0byBtYWtlIHRoZW0gc21vb3RoLjwvdGQ+CiAgICAgIDx0ZD40PC90ZD4KICAgICAgPHRkPkVudHJlZTwvdGQ+CiAgICAgIDx0ZD5TcHJpbmc8L3RkPgogICAgPC90cj4KICA8L3Rib2R5Pgo8L3RhYmxlPg==')


class BrowserFrame(tk.Frame):

    def __init__(self, master):
        self.browser = None
        tk.Frame.__init__(self, master)
        self.bind("<Configure>", self.on_browser_configure)

    def embed_browser(self):
        window_info = cef.WindowInfo()
        rect = [0, 0, self.winfo_width(), self.winfo_height()]
        window_info.SetAsChild(self.get_window_handle(), rect)
        self.browser = cef.CreateBrowserSync(window_info)
        assert self.browser
        self.message_loop_work()
        
    def set_url(self, url):
        if self.browser:
            self.browser.StopLoad()
            self.browser.LoadUrl(url)

    def set_html(self, html_string):
        self.set_url(cef.GetDataUrl(html_string))

    def get_window_handle(self):
        if self.winfo_id() > 0:
            return self.winfo_id()
        elif MAC:
            # On Mac window id is an invalid negative value (Issue #308).
            # This is kind of a dirty hack to get window handle using
            # PyObjC package. If you change structure of windows then you
            # need to do modifications here as well.
            # noinspection PyUnresolvedReferences
            from AppKit import NSApp
            # noinspection PyUnresolvedReferences
            import objc
            # Sometimes there is more than one window, when application
            # didn't close cleanly last time Python displays an NSAlert
            # window asking whether to Reopen that window.
            # noinspection PyUnresolvedReferences
            return objc.pyobjc_id(NSApp.windows()[-1].contentView())
        else:
            raise Exception("Couldn't obtain window handle")

    def message_loop_work(self):
        cef.MessageLoopWork()
        self.after(10, self.message_loop_work)

    def on_browser_configure(self, _):
        if not self.browser:
            self.embed_browser()

    def on_configure(self):
        if self.browser:
            if WINDOWS:
                WindowUtils.OnSize(self.get_window_handle(), 0, 0, 0)
            elif LINUX:
                self.browser.SetBounds(0, 0, self.winfo_width(), self.winfo_height())
            self.browser.NotifyMoveOrResizeStarted()

    def clear_browser_references(self):
        # Clear browser references that you keep anywhere in your
        # code. All references must be cleared for CEF to shutdown cleanly.
        self.browser = None


if __name__ == '__main__':
    main()

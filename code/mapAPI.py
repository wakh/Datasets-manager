from cefpython3 import cefpython as cef
try:
    import tkinter as tk
except ImportError:
    import Tkinter as tk
import platform
import pandas
import folium
from folium.plugins import MarkerCluster

# Fix for PyCharm hints warnings
WindowUtils = cef.WindowUtils()

# Platforms
WINDOWS = (platform.system() == "Windows")
LINUX = (platform.system() == "Linux")
MAC = (platform.system() == "Darwin")

# Constant
MAXROWS = 1000  # Limit rows for performance


class MainFrame(tk.Frame):

    def __init__(self, data):
        self.root = tk.Tk()
        self.result_frame = None
        self.map_frame = None
        self.button1 = None
        self.button2 = None
        self.map = None

        # Root
        self.root.geometry("1200x500")

        # MainFrame
        tk.Frame.__init__(self, self.root)
        self.master.title("Datasets Manager")
        self.master.protocol("WM_DELETE_WINDOW", self.on_close)
        self.master.bind("<Configure>", self.on_configure)

        # PanedWindow
        self.paned_window = tk.PanedWindow(self, orient=tk.HORIZONTAL, showhandle=1)
        self.paned_window.pack(fill=tk.BOTH, expand=1)

        # TableFrame
        self.table_frame = BrowserFrame(self.paned_window, data.head(MAXROWS).to_html())
        self.paned_window.bind("<Configure>", self.on_configure)
        self.table_frame.configure(width=700)
        self.paned_window.add(self.table_frame, minsize=200)

        # MapFrame
        self.map_frame = BrowserFrame(self.paned_window, self.get_map_url(data))
        self.paned_window.bind("<Configure>", self.on_configure)
        self.paned_window.add(self.map_frame, minsize=200)

        # Pack MainFrame
        self.pack(fill=tk.BOTH, expand=tk.YES)

    def get_map_url(self, data):
        # create empty map zoomed in on NYC
        map = folium.Map(location=[40.738, -73.98], zoom_start=12)

        if ('latitude' in data) or ('longitude' in data):
            # fill nan value
            data["latitude"].fillna(0, inplace=True)
            data["longitude"].fillna(0, inplace=True)

            # add a marker for every record in the filtered data, use a clustered view
            mc = MarkerCluster().add_to(map)
            for each in data[0:MAXROWS].iterrows():
                folium.Marker(location=[each[1]['latitude'], each[1]['longitude']]).add_to(mc)

        return map.get_root().render()

    def on_configure(self, _):
        if self.table_frame:
            self.table_frame.on_configure()
        if self.map_frame:
            self.map_frame.on_configure()

    def on_close(self):
        if self.table_frame:
            self.table_frame.clear_browser_references()
        if self.map_frame:
            self.map_frame.clear_browser_references()
        self.master.destroy()


class BrowserFrame(tk.Frame):

    def __init__(self, master, html):
        self.browser = None
        self.url = cef.GetDataUrl(html)
        tk.Frame.__init__(self, master)
        self.bind("<Configure>", self.on_browser_configure)

    def embed_browser(self):
        window_info = cef.WindowInfo()
        rect = [0, 0, self.winfo_width(), self.winfo_height()]
        window_info.SetAsChild(self.get_window_handle(), rect)
        self.browser = cef.CreateBrowserSync(window_info, url=self.url)
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

from cefpython3 import cefpython as cef
import ctypes
from tkinter import filedialog
from tkinter import *
import tkinter as tk
import sys
import os
import platform
import logging
import sqlite3

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
    logging.info("[GUI] - CEF Python {ver}".format(ver=cef.__version__))
    logging.info("[GUI] - Python {ver} {arch}".format(
            ver=platform.python_version(), arch=platform.architecture()[0]))
    logging.info("[GUI] - Tk {ver}".format(ver=tk.Tcl().eval('info patchlevel')))
    assert cef.__version__ >= "55.3", "CEF Python v55.3+ required to run this"
    sys.excepthook = cef.ExceptHook  # To shutdown all CEF processes on error
    root = tk.Tk()
    app = MainFrame(root)
    # Tk must be initialized before CEF otherwise fatal error (Issue #306)
    cef.Initialize()
    app.mainloop()
    cef.Shutdown()


class MainFrame(tk.Frame):

    def __init__(self, root):
        self.browser_frame = None

        # Root
        root.geometry("1024x768")
        tk.Grid.rowconfigure(root, 0, weight=1)
        tk.Grid.columnconfigure(root, 0, weight=1)

        # MainFrame
        tk.Frame.__init__(self, root)
        self.master.title("Think1st App Platform")
        self.master.protocol("WM_DELETE_WINDOW", self.on_close)
        self.master.bind("<Configure>", self.on_root_configure)
        self.setup_icon()
        self.bind("<Configure>", self.on_configure)
        self.bind("<FocusIn>", self.on_focus_in)
        self.bind("<FocusOut>", self.on_focus_out)

        # BrowserFrame
        self.browser_frame = BrowserFrame(self)
        self.browser_frame.grid(row=0, column=0,
                                sticky=(tk.N + tk.S + tk.E + tk.W))
        tk.Grid.rowconfigure(self, 0, weight=1)
        tk.Grid.columnconfigure(self, 0, weight=1)

        # Pack MainFrame
        self.pack(fill=tk.BOTH, expand=tk.YES)

    def on_root_configure(self, _):
        logging.debug("[GUI] -[GUI] - MainFrame.on_root_configure")
        if self.browser_frame:
            self.browser_frame.on_root_configure()

    def on_configure(self, event):
        logging.debug("[GUI] -[GUI] - MainFrame.on_configure")
        if self.browser_frame:
            width = event.width
            height = event.height
            self.browser_frame.on_mainframe_configure(width, height)

    def on_focus_in(self, _):
        logging.debug("[GUI] -MainFrame.on_focus_in")

    def on_focus_out(self, _):
        logging.debug("[GUI] -MainFrame.on_focus_out")

    def on_close(self):
        if self.browser_frame:
            self.browser_frame.on_root_close()
        self.master.destroy()

    def get_browser(self):
        if self.browser_frame:
            return self.browser_frame.browser
        return None

    def get_browser_frame(self):
        if self.browser_frame:
            return self.browser_frame
        return None

    def setup_icon(self):
        resources = os.path.join(os.path.dirname(__file__), "resources")
        icon_path = os.path.join(resources, "logo"+IMAGE_EXT)
        if os.path.exists(icon_path):
            self.icon = tk.PhotoImage(file=icon_path)
            # noinspection PyProtectedMember
            self.master.call("wm", "iconphoto", self.master._w, self.icon)


class BrowserFrame(tk.Frame):

    def __init__(self, master):
        self.closing = False
        self.browser = None
        tk.Frame.__init__(self, master)
        self.bind("<FocusIn>", self.on_focus_in)
        self.bind("<FocusOut>", self.on_focus_out)
        self.bind("<Configure>", self.on_configure)
        """For focus problems see Issue #255 and Issue #535. """
        self.focus_set()

    def on_save_project(self):
        self.dbFileName = filedialog.asksaveasfilename(initialdir = "/",title = "Select file",filetypes = (("think1st app files","*.app"),("all files","*.*")))
        self.dbconn = sqlite3.connect(self.dbFileName + str(".app"))

    def on_open_project(self):
        self.dbFileName = filedialog.askopenfilename(initialdir = "/",title = "Select file",filetypes = (("think1st app files","*.app"),("all files","*.*")))
        self.dbconn = sqlite3.connect(self.dbFileName)

    def embed_browser(self):
        window_info = cef.WindowInfo()
        rect = [0, 0, self.winfo_width(), self.winfo_height()]
        window_info.SetAsChild(self.get_window_handle(), rect)
        self.browser = cef.CreateBrowserSync(window_info,
                                             url="http://localhost:8080/")
        assert self.browser
        self.browser.SetClientHandler(LoadHandler(self))
        self.browser.SetClientHandler(FocusHandler(self))
        self.message_loop_work()

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

    def on_configure(self, _):
        if not self.browser:
            self.embed_browser()

    def on_root_configure(self):
        # Root <Configure> event will be called when top window is moved
        if self.browser:
            self.browser.NotifyMoveOrResizeStarted()

    def on_mainframe_configure(self, width, height):
        if self.browser:
            if WINDOWS:
                ctypes.windll.user32.SetWindowPos(
                    self.browser.GetWindowHandle(), 0,
                    0, 0, width, height, 0x0002)
            elif LINUX:
                self.browser.SetBounds(0, 0, width, height)
            self.browser.NotifyMoveOrResizeStarted()

    def on_focus_in(self, _):
        logging.debug("[GUI] -BrowserFrame.on_focus_in")
        if self.browser:
            self.browser.SetFocus(True)

    def on_focus_out(self, _):
        logging.debug("[GUI] -BrowserFrame.on_focus_out")
        """For focus problems see Issue #255 and Issue #535. """
        if LINUX and self.browser:
            self.browser.SetFocus(False)

    def on_root_close(self):
        if self.browser:
            self.browser.CloseBrowser(True)
            self.clear_browser_references()
        self.destroy()

    def clear_browser_references(self):
        # Clear browser references that you keep anywhere in your
        # code. All references must be cleared for CEF to shutdown cleanly.
        self.browser = None


class LoadHandler(object):

    def __init__(self, browser_frame):
        self.browser_frame = browser_frame


class FocusHandler(object):
    """For focus problems see Issue #255 and Issue #535. """

    def __init__(self, browser_frame):
        self.browser_frame = browser_frame

    def OnTakeFocus(self, next_component, **_):
        logging.debug("[GUI] -FocusHandler.OnTakeFocus, next={next}"
                     .format(next=next_component))

    def OnSetFocus(self, source, **_):
        logging.debug("[GUI] -FocusHandler.OnSetFocus, source={source}"
                     .format(source=source))
        if LINUX:
            return False
        else:
            return True

    def OnGotFocus(self, **_):
        logging.debug("[GUI] -FocusHandler.OnGotFocus")
        if LINUX:
            self.browser_frame.focus_set()

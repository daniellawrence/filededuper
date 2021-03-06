# This file is part of the File Deduper project. It is subject to
# the the revised 3-clause BSD license terms as set out in the LICENSE
# file found in the top-level directory of this distribution. No part of this
# project, including this file, may be copied, modified, propagated, or
# distributed except according to the terms contained in the LICENSE fileself.
import tkinter
from tkinter import simpledialog

from PIL import Image, ImageTk
import dialog


class HeroImageWithList(simpledialog.Dialog):
    data = []
    result = None
    _original_image_pil = None
    _resized_image = None
    mtitle = None
    listbox = None

    def __init__(self, parent, title=None):
        if parent is None:
            self.mparent = tkinter.Tk()
        else:
            self.mparent = parent

    def window_init(self):
        tkinter.Toplevel.__init__(self, self.mparent)

        if self.mtitle:
            self.title(self.mtitle)

        self.parent = self.mparent

        upper_frame = tkinter.Frame(self)
        # START FRAME_IN_CANVAS
        self.canvas = tkinter.Canvas(upper_frame, borderwidth=0,
            background="#ffffff")
        self.frame = tkinter.Frame(self.canvas, background="#ffffff")
        self.vsb = tkinter.Scrollbar(upper_frame, orient="vertical",
            command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.vsb.set)

        self.vsb.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)
        self.canvas.create_window((4, 4), window=self.frame, anchor="nw",
                                  tags="self.frame")

        self.frame.bind("<Configure>", self.OnFrameConfigure)

        # END FRAME_IN_CANVAS
        body = self.frame
        self.buttonbox()
        screen_height = self.parent.winfo_screenheight()
        max_height = screen_height * 0.9
        self.initial_focus = self.body(body,
            max_height=(max_height -
            self.button_box.winfo_reqheight()
            - 50),  # title bar
            max_width=self.parent.winfo_screenwidth())

        self.grab_set()

        upper_frame.pack(expand=True, fill="both")
        self.button_box.pack()

        if not self.initial_focus:
            self.initial_focus = self

        self.protocol("WM_DELETE_WINDOW", self.cancel)

        self.update_idletasks()

        if self.frame.winfo_reqheight() > self.canvas.winfo_reqheight():
            requested_height = self.frame.winfo_reqheight() \
                + self.button_box.winfo_reqheight()
        else:
            requested_height = self.canvas.winfo_reqheight() \
                + self.button_box.winfo_reqheight()

        requested_width = self.frame.winfo_reqwidth() \
            + self.vsb.winfo_reqwidth()

        if requested_height > max_height:
            requested_height = max_height

        self.geometry("%dx%d%+d%+d" % (requested_width,
                                   requested_height,
                                   0,
                                   0))

        self.initial_focus.focus_set()
        self.wait_window(self)

    def body(self, master, max_height, max_width):
        self.result = None

        scrollbar = tkinter.Scrollbar(master, orient=tkinter.VERTICAL)

        self.listbox = listbox = tkinter.Listbox(master,
            yscrollcommand=scrollbar.set)
        scrollbar.config(command=listbox.yview)
        scrollbar.pack(side=tkinter.LEFT, fill=tkinter.Y)

        listbox.pack(side=tkinter.LEFT, fill=tkinter.Y)

        try:
            self._original_image_pil = Image.open("%s"
                % self.data[0]['fullpath'])
            original_x = self._original_image_pil.size[0]
            original_y = self._original_image_pil.size[1]
            if original_x > max_width or original_y > max_height:
                if max_width < max_height:
                    # width is the limiter
                    desired_width = int(max_width)
                    desired_height = int(original_y *
                        (desired_width / original_x))
                else:
                    # height is the limiter
                    desired_height = int(max_height)
                    desired_width = int(original_x *
                        (desired_height / original_y))
                self._resized_image = ImageTk.PhotoImage(
                    self._original_image_pil.resize((desired_width,
                        desired_height)))
            else:
                self._resized_image = ImageTk.PhotoImage(
                    self._original_image_pil)

            label = tkinter.Label(master, image=self._resized_image)
            label.pack()
        except Exception as e:
            print('Unable to display image')
            print(e)

        for item in self.data:
            listbox.insert(tkinter.END, item['name'])
            if item['suggest']:
                print('set suggest flag')
                listbox.select_set(listbox.size() - 1)

    def resize(self, event):
        print(event.width, event.height)

    def apply(self):
        self.result = self.listbox.curselection()

    def set_data(self, data):
        self.data = data

    def OnFrameConfigure(self, event):
        '''Reset the scroll region to encompass the inner frame'''
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def buttonbox(self):
        self.button_box = tkinter.Frame(self)

        w = tkinter.Button(self.button_box, text="OK", width=10,
            command=self.ok, default=tkinter.ACTIVE)
        w.pack(side=tkinter.LEFT, padx=5, pady=5)
        w = tkinter.Button(self.button_box, text="Cancel", width=10,
            command=self.cancel)
        w.pack(side=tkinter.LEFT, padx=5, pady=5)

        self.bind("<Return>", self.ok)
        self.bind("<Escape>", self.cancel)

    def get_result(self):
        return self.result


class faux_tk_dialog(object):
    data = None
    mtitle = None
    _dlg = None
    _result = None

    def __init__(self, title="File deduper"):
        self._dlg = dialog.Dialog(dialog="dialog")
        self._dlg.set_background_title(title)

    def window_init(self):
        tuplelist = [('{0}'.format(num), item['name']) for num, item in
            enumerate(self.data)]
        suggested_item = [item for item in self.data if item['suggest']][0]
        assert suggested_item
        tuplelist.insert(0, ('-1', suggested_item['name']))

        rc, selected = self._dlg.menu(text='Select a file to keep',
            choices=tuplelist)

        if rc == 'ok':
            if selected == '-1':
                i = 0
                for i, item in enumerate(self.data):
                    if item['suggest']:
                        break
                self._result = (i, )
            else:
                self._result = (int(selected), )
        else:
            print('No image selected to keep or cancel pressed')
            self._result = None

    def get_result(self):
        return self._result

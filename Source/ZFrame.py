


from Properties import *

from tkinter import *


class ZFrame(Frame):
	def __init__(self, parent, bg):
		Frame.__init__(self, parent, bg=bg);
		self.parent = parent

		self.result_offset = 0;  # how deep into the query are we


	@staticmethod
	def new_element(element, side="top", padx=PADDING, pady=PADDING):
		element.pack(side=side, padx=padx, pady=pady, expand=True);
		return element;


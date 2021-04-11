

from tkinter import *

from Properties import *
from ZFrame import ZFrame



class Result_Frame(ZFrame):


	def __init__(self, parent, result_dictionary):
		ZFrame.__init__(self, parent, "blue");

		self.title = ""
		self.author = ""

		self.categories = self.new_element(ZFrame(self, "purple"));

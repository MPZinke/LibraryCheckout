

from tkinter import *

from Properties import *
from ZFrame import ZFrame



class Tab_Frame(ZFrame):
	def __init__(self, tk):
		ZFrame.__init__(self, tk, BACKGROUND);

		default_params = {"master":self, "bg":BUTTON_BG, "foreground":BUTTON_FG};
		
		open_browse_params = {"text":"Browse Books", "command":self.parent.open_browse, **default_params};
		open_browse_params["bg"] = BACKGROUND;
		self.open_browse_button = self.new_element(Button(**open_browse_params), "left");

		open_search_params = {"text":"Search For A Book", "command":self.parent.open_search, **default_params};
		self.open_search_button = self.new_element(Button(**open_search_params), "left");

		open_return_params = {"text":"Return A Book", "command":self.parent.open_return, **default_params};
		self.open_return_button = self.new_element(Button(**open_return_params), "left");

		open_add_params = {"text":"Add A Book", "command":self.parent.open_add, **default_params};
		self.open_add_button = self.new_element(Button(**open_add_params), "left");

		self.buttons = [self.open_browse_button, self.open_search_button, self.open_return_button, self.open_add_button];


	def highlight_browse_button(self):
		self.unhighlight_buttons();
		self.open_browse_button.configure(bg=BACKGROUND);


	def highlight_search_button(self):
		self.unhighlight_buttons();
		self.open_search_button.configure(bg=BACKGROUND);


	def highlight_return_button(self):
		self.unhighlight_buttons();
		self.open_return_button.configure(bg=BACKGROUND);


	def highlight_add_button(self):
		self.unhighlight_buttons();
		self.open_add_button.configure(bg=BACKGROUND);


	def unhighlight_buttons(self):
		for button in self.buttons: button.configure(bg=BUTTON_BG);
		


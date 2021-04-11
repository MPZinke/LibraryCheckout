

from tkinter import *

from Properties import *
from ZFrame import ZFrame
from DBFunctions import search, search_by_title, search_by_author, search_by_category



class Search_Frame(ZFrame):
	SEARCH_BY_ANY = "Any";
	SEARCH_BY_TITLE = "By Title";
	SEARCH_BY_AUTHOR = "By Author";
	SEARCH_BY_CATEGORY = "By Category";
	TYPES = {SEARCH_BY_ANY: search, SEARCH_BY_TITLE: search_by_title, SEARCH_BY_AUTHOR: search_by_author, 
			SEARCH_BY_CATEGORY: search_by_category};

	def __init__(self, tk):
		ZFrame.__init__(self, tk, "blue");

		# --------------- SEARCH FRAME ---------------
		self.search_type_button_frame = self.new_element(ZFrame(self, "blue"));
		button_params = {"master":self.search_type_button_frame, "bg":BUTTON_BG, "foreground":BUTTON_FG};

		self.search_entry = self.new_element(Entry(**button_params), "left");

		self.search_type = StringVar(self.search_type_button_frame);
		self.search_type.set(self.SEARCH_BY_ANY);
		option_params = [self.search_type_button_frame, self.search_type, self.SEARCH_BY_ANY,
			 self.SEARCH_BY_TITLE, self.SEARCH_BY_AUTHOR, self.SEARCH_BY_CATEGORY];
		self.search_option = self.new_element(OptionMenu(*option_params), "left");

		search_params = {**button_params, "text":"Search", "command":self.search};
		self.search_button = self.new_element(Button(**search_params), "left");

		# --------------- RESULT FRAME ---------------
		self.results = [];
		self.result_buttons = []


	def search(self):
		# search for string by type
		results, total = self.TYPES[self.search_type.get()](self.parent.cursor, self.search_entry.get());
		print(results)
		print("Total: " + str(total));
		  # display results


	def display_results(self, results):
		# clear previous results
		for x in range(len(self.results)):
			self.results[x].pack_forget();
			self.result_buttons[x].pack_forget();

		# for x in results:

		# 	self.results = [self.new_element(Button())]
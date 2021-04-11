
from tkinter import *;

from Properties import *;
from ZFrame import ZFrame;
from Result_Frame import Result_Frame;

import DBFunctions;


class Browse_Frame(ZFrame):
	BROWSE_BY_TITLE = 0;
	BROWSE_BY_AUTHOR = 1;
	BROWSE_BY_CATEGORY = 2;
	QUERY_FUNCTION = [DBFunctions.browse_title, DBFunctions.browse_author, DBFunctions.browse_category];

	def __init__(self, tk):
		ZFrame.__init__(self, tk, BACKGROUND);
		from string import ascii_uppercase;
		
		# set list of types to search by
		self.browse_type_button_frame = self.new_element(ZFrame(self, BACKGROUND));
		by_title_params = GLOBAL_BUTTON_PARAM(self.browse_type_button_frame, "By Title", \
				lambda x=self.BROWSE_BY_TITLE: self.set_type(x));
		self.browse_by_title_button = self.new_element(Button(**by_title_params), "left");
		by_author_params = GLOBAL_BUTTON_PARAM(self.browse_type_button_frame, "By Author", 
				lambda x=self.BROWSE_BY_AUTHOR: self.set_type(x));
		self.browse_by_author_button = self.new_element(Button(**by_author_params), "left");
		by_category_params = GLOBAL_BUTTON_PARAM(self.browse_type_button_frame, "By Category", 
				lambda x=self.BROWSE_BY_CATEGORY: self.set_type(x));
		self.browse_by_category_button = self.new_element(Button(**by_category_params), "left");

		# set list of first characters to get list by
		self.alphanum_frame = self.new_element(ZFrame(self, "blue"));
		chars = list(ascii_uppercase) + ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"];
		for x in range(36):
			alnum_button_params = {"master":self.alphanum_frame, **BUTTON_PARAM, "text":chars[x],
				"command":lambda x=chars[x]: self.browse(x)};
			self.alphanum_buttons = [self.new_grid_element(Button(**alnum_button_params), int(x/9), x%9)];


		self.result_frame = None;
		self.browse_type = self.BROWSE_BY_TITLE;  # which query function should we use


	# browse DB based on type of type and character.
	# takes leading character to search by.
	# uses set browse type and passed letter to query DB. results are then displayed.
	def browse(self, character):
		self.alphanum_frame.pack_forget();
		results = self.QUERY_FUNCTION[self.browse_type](self.parent.cursor, character);
		print(results);


	def set_type(self, browse_type):
		self.browse_type = browse_type;
		self.result_offset = 0;

		buttons = [self.browse_by_title_button, self.browse_by_author_button, self.browse_by_category_button];
		for button in buttons: button.configure(bg=BUTTON_BG);
		buttons[browse_type].configure(bg=BACKGROUND);
		self.alphanum_frame.pack(padx=PADDING, pady=PADDING);
		if(self.result_frame): self.result_frame.pack_forget();  # clear previous results


	def new_grid_element(self, element, row, column, rowspan=1, colspan=1, padx=PADDING, pady=PADDING):
		element.grid(row=row, column=column, rowspan=rowspan, columnspan=colspan, padx=padx, pady=pady, sticky="NSEW");
		return element;
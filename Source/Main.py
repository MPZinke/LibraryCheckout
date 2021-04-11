

from tkinter import *

from Properties import *
import DBFunctions

from Add_Frame import Add_Frame
from Browse_Frame import Browse_Frame
from Checkout_Frame import Checkout_Frame
from Return_Frame import Return_Frame
from Search_Frame import Search_Frame
from Tab_Frame import Tab_Frame


class App(Tk):
	def __init__(self):
		Tk.__init__(self)
		self.title(WINDOW_TITLE);
		self.configure(background=WINDOW_BACKGROUND);
		self.geometry("1000x700");

		self.tab_frame = self.new_element(Tab_Frame(self));

		self.add_frame = self.new_element(Add_Frame(self));
		self.browse_frame = self.new_element(Browse_Frame(self));
		self.checkout_frame = self.new_element(Checkout_Frame(self));
		self.return_frame = self.new_element(Return_Frame(self));
		self.search_frame = self.new_element(Search_Frame(self));

		self.open_browse();

		self.cnx, self.cursor = DBFunctions.connect_to_DB()
		self.currently_selected_book_id = 0;  # the book that is queued for checkout


	def new_element(self, element, padx=PADDING, pady=PADDING):
		element.pack(padx=padx, pady=pady);
		return element;

	
	def remove_all_lower_frames(self):
		for frame in [self.add_frame, self.browse_frame, self.checkout_frame, self.search_frame, self.return_frame]:
			frame.pack_forget();


	# ----------------------------------------------------------- BUTTON CALLBACKS -----------------------------------------------------------

	def open_add(self):
		self.tab_frame.highlight_add_button();
		self.remove_all_lower_frames();
		self.add_frame.pack(padx=PADDING, pady=PADDING);
		print("Opened add");

	def open_browse(self):
		self.tab_frame.highlight_browse_button();
		self.remove_all_lower_frames();
		self.browse_frame.pack(padx=PADDING, pady=PADDING);
		print("Opened browse");


	def open_return(self):
		self.tab_frame.highlight_return_button();
		self.remove_all_lower_frames();
		self.return_frame.pack(padx=PADDING, pady=PADDING);
		print("Opened return");


	def open_search(self):
		self.tab_frame.highlight_search_button();
		self.remove_all_lower_frames();
		self.search_frame.pack(padx=PADDING, pady=PADDING);
		print("Opened search");



def main():
	app = App();
	app.mainloop();


if __name__ == '__main__':
	main()
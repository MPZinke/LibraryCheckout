
# GUI
WINDOW_TITLE = "Library Catalogue";
WINDOW_BACKGROUND = "black" ;
BACKGROUND = "black";
BUTTON_BG = "#444444";
BUTTON_FG = "white";
BUTTON_PARAM = {"bg":BUTTON_BG, "foreground":BUTTON_FG};

PADDING = 16;


# DB
DB_USER = "root";
DB_PASSWD = "mysql";
DB_IP = "mpzinke-mac";
DB_IP = "10.0.0.23";
DB_PORT = "3306";
DB_NAME = "library";


QUERY_LIMIT = 10;


def GLOBAL_BUTTON_PARAM(master, text, command):
	return {"master":master, "text":text, "command":command, **BUTTON_PARAM};
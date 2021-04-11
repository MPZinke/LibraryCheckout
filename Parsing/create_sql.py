



# DB
DB_USER = "root";
DB_PASSWD = "mysql";
DB_IP = "mpzinke-mac";
DB_IP = "10.0.0.23";
DB_PORT = "3306";
DB_NAME = "spoc_library";



def __UTILITY__associate_query(cursor):
	headers = [header[0] for header in cursor._description];
	return [{header : (row[x].decode() if row[x] else None)	for x, header in enumerate(headers)} \
																for row in cursor._rows];




def get_books(cursor):
	query = "SELECT `ID`, `Author`, `Title`, `ISBN`, `DeweyNo`, `Note`, `NoCopies`, `AccessionNumber`, \
				`Cost`, `PublisherID`, `SubjectHeading1`, `SubjectHeading2`, `SubjectHeading3`, `SubjectHeading4`, \
				`SubjectHeading5` FROM `LibraryResources` ORDER BY `LibraryResources`.`Title` ASC;";
	cursor.execute(query);
	return __UTILITY__associate_query(cursor);


def determine_categories(book_list):
	categories = {};
	for book in book_list:
		for y in range(1, 6):
			if not book["SubjectHeading{0}".format(y)]: continue;
			category = book["SubjectHeading{0}".format(y)].rstrip().replace("'", "\\'");
			if(category not in categories): categories[category] = len(categories) + 1;

	return categories;


def determine_bookcats(book_list, categories):
	bookcats = {};
	for x, book in enumerate(book_list):
		bookcats[x+1] = [];
		for y in range(1, 6):
			if not book["SubjectHeading{0}".format(y)]: continue;
			category = book["SubjectHeading{0}".format(y)].rstrip().replace("'", "\\'");
			bookcats[x+1].append(categories[category]);

	return bookcats;


def create_categories(categories):
	return ["({0}, '{1}')".format(categories[category], category) for x, category in enumerate(categories)];


def create_books(book_list, categories):
	sql = [];
	for x, book in enumerate(book_list):
		variables = [x+1];
		for header in ["Title", "Author", "ISBN", "Note", "NoCopies", "Cost", "DeweyNo"]:
			if book[header]: variables.append(book[header].rstrip().replace("'", "\\'"));
			else: variables.append("NULL");

		for x in range(1, 5):
			if(variables[x] != "NULL"): variables[x] = "'"+variables[x]+"'"

		if(book["SubjectHeading1"]): variables.append(categories[book["SubjectHeading1"].rstrip().replace("'", "\\'")]);
		else: variables.append("NULL");
		sql.append("({0}, {1}, {2}, {3}, {4}, {5}, {6}, {7}, {8})".format(*variables));
	return sql;


def create_bookcats(bookcat_list):
	sql = [];
	for book in bookcat_list:
		for cat in bookcat_list[book]:
			sql.append("({0}, {1})".format(book, cat));
	return sql;


def write_data(book_sql, category_sql, bookcat_sql):
	with open("../SQL/output.sql", "w") as file:
		file.write("INSERT INTO `Categories` (`id`, `name`) VALUES\n");
		file.write(",\n".join(category_sql));
		file.write(";\n");

		file.write("INSERT INTO `Books` (`id`, `title`, `author`, `ISBN`, `description`, `copies`, `cost`, `dewey`, `category_id`) VALUES\n");
		file.write(",\n".join(book_sql));
		file.write(";\n");

		file.write("INSERT INTO `BookCategories` (`book_id`, `category_id`) VALUES\n");
		file.write(",\n".join(bookcat_sql));
		file.write(";\n");


def start_connection():
	try:
		import mysql.connector
		return mysql.connector.connect(	user=DB_USER, password=DB_PASSWD,
						                              host=DB_IP, port=DB_PORT,
						                              database=DB_NAME)
	except Exception as error:
		print(error);
		return None;


def connect_to_DB():
	cnx = start_connection()
	if(not cnx): raise Exception("Unable to connect to DB");
	cursor = cnx.cursor(buffered=True);
	return cnx, cursor;


def main():
	cnx, cursor = connect_to_DB();
	book_list = get_books(cursor);
	category_list = determine_categories(book_list);
	bookcat_list = determine_bookcats(book_list, category_list);

	category_sql = create_categories(category_list);
	book_sql = create_books(book_list, category_list);
	bookcat_sql = create_bookcats(bookcat_list);

	write_data(book_sql, category_sql, bookcat_sql);


if __name__ == '__main__':
	main()

from Properties import *

def __UTILITY__associate_query(cursor):
	headers = [header[0] for header in cursor._description];
	return [{header : (row[x].decode() if row[x] else None)	for x, header in enumerate(headers)} \
																for row in cursor._rows];



def add_book(cnx, cursor, title, author, description, category_id):
	query = "INSERT INTO `Books` (`title`, `author`, `description`, `category_id`) VALUES (%s, %s, %s, %s)";
	cursor.execute(query, (title, author, description, category_id));
	return cnx.commit();


def remove_book_from_inventory(cnx, cursor, book_id):
	query = "UPDATE `Books` SET `current` = FALSE WHERE `book_id` = %s";
	cursor.execute(query, (book_id));
	return cnx.commit();



def browse_title(cursor, character, offset=0, limit=QUERY_LIMIT):
	query = "SELECT * FROM `Books` WHERE UPPER(`title`) LIKE %s ORDER BY UPPER(`title`) ASC LIMIT %s, %s;";
	cursor.execute(query, (character+"%", offset, limit));
	return __UTILITY__associate_query(cursor);


def browse_author(cursor, character, offset=0, limit=QUERY_LIMIT):
	query = "SELECT * FROM `Books` WHERE UPPER(`author`) LIKE %s ORDER BY UPPER(`author`) ASC LIMIT %s, %s;" 
	cursor.execute(query, (character+"%", offset, limit));
	return __UTILITY__associate_query(cursor);


def browse_category(cursor, character, offset=0, limit=QUERY_LIMIT):
	query =	"""SELECT * FROM `Books` JOIN `Categories` ON `Categories`.`id` = `Books`.`category_id` WHERE 
				UPPER(`Categories`.`name`) LIKE %s ORDER BY UPPER(`Categories`.`name`) ASC LIMIT %s, %s;""";
	cursor.execute(query, (character+"%", offset, limit));
	return __UTILITY__associate_query(cursor);


# ----------------------------------------------------------------- CHECKIN/OUT -----------------------------------------------------------------

def checkout_book(cnx, cursor, book_id, name):
	# check if book is still held (current)
	cursor.execute("SELECT * FROM `Books` WHERE `book_id` = %s AND `current` = TRUE;", (book_id,));
	if(not cursor._rows): raise Exception("Book is no longer in inventory");

	# check if book is checked out
	# cursor.execute("SELECT * FROM `Checkouts` WHERE `book_id` = %s AND `checked_in` = NULL;", (book_id,));
	# if(cursor._rows): raise Exception("Book is currently checked out");

	# add instance of book checkout
	cursor.execute("INSERT INTO `Checkouts` (`book_id`, `name`) VALUES (%s, %s);", (book_id, name));
	return cnx.commit();


def checkin_book(cnx, cursor, checkout_id):
	query = "UPDATE `Checkouts` SET `checked_in` = CURRENT_TIMESTAMP WHERE `id` = %s;";
	cursor.execute(query, (checkout_id));
	return cnx.commit();


# --------------------------------------------------------------------- SEARCH ---------------------------------------------------------------------

def search_book_id(cursor, book_id):
	cursor.execute("SELECT * FROM `Books` WHERE `id` = %s;", (book_id,));
	book = __UTILITY__associate_query(cursor);
	if(not book): return book;

	# get categories
	cursor.execute("SELECT * FROM `BookCategories` WHERE `book_id` = %s;", (book_id,));
	return {**book[0], "categories" : [category["category_id"] for category in __UTILITY__associate_query(cursor)]};


def search(cursor, keyword, offset=0, limit=QUERY_LIMIT):
	query =	"""SELECT * FROM `Categories`
				LEFT JOIN `BookCategories` ON `BookCategories`.`category_id` = `Categories`.`id`
				LEFT JOIN `Books` ON `Books`.`id` = `BookCategories`.`book_id`
				WHERE LOWER(`Categories`.`name`) LIKE LOWER(%s)
				OR LOWER(`Books`.`title`) LIKE LOWER(%s) OR LOWER(`Books`.`author`) LIKE LOWER(%s)
				ORDER BY LOWER(`Books`.`title`), LOWER(`Books`.`author`), LOWER(`Categories`.`name`) 
				ASC LIMIT %s, %s;"""
	cursor.execute(query, ("%"+keyword+"%", "%"+keyword+"%", "%"+keyword+"%", offset, limit));
	return __UTILITY__associate_query(cursor);


def search_by_title(cursor, keyword, offset=0, limit=QUERY_LIMIT):
	query = "SELECT * FROM `Books` WHERE LOWER(`title`) LIKE LOWER(%s) ORDER BY `title` ASC LIMIT %s, %s;";
	cursor.execute(query, ("%"+keyword+"%", offset, limit));
	books = __UTILITY__associate_query(cursor);

	query = "SELECT COUNT(`id`) FROM `Books` WHERE LOWER(`title`) LIKE LOWER(%s) ORDER BY `title` ASC LIMIT %s, %s;";
	cursor.execute(query, ("%"+keyword+"%", offset, limit));
	return books, __UTILITY__associate_query(cursor)[0]["COUNT(`id`)"];


def search_by_author(cursor, keyword, offset=0, limit=QUERY_LIMIT):
	query = "SELECT * FROM `Books` WHERE LOWER(`author`) LIKE LOWER(%s) ORDER BY `author` ASC LIMIT %s, %s;";
	cursor.execute(query, ("%"+keyword+"%", offset, limit));
	books = __UTILITY__associate_query(cursor);

	query = "SELECT COUNT(`id`) FROM `Books` WHERE LOWER(`author`) LIKE LOWER(%s) ORDER BY `author` ASC LIMIT %s, %s;";
	cursor.execute(query, ("%"+keyword+"%", offset, limit));
	return books, __UTILITY__associate_query(cursor)[0]["COUNT(`id`)"];


def search_by_category(cursor, keyword, offset=0, limit=QUERY_LIMIT):
	query =	"""SELECT * FROM `Categories`
				LEFT JOIN `BookCategories` ON `BookCategories`.`category_id` = `Categories`.`id`
				LEFT JOIN `Books` ON `Books`.`id` = `BookCategories`.`book_id`
				WHERE LOWER(`Categories`.`name`) LIKE LOWER(%s) ORDER BY `Categories`.`name` ASC LIMIT %s, %s;"""
	cursor.execute(query, ("%"+keyword+"%", offset, limit));
	books = __UTILITY__associate_query(cursor);

	query =	"""SELECT COUNT(*) FROM `Categories`
				LEFT JOIN `BookCategories` ON `BookCategories`.`category_id` = `Categories`.`id`
				LEFT JOIN `Books` ON `Books`.`id` = `BookCategories`.`book_id`
				WHERE LOWER(`Categories`.`name`) LIKE LOWER(%s) ORDER BY `Categories`.`name` ASC LIMIT %s, %s;"""
	cursor.execute(query, ("%"+keyword+"%", offset, limit));
	return books, __UTILITY__associate_query(cursor)[0]["COUNT(*)"];


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
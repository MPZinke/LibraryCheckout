

CREATE TABLE `Categories`
(
	`id` INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
	`name` VARCHAR(256) NOT NULL UNIQUE,
	`description` VARCHAR(1024) DEFAULT NULL
);


CREATE TABLE `Publisher`
(
	`id` INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
	`name` VARCHAR(128) NOT NULL,
	`address` VARCHAR(128) DEFAULT NULL,
	`city` VARCHAR(64) DEFAULT NULL,
	`state` VARCHAR(24) DEFAULT NULL,
	`zip` VARCHAR(16) DEFAULT NULL,
	`phone_number` VARCHAR(24) DEFAULT NULL,
	`email` VARCHAR(64) DEFAULT NULL
);


CREATE TABLE `Books`
(
	`id` INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
	`title` VARCHAR(256) NOT NULL,
	`author` VARCHAR(256) DEFAULT NULL,
	`ISBN` VARCHAR(20) DEFAULT NULL,
	`dewey` DECIMAL(4,1) DEFAULT NULL,
	`copies` SMALLINT NOT NULL DEFAULT 1,
	`description` VARCHAR(512) DEFAULT NULL,
	`cost` DECIMAL(5,2) DEFAULT NULL,
	`category_id` INT DEFAULT NULL,
	FOREIGN KEY (`category_id`) REFERENCES `Categories`(`id`),
	`current` BOOLEAN NOT NULL DEFAULT TRUE,  -- whether it is still owned by the library
	`publisher` INT DEFAULT NULL,
	FOREIGN KEY (`publisher`) REFERENCES `Publisher`(`id`)
);


CREATE TABLE `BookCategories`
(
	`id` INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
	`category_id` INT NOT NULL,
	FOREIGN KEY (`category_id`) REFERENCES `Categories`(`id`),
	`book_id` INT NOT NULL,
	FOREIGN KEY (`book_id`) REFERENCES `Books`(`id`)
);


CREATE TABLE `Checkouts`
(
	`id` INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
	`book_id` INT NOT NULL,
	FOREIGN KEY (`book_id`) REFERENCES `Books`(`id`),
	`name` VARCHAR(64) NOT NULL,
	`checked_out` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
	`checked_in` DATETIME DEFAULT NULL
);


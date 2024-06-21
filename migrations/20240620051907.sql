-- Create "author" table
CREATE TABLE `author` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(30) NOT NULL,
  `bio` text NULL,
  `birthdate` date NULL,
  PRIMARY KEY (`id`)
) CHARSET latin1 COLLATE latin1_swedish_ci;
-- Create "book" table
CREATE TABLE `book` (
  `id` int NOT NULL AUTO_INCREMENT,
  `title` varchar(30) NOT NULL,
  `description` varchar(30) NOT NULL,
  `publish_date` varchar(30) NOT NULL,
  `author_id` int NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `author_id` (`author_id`),
  CONSTRAINT `book_ibfk_1` FOREIGN KEY (`author_id`) REFERENCES `author` (`id`) ON UPDATE RESTRICT ON DELETE RESTRICT
) CHARSET latin1 COLLATE latin1_swedish_ci;

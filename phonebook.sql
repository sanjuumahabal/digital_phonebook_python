SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";

CREATE TABLE IF NOT EXISTS users (
	User_id INT PRIMARY KEY AUTO_INCREMENT, 
    Name VARCHAR(30), 
    Username VARCHAR(30), 
    Password VARCHAR(20)
    );

CREATE TABLE IF NOT EXISTS contacts (
                Contact_id INT PRIMARY KEY AUTO_INCREMENT,
                FirstName VARCHAR(30),
                LastName VARCHAR(30),
                Email VARCHAR(30),
                PhoneNumber VARCHAR(30),
                User_id INT,
                FOREIGN KEY (User_id) REFERENCES users(User_id) ON DELETE CASCADE
            );
    

COMMIT;


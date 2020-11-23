CREATE DATABASE IF NOT EXISTS `Hogwarts` DEFAULT CHARACTER SET latin1;

USE `Hogwarts`;

CREATE TABLE `teams` (
  `teamID` mediumint(8) unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL DEFAULT '',
  PRIMARY KEY (`teamID`),
  UNIQUE KEY `teamName` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=189631 DEFAULT CHARSET=latin1;

CREATE TABLE `users` (
  `userID` mediumint(8) unsigned NOT NULL AUTO_INCREMENT,
  `teamID` mediumint(8) unsigned NOT NULL,
  `emailAddress` varchar(255) NOT NULL,
  PRIMARY KEY (`userID`),
  UNIQUE KEY `emailAddress` (`emailAddress`),
  CONSTRAINT `user_to_team` FOREIGN KEY (`teamID`) REFERENCES `teams` (`teamID`)
) ENGINE=InnoDB AUTO_INCREMENT=189631 DEFAULT CHARSET=latin1;

CREATE TABLE `points` (
  `date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `userID` mediumint(8) unsigned NOT NULL,
  `sourceUserID` mediumint(8) unsigned NOT NULL,
  `points` mediumint(8) unsigned NOT NULL,
  `emailAddress` varchar(255) NOT NULL DEFAULT '',
  PRIMARY KEY (`userID`, `sourceUserID`, `date`),
  CONSTRAINT `user_exists` FOREIGN KEY (`userID`) REFERENCES `users` (`userID`),
  CONSTRAINT `source_user_exists` FOREIGN KEY (`sourceUserID`) REFERENCES `users` (`userID`)
) ENGINE=InnoDB AUTO_INCREMENT=189631 DEFAULT CHARSET=latin1;

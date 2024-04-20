CREATE TABLE IF NOT EXISTS `cards` (
    `card_id`         int(11)  	   NOT NULL auto_increment	  COMMENT 'the id of this card',
    `board_id`        int(11)      NOT NULL                   COMMENT 'the id of the board the card is on',
    `card_text`       varchar(500) NOT NULL                   COMMENT 'The text of the card',
    `card_title`      varchar(20)  NOT NULL                   COMMENT 'The title of the card',
    `card_list`       varchar(20)  NOT NULL                   COMMENT 'The list the card is in. Will be either: ToDo, Doing, or Completed',
    PRIMARY KEY (`card_id`),
    FOREIGN KEY (board_id) REFERENCES boards(board_id)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COMMENT="Contains card information";
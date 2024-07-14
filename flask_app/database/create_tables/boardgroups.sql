CREATE TABLE IF NOT EXISTS `boardgroups` (
    `board_id`         int(11)  NOT NULL          COMMENT 'the id of this board',
    `user_email`       varchar(100) NOT NULL      COMMENT 'the email of this user',
    `board_name`       varchar(10) NOT NULL       COMMENT 'name of the board',
    FOREIGN KEY (board_id) REFERENCES boards(board_id)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COMMENT="Contains information regarding users in each board";
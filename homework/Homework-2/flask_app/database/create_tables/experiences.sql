CREATE TABLE IF NOT EXISTS `experiences` (
    `experience_id`        int(11)       NOT NULL AUTO_INCREMENT 	COMMENT 'The experience id' ,
    `position_id`          int(11)       NOT NULL 				    COMMENT 'FK:The position id',
    `name`                 varchar(100)  NOT NULL                	COMMENT 'The name of the experience',
    `description`          varchar(500)  NOT NULL                   COMMENT 'Description of experience',
    `hyperlink`            varchar(100)                             COMMENT 'a link where people can learn more about the experience',
    `start_date`           date          NOT NULL                   COMMENT 'My start date for this position',
    `end_date`             date          DEFAULT NULL               COMMENT 'The end date for this position',
    PRIMARY KEY  (`experience_id`),
    FOREIGN KEY (position_id) REFERENCES positions(position_id)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COMMENT="Experiences I had at each position";
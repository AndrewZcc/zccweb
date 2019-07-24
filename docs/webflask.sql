
/* 备份数据库 */
mysqldump -h127.0.0.1 -p3306 -uroot -pRoot@123 webflask > webflask.sql
/* 使用sql */
source ~/webflask.sql
[注意: 先把sql文件中所有与表结构相关的sql语句 删除, 只保留 数据类的sql语句! ]

drop database webflask;

create database webflask charset=utf8;

/* user */
INSERT INTO `user` VALUES (1,'zhchuch','123','Root'),(2,'general','123','General');

/* book */
INSERT INTO `book` (title, author_id) VALUES ('平凡的世界', 1);

/* book_author */
# binlog2sql    
针对binlog2sql mysql8版本的binlog写的脚本，5.7和5.6没有测试，欢迎大家尝试与提出bug,满意的话给个小星星。

## 参数介绍
~~~shell
-h 主机名或ip地址 -p 密码 -B 数据库名（如果不指定会返回binlog里面所有的dml语句）
--start_file 重那个binlog文件开始读取 --stop_file 到那个数据文件结束
-t 表名（如果指定了数据库没有指定表名，会返回库中所有的dml语句）
--start_time 重那个时间开始 --stop_time 到那个时间结束
-f 默认是false 需要 -f true 返回闪回语句
~~~

## 测试例子
~~~sql
CREATE TABLE orders (
  id INT NOT NULL AUTO_INCREMENT,
  customer_name VARCHAR(100) NOT NULL,
  order_date DATE NOT NULL,
  order_total DECIMAL(10,2) NOT NULL,
  PRIMARY KEY (id)
);

INSERT INTO orders (customer_name, order_date, order_total)
VALUES ('John Doe', '2021-10-01', 100.00),
       ('Jane Smith', '2021-10-02', 150.50);

UPDATE orders
SET order_total = 200.00
WHERE customer_name = 'John Doe';

UPDATE orders
SET order_total = 250.00
WHERE customer_name = 'Jane Smith';

DELETE FROM orders;

~~~
## 使用方法
~~~shell
python3 toclass3.py -h=10.0.0.11 -u kevin -B kdb -t orders --start_time '2023-11-06 10:19:39' --stop_time '2023-11-07 19:09:17' --start_file binlog.000027  -p aa
~~~

~~~sql
insert into kdb.orders(`id`, `customer_name`, `order_date`, `order_total`) values("1", "John Doe", "2021-10-01", "100.00");
insert into kdb.orders(`id`, `customer_name`, `order_date`, `order_total`) values("2", "Jane Smith", "2021-10-02", "150.50");
update kdb.orders set `id`="1", `customer_name`="John Doe", `order_date`="2021-10-01", `order_total`="200.00" where `id`="1" and `customer_name`="John Doe" and `order_date`="2021-10-01" and `order_total`="100.00";
update kdb.orders set `id`="2", `customer_name`="Jane Smith", `order_date`="2021-10-02", `order_total`="250.00" where `id`="2" and `customer_name`="Jane Smith" and `order_date`="2021-10-02" and `order_total`="150.50";
delete from kdb.orders where `id`="1" and `customer_name`="John Doe" and `order_date`="2021-10-01" and `order_total`="200.00";
delete from kdb.orders where `id`="2" and `customer_name`="Jane Smith" and `order_date`="2021-10-02" and `order_total`="250.00";

~~~

~~~shell
python3 toclass3.py -h=10.0.0.11 -u kevin -B kdb -t orders --start_time '2023-11-06 10:19:39' --stop_time '2023-11-07 19:09:17' --start_file binlog.000027  -p aa -f true

~~~
~~~sql
delete from kdb.orders where `id`="1" and `customer_name`="John Doe" and `order_date`="2021-10-01" and `order_total`="100.00";
delete from kdb.orders where `id`="2" and `customer_name`="Jane Smith" and `order_date`="2021-10-02" and `order_total`="150.50";
update kdb.orders set `id`="1", `customer_name`="John Doe", `order_date`="2021-10-01", `order_total`="100.00" where `id`="1" and `customer_name`="John Doe" and `order_date`="2021-10-01" and `order_total`="200.00";
update kdb.orders set `id`="2", `customer_name`="Jane Smith", `order_date`="2021-10-02", `order_total`="150.50" where `id`="2" and `customer_name`="Jane Smith" and `order_date`="2021-10-02" and `order_total`="250.00";
insert into kdb.orders(`id`, `customer_name`, `order_date`, `order_total`) values("1", "John Doe", "2021-10-01", "200.00");
insert into kdb.orders(`id`, `customer_name`, `order_date`, `order_total`) values("2", "Jane Smith", "2021-10-02", "250.00");

~~~
### 有做好的二进制包Linux Centos 7.5平台的
https://github.com/yzcy/binlog2sql/releases/tag/untagged-55204cd70a7dcf553684


## 参考连接
https://github.com/danfengcao/binlog2sql 
https://github.com/julien-duponchelle/python-mysql-replication/tree/master
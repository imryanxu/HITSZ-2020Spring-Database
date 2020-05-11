# 2020Spring-Database
The lab work of Database Course in 2020 Spring Semester.

## 实验2：使用高级语言操作MySQL数据库
### 基础任务 :writing_hand:
在COMPANY数据库上，用高级语言编写应用程序，完成如下功能（%%为高级语言程序的输入参数）：
1. 查询直接领导为%ENAME%的员工编号；
2. 查询项目所在地为%PLOCATION%的部门名称；
3. 查询参与%PNAME%项目的所有工作人员的名字和居住地址；
4. 查询部门领导居住地在%ADDRESS%且工资不低于%SALARY%元的员工姓名和居住地；
5. 查询没有参加项目编号为%PNO%的项目的员工姓名；
6. 查询部门领导工作日期在%MGRSTARTDATE%之后的部门名；
7. 查询总工作量大于%HOURS%小时的项目名称；
8. 查询员工平均工作时间低于%HOURS%的项目名称；
9. 查询至少参与了%N%个项目并且工作总时间超过%HOURS%小时的员工名字；
10. 在employee表新增记录2条记录；
11. 将第10步新增的其中1条记录的地址改成“深圳市南山区西丽大学城哈工大（深圳）”；
12. 将第10步新增的2条记录中没有修改的那条记录删除。

### 附加任务：为其加一个不丑的界面 :man_facepalming:
在PyQt5和Tkinter间，学了后者30分钟后果断选择前者 :roll_eyes:

Thanks to @ziye0229 for making GUI come true :kissing_heart:


## 实验3：小型管理信息系统的设计和实现
### 选题范围 :writing_hand:
1. 电商：订单管理、用户管理、商品的增删改查、登录安全、购物车
2. 疫情：全国疫情动态查询、患者状态更新维护、同行程查询、病例分布、轨迹查询、登录管理、用户管理
3. 微信：朋友圈、评论管理、消息、群消息、好友增删改查、登录

### 基本要求 :anger:
1. 该系统的E-R图至少包括8个实体和7个联系（必须有1:1联系、1:n联系、m:n联系）。
2. 在设计的关系中需要体现关系完整性约束：主键约束、外键约束，空值约束。
3. 对几个常用的查询创建视图、并且在数据库中为常用的属性（非主键）建立索引。
4. 该系统功能必须包括：实现插入、删除、修改、查询（连接、嵌套、分组）。其中插入、删除、修改操作需体现关系表的完整性约束，例如插入空值、重复值时需给予提示或警告等。
5. 至少提供单表的增、删、改以及多个表的连接查询、嵌套查询、分组查询图形界面。

### 附加要求（已经自闭了） :man_facepalming:
1. 绘制LDM、PDM图（可用数据库设计工具直接生成），并完成实验报告中附加题的部分；
2. 提供功能完备的系统和友好的用户界面；
3. 设计事务管理、触发器等。

Thanks to @ziye0229 for making PyQt moving :kissing_heart:

A big sigh to things happening recently :sob:

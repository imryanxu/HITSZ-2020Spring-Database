import pymysql


# 查询直接领导为ENAME的员工编号；
def func_select_1():
    print("请输入领导姓名ENAME：")
    ename = input()

    cursor = conn.cursor()
    # 使用execute()方法执行SQL查询
    sql = "select e1.essn from employee e1, employee e2 \
where e1.superssn = e2.essn and e2.ename =" + "\'" + ename + "\';"
    print(sql)
    try:
        cursor.execute(sql)
        numrows = int(cursor.rowcount)
        print("直接领导是" + ename + "的员工编号如下：")
        result = cursor.fetchall()
        for row in result:
            print(row[0])
        print("\n共查询到%d条" % numrows)
    except:
        print("Error： Unable to fetch data")
    cursor.close()
    return


# 查询项目所在地为PLOCATION的部门名称；
def func_select_2():
    print("请输入项目所在地PLOCATION：")
    plocation = input()

    cursor = conn.cursor()
    # 使用execute()方法执行SQL查询
    sql = "select dname from project, department \
where project.dno = department.dno and plocation =" + "\'" + plocation + "\';"
    print(sql)
    try:
        cursor.execute(sql)
        numrows = int(cursor.rowcount)
        print("项目所在地为" + plocation + "的部门名称如下：")
        result = cursor.fetchall()
        for row in result:
            print(row[0])
        print("\n共查询到%d条" % numrows)
    except:
        print("Error： Unable to fetch data")
    cursor.close()
    return


# 查询参与%PNAME%项目的所有工作人员的名字和居住地址；
def func_select_3():
    print("请输入所参与项目PNAME：")
    pname = input()

    cursor = conn.cursor()
    # 使用execute()方法执行SQL查询
    sql = "select ename, address from employee \
where essn in \n (select essn from works_on, project \
where works_on.pno = project.pno and pname = \'%s\'); " % pname
    print(sql)
    try:
        cursor.execute(sql)
        numrows = int(cursor.rowcount)
        print("参与" + pname + "项目的所有工作人员的名字和居住地址如下：")
        result = cursor.fetchall()
        for row in result:
            print(row[0], row[1])
        print("\n共查询到%d条" % numrows)
    except:
        print("Error： Unable to fetch data")
    cursor.close()
    return


# 查询部门领导居住地在%ADDRESS%且工资不低于%SALARY%元的员工姓名和居住地；
def func_select_4():
    print("请输入部门领导所在地ADDRESS：")
    address = input()
    print("请输入员工工资不低于SALARY：")
    salary = input()

    cursor = conn.cursor()
    # 使用execute()方法执行SQL查询
    sql = "select ename,address from employee where \
salary>=" + salary + " and dno in\n \
(select department.dno from department, employee\n \
where department.mgrssn = employee.essn and address like \'%" + address + "%\');"
    print(sql)
    try:
        cursor.execute(sql)
        numrows = int(cursor.rowcount)
        print("部门领导居住地在" + address + "且工资不低于" + salary + "元的员工姓名和居住地如下：")
        result = cursor.fetchall()
        for row in result:
            print(row[0], row[1])
        print("\n共查询到%d条" % numrows)
    except:
        print("Error： Unable to fetch data")
    cursor.close()
    return


# 查询没有参加项目编号为%PNO%的项目的员工姓名；
def func_select_5():
    print("请输入项目编号PNO：")
    pno = input()
    pre = "select * from project where pno = \'%s\';" %pno

    # 首先判断是否存在这个项目编号PNO
    cursor = conn.cursor()
    try:
        cursor.execute(pre)
        numrows = cursor.rowcount
        if(numrows == 0):
            print("没有项目编号为%s的项目！" % pno)
            return
    except:
        print("Error： Unable to fetch data")
    cursor.close()

    # 使用execute()方法执行SQL查询
    cursor = conn.cursor()
    sql = "select ename from employee where\n \
not exists(select * from works_on where essn = employee.essn and pno = \'%s\');" %pno
    print(sql)
    try:
        cursor.execute(sql)
        numrows = int(cursor.rowcount)
        print("没有参加项目编号为" + pno + "的项目的员工姓名如下：")
        result = cursor.fetchall()
        for row in result:
            print(row[0])
        print("\n共查询到%d条" % numrows)
    except:
        print("Error： Unable to fetch data")
    cursor.close()
    return


# 查询部门领导工作日期在%MGRSTARTDATE%之后的部门名；
def func_select_6():
    print("请输入某工作日期MGRSTARTDATE\n（请以格式YYYY-MM-DD书写，如：2020-04-05）:")
    mgrstartdate = input()

    cursor = conn.cursor()
    # 使用execute()方法执行SQL查询
    sql = "select dname from department where mgrstartdate > \'%s\';" % mgrstartdate
    print(sql)
    try:
        cursor.execute(sql)
        numrows = int(cursor.rowcount)
        print("部门领导工作日期在" + mgrstartdate + "之后的部门名如下：")
        result = cursor.fetchall()
        for row in result:
            print(row[0])
        print("\n共查询到%d条" % numrows)
    except:
        print("Error： Unable to fetch data")
    cursor.close()
    return


# 查询总工作量大于%HOURS%小时的项目名称；
def func_select_7():
    print("请输入工作量时间HOURS（小时）：")
    hours = input()

    cursor = conn.cursor()
    # 使用execute()方法执行SQL查询
    sql = "select pname from project where pno in \n \
(select pno from works_on group by pno having sum(hours)>%s );" % hours
    print(sql)
    try:
        cursor.execute(sql)
        numrows = int(cursor.rowcount)
        print("总工作量大于" + hours + "小时的项目名称如下：")
        result = cursor.fetchall()
        for row in result:
            print(row[0])
        print("\n共查询到%d条" % numrows)
    except:
        print("Error： Unable to fetch data")
    cursor.close()
    return


# 查询员工平均工作时间低于%HOURS%的项目名称；
def func_select_8():
    print("请输入员工平均工作时间HOURS（小时）：")
    hours = input()

    cursor = conn.cursor()
    # 使用execute()方法执行SQL查询
    sql = "select pname from project where pno in \n \
    (select pno from works_on group by pno having avg(hours)<%s );" % hours
    print(sql)
    try:
        cursor.execute(sql)
        numrows = int(cursor.rowcount)
        print("员工平均时间低于" + hours + "小时的项目名称如下：")
        result = cursor.fetchall()
        for row in result:
            print(row[0])
        print("\n共查询到%d条" % numrows)
    except:
        print("Error： Unable to fetch data")
    cursor.close()
    return


# 查询至少参与了%N%个项目并且工作总时间超过%HOURS%小时的员工名字；
def func_select_9():
    print("请输入员工参与的项目数N：")
    n = input()
    print("请输入员工工作总时间HOURS：")
    hours = input()

    cursor = conn.cursor()
    # 使用execute()方法执行SQL查询
    sql = "select ename from employee where essn in (select essn from works_on\n \
group by essn having (count(pno)>=%s and sum(hours)>%s));" %(n, hours)
    print(sql)
    try:
        cursor.execute(sql)
        numrows = int(cursor.rowcount)
        print("至少参与了%s个项目且工作总时间超过%s小时的员工名字如下：" %(n, hours))
        result = cursor.fetchall()
        for row in result:
            print(row[0])
        print("\n共查询到%d条" % numrows)
    except:
        print("Error： Unable to fetch data")
    cursor.close()
    return


def func_select():
    while True:
        print("""
您想查询以下哪一项？
-----------------------
1. 查询直接领导为ENAME的员工编号；
2. 查询项目所在地为PLOCATION的部门名称；
3. 查询参与%PNAME%项目的所有工作人员的名字和居住地址；
4. 查询部门领导居住地在%ADDRESS%且工资不低于%SALARY%元的员工姓名和居住地；
5. 查询没有参加项目编号为%PNO%的项目的员工姓名；
6. 查询部门领导工作日期在%MGRSTARTDATE%之后的部门名；
7. 查询总工作量大于%HOURS%小时的项目名称；
8. 查询员工平均工作时间低于%HOURS%的项目名称；
9. 查询至少参与了%N%个项目并且工作总时间超过%HOURS%小时的员工名字；
10. 退出
-----------------------
请选择：""")
        query = input()
        if int(query) == 1:
            func_select_1()
        elif int(query) == 2:
            func_select_2()
        elif int(query) == 3:
            func_select_3()
        elif int(query) == 4:
            func_select_4()
        elif int(query) == 5:
            func_select_5()
        elif int(query) == 6:
            func_select_6()
        elif int(query) == 7:
            func_select_7()
        elif int(query) == 8:
            func_select_8()
        elif int(query) == 9:
            func_select_9()
        elif int(query) == 10:
            break
        else:
            print("--------请重新输入!---------\n\n")
            continue
    return


def func_insert():
    print("请输入新员工名字ENAME：")
    ename = input()

    # ESSN不可以有重复！
    repeat = 1
    while repeat:
        print("请输入新员工编号ESSN：")
        essn = input()
        cursor = conn.cursor()
        try:
            check = "select * from employee where essn = \'%s\'" % essn
            cursor.execute(check)
            if cursor.rowcount == 0:
                repeat = 0
            else:
                print("该编号ESSN已存在，请重新输入ESSN！")
        except:
            print("Error： Unable to fetch data")
        cursor.close()

    print("请输入新员工居住地址ADDRESS：")
    address = input()

    print("请输入新员工工资SALARY：")
    salary = input()

    # SUPERSSN可能做外键，这里不考虑其为NULL（该员工是部门领导）情况
    exist = 0
    while exist==0:
        print("请输入新员工直接领导编号SUPERSSN：")
        superssn = input()
        cursor = conn.cursor()
        try:
            check = "select * from employee where essn = \'%s\'" % superssn
            cursor.execute(check)
            if cursor.rowcount == 1:
                exist = 1
            else:
                print("该SUPERSSN不存在于所有ESSN内，请重新输入SUPERSSN！")
        except:
            print("Error： Unable to fetch data")
        cursor.close()

    # DNO可能做外键
    exist = 0
    while exist == 0:
        print("请输入新员工所属部门号DNO：")
        dno = input()
        cursor = conn.cursor()
        try:
            check = "select * from department where dno = \'%s\'" % dno
            cursor.execute(check)
            if cursor.rowcount == 1:
                exist = 1
            else:
                print("该DNO不存在于Department表中的所有DNO内，请重新输入DNO！")
        except:
            print("Error： Unable to fetch data")
        cursor.close()

    sql = "insert into employee \n \
values (\'%s\', \'%s\', \'%s\', %s, \'%s\', \'%s\');" %(ename, essn, address, salary, superssn, dno)
    cursor = conn.cursor()
    try:
        # 执行SQL语句
        cursor.execute(sql)
        # 提交到数据库执行
        conn.commit()
    except:
        # 如果发生错误就回滚
        conn.rollback()
        print("增加新员工信息失败！")
        return
    print(sql)
    print("已增加员工号为%s的员工信息！" % essn)
    cursor.close()
    return


def func_update():
    exist = 0
    while exist == 0:
        print("请输入要更新信息的员工的员工号ESSN：")
        essn = input()
        cursor = conn.cursor()
        try:
            check = "select * from employee where essn = \'%s\'" % essn
            cursor.execute(check)
            if cursor.rowcount == 1:
                exist = 1
            else:
                print("要更新的员工的ESSN不存在，请重新输入ESSN！")
        except:
            print("Error： Unable to fetch data")
        cursor.close()

    while True:
        print("""
您想要修改哪一项？
--------------------------
1. 员工姓名ENAME
2. 员工居住地址ADDRESS
3. 员工工资SALARY
4. 员工直接领导编号SUPERSSN
5. 所属部门号DNO
6. 退出
--------------------------
请选择：""")
        query = input()
        if int(query) == 1:
            print("员工姓名修改为：")
            ename = input()
            cursor = conn.cursor()
            sql = "update employee set ename = \'%s\' where essn = \'%s\';" % (ename, essn)
            try:
                cursor.execute(sql)
                conn.commit()
            except:
                conn.rollback()
                print("修改员工姓名失败！")
                continue
            print(sql)
            print("已更新员工号为%s的员工的姓名ENAME" % essn)
            cursor.close()

        elif int(query) == 2:
            print("员工居住地址修改为：")
            address = input()
            cursor = conn.cursor()
            sql = "update employee set address = \'%s\' where essn = \'%s\';" % (address, essn)
            try:
                cursor.execute(sql)
                conn.commit()
            except:
                conn.rollback()
                print("修改员工居住地址失败！")
                continue
            print(sql)
            print("已更新员工号为%s的员工的居住地址ADDRESS" % essn)
            cursor.close()

        elif int(query) == 3:
            print("员工工资修改为：")
            salary = input()
            cursor = conn.cursor()
            sql = "update employee set salary = %s where essn = \'%s\';" % (salary, essn)
            try:
                cursor.execute(sql)
                conn.commit()
            except:
                conn.rollback()
                print("修改员工工资失败！")
                continue
            print(sql)
            print("已更新员工号为%s的员工的工资SALARY" % essn)
            cursor.close()

        elif int(query) == 4:
            print("员工直接领导编号SUPERSSN修改为：")
            superssn = input()
            cursor = conn.cursor()
            sql = "update employee set superssn = \'%s\' where essn = \'%s\';" % (superssn, essn)
            try:
                cursor.execute(sql)
                conn.commit()
            except:
                conn.rollback()
                print("修改员工直接领导编号失败！")
                continue
            print(sql)
            print("已更新员工号为%s的员工的直接领导编号SUPERSSN" % essn)
            cursor.close()

        elif int(query) == 5:
            print("员工所属部门号修改为：")
            dno = input()
            cursor = conn.cursor()
            sql = "update employee set dno = \'%s\' where essn = \'%s\';" % (dno, essn)
            try:
                cursor.execute(sql)
                conn.commit()
            except:
                conn.rollback()
                print("修改员工所属部门号失败！")
                continue
            print(sql)
            print("已更新员工号为%s的员工的所属部门号DNO" % essn)
            cursor.close()

        elif int(query) == 6:
            break
        else:
            print("--------请重新输入!---------\n\n")
    return


def func_delete():
    exist = 0
    while exist == 0:
        print("请输入要删除的员工的员工号ESSN：")
        essn = input()
        cursor = conn.cursor()
        try:
            check = "select * from employee where essn = \'%s\'" % essn
            cursor.execute(check)
            if cursor.rowcount == 1:
                exist = 1
            else:
                print("要删除的ESSN不存在，请重新输入ESSN！")
        except:
            print("Error： Unable to fetch data")
        cursor.close()

    cursor = conn.cursor()
    sql = "delete from employee where essn = \'%s\';" % essn
    try:
        cursor.execute(sql)
        conn.commit()
    except:
        conn.rollback()
        print("删除员工信息失败！")
        return
    print(sql)
    print("已删除员工号为%s的员工信息！" % essn)
    cursor.close()
    return


conn = pymysql.connect(host="localhost", user="root", password="HelloSQL", database="company")
while True:
    print("""
欢迎来到公司管理系统！
---------------------
1. 查询员工信息
2. 增加新员工信息
3. 更新员工信息
4. 删除员工信息
5. 退出
---------------------
请选择以上功能之一：""")
    choice = input()
    if int(choice) == 1:
        func_select()
    elif int(choice) == 2:
        func_insert()
    elif int(choice) == 3:
        func_update()
    elif int(choice) == 4:
        func_delete()
    elif int(choice) == 5:
        break
    else:
        print("--------请重新输入!---------\n\n")
        continue

conn.close()
print("成功退出！")

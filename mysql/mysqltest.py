import pymysql


def conn():
    db = pymysql.connect('localhost','root','123456','mytest')
    return db


def createtable(db):
    cursor = db.cursor()
    sql = """CREATE TABLE EMPLOYEE (
             FIRST_NAME  CHAR(20) NOT NULL,
             LAST_NAME  CHAR(20),
             AGE INT,  
             SEX CHAR(1),
             INCOME FLOAT )"""
    cursor.execute(sql)
    db.close()


def insert(db):
    cursor = db.cursor()
    sql = """INSERT INTO EMPLOYEE(FIRST_NAME,
         LAST_NAME, AGE, SEX, INCOME)
         VALUES ('Mac2', 'Mohan2', 21, 'W', 2001),
         ('Mac3', 'Mohan3', 22, 'M', 2002),
         ('Mac4', 'Mohan4', 23, 'W', 2003),
         ('Mac5', 'Mohan5', 24, 'M', 2004),
         ('Mac6', 'Mohan6', 25, 'W', 2005)
         """
    try:
        print('正在插入')
        # 执行sql语句
        cursor.execute(sql)
        # 提交到数据库执行
        db.commit()
        print('插入成功')
    except:
        # 如果发生错误则回滚
        db.rollback()
    # 关闭数据库连接
    db.close()


if __name__ == '__main__':
    db = conn()
  #  insert(db)


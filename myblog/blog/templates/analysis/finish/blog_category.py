import pymysql.cursors
import json


class MySQL:
    # def __init__(self,host=None,user=None,pwd=None,db=None):
    def __init__(self):
        self.host = '127.0.0.1'
        self.user = 'root'
        self.pwd = '1998818'
        self.db = 'PythonWeb'

        self._conn = self.GetConnect()
        if (self._conn):
            self._cur = self._conn.cursor()

    # 连接数据库
    def GetConnect(self):
        conn = False
        try:
            conn = pymysql.connect(
                host=self.host,
                user=self.user,
                password=self.pwd,
                database=self.db
            )
        except Exception as err:
            print("连接数据库失败, %s" % err)
        else:
            return conn

    # 执行查询
    def ExecQuery(self, sql):
        res = ""
        try:
            self._cur.execute(sql)
            res = self._cur.fetchall()
        except Exception as err:
            print("查询失败, %s" % err)
        else:
            return res

    # 执行含参数查询
    def ExecDataQuery(self, sql, data):
        res = ""
        try:
            self._cur.execute(sql % data)
            res = self._cur.fetchall()
        except Exception as err:
            print("查询失败, %s" % err)
        else:
            return res

    # 执行非查询类语句
    def ExecNonQuery(self, sql):
        flag = False
        try:
            self._cur.execute(sql)
            self._conn.commit()
            flag = True
        except Exception as err:
            flag = False
            self._conn.rollback()
            print("执行失败, %s" % err)
        else:
            return flag

    # 获取连接信息
    def GetConnectInfo(self):
        print("连接信息：")
        print("服务器:%s , 用户名:%s , 数据库:%s " % (self.host, self.user, self.db))

    # 关闭数据库连接
    def Close(self):
        if (self._conn):
            try:
                if (type(self._cur) == 'object'):
                    self._cur.close()
                if (type(self._conn) == 'object'):
                    self._conn.close()
            except:
                raise ("关闭异常, %s,%s" % (type(self._cur), type(self._conn)))


#
def blog():
    db = MySQL()
    sql = "select blog_category, count(*) from blog_blog group by blog_category"
    blogs = db.ExecQuery(sql)
    blogs_list = []
    for row in blogs:
        blogs = {'category': row[0], 'number': row[1]}
        blogs_list.append(blogs)
    # print(blog_time_list)
    jsonDate = json.dumps(blogs_list, ensure_ascii=False)
    print(jsonDate)

if __name__ == '__main__':
    blog()
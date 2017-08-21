import json
import redis
import MySQLdb

def main():
    r = redis.StrictRedis(host='localhost', port=6379, db=0)
    conn = MySQLdb.connect(host='localhost', user='root', passwd='1234', db='test', port=3306, charset="utf8")
    while True:
        source, data = r.blpop(["apple:items"])
        item = json.loads(data)
        try:
            cur = conn.cursor()
            sql = "insert into apple values('%s','%s')" % (item['time'],item['title'])
            # print(sql)
            cur.execute(sql)
            conn.commit()
            cur.close()
        except MySQLdb.Error as e:
            print("Mysql Error %d: %s" % (e.args[0], e.args[1]))

if __name__ == '__main__':
    main()
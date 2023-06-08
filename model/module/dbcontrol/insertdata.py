import pymysql
from module.tool import read_json


class database:

    def __init__(self, db='edutest') -> None:
        self.db = db
        data = read_json('conf\Credential.json')
        self.host = data["host"]
        self.port = data["post"]
        self.user = data['user']
        self.password = data["password"]
        self.charset = 'utf8'
        self.db = pymysql.connect(host=self.host,
                                  port=self.port,
                                  user=self.user,
                                  password=self.password,
                                  db=self.db,
                                  use_unicode=True)

    def insert(self, table, a):
        if not a:
            return 0
        cursor = self.db.cursor()
        cursor.execute("SET character_set_connection=utf8mb4")
        data = a[0]
        cols = ", ".join('`{}`'.format(k) for k in data.keys())

        val_cols = ', '.join('%({})s'.format(k) for k in data.keys())

        sql = f"insert into {table}(%s) values(%s)"
        res_sql = sql % (cols, val_cols)

        cursor.executemany(res_sql, a)
        self.db.commit()

    def close(self):
        self.db.close()


if __name__ == "__main__":
    data = [
        {
            'sno': "S20",
            'cno': "C20",
            "grade": 99.00,
            "qty": None
        },
        {
            'sno': "S21",
            'cno': "C21",
            "grade": 98.00,
            "qty": None
        },
    ]
    db = database().insert("SC", data)

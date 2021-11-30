import mysql.connector


class database:
  def __init__(self, host="localhost", database="gannybot", port=3306, user="root", password=""):
    self.mydb = None
    self.HOST = host
    self.DB = database
    self.PORT = port
    self.USER = user
    self.PASSWORD = password

  def connect(self):
    self.mydb = mysql.connector.connect(
                  host = self.HOST,
                  database= self.DB,
                  port = self.PORT,
                  user = self.USER,
                  password = self.PASSWORD
                )
  
  def select(self, sql, val):
    # sql = "INSERT INTO customers (name, address) VALUES (%s, %s)"
    # val = ("John", "Highway 21")
    mycursor = self.mydb.cursor(dictionary=True)
    mycursor.execute(sql, val)
    data = mycursor.fetchall()
    self.mydb.commit()
    return data

if __name__ == "__main__":
  db = database()
  db.connect()

  
import random
import sqlite3
import hashlib
    #шифрование пароля алгоритмом с помощью hashlib
def md5sum(value):
    return hashlib.md5(value.encode()).hexdigest()
    #md5sum это функция модуля hashlib



with sqlite3.connect("database.db") as db:
    cursor = db.cursor()

    query = """
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY,
        name VARCHAR(30),
        age INTEGER(3),
        sex INTEGER NOT NULL DEFAULT 1,
        balance INTEGER NOT NULL DEFAULT 2000,
        login VARCHAR(15),
        password VARCHAR(20)
    );
    CREATE TABLE IF NOT EXISTS roulette(
        name VARCHAR(50),
        description TEXT(300),
        balance BIGINT NOT NULL DEFAULT 10000
    )
     """

    cursor.executescript(query)
    #с помощью метода executescript  мы сможем выполнить несколько запросов одновременно

    #запись и регистрация
def registration():
    name = input("Name: ")
    age = int(input("Age: "))
    sex = int(input("Sex: "))
    login = input("Login: ")
    password = input("Password: ")

    try:
        db =  sqlite3.connect("database.db")
        cursor = db.cursor()

        db.create_function("md5", 1, md5sum)




        cursor.execute("SELECT login FROM users WHERE login = ?", [login])
        if cursor.fetchone() is None:
            values = [name, age, sex, login, password]
            cursor.execute("INSERT INTO users(name, age, sex, login, password) VALUES(?, ?, ?, ?, md5(?))", values)
            db.commit()
        else:
            print("Такой логин уже существует!")
            registration()
    except sqlite3.Error as e:
        print("Error", e)
    finally:
        cursor.close()
        db.close()




def log_in():
    login = input("Login: ")
    password  = input("Password: ")

    try:
       db = sqlite3.connect("database.db")
       cursor = db.cursor()

       db.create_function("md5", 1, md5sum)

       cursor.execute("SELECT login FROM users WHERE login = ?", [login])
       if cursor.fetchone() is None:
        #если такого логина не существует в нашей таблице
          print("Такого логина не существует!")
       else:
            cursor.execute("SELECT password FROM users WHERE login = ? AND password = md5(?)", [login, password])
        #если же логин  существует,то делаем проверку на пароль.
            if cursor.fetchone() is None:
                print("Пароль неверный!")
            else:
        #если пароль верный,то перекидываем пользователя в функцию roulette.
                play_roulette(login)
    except sqlite3.Error as e:
        print("Error", e)
    finally:
        cursor.close()
        db.close()

def play_roulette(login):
    print("\ nRoulette ^-^")
    try:
        db = sqlite3.connect("database.db")
        cursor = db.cursor()


        cursor.execute("SELECT age FROM users WHERE login = ? AND age >=?", [login, 16])
        #проверка пользователя на возвраст.Если ему не меьнше 16, то он не проходит.
        if cursor.fetchone() is None:
            print("Вам недостаточно лет!")
        else:
            bet = int(input("Bet: "))
        #ставка в рулетке
            number = random.randint(1, 100)
        #ставим простой диапазон

            balance = cursor.execute("SELECT balance FROM users WHERE login = ?", [login]).fetchone()[0]
            if balance < bet:
        #если балланс меньше ставки
                print("Поднимай жопу из-за компьютера и иди работай,а не сливай кэш в рулетку:)")
            elif balance <=0:
        #если балланс отрицательный или равен 0,то пользователь также не сможет играть в рулетку.
                print("Поднимай жопу из-за компьютера и иди работай,а не сливай кэш в рулетку:)")
            else:
                if number < 50:
        #если в переменной "number"  получилось число меньше 50,то пользователь проигрывает и деньги переводятся на счет рулетки.
                    cursor.execute("UPDATE users SET balance - ? WHERE login =? ", [bet, login])
                    cursor.execute("UPDATE roulette SET balance = balance + ?", [bet])

                    print("Fale:(")
                else:
                    cursor.execute("UPDATE users SET balance + ? WHERE login =?", [bet, login])
                    cursor.execute("UPDATE roulette SET balance = balance - ?", [bet])

                    print("You win! ")
                db.commit()
                play_roulette(login)
    except sqlite3.Error as e:
        print("Error", e)
    finally:
        cursor.close()
        db.close()

registration()
log_in()

import mysql.connector

def main():
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password=""
    )

    print(mydb)


if __name__ == "__main__":
    main()

from mysql.connector import MySQLConnection

from read_config import read_db_config


def re_connect():                                   #setzt eine neue Verbindung, wegen MySQL timeout
    dbconfig = read_db_config()                     #benutzt library Config-Reader für die Konfiguration
    conn = MySQLConnection(**dbconfig)              #verbindung zur Datenbank wird hergestellt
    cursor = conn.cursor()                          #setzt den Curser, der die Befehle ausführt

    return cursor, conn                             #gibt den Cursor und die Verbindung zurück



def insert_book(ISBN, Titel, Verlag, preis=0):
    cursor, conn =re_connect()
    values=[ISBN, Titel, Verlag, preis]
    cursor.execute("INSERT INTO buecher (ISBN, Titel, Verlag, preis) VALUES (%s, %s, %s, %s)", values)
    conn.commit()


def update_book(ISBN, Titel, Verlag, preis):
    cursor, conn =re_connect()
    cursor.execute(""""UPTATE buecher SET Titel='%s', Verlag='%s', preis=%s WHERE ISBN=%s""" % (Titel, Verlag, preis, ISBN))
    conn.commit()


def insert_taken_book_add(Sch_ID, ISBN, Anzahl=1):
    cursor, conn =re_connect()
    cursor.execute("""SELECT Anzahl FROM ausgeliehen WHERE ID='%s' AND ISBN=%s""" % (Sch_ID, ISBN))
    result=cursor.fetchall()
    if len(result)!=0:
        books=result[0][0]
        cursor.execute("""UPDATE ausgeliehen SET Anzahl=%s WHERE ID='%s' AND ISBN=%s""" % (books+Anzahl, Sch_ID, ISBN))
        conn.commit()
    else:
        cursor.execute("""INSERT INTO ausgeliehen (ID, ISBN, Anzahl) VALUES ('%s', %s, %s)""" % (Sch_ID, ISBN, Anzahl))
        conn.commit()


def insert_taken_book_absolute(Sch_ID, ISBN, Anzahl=1):
    cursor, conn =re_connect()
    cursor.execute("""SELECT Anzahl FROM ausgeliehen WHERE ID='%s' AND ISBN=%s""" % (Sch_ID, ISBN))
    result=cursor.fetchall()
    if len(result)!=0:
        books=result[0][0]
        cursor.execute("""UPDATE ausgeliehen SET Anzahl=%s WHERE ID='%s' AND ISBN=%s""" % (Anzahl, Sch_ID, ISBN))
        conn.commit()
    else:
        cursor.execute("""INSERT INTO ausgeliehen (ID, ISBN, Anzahl) VALUES ('%s', %s, %s)""" % (Sch_ID, ISBN, Anzahl))
        conn.commit()
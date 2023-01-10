import sys
import os
import psycopg2
import csv
from faker import Faker
import json

# of course can be modified , to specific country like
# ('en_US') for USA , ('de_DE') for Germany, ('ar_SA') for Arabic ...etc.
# check faker documentation

fake = Faker()


def connect(db, usr, pas, hostname):
    # starting new connection to your postgresSql's DataBase
    connection = psycopg2.connect(dbname=db, user=usr, password=pas, host=hostname)
    return connection


'''
# I am working on it right away, do not use it.

def insert_from_csv(csv_file):
    conn = connect()
    cursor = conn.cursor()

    with open(csv_file, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            cursor.execute("INSERT INTO tableName VALUES (%s, %s, %s)", (row["Ids"], row["Names"], row["Ages"]))

    conn.commit()
    cursor.close()
    conn.close()
'''


def color(text):
    os.system("")
    pruple = ""
    red = 40
    for line in text.splitlines():
        pruple += (f"\033[38;2;{red};0;220m{line}\033[0m\n")
        if not red == 255:
            red += 15
            if red > 255:
                red = 255
    return pruple


def generator(f1, f2, f3, f4, f5):
    # Getting the data from the parameters and then returning the result
    return [getattr(fake, f1)(), getattr(fake, f2)(), getattr(fake, f3)(), getattr(fake, f4)(), getattr(fake, f5)()]


def create_json(filepath):
    # create an Array to hold our file
    data = {}
    pk = input("Which column is your Primary Key: ")
    # Open a csv reader and read the data inside it
    with open(filepath, encoding='utf-8') as csvf:
        reader = csv.DictReader(csvf)

        # Convert each row into a dictionary
        # and add it to data
        for rows in reader:
            # Assuming a given column pk
            # be the primary key
            key = rows[f'{pk}']
            data[key] = rows

    # Open a json writer, and use the json.dumps()
    # function to dump data to json file
    with open("Output.json", 'w', encoding='utf-8') as jsonf:
        jsonf.write(json.dumps(data, indent=4))


print(color("""
███████  ██████  ██      ███████ ██████      
██      ██    ██ ██      ██      ██   ██     
███████ ██    ██ ██      █████   ██████      
     ██ ██ ▄▄ ██ ██      ██      ██   ██     
███████  ██████  ███████ ███████ ██   ██     
 abodx@gmx.de ▀▀  ...  ... made by:Abodx

In order to successfully generate your data take a
look in Supported Data.txt

You need to read it...otherwise it won't work , cause 
it is important to understand what are you generating
--------------------------------------------------

1- Generate Fake data 
2- Convert the Csv file to Insert statement
3- Remove Empty Lines from csv file
4- Convert the Csv file to Json
5- Connect to your database (Postgres)
6- Insert records from csv file to your database - Soon

"""))
ch = int(input("What is your Choice: "))

if ch == 1:
    attri1 = input("Enter the first attribute's name: ")
    attri2 = input("Enter the second attribute's name: ")
    attri3 = input("Enter the third attribute's name: ")
    attri4 = input("Enter the fourth attribute's name: ")
    attri5 = input("Enter the fifth attribute's name: ")

    fake1 = input(f"What type of data, you want to generate for {attri1}: ")
    fake2 = input(f"What type of data, you want to generate for {attri2}: ")
    fake3 = input(f"What type of data, you want to generate for {attri3}: ")
    fake4 = input(f"What type of data, you want to generate for {attri4}: ")
    fake5 = input(f"What type of data, you want to generate for {attri5}: ")

    cfn = input("What do u want to call the csv file: ")
    rec = int(input("How many rows do u need: "))
    with open(f'{cfn}.csv', 'w') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([f'{attri1}', f'{attri2}', f'{attri3}', f'{attri4}', f'{attri5}'])
        for n in range(rec):
            writer.writerow(generator(fake1, fake2, fake3, fake4, fake5))

        input("\n\nDone Press Enter to Exit...")

elif ch == 2:
    x = input("What is the name of ur table: ")
    f = input("Drag and Drop csv file here: ")
    # Check if the file exists then remove it, in order not to append the new text with the old;
    if os.path.exists("inserted.txt"): os.remove("inserted.txt")

    # Open the csv file and adding the Insert into, with all data after parsing them with join
    file = open(f, 'r')
    cf = csv.reader(file)
    insert = 'INSERT INTO ' + x + " VALUES "
    for row in cf:
        values = map((lambda x: "'" + x + "'"), row)
        with open('inserted.txt', 'a') as inst:
            # write all statements in a text file, in order to copy it easily
            inst.write(insert + "(" + ", ".join(values) + ");")
            # Writing a new line, so the inserted would not be a mess
            inst.write("\n")

    input("\n\nData has been exported to inserted.txt ...")
    file.close()
    sys.exit(0)

elif ch == 3:
    rml = input("Drag and Drop the csv file here: ")
    nf = input("Enter new name for csv file: ")

    # Open the csv file without this new line and then just save it to another file
    # Found this script in stackoverflow, and it helps a lot
    with open(rml, newline='') as in_file:
        with open(f'{nf}.csv', 'a', newline='') as out_file:
            writer = csv.writer(out_file)
            for row in csv.reader(in_file):
                if row:
                    writer.writerow(row)
    input("\n\nDone Press Enter to Exit...")
    sys.exit(0)

elif ch == 4:
    fj = input("Drag and Drop csv file here: ")
    create_json(fj)
    input("\n\nDone Press Enter to Exit...")
    sys.exit(0)

elif ch == 5:
    dbname = input("Enter Your Database's name: ")
    usrname = input("Enter Your user name: ")
    usrpass = input("Enter your password: ")
    host = input("Enter the database host: ")

    conn = connect(dbname, usrname, usrpass, host)
    cursor = conn.cursor()

    while True:
        print(color("""
        Connected Successfully 
-----------------------------------------
                                        |
1- Excute Commands (Select,Insert..)    |
2- Commit changes                       |
3- Rollback (do not save any changes)   |
     Press any key to quit              |
-----------------------------------------

"""))
        chos = int(input("What is your Option: "))

        if chos == 1:
            try:
                command = input("Enter Any Postgres_Sql command here: ")

                # execute a statement
                cursor.execute(command)
                command_ret = cursor.fetchall()
                print(command_ret)
                print(cursor.statusmessage)
                # close the cursor and connection
                cursor.close()

            except(Exception, psycopg2.DatabaseError) as error:
                print(error)
                break
        elif chos == 2:
            conn.commit()
            conn.close()
            break

        elif chos == 3:
            conn.rollback()
            conn.close()
            break

        else:
            print("Thanks for using this Tool")
            sys.exit(0)

elif ch == 6:
    input("\nThis option is coming soon...")
    sys.exit(0)
else:
    input("\n\nInvalid Choice try again...")
    sys.exit(1)

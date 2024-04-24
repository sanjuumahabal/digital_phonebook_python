import getpass
import datetime
import os
import time
import sys

mypath = r"C:\Users\D-Tech\AppData\Local\Programs\Python\Python312\Lib\site-packages"

sys.path.append(mypath)

from prettytable import PrettyTable

# from colorama import Fore, Style
import colorama
from colorama import *

colorama.init()

import mysql.connector

class Mydb:
    try:
        def __init__(self):
            try:
                self.mytable = PrettyTable()

                self.mytable.field_names = ["ID","Name","Mobile","Salary"]

                self.conn = mysql.connector.connect(host='localhost',user='root',password='jagdish',database='phonebook')
                self.cur = self.conn.cursor()

                self.query = """create table if not exists users (
                    User_id int primary key AUTO_INCREMENT, 
                    Name varchar(30), 
                    Username varchar(30), 
                    Password varchar(20))"""
            
                self.cur.execute(self.query)

                self.conn.commit()
            except Exception as e:
                print("Cannot Establish Connection with Database.")

        # NOT USEFUL FOR NOW
    
        # def showData(self):
        #     try:
        #         cur = self.conn.cursor()
        #         query = "select * from users"
        #         cur.execute(query)
        #         for r in cur:
        #             self.mytable.add_row(r)
                
        #         print(self.mytable)

        #     except Exception as e:
        #         print(e)

        def NewRegistration(self,name,username, passwd):
            try:
                cur = self.conn.cursor()
                query = "insert into users (Name, Username, Password) values (%s,%s,%s)"
                cur.execute(query,(name,username,passwd))
                self.conn.commit()
                text = f"{Fore.GREEN} USER REGISTERED SUCCESSFULLY !!!! {Style.RESET_ALL}"
                print(text)
            except Exception as e:
                print(e)

        def checkUser(self,uname,passwd):
            try:
                cur = self.conn.cursor()

                query = "select * from users"

                cur.execute(query)

                for row in cur:
                    if (row[2]==uname and row[3]==passwd):
                        text = f"{Fore.GREEN} LOGIN SUCCESSFULL!!!! {Style.RESET_ALL}"
                        print(text)
                        return row[0]
                return None
            except Exception as e:
                print(e)
    except Exception as e:
        print("Mydb Class ",e)
        
class MyOperations(Mydb):
    def __init__(self):
        try:
            super().__init__()
            self.myconn = mysql.connector.connect(host='localhost',user='root',password='jagdish',database='phonebook')
            self.mycur = self.myconn.cursor()
            self.mynewtable = PrettyTable()

            self.mynewtable.field_names = ["CONTACT ID","FIRST NAME","LAST NAME","E-MAIL","PHONE NUMBER","User_ID"]

            # self.myquery = "create table if not exists contacts (Contact_id int primary key AUTO_INCREMENT, FirstName varchar(30), LastName varchar(30), Email varchar(30), PhoneNumber varchar(30))"

            self.myquery = """CREATE TABLE IF NOT EXISTS contacts (
                Contact_id INT PRIMARY KEY AUTO_INCREMENT,
                FirstName VARCHAR(30),
                LastName VARCHAR(30),
                Email VARCHAR(30),
                PhoneNumber VARCHAR(30),
                User_id INT,
                FOREIGN KEY (User_id) REFERENCES users(User_id) ON DELETE CASCADE
            );"""
       
            self.mycur.execute(self.myquery)
        except Exception as e:
            print("init function ",e)
    
    def showUser(self, user_id):
        try:
            query = f"select * from users where User_id = {user_id}"
            self.cur.execute(query)

            result = self.cur.fetchone()

            x = datetime.datetime.now()
            text = f"{Fore.GREEN} [ USER {result[1]} LOGGED IN SUCCESSFULLY !!!! ]{Style.RESET_ALL}\n{x.strftime('%c')}"
            print(text)
        except Exception as e:
            print("showUser ",e)

    def isEmpty(self, uid):
        try:
            query = f"select * from contacts where User_id = {uid}"
            self.mycur.execute(query)

            ros = self.mycur.fetchall()

            if not ros:
                return True
            else:
                return False
        except Exception as e:
            print("isEmpty class ",e)

    def isAllTableEmpty(self):
        query = f"select * from contacts"
        self.mycur.execute(query)

        ros = self.mycur.fetchall()

        if not ros:
            query = "ALTER TABLE contacts AUTO_INCREMENT = 1"
            self.mycur.execute(query)
            self.myconn.commit()
        else:
            pass       
        
    def addContact(self, uid):
        try:
            fname = input("Enter First Name: ").lower().capitalize()
            lname = input("Enter Last Name: ").lower().capitalize()
            uemail = input("Enter Email: ")
            phnum = input("Enter Phone Number: ")

            
            if fname!='' and lname!='' and uemail!='' and phnum!='':
                myquery = "insert into contacts (FirstName, LastName, Email, PhoneNumber, User_id) values (%s,%s,%s,%s,%s)"
                self.mycur.execute(myquery,(fname,lname,uemail,phnum,uid))
                self.myconn.commit()
                text = f"{Fore.GREEN} [ NEW CONTACT ADDED SUCCESSFULLY !!!! ]{Style.RESET_ALL}"
                print(text)
                input("Press Enter to Continue......")
                clear_screen()
            else:
                text = f"{Fore.RED} Please Enter Correct Data, Do not left any field Empty!! {Style.RESET_ALL}"
                print(text)
                return
        except Exception as e:
            print("addContact function ",e)

    def readAllContacts(self, uid):
        temp = MyOperations()
        try:
            if temp.isEmpty(uid):
                text = f"{Fore.RED} NO CONTACTS!!! {Style.RESET_ALL}"
                print(text)
                input("Press Enter to Continue...")
                clear_screen()
                return
            else:
                query = f"select Contact_id, FirstName, LastName, Email, PhoneNumber from contacts WHERE User_id = {uid}"
                self.mycur.execute(query)
                ros = self.mycur.fetchall()

                text = f"{Fore.GREEN} YOUR CONTACT LIST !!! {Style.RESET_ALL}"
                print(text)
                
                
                mynewtable = PrettyTable()
                mynewtable.field_names = ["CONTACT ID", "FIRST NAME", "LAST NAME", "E-MAIL", "PHONE NUMBER"]

                for r in ros:
                    mynewtable.add_row(r) 
                print(mynewtable)
                input("Press Enter to Continue...")
                clear_screen()
        except Exception as e:
            print("realAllContact Exception",e)
    
    def readSpecificContact(self, uid):
        flag = 0
        temp = MyOperations()
        try:
            if temp.isEmpty(uid):
                text = f"{Fore.RED} NO CONTACTS!!! {Style.RESET_ALL}"
                print(text)
                input("Press Enter to Continue...")
                clear_screen()
                return
            else:
                query = f"select Contact_id, FirstName, LastName, Email, PhoneNumber from contacts WHERE User_id = {uid}"
                self.mycur.execute(query)

                ros = self.mycur.fetchall()

                fname = input("Enter First Name of the Person: ").lower().capitalize()
                lname = input("Enter Last Name of the Person: ").lower().capitalize()
                
                for r in ros:
                    if r[1] == fname and r[2] == lname:
                        mynewtable = PrettyTable()
                        mynewtable.field_names = ["CONTACT ID", "FIRST NAME", "LAST NAME", "E-MAIL", "PHONE NUMBER"]
                        mynewtable.add_row(r)
                        print(mynewtable)
                        flag = 1
                if flag == 1:
                    input("Press Enter to Continue...")
                    clear_screen()
                else:
                    print("No Contact Found!!!")
                    input("Press Enter to Continue...")
                    clear_screen()
                
        except Exception as e:
            print("realSpecificContact Exception",e)

    def updateContact(self, uid):
        temp = MyOperations()
        try:
            if temp.isEmpty(uid):
                text = f"{Fore.RED} NO CONTACTS!!! {Style.RESET_ALL}"
                print(text)
                input("Press Enter to Continue...")
                clear_screen()
                return
            else:
                query = f"select * from contacts where User_id = {uid}"
                self.mycur.execute(query)

                text = f"{Fore.GREEN} Your Contact List !!! {Style.RESET_ALL}"
                print(text)

                for r in self.mycur:
                    self.mynewtable.add_row(r)
                
                print(self.mynewtable)

                upchoice = int(input("Enter Contact ID of the person whose contact details you want to update: "))

                query = f"SELECT * FROM contacts where User_id = {uid}"
                self.mycur.execute(query)

                count = self.mycur.fetchall()

                cid_list = [int(r[0]) for r in count if r] 
                try:
                    for cid in cid_list:
                        if cid == upchoice:
                            flag = 1
                            while flag:
                                print("Please Specify What do You want to Update: ")
                                print("1. First Name")
                                print("2. Last Name: ")
                                print("3. Email ")
                                print("4. Mobile No ")
                                print("5. Exit")

                                
                                choice = int(input())
                                match choice:
                                    case 1:
                                        fname = input("Enter New First Name: ")
                                        query = f"update contacts set FirstName = '{fname}' where Contact_id = {upchoice}"
                                        self.mycur.execute(query)
                                        self.myconn.commit()
                                        text = f"{Fore.GREEN} DATA UPDATED SUCCESSFULLY !! {Style.RESET_ALL}"
                                        print(text)
                                        time.sleep(1)
                                    case 2:
                                        lname = input("Enter New Last Name: ")
                                        query = f"update contacts set LastName = '{lname}' where Contact_id = {upchoice}"
                                        self.mycur.execute(query)
                                        self.myconn.commit()
                                        text = f"{Fore.GREEN} DATA UPDATED SUCCESSFULLY !! {Style.RESET_ALL}"
                                        print(text)
                                        time.sleep(1)
                                    case 3:
                                        uemail = input("Enter New Email Address: ")
                                        query = f"update contacts set Email = '{uemail}' where Contact_id = {upchoice}"
                                        self.mycur.execute(query)
                                        self.myconn.commit()
                                        text = f"{Fore.GREEN} DATA UPDATED SUCCESSFULLY !! {Style.RESET_ALL}"
                                        print(text)
                                        time.sleep(1)
                                    case 4:
                                        Mobno = input("Enter New Mobile No.: ")
                                        query = f"update contacts set PhoneNumber = '{Mobno}' where Contact_id = {upchoice}"
                                        self.mycur.execute(query)
                                        self.myconn.commit()
                                        text = f"{Fore.GREEN} DATA UPDATED SUCCESSFULLY !! {Style.RESET_ALL}"
                                        print(text)
                                        time.sleep(1)
                                    case 5:
                                        clear_screen()
                                        return
                                new_choice = input("Do you want to update anything else [y/n]")

                                if new_choice == 'y' or new_choice=='Y':
                                    continue
                                else:
                                    flag = 0
                                    clear_screen()
                                    return
                    else:
                        text = f"{Fore.RED} INVALID CHOICE !! {Style.RESET_ALL}"
                        print(text)
                        input("Press Enter to Continue.......")
                        clear_screen()
                except ValueError as e:
                    print("Integer Only: ",e)
                    input("Press Enter to Continue......")
                    clear_screen()
        except Exception as e:
            print("Update Contact ",e)
            input("Press Enter to Continue......")
            clear_screen()

    def deleteContact(self,uid):
        temp = MyOperations()
        try:
            if temp.isEmpty(uid):
                text = f"{Fore.RED} NO CONTACTS !! {Style.RESET_ALL}"
                print(text)
                input("Press Enter to Continue...")
                clear_screen()
                return
            else:
                query = f"select * from contacts where User_id = {uid}"
                self.mycur.execute(query)


                print("Your Contact List!!")
                for r in self.mycur:
                    self.mynewtable.add_row(r)
                
                print(self.mynewtable)

                upchoice = int(input("Enter Contact ID of the Person Whose data You want to Delete: "))

                query = f"SELECT * FROM contacts where User_id = {uid}"
                self.mycur.execute(query)

                count = self.mycur.fetchall()

                cid_list = [int(r[0]) for r in count if r] 

                try:
                    for cid in cid_list:
                        if cid == upchoice:
                            query = f"select * from contacts where Contact_id = {upchoice}"
                            self.mycur.execute(query)
                            data = self.mycur.fetchone()
                            print("Contact ID: ",data[0])
                            print("First Name: ",data[1])
                            print("Last Name: ",data[2])
                            print("Email: ",data[3])
                            print("Contact Number: ",data[4])

                            text = f"{Fore.GREEN}THE CONTACT {data[1]} DELETED SUCCESSFULLY!!{Style.RESET_ALL}"
                            print(text)

                            query = f"delete from contacts where Contact_id = {upchoice}"
                            self.mycur.execute(query)
                            temp.isAllTableEmpty()
                            self.myconn.commit()
                            input("Press any key to Continue.....")
                            clear_screen()
                            return
                    else:
                        text = f"{Fore.RED} INVALID CONTACT ID !! {Style.RESET_ALL}"
                        print(text)
                        input("Press Enter to Continue......")
                        clear_screen()
                except Exception as e:
                    print("delete specific ",e)
                # time.sleep(1)
                
        except Exception as e:
            print("DeleteContact function ",e)
            input("Press Enter to Continue.......")
            clear_screen()

    def deleteAll(self,uid):
        temp = MyOperations()
        try:
            if temp.isEmpty(uid):
                text = f"{Fore.RED} NO CONTACTS !! {Style.RESET_ALL}"
                print(text)
                input("Press Enter to Continue...")
                clear_screen()
                return
            else:
                query = f"delete from contacts where User_id = {uid}"
                choice = input("You Sure you want to Delete All the Contacts [y/n]")
                
                if choice=='y' or choice=='Y':
                    self.mycur.execute(query)
                    text = f"{Fore.GREEN} DELETED ALL THE CONTACTS SUCCESSFULLY !! {Style.RESET_ALL}"
                    print(text)
                    # print("Delete All the Contacts Successfully!!!")
                    input("Press Enter to Continue......")
                    clear_screen()

                    #For checking if table is fully empty
                    temp.isAllTableEmpty()
                    self.myconn.commit()
                else:
                    return
        except Exception as e:
            print("delete all",e)

def operations(user_id):
    choice = 0

    while choice != 7:
        myop = MyOperations()
        myop.showUser(user_id)
        print("What do you want to do?")
        print("1. Add Contact")
        print("2. Read All Contacts")
        print("3. Read Any Specific Contact")
        print("4. Update Any Specific Contact")
        print("5. Delete any Specific Contact")
        print("6. Delete All Contacts")
        print("7. Exit ")

        choice = int(input("Enter Choice from above: "))

        match choice:
            case 1:
                myop.addContact(user_id)
            case 2:
                myop.readAllContacts(user_id)
            case 3:
                myop.readSpecificContact(user_id)
            case 4:
                myop.updateContact(user_id)
            case 5:
                myop.deleteContact(user_id)
            case 6:
                myop.deleteAll(user_id)
            case 7:
                choice = input("You Sure you want to sign out ? [y/n] ")

                if choice=='y' or choice=='Y':
                    myop.isAllTableEmpty()

                    time.sleep(1)
                    clear_screen()
                    return  
                else:
                    clear_screen()
                    continue

def clear_screen():
    os.system('cls')


def validateUser():
    while True:
        d1 = Mydb()
        try:

            print("1. Registration")
            print("2. Login (If user is already registered)")
            print("3. Exit ")

            choice = int(input("Enter Your Choice from Above "))

            match choice:
                case 1:
                    name = input("Enter Your Name: ")
                    uname = input("Enter User Name (UserName should contain Leters, Numbers and Special Characters): ")
                    upasswd = getpass.getpass(prompt="Enter your password: ")
                    if uname!='' and upasswd!='':
                        d1.NewRegistration(name, uname, upasswd)
                        # time.sleep(1)
                        input("Press Enter to Continue......")
                        clear_screen()
                    else:
                        if uname=='':
                            text = f"{Fore.RED} Pls Enter Valid Username !!! {Style.RESET_ALL}"
                            print(text)
                        elif upasswd=='':
                            text = f"{Fore.RED} Pls Enter Valid Password !!! {Style.RESET_ALL}"
                            print(text)
                case 2:
                    uname = input("Enter Registred UserName: ")
                    upasswd = getpass.getpass(prompt="Enter your password: ")
                    if uname != '' and upasswd!='':
                        test = d1.checkUser(uname,upasswd)
                        if test == None:
                            text = f"{Fore.RED} Error: Wrong Credentials!!. {Style.RESET_ALL}"
                            print(text)
                            # time.sleep(1)
                            input("Press Enter to Continue......")
                            clear_screen()
                        else:
                            # input("Press Enter to continue...")
                            clear_screen()
                            operations(test)
                case 3:
                    print("Thank You!!!")
                    print("Come Again!!!")
                    time.sleep(1)
                    clear_screen()
                    sys.exit()
        except ValueError as e:
            print("Enter integer only ",e)
            time.sleep(1)
            clear_screen()

        except Exception as e:
            print(e)

validateUser()
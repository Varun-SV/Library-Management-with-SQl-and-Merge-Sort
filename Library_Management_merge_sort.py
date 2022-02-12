# Library Management Using Merge Sort

import mysql.connector
import time as t
import random

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="2486"
)
fnme = ""
lnme = ""
usrname = ""
F = ''
L = ''
U = ''
P = ''
A = ''
books_with_srno = {}
dict_for_list = {}
list_for_sorting = []
students_with_srno = {}


def MSort_for_BandS(myList):
    if len(myList) > 1:
        mid = len(myList) // 2
        left = myList[:mid]
        right = myList[mid:]

        # Recursive call on each half
        MSort_for_BandS(left)
        MSort_for_BandS(right)

        # Two iterators for traversing the two halves
        i = 0
        j = 0

        # Iterator for the main list
        k = 0

        while i < len(left) and j < len(right):
            if left[i] < right[j]:
                # The value from the left half has been used
                myList[k] = left[i]
                # Move the iterator forward
                i += 1
            else:
                myList[k] = right[j]
                j += 1
            # Move to the next slot
            k += 1

        # For all the remaining values
        while i < len(left):
            myList[k] = left[i]
            i += 1
            k += 1

        while j < len(right):
            myList[k] = right[j]
            j += 1
            k += 1


def list_maker(a):  # will make mycursor to a list!!!
    list_for_sorting = []
    dict_for_list = {}
    dict_for_list_sorted = {}
    list_Count = 0
    for list_var in a:
        list_Count += 1
        dict_for_list[list_Count] = list_var[0]
    l = 0
    # print((dict_for_list))
    for l in range(0, list_Count):
        list_for_sorting.append(dict_for_list[int(l + 1)])
    MSort_for_BandS(list_for_sorting)
    # print(list_for_sorting)

    for l in range(0, list_Count):
        dict_for_list_sorted[l + 1] = list_for_sorting[l]
    # print(dict_for_list_sorted)
    return dict_for_list_sorted


def Sort_Everything_By_Names(choice):
    mycursor = mydb.cursor()
    mycursor.execute("Use Staff;")
    if choice == 1:
        sorted_book_names = {}
        sorted_book_names_with_author_names = {}
        auth_names = []
        serial_no = []
        mycursor.execute("SELECT Book_Name from Books;")
        sorted_book_names = list_maker(mycursor)
        try:
            mycursor.execute(
                "CREATE TABLE Sorted_Books (Book_Name varchar(50) NOT NULL ,Author_Name varchar(50) NOT NULL, Serial_No varchar(50));")
            for book_names in sorted_book_names:
                auth_state = "Select Author_Name from Books where Book_Name = '" + sorted_book_names[book_names] + "';"
                mycursor.execute(auth_state)
                for k in mycursor:
                    auth_names.append(k[0])
            for o in range(0, len(auth_names)):
                sorted_book_names_with_author_names[sorted_book_names[o + 1]] = auth_names[o]
            n = 0
            for i in sorted_book_names_with_author_names:
                sstmmt = "Select Serial_No from Books where Book_Name = '" + i + "';"
                mycursor.execute(sstmmt)
                for ser in mycursor:
                    serial_no.append(ser[0])
                stmt = "insert into Sorted_Books values ('" + i + "','" + sorted_book_names_with_author_names[
                    i] + "','" + serial_no[n] + "');"
                n += 1
                mycursor.execute(stmt)

        except:
            mycursor.execute("Drop table Sorted_Books;")
            mycursor.execute(
                "CREATE TABLE Sorted_Books (Book_Name varchar(50) NOT NULL ,Author_Name varchar(50) NOT NULL, Serial_No varchar(50));")
            for book_names in sorted_book_names:
                auth_state = "Select Author_Name from Books where Book_Name = '" + sorted_book_names[book_names] + "';"
                mycursor.execute(auth_state)
                for k in mycursor:
                    auth_names.append(k[0])
            for o in range(0, len(auth_names)):
                sorted_book_names_with_author_names[sorted_book_names[o + 1]] = auth_names[o]
            n = 0
            for i in sorted_book_names_with_author_names:
                sstmmt = "Select Serial_No from Books where Book_Name = '" + i + "';"
                mycursor.execute(sstmmt)
                for ser in mycursor:
                    serial_no.append(ser[0])
                stmt = "insert into Sorted_Books values ('" + i + "','" + sorted_book_names_with_author_names[
                    i] + "','" + serial_no[n] + "');"
                n += 1
                mycursor.execute(stmt)
        mydb.commit()

    elif choice == 2:
        sorted_U_names = {}
        sorted_U_names_with_passwords = {}
        F_name = []
        L_name = []
        password_ls = []
        mycursor.execute("SELECT User_Name from Students;")
        sorted_U_names = list_maker(mycursor)
        try:
            mycursor.execute(
                "CREATE TABLE Sorted_St(First_Name varchar(50),Last_Name varchar(50),User_Name varchar(50) Unique,Password varchar(50) Not Null);")
        except:
            mycursor.execute("Drop Table Sorted_St;")
            mycursor.execute(
                "CREATE TABLE Sorted_St(First_Name varchar(50),Last_Name varchar(50),User_Name varchar(50) Unique,Password varchar(50) Not Null);")
        for users in sorted_U_names:
            users_state = "Select Password from Students where User_Name = '" + sorted_U_names[users] + "';"
            mycursor.execute(users_state)
            for k in mycursor:
                password_ls.append(k[0])
        for o in range(0, len(password_ls)):
            sorted_U_names_with_passwords[sorted_U_names[o + 1]] = password_ls[o]
        n = 0
        for i in sorted_U_names_with_passwords:
            # user_count = 0
            Ftmmt = "Select First_Name from Students where User_Name = '" + i + "';"
            mycursor.execute(Ftmmt)
            for Fnme in mycursor:
                F_name.append(Fnme[0])
            Ltmmt = "Select Last_Name from Students where User_Name = '" + i + "';"
            mycursor.execute(Ltmmt)
            for Lnme in mycursor:
                L_name.append(Lnme[0])
            stmt = "Insert into Sorted_St values('" + F_name[n] + "','" + L_name[n] + "','" + i + "','" + \
                   sorted_U_names_with_passwords[i] + "');"
            n += 1
            mycursor.execute(stmt)
        mydb.commit()


def book_details():
    book_count = 0
    mycursor = mydb.cursor()
    mycursor.execute("USE Staff;")
    mycursor.execute("Select Book_name from Sorted_Books;")
    print("Books currently in Library : ")
    for books in mycursor:
        book_count += 1
        print(str(book_count), " : ", books[0])
        books_with_srno[book_count - 1] = books[0]


def book_auth_details():
    flag = 0
    mycursor = mydb.cursor()
    mycursor.execute("Use staff")
    book_details()
    want_to_see_more = 'y'
    while (want_to_see_more == 'y' or want_to_see_more == 'Y'):
        try:
            a = int(input("Enter the Book Number : "))
        except:
            print("\nOnly integer inputs are accepted!!! ")
            a = int(input("Enter the Book Number : "))
        for i in books_with_srno:
            if i + 1 == a:
                flag = 1
        if flag == 0:
            print("Select from the given Book Options !!!")
        elif flag == 1:
            print("Book No : " + str(int(a)))
            print("Book Name : " + books_with_srno[a-1] + ".")
            stmt = "Select Author_Name from Sorted_Books where Book_Name = '" + books_with_srno[a-1] + "';"
            mycursor.execute(stmt)
            print("Author Name :", end=" ")
            for j in mycursor:
                print(j[0])
            stmt = "Select Serial_No from Sorted_Books where Book_Name = '" + books_with_srno[a-1] + "';"
            mycursor.execute(stmt)
            print("Serial No. :", end=" ")
            for j in mycursor:
                print(j[0])
        want_to_see_more = input("Want to Check other Book (Y/n) ?")


def student_details():
    stud_count = 0
    mycursor = mydb.cursor()
    mycursor.execute("Use Staff;")
    mycursor.execute("Select User_Name from Sorted_St;")
    for students in mycursor:
        stud_count += 1
        print(str(stud_count), " : ", students[0])
        students_with_srno[stud_count - 1] = students[0]


def store_a_book():
    choice = 'y'
    while choice == 'y' or choice == 'Y':
        book_name = input("Book Name : ")
        auth_name = input("Author Name : ")
        serial_no = input("Serial Number : ")
        mycursor = mydb.cursor()
        mycursor.execute("USE staff;")
        stmt = "INSERT INTO Books values ('" + book_name + "','" + auth_name + "','" + serial_no + "');"
        try:
            mycursor.execute(stmt)
            mycursor.execute("SELECT * FROM Books;")
            for i in mycursor:
                print(i)
        except:
            mycursor.execute(
                "CREATE TABLE Books(Book_Name varchar(50) NOT NULL ,Author_Name varchar(50) NOT NULL, Serial_No varchar(50));")
            mycursor.execute(stmt)
            mycursor.execute("SELECT * FROM Books;")
            for i in mycursor:
                print(i)
        choice = input("Do you want to add more books (Y/N) ? ")
        mydb.commit()


def delete_a_book():
    mycursor = mydb.cursor()
    Sort_Everything_By_Names(1)
    book_details()
    flag = 0
    book_to_be_deleted = ""
    want_to_delete = 'y'
    while (want_to_delete == 'y' or want_to_delete == 'Y'):
        try:
            a = int(input("\nEnter the Book No To be deleted : "))
        except:
            print("\nOnly integer inputs are accepted!!! ")
            a = int(input("\nEnter the Book No To be deleted : "))
        for i in books_with_srno:
            if i + 1 == a:
                book_to_be_deleted = books_with_srno[i]
                flag = 1
        if flag == 0:
            print("Book Not Found!!!")
            want_to_delete = input("Do you want to delete a book ? (y/n) ")
        elif flag == 1:
            stmt = "Delete from Sorted_Books where Book_Name = '" + book_to_be_deleted + "';"
            mycursor.execute(stmt)
            stmt = "Delete from Books where Book_Name = '" + book_to_be_deleted + "';"
            mycursor.execute(stmt)
            book_details()
            want_to_delete = input("Do you want to delete another book ? (y/n) ")
    mydb.commit()


def staffandstud_Check(Usrnme, Pass, SorSt):
    if SorSt == 1:  # Means Checking for staff
        mycursor = mydb.cursor()
        mycursor.execute("Use Staff;")
        stmt = "Select Password From Staffmembers where User_name = " + "'" + Usrnme + "';"
        #print(stmt)
        mycursor.execute(stmt)
        string = [""]
        for i in mycursor:
            string += i
        print(string)
        try:
            if (Pass == string[1]):
                return 1
            else:
                return 0
        except:
            return 0
            # print("\nThe Details are nowhere to be found! Sorry!!!")
    elif SorSt == 2:
        mycursor = mydb.cursor()
        mycursor.execute("Use Staff;")
        stmt = "Select Password From Students where User_name = " + "'" + Usrnme + "';"
        print(stmt)
        mycursor.execute(stmt)
        string = [""]
        for i in mycursor:
            string += i
        print(string)
        try:
            if (Pass == string[1]):
                return 1
            else:
                return 0
        except:
            return 0
            # print("\nThe Details are nowhere to be found! Sorry!!!")


def staffstore(F, L, U, P, A):
    mycursor = mydb.cursor()  # A=1 : For Registering A Staff Member. A=2: For inserting Student information
    mycursor.execute("Use staff;")
    if A == 1:
        try:
            mycursor.execute(
                "CREATE TABLE Staffmembers(First_Name varchar(50),Last_Name varchar(50),User_Name varchar(50) Unique,Password varchar(50) Not Null);")
            mycursor.execute("insert into Staffmembers values('" + F + "','" + L + "','" + U + "','" + P + "');")
        except:
            mycursor.execute("insert into Staffmembers values('" + F + "','" + L + "','" + U + "','" + P + "');")
            mycursor.execute("select * from Staffmembers;")
        for i in mycursor:
            print(i)
        mydb.commit()
    elif A == 2:
        try:
            mycursor.execute(
                "CREATE TABLE Students(First_Name varchar(50),Last_Name varchar(50),User_Name varchar(50) Unique,Password varchar(50) Not Null);")
            mycursor.execute("insert into Students values('" + F + "','" + L + "','" + U + "','" + P + "');")
        except:
            mycursor.execute("insert into Students values('" + F + "','" + L + "','" + U + "','" + P + "');")
            mycursor.execute("Select * from Students;")
        for i in mycursor:
            print(i)
        mydb.commit()


def registerstud():                                                                                                                                                         # This section will go under GUI
    fnme = input("\nFirst Name : ")
    lnme = input("\nLast Name : ")
    usrnme = input("\nPreferred User Name : ")
    while (True):
        passs = input("\nPassword : ")
        tpass = input("\nRetype Password : ")
        if tpass != passs:
            print("\nPassword Don't match!")
            t.sleep(0.500)
        else:
            break
    staffstore(fnme, lnme, usrnme, passs, 2)


def delete_a_student():
    mycursor = mydb.cursor()
    Sort_Everything_By_Names(2)
    student_details()
    flag = 0
    student_to_be_deleted = ""
    want_to_delete = 'y'
    while (want_to_delete == 'y' or want_to_delete == 'Y'):
        try:
            a = int(input("\nEnter the Number of the Student To be deleted : "))
        except:
            print("\nOnly integer inputs are accepted!!! ")
            a = int(input("\nEnter the Number of the Student To be deleted : "))
        for i in students_with_srno:
            if i + 1 == a:
                student_to_be_deleted = students_with_srno[i]
                flag = 1
        if flag == 0:
            print("Student Not Found!!!")
            want_to_delete = input("Do you want to delete a Student ? (y/n) ")
        elif flag == 1:
            stmt = "Delete from Sorted_St where User_Name = '" + student_to_be_deleted + "';"
            mycursor.execute(stmt)
            stmt = "Delete from Students where User_Name = '" + student_to_be_deleted + "';"
            mycursor.execute(stmt)
            student_details()
            want_to_delete = input("Do you want to delete another Student ? (y/n) ")
    mydb.commit()


def registerstaff():  # This section will go under GUI
    fnme = input("\nFirst Name : ")
    lnme = input("\nLast Name : ")
    usrnme = input("\nPreferred User Name : ")
    while (True):
        passs = input("\nPassword : ")
        tpass = input("\nRetype Password : ")
        if tpass != passs:
            print("\nPassword Don't match!")
            t.sleep(0.500)
        else:
            break
    mycursor = mydb.cursor()  # A=1 : For Registering A Staff Member. A=2: For inserting Student information
    mycursor.execute("Use staff;")
    try:
        mycursor.execute(
            "CREATE TABLE Staffmembers(First_Name varchar(50),Last_Name varchar(50),User_Name varchar(50) Unique,Password varchar(50) Not Null);")
        mycursor.execute(
            "insert into Staffmembers values('" + fnme + "','" + lnme + "','" + usrnme + "','" + passs + "');")
    except:
        mycursor.execute(
            "insert into Staffmembers values('" + fnme + "','" + lnme + "','" + usrnme + "','" + passs + "');")
    mycursor.execute("select * from Staffmembers;")
    for i in mycursor:
        print(i)


def loginstaff():
    print("\t\t\tWelcome to Login Page! ")
    usrnme = input("\nUser ID : ")
    passs = input("\nPassword : ")
    present = int(staffandstud_Check(usrnme, passs, 1))
    return present


def loginstudent():
    usrnme = input("\nUser ID : ")
    passs = input("\nPassword : ")
    present = staffandstud_Check(usrnme, passs, 2)
    return present


#main code

print("\t\t\t|| Welcome to Library Management || ")
try:
    stop = int(input("\n1.STAFF\n2.STUDENT\n3.Exit\nEnter you Choice : "))
except:
    print("\nOnly integer inputs are accepted!!! ")
    stop = int(input("\n1.STAFF\n2.STUDENT\n3.Exit\nEnter you Choice : "))
mycursor = mydb.cursor()

if stop == 1:
    print("Loading ...", end="")
    for i in range(0, 5):
        delaytime = (random.randint(250, 1000))
        print(".....", end="")
        t.sleep(delaytime / 1000)
    staffopt = 0
    while (staffopt != 3):
        print("\n\t\t\t|| Welcome to Library Management for Staff || ")
        try:
            staffopt = int(input("\n1.Register a New Staff.\n2.Login For an Existing Staff.\n3.Exit\nEnter Your Choice : "))
        except:
            print("\nOnly integer inputs are accepted!!! ")
            staffopt = int(input("\n1.Register a New Staff.\n2.Login For an Existing Staff.\n3.Exit\nEnter Your Choice : "))


        if staffopt == 1:
            try:
                mycursor.execute("CREATE DATABASE STAFF")
                registerstaff()
            except:
                registerstaff()

        elif staffopt == 2:
            if (loginstaff() == 1):
                print("\nLogin Success!!!")
                stafflogin = 0
                while (stafflogin != 7):
                    print("\n\t\t|| LIBRARY MANAGEMENT SYSTEM (AUTHORIZED ONLY) ||")
                    print(
                        "\n1.Store a Book\n2.Delete a book\n3.Show All Books\n4.Add a student\n5.Remove a Student\n6.Show All Students\n7.Exit\n")
                    try:
                        stafflogin = int(input("Enter a choice : "))
                    except:
                        print("\nOnly integer inputs are accepted!!! ")
                        stafflogin = int(input("Enter a choice : "))
                    if stafflogin == 1:
                        store_a_book()
                        Sort_Everything_By_Names(1)

                    elif stafflogin == 2:
                        delete_a_book()

                    elif stafflogin == 3:
                        Sort_Everything_By_Names(1)
                        book_details()

                    elif stafflogin == 4:
                        registerstud()
                        Sort_Everything_By_Names(2)

                    elif stafflogin == 5:
                        delete_a_student()

                    elif stafflogin == 6:
                        Sort_Everything_By_Names(2)
                        student_details()

                    elif stafflogin == 7:
                        print("\nThank You!!!")
                        t.sleep(1.000)
                        exit(0)

                    else:
                        print("\nPlease select from the given options!!!\n")

            else:
                print("\nIncorrect User ID or Password!!!")
                print("\nPlease Try Registering! \n")
                t.sleep(1.000)
                staffopt=0

        elif staffopt == 3:
            print("\nThank You!!!!")
            t.sleep(1.000)
            exit(0)
        else:
            print("\nChoose from the given Options!!!")
            t.sleep(1)

elif stop == 2:

    print("Loading ...", end="")

    for i in range(0, 5):
        delaytime = (random.randint(250, 1000))
        print(".....", end="")
        t.sleep(delaytime / 1000)

    print("\n\t\t\t || Welcome to Library Management or Student || ")
    # print("\n1.Login for an Existing Student.\n2.Go Back to previous Menu.\n3.Exit\n")
    # studop=int(input("\nEnter your Choice : "))

    # if studop==1:
    if loginstudent():
        print("\nLogin Successfull.\n")
        print("Loading...", end="")
        for i in range(0, 5):
            delaytime = (random.randint(250, 1000))
            print(".....", end="")
            t.sleep(delaytime / 1000)
        studlogin = 0
        while (studlogin != 3):
            print("\n\t\tLIBRARY MANAGEMENT SYSTEM (STUDENTS)")
            print("\n1.Book's List. \n2. Book Details. \n3. Exit.")
            try:
                studlogin = int(input("\nEnter the choice : "))
            except:
                print("\nOnly integer inputs are accepted!!! ")
                studlogin = int(input("\nEnter the choice : "))
            if studlogin == 1:
                Sort_Everything_By_Names(1)
                book_details()

            elif studlogin == 2:
                Sort_Everything_By_Names(1)
                book_auth_details()

            elif studlogin == 3:
                print("\nThank You!!!")
                t.sleep(1.000)
                exit(0)

            else:
                print("\nPlease select from the given options! ")
                t.sleep(1.000)
        else:
            print("\nLogin Details Not Found!!!")
        # elif studop == 2:
        #     print("Loading ...")
        #     for i in range(0, 5):
        #         delaytime = (random.randint(250, 1000))
        #         print(".....")
        #         t.sleep(delaytime / 1000)
        #
        # elif studop == 3:
        #     print("\nThank You!!!")
        #     t.sleep(1.000)
        #     exit(0)
        #
        # else:
        #     print("\nChoose from the given Options !!! ")
        #     t.sleep(1.000)

elif stop == 3:
    print("\nThank You!!!")
    t.sleep(1.000)

mydb.close()
print("\nThank You!!!!")
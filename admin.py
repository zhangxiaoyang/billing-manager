#!/usr/bin/env python
# -*- coding: utf-8 -*-  
import sys
import models
import time

db = models.db()

def usage():
    print "usage:"
    print "./admin.py  actor    [name]"
    print "./admin.py  deposit  [name]  [money]"
    print "./admin.py  expense  [money] [details]"
    print "./admin.py  list"

'''
    actor
'''
def show_actor():
    print "NAME\tNAME_ID"
    if None == db.show_table("actor"):
        print "Show table error!"
        
def add_actor(name):
    if name != "_default_":
        nameid = 2 ** (len(db.get_table("actor"))-1)
        if None == db.add_row("actor", ["\"" + name + "\"", str(nameid)]):
            print "Add actor error!"
        else:
            show_actor()
    else:
        show_actor()
        s = input("Input sum: ")
        if None == db.set_item("actor", "nameid", str(s), "name", "\"" + "_default_" + "\""):
            print "Update default field error!"
        show_actor()
'''
    deposit
'''
def show_deposit():
    print "DATE\tMONEY\tNAME_ID"
    if None == db.show_table("deposit"):
        print "Show table error!"

def add_deposit(name, money):
    t = time.strftime("%Y-%m-%d %H:%M", time.localtime(time.time()))
    nameid = db.get_item("actor", "nameid", "name", "\"" + name + "\"")
    if nameid == None:
        print "Can\'t find actor: ", name
        exit(1)

    if None == db.add_row("deposit", ["\"" + t + "\"",  str(money), str(nameid)]):
        print "Add deposit error!"
    else:
        show_deposit()

'''
    expense
'''
def show_expense():
    print "DATE\tMONEY\tDETALS\tNAME_ID_SET"
    if None == db.show_table("expense"):
        print "Show table error!"

def add_expense(money, details):
    nameids = db.get_item("actor", "nameid", "name", "\"" + "_default_" + "\"")
    if nameids == None:
        print "Database error! Can\'t find default field!"
        exit(1)
    else:
        flag = 0
        s = str(bin(nameids)[2:])
        for i in range(1, 1000):
            if i > len(s):
                break
            nameid = int(s[-1*i]) * (2**(i-1))
            if nameid != 0:
                name = db.get_item("actor", "name", "nameid", str(nameid))
                if name == None:
                    print s[ -1*i]
                    print i-1

                    print nameid, "Database error! Can\'t find default value!"
                else:
                    print name + " ",
                    flag = 1

        if flag == 0:
            print "No sharing! Execute ./admin.py actor _default_ !"
            exit(1)
        else:
            print "go shares"

    t = time.strftime("%Y-%m-%d %H:%M", time.localtime(time.time()))
    if None == db.add_row("expense", ["\"" + t + "\"" , str(money), "\"" + details + "\"", str(nameids)]):
        print "Add expense error!"

'''
    list
'''
def show_list():
    actor = list()
    deposit = list()
    expense = list()

    l = db.get_row("actor")
    for row in l:
        if row[0] != "_default_":
            actor.append(row[0]) 
    
    for row in l:
        if row[0] != "_default_":
            nameid = row[1]
            tb = db.cmd("select sum(money) from deposit where nameid = " + str(nameid) + " group by nameid")
            if tb != None:
                deposit.append(tb[0][0])
    
    for row in l:
        if row[0] != "_default_":
            nameid = row[1]
            s = 0.0
            tb = db.cmd("select money, nameids from expense")
            if tb != None:
                for i in tb:
                    if nameid & i[1] == nameid:
                        num = 0.0
                        for j in list(str(bin(i[1])[2:])):num += int(j)
                        s += i[0]/num
            expense.append(s)

    for i in actor:
        print "%20s" % i,
    print ""

    for i in deposit:
        print "%20s" % i,
    print ""

    for i in expense:
        print "%20s" % i,
    print ""

    for i in [ deposit[i] - expense[i] for i in range(len(deposit)) ]:
        print "%20s" % i,
    print ""
    
'''
    main
'''
if __name__ == "__main__":
    
    try:
        db.open_db("./bills.db")
    except:
        print "Can\'t find database file!"
        exit(1)

    try:
        if sys.argv[1] == "actor":
            if len(sys.argv) == 2:
                show_actor()
            else:
                add_actor(sys.argv[2])

        elif sys.argv[1] == "deposit":
            if len(sys.argv) == 2:
                show_deposit()
            else:
                add_deposit(sys.argv[2], sys.argv[3])

        elif sys.argv[1] == "expense":
            if len(sys.argv) == 2:
                show_expense()
            else:
                add_expense(sys.argv[2], sys.argv[3])
        
        elif sys.argv[1] == "list":
            show_list()
    except:
        usage()
    
    try:
        db.close_db()
    except:
        print "Disconnect database error!"

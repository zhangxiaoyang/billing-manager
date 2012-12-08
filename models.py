#!/usr/bin/env python
# -*- coding: utf-8 -*-  
import sqlite3
class db:
    conn = None

    def open_db(self, dbname):
        try:
            self.conn = sqlite3.connect(dbname)
            return 1
        except:
            return None

    def show_table(self, tbname):
        try:
            tb = self.conn.execute("select * from " + tbname)
            for row in tb.fetchall():
                for item in row:
                    print item, "\t",
                print ""
            
            return 1
        except:
            return None

    def add_row(self, tbname, items):
        sql = "insert into " + tbname + " values (";
        for i in range(1000):
            if len(items) == i + 1:
                sql += items[i] + ")"
                break
            else:
                sql += items[i] + ", "
        try:
            self.conn.execute(sql)
            self.conn.commit()
            return 1
        except:
            return None
    
    def get_table(self, tbname):
        tb = self.conn.execute("select * from " + tbname)
        return tb.fetchall()
    
    def get_item(self, tbname, q, col, colval):
        try:
            tb = self.conn.execute("select " + q + " from " + tbname + " where " + col + " = " + colval)
            tb = tb.fetchall()
            if len(tb) == 0:
                return None
            else:
                return tb[0][0]
        except:
            return None
    
    def set_item(self, tbname, col1, colval1, col2, colval2):
        try:
            self.conn.execute("update " + tbname + " set " + col1 + " = " + colval1 + " where " + col2 + " = " + colval2)
            return 1
        except:
            return None
    
    def get_row(self, tbname):
        try:
            tb = self.conn.execute("select * from " + tbname)
            tb = tb.fetchall()
            return tb
        except:
            return None

    def cmd(self, sql):
        try:
            tb = self.conn.execute(sql)
            tb = tb.fetchall()
            return tb
        except:
            return None
    def close_db(self):
        try:
            self.conn.close()
            return 1
        except:
            return None


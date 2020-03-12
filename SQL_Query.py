'''This file contains a sqlite class which includes all the required methods for inserting, updating stuff.''' 

# Load reqd libraries
import sqlite3
import datetime

# create a global variable for connectObject and crsr
global connectObject 
connectObject = sqlite3.connect('Emp.db')
global crsr
crsr = connectObject.cursor()


checkoutTime = None
x = None

class sqliteObject():

	DB_Location = "/database/location/Emp.db"

	def __init__ (self):
		# tablename = 'sheet15'
		# self.database = database
		self.connect = sqlite3.connect(sqliteObject.DB_Location)
		self.cursor = self.connect.cursor()
		# self.connect.execute("PRAGMA journal_mode=WAL") # to improve concurrency
		self.connected = True


	def createTable(self ):
		self.cursor.execute("""CREATE TABLE IF NOT EXISTS SHEET60(
                    ID INTEGER,
                    DATE_ TIMESTAMP NULL,
                    NAME TEXT,
                    CHECKIN TIMESTAMP NULL,
		    		CHECKOUT TIMESTAMP NULL,
		    		PRIMARY KEY (DATE_, NAME))""") # this is to avoid multiple instance problem
		self.connect.commit()
		# self.connect.close()

#-------------------------------------------------COMMENTED CONNECT FUNCTION BCOZ I HAD INSERTED THE SAME CODE UNDER INIT METHOD

# connect function - connects the database mentioned
	def connect(self):
		self.connect = sqlite3.connect(self.database)
		self.cursor = self.connect.cursor()
		# self.connect.execute("PRAGMA journal_mode=WAL") # to improve concurrency
		self.connected = True

# close - commits any changes and closes the same
	def close(self):	
		self.connect.commit()
		self.connect.close()
		self.connected = False


	def updateCheckout(self, name, checkoutTime):
		self.checkoutTime = checkoutTime
		self.name = name	
		if not self.connected:
			self.connect()
		else:
			self.checkoutTime = str(datetime.datetime.now().hour) +':'+ str(datetime.datetime.now().minute)
			args = (self.checkoutTime, self.name) # list up the data required \

			arg1 = self.checkoutTime
			
			# No need to use try and except here. Use if you need it.
			
			try:
				print(args)
				# QUERY UPDATES LATEST CHECKOUT TIME
				connectObject.execute("UPDATE SHEET60 SET checkout = ? WHERE checkout IS NULL  ", arg1)
				# QUERY UPDATES ONLY THE FIRST CHECKOUT TIME
				connectObject.execute("UPDATE SHEET60 SET checkout = ? WHERE checkout IS NULL AND NAME = ? ", args)
				print('No updates')
				connectObject.commit()
				print('time updated..')
			except Exception as e:
				print(e)
				# connectObject.execute("UPDATE SHEET101 SET checkout = ?", args)
				# connectObject.commit()
				# connectObject.close() # save changes here


	def insertData(self, ID, Date, name, checkin, checkout):
		self.ID = ID
		self.Date = Date
		self.name = name
		self.checkin = checkin
		self.checkout = checkout

		if not self.connected:
			self.connect()
		else:
			x = datetime.datetime.today() 
			Date = x.strftime("%d-%m-%Y")
			args = (self.ID, self.Date, self.name, self.checkin, self.checkout)
			connectObject.execute("INSERT INTO SHEET60 VALUES (?, ?, ?, ?, ?)",args)
			connectObject.commit() # save changes here
			# connectObject.close()


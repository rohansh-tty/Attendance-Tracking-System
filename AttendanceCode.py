# load all the libraries
import cv2
import datetime
import openpyxl # this lib is used to read and write files
import xlsxwrite
import os

# day, date and month variables
now = datetime.datetime.now()
today = now.day
month = now.month


# # create a worksheet
# book =  openpyxl.Workbook()
# attendance_sheet = book.active

# create a new workbook
w1 = xlsxwriter.Workbook('sample1.xlsx')
# add a new worksheet
ws =w1.add_worksheet()
import datetime
date = datetime.datetime.today().strftime('%Y-%m-%d')

# widen the col A for extra visibility
ws.set_column('A:A',30)

# date format for each column
format2 = w1.add_format({'num_format': 'dd/mm/yy'})
ws.write('B1', date, format2)       # 28/02/13

# generate the dates
#
# for cell in Sheet1.row: # IDK what to do just leave it
#
#     value = cell.value
#
#     response = os.system("ping -n 2" + value)
#     s.write(value, 'is up' if response == 0 else 'is down)
#

w1.close() # this is a mandatory line inorder for you to create a new file or update the same
# w1("sample1.xlsx")


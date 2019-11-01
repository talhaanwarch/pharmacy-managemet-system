# -*- coding: utf-8 -*-
"""
Created on Tue Oct 22 15:17:12 2019

@author: Talha
"""

from tkinter import *
import sqlite3
import pandas as pd
from tabulate import tabulate


mydb=sqlite3.connect("medicines.db")
cursor=mydb.cursor()






root=Tk()

#create main frame
main_frame=Frame(root)
main_frame.grid()


#create heading frame
header_frame=Frame(main_frame,width=1000,bg='cadet blue',bd=4,relief='ridge')
header_frame.pack(fill='x')

header_label=Label(header_frame,text='Al Khair Eye Care',bg='cadet blue',fg='white',font=('arial',25,'bold'))
header_label.pack()


#create login box
login_frame=Frame(main_frame,width=1000,height=70,padx=10,bg='cadet blue',bd=4,relief='ridge')
login_frame.pack(fill='x')

login_label=Label(login_frame,text='user name  ',font=('arial',15),bg='cadet blue')
login_label.pack(side='left')

login_label_entry=Entry(login_frame)
login_label_entry.config(font=('arial',15))
login_label_entry.pack(side='left')

pass_label_entry=Entry(login_frame)
pass_label_entry.config(font=('arial',15))
pass_label_entry.pack(side='right')

pass_label=Label(login_frame,text='  password  ',font=('arial',15),bg='cadet blue')
pass_label.pack(side='right')

#create middle frame
middle_frame=Frame(main_frame,bd=4,width=1000,height=300,relief='ridge',bg='cadet blue')
middle_frame.pack()

#create left and right frame in middle frame
left_frame=LabelFrame(middle_frame,text='Add data',font=('arial',15),bd=2,width=500,height=300,relief='ridge',bg='cadet blue')
left_frame.pack(side='left')

right_frame=LabelFrame(middle_frame,text='Update data',font=('arial',15),bd=2,width=500,height=300,relief='ridge',bg='cadet blue')
right_frame.pack(side='right')

#create bottom frame
bottom_frame_update=LabelFrame(main_frame,text='update qty and price',font=('arial',15),bd=2,width=500,height=300,relief='ridge',bg='cadet blue')
bottom_frame_update.pack(side='bottom',fill='x')



#now create labels and entry boxes for add data frame
def submit(): #if we remove event , binding will stop working
    ##add data to db
    insertion='INSERT INTO medicines (name,code,qty,price) VALUES (?,?,?,?)'
    record=(enter_name.get().lower(),enter_code.get().lower(),enter_qty.get(),enter_price.get())
    cursor.execute(insertion,record)
    mydb.commit()
    enter_name.delete(0,END)
    enter_code.delete(0,END)
    enter_qty.delete(0,END)
    enter_price.delete(0,END)
    cursor.execute('SELECT COUNT(id) FROM medicines')
    count=cursor.fetchone()[0]
    label=Label(left_frame,text='Total medicines added '+ str(count))
    label.place(relx=0.3,rely=0.6)


name=Label(left_frame,text='Enter name of medicines',bg='cadet blue',font=('arial',11))
name.place(relx=0.05,rely=0.1)
enter_name=Entry(left_frame,font=('arial',12))
enter_name.place(relx=0.5,rely=0.1)

code=Label(left_frame,text='Enter Code',bg='cadet blue',font=('arial',11))
code.place(relx=0.05,rely=0.2)
enter_code=Entry(left_frame,font=('arial',12))
enter_code.place(relx=0.5,rely=0.2)

qty=Label(left_frame,text='Enter quantity of medicines',bg='cadet blue',font=('arial',11))
qty.place(relx=0.05,rely=0.3)
enter_qty=Entry(left_frame,font=('arial',12))
enter_qty.place(relx=0.5,rely=0.3)

price=Label(left_frame,text='Enter price per item',bg='cadet blue',font=('arial',11))
price.place(relx=0.05,rely=0.4)
enter_price=Entry(left_frame,font=('arial',12))
enter_price.place(relx=0.5,rely=0.4)



button=Button(left_frame,text='submit',command=submit,fg='white',bg='black',width=10)
button.place(relx=0.3,rely=0.5)
#button.bind('<Return>',submit)
root.bind('<Return>',submit)


#fetch data according to date
def fetch_date():
    cursor.execute('SELECT date,SUM(qty), SUM(price) FROM transactions GROUP BY date ORDER BY date DESC')
    date=cursor.fetchall()
    data=pd.DataFrame(date,columns=['Date','Price','Quantity'])
    newwin=Toplevel(right_frame)
    newwin.geometry('600x800')
    Label_data=Label(newwin,text=tabulate(data, headers='keys',tablefmt='psql',showindex=False),font=('Consolas',14))
    Label_data.place(x=20,y=10)
    



def display_date():
    cursor.execute('SELECT * FROM medicines')
    disp=cursor.fetchall()
    disp=pd.DataFrame(disp,columns=['id','name','code','qty','price'])
    newwin = Toplevel(right_frame)
    newwin.geometry('600x800')
    Label_data=Label(newwin,text=tabulate(disp, headers='keys',tablefmt='github',showindex=False),font=('Consolas',14))
    Label_data.place(x=20,y=50)

button_date=Button(right_frame,text='Display',command=display_date)
button_date.place(x=100,y=20)

#date_label=Label(right_frame,text='fetch',bg='cadet blue',font=('arial',11))
#date_label.place(x=0,y=10)

button_date=Button(right_frame,text='fetch',command=fetch_date)
button_date.place(x=30,y=20)




# create qty update for bottom update box
cursor.execute('SELECT name FROM medicines')
result=cursor.fetchall()
def update_qty_data():
    global S
    isf=clicked_qty.get()
    r=isf[isf.find("'")+len("'"):isf.rfind("'")]
    print(r)
    S="'"+r+"'"
    cursor.execute("UPDATE medicines SET qty =qty+ {} WHERE name = {} ".format(entry_update_qty.get(),S))
    mydb.commit()
    print(S)
    cursor.execute("Select name,qty FROM medicines WHERE name = {} ".format(S))
    update_qty=cursor.fetchall()

    label=Label(bottom_frame_update,text='{} new qty is {}'.format(update_qty[0][0],update_qty[0][1]))
    label.place(relx=0.8,rely=0.1)
        
clicked_qty=StringVar()    
update_qty=Label(bottom_frame_update,text='update qty of medicines',font=('arial',11))
update_qty.place(relx=0.01,rely=0.1)

menu_update_qty=OptionMenu(bottom_frame_update,clicked_qty,*result)
menu_update_qty.config(width=10,padx=10,font=('arial',11))
menu_update_qty.place(relx=0.26,rely=0.1)

entry_update_qty=Entry(bottom_frame_update,width=15,borderwidth=5,font=('arial',11))
entry_update_qty.place(relx=0.45,rely=0.1)
select_qty=Button(bottom_frame_update,text='select & update',command=update_qty_data,fg='white',bg='black',width=20)
select_qty.place(relx=0.6,rely=0.1)





#update price in bottom update box

def update_price_data():
    global R
    isf=clicked.get()
    r=isf[isf.find("'")+len("'"):isf.rfind("'")]
    
    R="'"+r+"'"
    cursor.execute("UPDATE medicines SET price = {} WHERE name = {} ".format(entry_update_price.get(),R))
    mydb.commit()
    print(R)
    cursor.execute("Select name,price FROM medicines WHERE name = {} ".format(R))
    update_price=cursor.fetchall()

    label=Label(bottom_frame_update,text='{} new price is {}'.format(update_price[0][0],update_price[0][1]))
    label.place(relx=0.8,rely=0.3)
        
clicked=StringVar()    
update_price=Label(bottom_frame_update,text='update price of medicines',font=('arial',11))
update_price.place(relx=0.01,rely=0.3)

menu_update_price=OptionMenu(bottom_frame_update,clicked,*result)
menu_update_price.config(width=10,padx=10,font=('arial',11))
menu_update_price.place(relx=0.26,rely=0.3)

entry_update_price=Entry(bottom_frame_update,width=15,borderwidth=5,font=('arial',11))
entry_update_price.place(relx=0.45,rely=0.3)
select_price=Button(bottom_frame_update,text='select & update',command=update_price_data,fg='white',bg='black',width=20)
select_price.place(relx=0.6,rely=0.3)



root.configure(bg='cadet blue')
root.geometry('1000x600')
root.mainloop()
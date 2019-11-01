# -*- coding: utf-8 -*-
"""
Created on Wed Oct 23 17:08:53 2019

@author: Talha
"""

from tkinter import *
import numpy as np
import sqlite3
import pandas as pd
from tabulate import tabulate


mydb=sqlite3.connect("medicines.db")
cursor=mydb.cursor()


#create a list to append all products purchased by customer
med_list=[]
qty_list=[]
price_list=[]
med_name=[]

root=Tk()

main_frame=Frame(root,bg='white')
main_frame.place(x=0,y=0)

header_frame=Frame(main_frame,width=1000,bg='cadet blue',bd=4,relief='ridge')
header_frame.pack(fill='x')

header_label=Label(header_frame,text='Al Khair Eye Care',bg='cadet blue',fg='white',font=('arial',25,'bold'))
header_label.pack()

left_frame=Frame(main_frame,width=600,height=550,bg='white')
left_frame.pack(side='left')

right_frame=Frame(main_frame,width=400,height=550,bg='lightblue')
right_frame.pack(side='right')

right_frame_header=Frame(right_frame,width=400,height=40,bg='lightblue')
right_frame_header.pack(side='top')

right_frame_body=Frame(right_frame,width=400,height=510,bg='lightblue')
right_frame_body.pack(side='bottom')


#fill right frame
label_name_right=Label(right_frame_header,text='Medicie',font=('arial',15))
label_name_right.place(x=10,y=10)

label_qty_right=Label(right_frame_header,text='Quantity',font=('arial',15))
label_qty_right.place(x=150,y=10)

label_amount_right=Label(right_frame_header,text='Amount',font=('arial',15))
label_amount_right.place(x=280,y=10)





#fill left frame
label_name_left=Label(left_frame,text='Enter Medicines Name',font=('arial',15))
label_name_left.place(x=10,y=10)

entry_name_left=Entry(left_frame,font=('arial',15),bg='light blue')
entry_name_left.place(x=290,y=10)

label_qty_left=Label(left_frame,text='Enter quantity',font=('arial',15))
label_qty_left.place(x=10,y=50)

entry_qty_left=Entry(left_frame, font=('arial',15),bg='light blue')
entry_qty_left.place(x=290,y=50)


label_price_rec=Label(left_frame,text='Amount paid by Customer',font=('arial',15))
label_price_rec.place(x=10,y=200)
entry_price_rec=Entry(left_frame,font=('arial',15),width=10,bg='light blue')
entry_price_rec.place(x=350,y=200)

def balance(temp_final):
    balance_amount=float(entry_price_rec.get())-float(temp_final)
    if balance_amount<0:
        messagebox.showwarning('Warning','Amound paid is less than total dues')
    else:
        remain_label=Label(left_frame,text='Remaining amount : '+str(balance_amount),font=('arial',15))
        remain_label.place(x=20,y=400)
    #entry_price_rec.delete(0,END)

#search medicine in database
def add_cart():

    
    med_code="'"+entry_name_left.get()+"'"
    med_qty=int(entry_qty_left.get())
    cursor.execute('SELECT * FROM medicines WHERE code={}'.format(med_code))
    med=cursor.fetchall()
    if med_qty>med[0][3]:
        messagebox.showinfo('error','Medicine quantity in stock is less than entered ')
    else:
        med_name.append(med[0][1])
        final_price=med_qty*med[0][4]
        med_list.append(entry_name_left.get())
        qty_list.append(med_qty)
        price_list.append(final_price)
        #print(med_list,qty_list,price_list)
        y_index=10
        global counter
        counter=0
        global temp_final

        for i in med_name:
            temp_med=Label(right_frame_body,text=str(med_name[counter]))
            temp_med.place(x=10,y=y_index)
            temp_qty=Label(right_frame_body,text=str(qty_list[counter]))
            temp_qty.place(x=150,y=y_index)
            temp_price=Label(right_frame_body,text=str(price_list[counter]))
            temp_price.place(x=300,y=y_index)
            temp_final=sum(price_list)
            temp_final_label=Label(right_frame_body,text='Total Price' + 'Rs.' + str(temp_final),font=('arial',20))
            temp_final_label.place(x=100,y=400)
            #balance(temp_final)
            
            y_index+=30
            counter+=1
        entry_name_left.delete(0,END)
        entry_qty_left.delete(0,END)

from datetime import date
today = date.today()
#updata data
def update_db():
    for i,j,k in zip(med_list,qty_list,price_list):
        print(i,j,k)
        cursor.execute('UPDATE medicines SET qty=qty-{} WHERE code = {}'.format(j,"'"+i+"'"))
        mydb.commit()
        cursor.execute('INSERT into transactions (name,price,qty,date) VALUES (?,?,?,?)',(i,j,k,today))
        mydb.commit()
        
        balance(temp_final)
    for child in right_frame_body.winfo_children():
        child.destroy()
    del (med_list[:])
    del (qty_list[:])
    del (price_list[:])
    del (med_name[:])



def display_date():
    cursor.execute('SELECT * FROM medicines')
    disp=cursor.fetchall()
    disp=pd.DataFrame(disp,columns=['id','name','code','qty','price'])
    newwin = Toplevel(right_frame)
    newwin.geometry('700x800')
    Label_data=Label(newwin,text=tabulate(disp, headers='keys',tablefmt='github',showindex=False),font=('Consolas',14))
    Label_data.place(x=0,y=0)




btn_update=Button(left_frame,text='Print',command=update_db,width=80,relief='ridge')
btn_update.place(x=0,y=250)    
    
btn_update=Button(left_frame,text='Display',command=display_date,width=80,relief='ridge')
btn_update.place(x=0,y=300)  

btn_add_cart=Button(left_frame,text='Add to cart',command=add_cart)
btn_add_cart.place(x=300,y=100)



root.geometry('1000x600')
root.mainloop()
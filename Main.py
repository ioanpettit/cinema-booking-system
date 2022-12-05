

#! pip install tkinter
#! pip install customtkinter


# importing packages
import names
import random
import pandas as pd
import numpy as np
import win32com.client as client
import sqlite3
from tkinter import *
from tkinter import ttk
import customtkinter



#drawing random names
random.seed(10) # set seed to ensure same names each time
men = [names.get_full_name(gender='male') for i in range(0,35)]
women = [names.get_full_name(gender='female') for i in range(0,35)]
pnts = [names.get_full_name() for i in range(0,5)]
other = [names.get_full_name() for i in range(0,5)]


# creating a list of all names
everyone = men+women+pnts+other
random.seed(10)
random.shuffle(everyone)


# appending gender based on their name from before
gender = []
for i in everyone:
    if i in men:
        gender.append('male')
    elif i in women:
        gender.append('female')
    elif i in pnts:
        gender.append('prefer not to say')
    else:
        gender.append('other')



# setting up Customers dataframe, setting seed to ensure same ages and email each time
random.seed(10)
Customers = pd.DataFrame({'ID':range(1,81),'Name':everyone,'Gender':gender, 
                          'Age':[random.randint(12,90) for i in range(len(everyone))],
                         'Email Address':[i.replace(' ','').lower()+random.choice(['@notreal.com','@fakemail.com','@madeup.com']) for i in everyone]})


# creating a dataframe of the films 
Films = pd.DataFrame({'ID': range(1,6), 'Name':['Avatar: The Way of Water', 
                                                'Black Panther: Wakanda Forever',
                                                'She Said',
                                                'Glass Onion: A Knives Out Mystery',
                                               'Aftersun'],
                     'Genre': ['Fantasy','Action','Drama','Mystery','Drama'],
                                           'Rating': [12,12,15,12,12]})
                    


# creating a dataframe of the showings
times = []
Showings = pd.DataFrame({'ID': range(1,9),'Time':['2022-12-5 08:30','2022-12-5 09:00', '2022-12-5 11:15', '2022-12-5 11:15','2022-12-5 13:05','2022-12-5 14:00','2022-12-5 16:50', '2022-12-5 20:00'], 'Screen':[1,3,4,2,4,3,2,1], 'Film ID':[4,2,1,5,3,2,4,1]})



# Creating the seat options available for each showing
seat_options = []
for k in range(1,9):
    for i in ['A','B','C','D']:
        for j in range(1,6):
            seat_options.append(f'S{k} {i}{j}')


# making 80 seat choices randomly from the ones available
random.seed(10) # set seed
seat_options_remove = seat_options.copy() # creating a new data frame from which we can remove the chosen seats
seat_number = [] # list to append chosen seats
for i in range(1,81):
    choice = random.choice(seat_options_remove) # choosing a seat 
    seat_options_remove.remove(choice) # rmeoving this seat so it can't be chosen again
    seat_number.append(choice) # appending choice to list


# creating a dataframe for the bookings
random.seed(10) # set seed
showingid = [i[1:2] for i in seat_number] # taking the showing number from the list
bookings = pd.DataFrame({'ID':range(1,81),'Customer ID':random.sample(range(1,81),80), # sampling a random customer ID
                         'Showing ID': showingid, 
                        'Seat Number': [i[-2:] for i in seat_number]}) # taking the seat number from the list


# split up the lists based on screening. This is for the combination dropdown box in the UI
# need the dropdown box to change based on which film is selected
screening_free = dict()

for i in range(len(Showings)):
    screening_free[i+1] = []

for j in range(len(seat_options_remove)):
    for k in range(len(Showings)):
        if seat_options_remove[j][0:2] == f'S{k+1}':
            screening_free[k+1].append(seat_options_remove[j][-2:])



# joining showings and films to get names

sho_join = Showings.merge(Films, left_on = 'Film ID', right_on = 'ID' )[['ID_x', 'Name']]
sho_join.sort_values('ID_x', inplace = True)
sho_join.reset_index(drop=True, inplace=True)

names_showings = []

for i in range(len(sho_join)):
     names_showings.append(f'Showing {sho_join["ID_x"][i]}: {sho_join["Name"][i]}')



# getting all the data into lists of tuples to be able to send to the database

showings_for_db = []
bookings_for_db = []
films_for_db = []
customers_for_db = []


for i in range(len(Showings)):
    showings_for_db.append(tuple(Showings.iloc[i,:].map(str)))
for i in range(len(bookings)):
    bookings_for_db.append(tuple(bookings.iloc[i,:].map(str)))
for i in range(len(Films)):
    films_for_db.append(tuple(Films.iloc[i,:].map(str)))
for i in range(len(Customers)):
    customers_for_db.append(tuple(Customers.iloc[i,:].map(str)))
 


## this sends all the original data to the database
conn = sqlite3.connect('cinema_booking_db.db') # connects to the database file
c= conn.cursor() # creates a cursor

# next 4 lines creates variables for the tables and defines datatypes
customers_create = """CREATE TABLE IF NOT EXISTS Customers (ID integer,Name text,Gender text,Age integer, Email text)"""
bookings_create = """CREATE TABLE IF NOT EXISTS Bookings (ID integer,Customer ID integer,Showing ID integer,Seat Number)"""
films_create = """CREATE TABLE IF NOT EXISTS Films (ID integer,Name,Genre,Rating)"""
showings_create = """CREATE TABLE IF NOT EXISTS Showings (ID integer,Time,Screen,Film ID)"""

# creates a list of all the queries to send from above 
tables = [customers_create, bookings_create,films_create,showings_create]

#executes the queries for each table
for i in tables:
    c.execute(i)

# inserts the data into the database    
c.executemany('insert into Customers values (?,?,?,?,?)', customers_for_db)
c.executemany('insert into Films values (?,?,?,?)', films_for_db)
c.executemany('insert into Showings values (?,?,?,?)', showings_for_db)
c.executemany('insert into Bookings values (?,?,?,?)', bookings_for_db)


# commits and closes the database session
conn.commit()
conn.close()


def update_database(name,age,gender,email,showing_seat,showing):
    '''This function will update the SQL database when new bookings are made'''
    # starts connection    
    update_conn = sqlite3.connect('cinema_booking_db.db')
    uc= update_conn.cursor()
    #new list to update the booking table
    bookings_update = [(len(bookings.index),cust_id,showing,showing_seat)]
    # checking if the customer already exists. If not, adds them to the customers database
    if email in list(Customers2['Email Address']):
        pass
    else:
        customers_update = [(cust_id,name,gender,age,email)]
        # executes adding the customer
        uc.executemany('insert into Customers values (?,?,?,?,?)', customers_update)
    #executes adding the booking
    uc.executemany('insert into Bookings values (?,?,?,?)', bookings_update)
    # commits changes and closes the session    
    update_conn.commit()
    update_conn.close()


def remove_seats(seat):
    '''This function will remove the seats from the seat_options remove list so that
    it cannot be booked again Takes the input as the seat number booked'''
    # defines a global variable so it can be used in other functions
    global screening_free
    # gets the showing that the seat was booked and concatenates them so in same format as in the list
    for s in range(len(screening_free)):
        if my_combo.get() == names_showings[s]:
            showing_and_seat = f'S{s+1} {seat}'
            # removes from the list
            seat_options_remove.remove(showing_and_seat)
    # recreates the global screening free dictionary with the seats that are left
    # needs to do this as this dictionary is what is used by the dropdown menu in the window
    screening_free = dict()
    #creates a new key for each showing
    for i in range(len(Showings)):
        screening_free[i+1] = []
    # appends the seat number left for each showing
    for j in range(len(seat_options_remove)):
        for k in range(len(Showings)):
            if seat_options_remove[j][0:2] == f'S{k+1}':
                screening_free[k+1].append(seat_options_remove[j][-2:])



def ensure_filled():
    '''makes sure that all the variables are filled out. returns 0 if something isnt filled out '''
    checker = ''
    # if statement that checks all the fields have something in them. 
    if (textentryname.get()) and (textentryage.get()) and  (genderentry.get()) and (my_combo2.get()) and  (textentryemail.get()):
        checker = 1
        return checker
    else:
        checker = 0
        return checker



def update_dataframes(name,age,gender,email,showing_seat,showing):
    '''function to update the dataframes with new booking info'''
    ## defines global variables so they can be used in other functions
    global cust_id
    global Customers2
    cust_id =[]
    # creates a new customers dataframe. This is needed as otherwise the update database function will think that
    # every new customer already exists. Thus this creates a copy for that function.
    Customers2 = Customers.copy()
    # checks if the email already exists, and if so finds their customer id. otherwise defines a new customerID
    if email in list(Customers['Email Address']):
        cust_id = int(Customers[Customers['Email Address'] == email]['ID'])
    else:
        cust_id = len(Customers.index)+1
        #appends to the customer table
        Customers.loc[len(Customers.index)] = [cust_id,name,gender,age,email]
    #appends to the booking table    
    bookings.loc[len(bookings.index)] = [len(bookings.index)+1,cust_id,showing,showing_seat]



def click():
    '''This is the function that runs whenever the submit button is clicked'''
    # next 5 lined  gets the relevant information
    entered_text_name = textentryname.get()
    entered_text_age = textentryage.get()
    entered_gender = genderentry.get()
    entered_showing = my_combo2.get()
    entered_email = textentryemail.get()

    
    # checks that the information is filled out using ensure_filled() function defined earlier
    if ensure_filled() == 0:
        enter_info_label = customtkinter.CTkLabel(window, text='Please Enter All Information', fg_color=('red','red'), bg='#1F1F1F',text_font=('Quire Sans',-20))
        enter_info_label.place(relx=0.5,rely=0.78, anchor=CENTER) 
    elif ensure_filled() == 1:
        for s in range(len(screening_free)):
            if my_combo.get() == names_showings[s]:
                showing = s+1
        
        # runs update_dataframes() function to update dataframes
        update_dataframes(entered_text_name,int(entered_text_age),entered_gender,entered_email,entered_showing,showing)
        # runs the remove seats() function which removes the seats from the seat_options_remove list 
        # and repudates the dictionary with remaining seats
        remove_seats(entered_showing)
        #updates the sql database
        update_database(entered_text_name,int(entered_text_age),entered_gender,entered_email,entered_showing,showing)
        # opens the confirmation window
        open_popup()
        

def pick_Seat(e):
    '''function that runs from the first dropdown menu to get values for the second dropdown menu'''
    for s in range(len(screening_free)):
        if my_combo.get() == names_showings[s]:
            my_combo2.config(value = screening_free[s+1])



def open_popup():
    '''creates a new window that gives confirmation of booking'''
    # defines the new window
    top= customtkinter.CTkToplevel(window)
    top.geometry("1200x550+10+10")
    top.title("Booking Confirmation")
    # next 4 lines adds a label and 2 buttons to the window
    customtkinter.CTkLabel(top, text= "Thank You for Booking at Rockborne Cinema", text_font=("Quire Sans", -30)).place(relx=0.5,rely=0.5,anchor=CENTER)    
    customtkinter.CTkButton(top,text='Book Again', width=100, height =50, command=top.destroy,text_font=("Quire Sans", -40)).place(relx=0.4,rely=0.9, anchor=CENTER)
    exit = customtkinter.CTkButton(top,text='Exit', width=100, height =50, command=window.destroy,text_font=("Quire Sans", -40))
    exit.place(relx=0.6,rely=0.9,anchor=CENTER)



## This runs the UI

# sets the appearance of the UI
customtkinter.set_appearance_mode('Dark')
customtkinter.set_default_color_theme('dark-blue')


#defines the window and the geometry of the window
window = customtkinter.CTk()
window.geometry("1200x500+10+10")
window.title('Cinema Booking System')

# creates a label with text saying 'name' and places it in the window
namelabel = customtkinter.CTkLabel(window, text = "Name: ",text_font=("Quire Sans", -50), pady=10)
namelabel.place(relx=0.1,rely=0.3,anchor=CENTER)

# creates a text entry box for 'name' and places it in the window
textentryname = customtkinter.CTkEntry(window, width=200, bg='white')
textentryname.place(relx=0.3,rely=0.3,anchor=CENTER)

# creates a label with text saying 'age' and places it in the window
agelabel = customtkinter.CTkLabel(window, text = "Age: ",text_font=("Quire Sans", -50), pady=10)
agelabel.place(relx=0.1,rely=0.5,anchor=CENTER)

# creates a text entry box for 'age' and places it in the window
textentryage = customtkinter.CTkEntry(window, width = 200, bg = 'white')
textentryage.place(relx=0.3,rely=0.5,anchor=CENTER)

# creates a label with text saying 'gender' and places it in the window
genderlabel = customtkinter.CTkLabel(window, text = "Gender: ",text_font=("Quire Sans", -50), pady=10)
genderlabel.place(relx=0.1,rely=0.7,anchor=CENTER)

# defines possible gender options, creates a dropdown and places it in the window
Gender = ['male','female', 'other','prefer not to say']
genderentry = ttk.Combobox(window, value=Gender, width = 20)
genderentry.place(relx=0.3,rely=0.7,anchor=CENTER)

# cretes a button to submit info. Has command click.
#Thus when submit button is pressed it runs click function previously defined
submit = customtkinter.CTkButton(window,text='Submit', width=90, height=50,command=click,text_font=("Quire Sans", -50))
submit.place(relx=0.4,rely=0.9,anchor=CENTER)

#variable = StringVar(window)
#OptionMenu(window, variable, *seat_options_remove).grid(row=5,column=2, sticky=W)

# creates a label with text saying 'showing' and places it in the window
showinglabel = customtkinter.CTkLabel(window, text = "Showing: ",text_font=("Quire Sans", -50), pady=10)
showinglabel.place(relx=0.6,rely=0.3,anchor=CENTER)

# creates a combobox with all the names of the showings and places it in the window
my_combo =ttk.Combobox(window, value=names_showings, width = 40)
my_combo.current(0)
my_combo.place(relx=0.85,rely=0.3,anchor=CENTER)

# binds the combobox to the second bse don pick_Seat() function. This means that when a showing is selected,
# the options in the second combobox will change
my_combo.bind("<<ComboboxSelected>>", pick_Seat)

# creates a label with text saying 'seat' and places it in the window
seatlabel = customtkinter.CTkLabel(window, text = "Seat: ",text_font=("Quire Sans", -50), pady=10)
seatlabel.place(relx=0.6,rely=0.5,anchor=CENTER)

# creates the second combobox and places it in the window
# will have its values based on what is selected in first combobox
my_combo2 = ttk.Combobox(window, value=[''], width = 5)
my_combo2.current()
my_combo2.place(relx=0.85,rely=0.5,anchor=CENTER)

# creates a label saying 'email' and places it in the window
emaillabel = customtkinter.CTkLabel(window, text = "Email: ",text_font=("Quire Sans", -50), pady=10)
emaillabel.place(relx=0.6,rely=0.7,anchor=CENTER)

# creates a text entry box for 'email' and places it in the window
textentryemail = customtkinter.CTkEntry(window, width=200, bg='#2596be')
textentryemail.place(relx=0.85,rely=0.7,anchor=CENTER)

# creates a button saying exit which kills the session
exit = customtkinter.CTkButton(window,text='Exit', width=100, height =50, command=window.destroy,text_font=("Quire Sans", -50))
exit.place(relx=0.6,rely=0.9,anchor=CENTER)

# gets logo image from file and puts it in the window
img = PhotoImage(file="CinemaLogo.gif")
img = img.subsample(2)
logo = customtkinter.CTkLabel(window, image=img,bg='black')
logo.image = img
logo.place(relx=0.5,rely=0,anchor='n')


# starts loop to run the session
window.mainloop()


from tkinter import *
from tkinter import messagebox
from tkinter import ttk
#from tkmacosx import *
import math

import mysql.connector
mydb = mysql.connector.connect(
    host='localhost',
    user='root',
    passwd='rootpw',  #YOUR PASSWORD HERE
    database='ott')

myCursor = mydb.cursor()


# SEARCH FUNCTIONS
#search movies that have property of title that incorporates typed entry by the user
def title_search(entry):
    title_search_query = """ SELECT ID FROM movie WHERE title LIKE '%s'"""
    myCursor.execute(title_search_query % ('%' + entry.get() + '%'))
    print(title_search_query % ('%' + entry.get() + '%'))
    condition_title = myCursor.fetchall()
    condition_title = set(condition_title)
    #result set is made by intersecting each search result
    global result_set
    result_set = result_set.intersection(condition_title)
    print('title search:', len(result_set))

#search movies that have property of director that incorporates typed entry by the user
def dir_search(entry):
    dir_search_query = """ SELECT m.ID FROM director d JOIN directedBy db ON db.dirID=d.dirID
            JOIN movie m ON m.ID=db.movieID
            WHERE d.dirName LIKE '%s'"""
    myCursor.execute(dir_search_query % ('%' + entry.get() + '%'))
    print(dir_search_query % ('%' + entry.get() + '%'))
    condition_dir = myCursor.fetchall()
    condition_dir = set(condition_dir)
    global result_set
    result_set = result_set.intersection(condition_dir)
    print('after dir search:', len(result_set))

#search movies that have property of selected genre by the user
def genre_search(option):
    genre_search_query= """ SELECT m.ID FROM genre g JOIN hasGenre hg ON hg.genreID=g.genreID
    JOIN movie m ON m.ID=hg.movieID
    WHERE g.genreName LIKE '%s'"""
    myCursor.execute(genre_search_query %('%'+ option.get()[2:-3] +'%'))
    print(genre_search_query %('%'+ option.get()[2:-3] +'%'))
    condition_genre= myCursor.fetchall()
    condition_genre= set(condition_genre)
    global result_set
    result_set= result_set.intersection(condition_genre)
    print('after genre search:', len(result_set))

#search movies that have property of selected language by the user
def lang_search(option):
    lang_search_query = """ SELECT m.ID FROM language l JOIN inLanguage il ON il.languageID=l.languageID
        JOIN movie m ON m.ID=il.movieID
        WHERE l.languageName LIKE '%s'"""
    myCursor.execute(lang_search_query % ('%' + option.get()[2:-3] + '%'))
    print(lang_search_query %('%'+ option.get()[2:-3] +'%'))
    condition_lang = myCursor.fetchall()
    condition_lang = set(condition_lang)
    global result_set
    result_set = result_set.intersection(condition_lang)
    print('after lang search:', len(result_set))

#search movies that have property of selected country by the user
def country_search(option):
    country_search_query = """ SELECT m.ID FROM country c JOIN fromCountry fc ON fc.countryID=c.countryID
            JOIN movie m ON m.ID=fc.movieID
            WHERE c.countryName LIKE '%s'"""
    myCursor.execute(country_search_query % ('%' + option.get()[2:-3] + '%'))
    print(country_search_query % ('%' + option.get()[2:-3] + '%'))
    condition_country = myCursor.fetchall()
    condition_country = set(condition_country)
    global result_set
    result_set = result_set.intersection(condition_country)
    print('after country search:', len(result_set))

#search movies that have property of selected year by the user
def year_search(option):
    year_search_query = " SELECT ID FROM movie WHERE year= %s "
    myCursor.execute(year_search_query % (option.get()[1:-2]))
    print(year_search_query % (option.get()[1:-2]))
    condition_year = myCursor.fetchall()
    condition_year = set(condition_year)
    global result_set
    result_set = result_set.intersection(condition_year)
    print('after year search:', len(result_set))

#search movies that are available in one or more service
def service_search(option_list, service_list):
    option_set= set()
    not_selected_service=0
    for option in range(len(option_list)):
        if option_list[option].get() == 'yes':
            option_query="""SELECT m.ID FROM movie m 
                JOIN availableOn ao ON ao.movieID = m.ID
                JOIN service s ON s.serviceID = ao.serviceID
                WHERE s.serviceName = '%s' """ %(service_list[option])
            myCursor.execute(option_query)
            print(option_query)
            condition_service= myCursor.fetchall()
            condition_service= set(condition_service)
            option_set= option_set.union(condition_service)
        else:
            not_selected_service+=1
    if not_selected_service!=4:
        global result_set
        result_set = result_set.intersection(option_set)
        print('after sevice search:', len(result_set))

############################################################################

# clearing the frame
def clear(frame):
    for widget in frame.winfo_children():
        widget.destroy()


# USER-MADE LIST FUNCTIONS
## dict stands for dictionary containing all of the movies in a screen
def add_list_stringvar(dict):
    global add_list_top
    add_list_top= Toplevel()
    add_list_top.geometry('200x200')
    list_user_made_query= "SELECT listName FROM list WHERE username= '%s'" %(username)
    myCursor.execute(list_user_made_query)
    print('list of user', list_user_made_query)
    global list_user_made
    list_user_made= myCursor.fetchall()

    if list_user_made:
        Label(add_list_top, text='Select the list').grid(row=1, column=1)
        list_user_made_var= StringVar()
        list_user_made_var.set('Choose one')
        list_user_made_drop= OptionMenu(add_list_top, list_user_made_var, *list_user_made,
                                        command= lambda e: add_movie_to_list(list_user_made_var.get(), username, add_list_top, dict))
        list_user_made_drop.grid(row=2, column=1)
        Label(add_list_top, text='Add list').grid(row=4, column=1)
    else:
        Label(add_list_top, text='No lists have been created.').grid(row=1, column=1)

    list_ = StringVar()
    list_entry = Entry(add_list_top, textvariable=list_)
    list_entry.grid(row=5, column=1)

    list_create_button= Button(add_list_top, text='Create list', command= lambda: create_user_list(list_entry))
    list_create_button.grid(row=6, column=1)


#Create user-made list
def create_user_list(list_entry):
    global username
    print('list_user_made:', list_user_made)
    if list_entry.get() == '':
        messagebox.showinfo("Error", "List name cannot be empty.", icon="error")
    #list name column is VARCHAR(255)
    elif len(list_entry.get()) > 255:
        messagebox.showinfo("Error", "List name is too long." , icon= "error")
    elif (list_entry.get(),) in list_user_made:
        messagebox.showinfo("Error", "There is already a list named " + list_entry.get() + ".", icon= 'error')
    else:
        user_list_add_query= '''INSERT INTO list(listName, username) VALUES ("%s", "%s")'''%(list_entry.get(), username)
        print(user_list_add_query)
        myCursor.execute(user_list_add_query)
        mydb.commit()
    add_list_top.destroy()
    add_list_stringvar(checkbox_id_dict)




# add movie to the list
def add_movie_to_list(listname, username, frame, dict):
    # add_list_id is the id of movie that the user wants to add to the list
    add_list_id=[]
    for i in dict.keys():
        if dict[i][0].get()=='yes':
            add_list_id.append(dict[i][1])
    print('I will add', add_list_id)

    # which list to add the movie
    adding_list_id_query='''SELECT listID FROM list WHERE listName="%s" AND username="%s"'''%(str(listname)[2:-3], username)
    myCursor.execute(adding_list_id_query)
    adding_list_id = myCursor.fetchall()
    adding_list_id = int(str(adding_list_id)[2:-3])
    print('I will add to',adding_list_id)

    # get the movie in the list
    adding_list_movie_query="SELECT movieID FROM inList WHERE listID=%d"%(adding_list_id)
    myCursor.execute(adding_list_movie_query)
    adding_list_movie_ids= myCursor.fetchall()
    print(adding_list_movie_ids)
    adding_list_movie = []
    for id in adding_list_movie_ids:
        adding_list_movie.append(int(str(id)[1:-2]))
    print('The movie in the list',adding_list_movie)

    # add movie to the list
    add_movie_to_list_query="INSERT INTO inList (listID, movieID) VALUES (%d, %d)"
    for k in add_list_id:
        if k not in adding_list_movie:
            myCursor.execute(add_movie_to_list_query %(adding_list_id, k))
            mydb.commit()

    check_list_button= Button(frame, text='check list', command=lambda: check_list(adding_list_id))
    check_list_button.grid(row=3, column=1)

# display selected list
def check_list(list_id):
    movie_in_the_list_query="SELECT movieID FROM inList WHERE listID=%d"%(list_id)
    myCursor.execute(movie_in_the_list_query)
    id_list= myCursor.fetchall()

    # info. of movie in id_list
    id_int=[]
    for k in id_list:
        id_int.append(int(str(k)[1:-2]))
    print('id_int:', id_int)

    id_info_query= '''SELECT m.ID, m.title, GROUP_CONCAT(d.dirName ORDER BY d.dirID SEPARATOR ", ") AS dirName, 
                    m.year, m.age, m.runtime FROM movie m
                    JOIN directedBy db ON m.ID=db.movieID
                    JOIN director d ON db.dirID=d.dirID 
                    WHERE m.ID IN %s 
                    GROUP BY m.ID, m.title, m.year, m.age, m.runtime'''
    myCursor.execute(id_info_query %('('+str(id_int)[1:-1]+')'))
    list_in= myCursor.fetchall()

    check_list_top= Toplevel()
    check_list_top.geometry('500x500')
    # label grid
    column_label=['title', 'director', 'year', 'age', 'runtime']
    c=1
    for i in column_label:
        Label(check_list_top, text= i, bg='#999999').grid(row=1, column=c)
        c+=1

    r=2
    for row in list_in:
        for k in range(1, len(row)):
            Label(check_list_top, text=row[k]).grid(row=r, column=k)
        r+=1
    service_match(list_id)


# Count how many movies in list are available for each service
def service_match(listID):
    match_query='''SELECT serviceName, COUNT(i.movieID) AS `movies available`
                FROM inList i JOIN availableOn a JOIN service s WHERE i.movieID=a.movieID AND a.serviceID=s.serviceID
                AND listID=%s
                GROUP BY serviceName ORDER BY 2 DESC'''
    myCursor.execute(match_query, (listID,))
    match_results=myCursor.fetchall()

    match_window=Toplevel()

    frame=Frame(match_window, bg='azure')
    frame.place(relx=0.1, rely=0.1, relheight=0.8, relwidth=0.8)

    for result in match_results:
        Label(frame, text=str(result[1])+" available on "+str(result[0])+".", bg='azure').pack()


#######################################################


# DISPLAY SEARCH RESULT FUNCTIONS
#Previous page
def print_movie_prev(result, result_row_n, frame):
    clear(frame)
    global page
    if page > 1:
        page -= 1
    for i in range(len(order_col)):
        Label(frame, text=order_col[i], bg='#999999').grid(row=1, column=i + 1)

    display_row = result[10 * page - 10: 10 * page - 10 + result_row_n]
    global checkbox_id_dict
    checkbox_id_dict = {}

    r = 2
    for row in display_row:
        for k in range(1, len(row)):
            Label(frame, text=row[k], bg='azure').grid(row=r, column=k)
        result_string_var = StringVar()
        result_check = Checkbutton(frame, variable=result_string_var, onvalue='yes', offvalue='no', bg='azure')
        result_check.deselect()
        result_check.grid(row=r, column=0)
        checkbox_id_dict[r - 2] = [result_string_var, row[0]]
        r += 1
    print('checkbox_id_dict:', checkbox_id_dict)

    global window_l_frame
    add_button = Button(window_l_frame, text='add', command=lambda: add_list_stringvar(checkbox_id_dict))
    add_button.place(relwidth=0.1, relheight=0.05, rely=0.925, relx=0.5, anchor=N)

    Label(result_frame, text=str(page) + '/' + str(page_max), bg='azure').place(relx=0.5, rely=0.9)

#Next page
def print_movie_next(result, result_row_n, frame):
    clear(frame)
    global page
    if page < page_max:
        page+=1
    for i in range(len(order_col)):
        Label(frame, text=order_col[i], bg='#999999').grid(row=1, column=i + 1)

    display_row= result[10* page - 10: 10* page -10 +result_row_n]
    global checkbox_id_dict
    checkbox_id_dict = {}

    r = 2
    for row in display_row:
        for k in range(1, len(row)):
            Label(frame, text=row[k], bg='azure').grid(row=r, column=k)
        result_string_var = StringVar()
        result_check = Checkbutton(frame, variable=result_string_var, onvalue='yes', offvalue='no', bg='azure')
        result_check.deselect()
        result_check.grid(row=r, column=0)
        checkbox_id_dict[r - 2] = [result_string_var, row[0]]
        r += 1
    print('checkbox_id_dict:', checkbox_id_dict)

    global window_l_frame
    add_button = Button(window_l_frame, text='add', command=lambda: add_list_stringvar(checkbox_id_dict))
    add_button.place(relwidth=0.1, relheight=0.05, rely=0.925, relx=0.5, anchor=N)

    Label(result_frame, text=str(page) + '/' + str(page_max), bg='azure').place(relx=0.5, rely=0.9)

#First result page: prints the result that the user is searching for
def print_result(result_id, frame, col):
    clear(frame)
    query_col = ['m.title', 'dirName', 'm.year', 'm.age', 'm.runtime']
    global order_col
    col_query= query_col[order_col.index(col)]
    if len(result_id)!=0:
        #frame.grid_columnconfigure(0, weight=1)
        #frame.grid_columnconfigure(9, weight=1)
        for i in range(len(order_col)):
            Label(frame, text=order_col[i], bg='#999999').grid(row=1, column=i + 1)

        result_query= """SELECT m.ID, m.title, GROUP_CONCAT(d.dirName ORDER BY d.dirID SEPARATOR ", ") AS dirName, m.year, m.age, m.runtime FROM movie m
                    JOIN directedBy db ON m.ID=db.movieID
                    JOIN director d ON db.dirID=d.dirID 
                    WHERE m.ID IN %s 
                    GROUP BY m.ID, m.title, m.year, m.age, m.runtime
                    ORDER BY %s""" %('('+str(result_id)[1:-1]+')', col_query)
        myCursor.execute(result_query)
        result= myCursor.fetchall()
        print(result_query)
        print(result)
        print(len(result))
        # how many rows to be displayed in result_frame at once
        result_row_n=10
        global page
        global page_max
        page_max = math.ceil(len(result) / result_row_n)

        global checkbox_id_dict
        checkbox_id_dict={}
        r=2
        page = 1
        for row in result[0:10]:
            for k in range(1,len(row)):
                Label(frame, text=row[k], bg='azure').grid(row=r, column=k)
            result_string_var = StringVar()
            result_check = Checkbutton(frame, variable=result_string_var, onvalue='yes', offvalue='no', bg='azure')
            result_check.deselect()
            result_check.grid(row=r, column=0)
            checkbox_id_dict[r-2]=[result_string_var, row[0]]

            r+=1

        print('checkbox_id_dict:', checkbox_id_dict)

        Label(result_frame, text= str(page)+'/'+str(page_max), bg='azure').place(relx=0.5, rely=0.9)
        next_button= Button(window_l_frame, text='>', command= lambda: print_movie_next(result, result_row_n, frame))
        next_button.place(relwidth=0.05, relheight=0.05, relx=0.9, rely=0.8)
        prev_button = Button(window_l_frame, text='<', command=lambda: print_movie_prev(result, result_row_n, frame))
        prev_button.place(relwidth=0.05, relheight=0.05, relx=0.05, rely=0.8)

        global username
        add_button = Button(window_l_frame, text='add', command=lambda: add_list_stringvar(checkbox_id_dict))
        add_button.place(relwidth=0.1, relheight=0.05, rely=0.925, relx=0.5, anchor=N)

    else:
        frame.grid_columnconfigure(0, weight=1)
        frame.grid_columnconfigure(2, weight=1)
        Label(frame, text='No movie satisfies those conditions.', bg='azure').grid(row=1, column=1)

# if the user selected nothing on the initial window, displays all movies available
def search_result():
    global result_frame
    clear(result_frame)

    # define result set
    query = 'SELECT ID FROM movie'
    myCursor.execute(query)
    global result_set
    result_set = myCursor.fetchall()
    result_set = set(result_set)

    global string_var_title
    global title_entry
    if string_var_title.get() == 'yes':
        title_search(title_entry)

    global string_var_dir
    global dir_entry
    if string_var_dir.get() == 'yes':
        dir_search(dir_entry)

    global string_var_genre
    global genre_option
    if string_var_genre.get() == 'yes':
        genre_search(genre_option)

    global string_var_lang
    global language_option
    if string_var_lang.get() == 'yes':
        lang_search(language_option)

    global string_var_country
    global country_option
    if string_var_country.get() == 'yes':
        country_search(country_option)

    global string_var_year
    global year_option
    if string_var_year.get() == 'yes':
        year_search(year_option)

    option_list = [service_var_nf, service_var_hu, service_var_di, service_var_az]
    service_list= ['Netflix', 'Hulu', 'Prime Video', 'Disney+']
    service_search(option_list, service_list)

    # result_set into ID_list (since result_set is made up of tuple, the following code is to transform the result into suitable form for the query)

    result_ = list()
    for k in result_set:
        result_.append(int(str(k)[1:-2]))

    global order_col
    order_col = ['title', 'director', 'year', 'age', 'runtime']

    #since there are a lot of rows that satisfies the conditions, it will be great to add order-by dropdown to the frame
    Label(window_l_frame, text='order by:').place(relx=0.1, rely=0)
    orderby_var=StringVar()
    orderby_var.set('title')
    order_drop= OptionMenu(window_l_frame, orderby_var, *order_col, command= lambda e: print_result(result_, result_frame, orderby_var.get()))
    order_drop.place(relx=0.2)

#############################################################################################################

# UI WINDOWS AND USER CREATION/DELETION FUNCTIONS
#DISPLAY search window
def display_search():
    global top_user
    top_user.title('MovieFinder')
    top_user.geometry('800x800')
    top_user.configure(bg='white')

    window_t_frame = Frame(top_user)
    window_t_frame.place(relwidth=1, relheight=0.1, rely=0)

    global window_m_frame
    window_m_frame = Frame(top_user)
    window_m_frame.place(relwidth=1, relheight=0.4, rely=0.1)

    global window_l_frame
    window_l_frame = Frame(top_user)
    window_l_frame.place(relwidth=1, relheight=0.5, rely=0.5)

    top_label = Label(window_t_frame, text='MovieFinder', font=('Arial', 20, 'bold'))
    top_label.grid(row=1, column=1, sticky='news')
    window_t_frame.grid_rowconfigure(0, weight=1)
    window_t_frame.grid_rowconfigure(2, weight=1)
    window_t_frame.grid_columnconfigure(0, weight=1)
    window_t_frame.grid_columnconfigure(2, weight=1)

    window_m_frame.grid_rowconfigure(0, weight=1)
    window_m_frame.grid_rowconfigure(7, weight=1)
    window_m_frame.grid_columnconfigure(0, weight=1)
    window_m_frame.grid_columnconfigure(5, weight=1)
    window_m_frame.grid_columnconfigure(7, weight=1)

    #title_checkbox
    global string_var_title
    string_var_title = StringVar()
    search_title = Checkbutton(window_m_frame, variable=string_var_title, onvalue='yes', offvalue='no')
    search_title.grid(row=1, column=1)
    search_title.deselect()

    #director_checkbox
    global string_var_dir
    string_var_dir = StringVar()
    search_dir = Checkbutton(window_m_frame, variable=string_var_dir, onvalue='yes', offvalue='no')
    search_dir.grid(row=2, column=1)
    search_dir.deselect()

    #genre_checkbox
    global string_var_genre
    string_var_genre = StringVar()
    search_genre = Checkbutton(window_m_frame, variable= string_var_genre, onvalue='yes', offvalue='no')
    search_genre.grid(row=3, column=1)
    search_genre.deselect()

    #language_checkbox
    global string_var_lang
    string_var_lang = StringVar()
    search_lang = Checkbutton(window_m_frame, variable= string_var_lang, onvalue='yes', offvalue='no')
    search_lang.grid(row=4, column=1)
    search_lang.deselect()

    #country_checkbox
    global string_var_country
    string_var_country = StringVar()
    search_country = Checkbutton(window_m_frame, variable= string_var_country, onvalue='yes', offvalue='no')
    search_country.grid(row=5, column=1)
    search_country.deselect()

    #year_checkbox
    global string_var_year
    string_var_year = StringVar()
    search_year = Checkbutton(window_m_frame, variable=string_var_year, onvalue='yes', offvalue='no')
    search_year.grid(row=6, column=1)
    search_year.deselect()

    # title, director, genre, language, country, year labels
    title_label = Label(window_m_frame, text="Title")
    title_label.grid(row=1, column=2)
    dir_label = Label(window_m_frame, text="Director")
    dir_label.grid(row=2, column=2)
    genre_label = Label(window_m_frame, text="Genre")
    genre_label.grid(row=3, column=2)
    lang_label = Label(window_m_frame, text="Language")
    lang_label.grid(row=4, column=2)
    country_label = Label(window_m_frame, text="Country")
    country_label.grid(row=5, column=2)
    year_label = Label(window_m_frame, text="Year")
    year_label.grid(row=6, column=2)

    global title_entry
    title_entry = Entry(window_m_frame)
    title_entry.grid(row=1, column=3)

    global dir_entry
    dir_entry = Entry(window_m_frame)
    dir_entry.grid(row=2, column=3)

    global genre_option
    genre_option = StringVar()
    genre_option.set('Choose one')
    genre_drop = OptionMenu(window_m_frame, genre_option, *genre_list)
    genre_drop.grid(row=3, column=3)

    global language_option
    language_option = StringVar()
    language_option.set('Choose one')
    language_drop = OptionMenu(window_m_frame, language_option, *lang_list)
    language_drop.grid(row=4, column=3)

    global country_option
    country_option = StringVar()
    country_option.set('Choose one')
    country_drop = OptionMenu(window_m_frame, country_option, *country_list)
    country_drop.grid(row=5, column=3)

    global year_option
    year_option = StringVar()
    year_option.set('Choose one')
    year_drop = OptionMenu(window_m_frame, year_option, *year_list)
    year_drop.grid(row=6, column=3)

    # frame for displaying search results
    global result_frame
    result_frame= Frame(window_l_frame, bg='azure', borderwidth= 3, relief= 'ridge')
    result_frame.place(relwidth=0.8, relheight=0.8, rely=0.1, relx=0.1)

    search_button= Button(window_m_frame, text='Search', command=search_result)
    search_button.grid(row=8, column=3)

    window_m_frame.grid_rowconfigure(0, weight=1)
    window_m_frame.grid_rowconfigure(7, weight=1)
    window_m_frame.grid_rowconfigure(9, weight=1)

    #service_frame
    service_frame= LabelFrame(window_m_frame, text='Service', padx=50, pady=50, bg='azure')
    service_frame.grid(row=1, column=6, rowspan=6)

    # Netflix checkbutton
    global service_var_nf
    service_var_nf = StringVar()
    search_service_nf = Checkbutton(service_frame, variable=service_var_nf, onvalue='yes', offvalue='no', bg='azure')
    search_service_nf.grid(row=1, column=1)
    search_service_nf.deselect()

    # Hulu checkbutton
    global service_var_hu
    service_var_hu = StringVar()
    search_service_hu = Checkbutton(service_frame, variable=service_var_hu, onvalue='yes', offvalue='no', bg='azure')
    search_service_hu.grid(row=2, column=1)
    search_service_hu.deselect()

    # Disney+ checkbutton
    global service_var_di
    service_var_di = StringVar()
    search_service_di = Checkbutton(service_frame, variable=service_var_di, onvalue='yes', offvalue='no', bg='azure')
    search_service_di.grid(row=3, column=1)
    search_service_di.deselect()

    # Amazon Prime Video checkbutton
    global service_var_az
    service_var_az = StringVar()
    search_service_az = Checkbutton(service_frame, variable=service_var_az, onvalue='yes', offvalue='no', bg='azure')
    search_service_az.grid(row=4, column=1)
    search_service_az.deselect()

    netflix_label = Label(service_frame, text="Netflix", bg='azure')
    netflix_label.grid(row=1, column=2)
    hulu_label = Label(service_frame, text="Hulu", bg='azure')
    hulu_label.grid(row=2, column=2)
    disney_label = Label(service_frame, text="Amazon Prime", bg='azure')
    disney_label.grid(row=3, column=2)
    az_label = Label(service_frame, text="Disney+", bg='azure')
    az_label.grid(row=4, column=2)
    service_frame.grid_columnconfigure(0, weight=1)
    service_frame.grid_columnconfigure(5, weight=1)
    service_frame.grid_rowconfigure(0, weight=1)
    service_frame.grid_rowconfigure(5, weight=1)

#User select window
def user_select_window():
    global top_user
    top_user = Tk()
    top_user.configure(bg='azure')
    top_user.grab_set()
    top_user.title('User Select')
    label = Label(top_user, text="Welcome to MovieFinder!")
    label.pack()
    #top_user.overrideredirect(True)
    #x = window.winfo_x()
    #y = window.winfo_y()
    #top_user.geometry("300x300+%d+%d" % (x+150, y+150))
    top_user.geometry('300x300')
    #top_user.focus_force()
    user_window_widget(top_user)
    top_user.mainloop()

# New user creation function
def new_user(text):
    a = (text,)
    #username must be unique
    if a in user_list:
        messagebox.showinfo("Error", "There is already a user named "+text+".")
    #username column is VARCHAR(255)
    elif len(text) > 255:
        messagebox.showinfo("Error", "Username is too long.")
    #username cannot be blank as exceptions are handled with a blank string
    elif text == '':
        messagebox.showinfo("Error", "Username cannot be blank.")
    else:
        global user_option
        add = "INSERT INTO user(username) VALUE (%s)"
        user_option = a
        myCursor.execute(add, a)
        mydb.commit()
        messagebox.showinfo("User Created", "New user "+text+" created!")
        myCursor.execute(query)
        user_list[:] = myCursor.fetchall()
        user_window_widget(top_user)

# Declare and initialize username to blank string
username=''

# Set global variable username to current user
def set_user(text):
    global username
    username= '{}'.format(text[2:-3])
    #print(username)

# After username is selected, remove all widgets and change to search window
def top_destroy(top):
    if username=='':
        messagebox.showinfo("Error", "Please select your username!")
    else:
        display_search()

# delete user
def delete_user_button():
    # messagebox for confirmation of deletion, as deleting a user will also delete all lists that user has
    delete_ask = messagebox.askquestion("Delete User", "Delete user "+str(username)+"?\nAll lists for this user\nwill also be deleted.", icon="warning")
    if delete_ask =="yes":
        delete_user_query="DELETE FROM `user` WHERE username=%s"
        myCursor.execute(delete_user_query, (str(username),))
        mydb.commit()
        myCursor.execute(query)
        user_list[:] = myCursor.fetchall()
        user_window_widget(top_user)
    else:
        return

#User Selection/Creation window
def user_window_widget(top_user):
    for widget in top_user.winfo_children():
        widget.destroy()
    # if statement checking if there are any users registered already to display list of users
    if user_list:
        label2 = Label(top_user, text="Please select your username.", bg='azure', font=('Arial', 15))
        label2.pack()
        global user_option
        user_option = StringVar()
        user_option.set('Select User')
        user_drop = OptionMenu(top_user, user_option, *user_list, command= lambda e: set_user(user_option.get()))
        user_drop.pack()
        delete_button = Button(top_user, text="Delete User", command=delete_user_button)
        delete_button.pack()
        label3 = Label(top_user, text="Create New User", bg='azure', font=('Arial', 15))
        label3.pack()
        start_button = Button(top_user, text='start', command= lambda: top_destroy(top_user))
        start_button.pack(side='bottom')
    # only displays user creation elements to ensure username is made
    else:
        label4 = Label(top_user, text="Please create a new username to begin.", bg='azure')
        label4.pack()
    username_var = StringVar()
    username_entry = Entry(top_user, textvariable=username_var)
    username_entry.pack()
    user_create = Button(top_user, text="Create", command=lambda: new_user(username_var.get()))
    user_create.pack()



#USER_LIST
query='SELECT username FROM user ORDER BY username'
myCursor.execute(query)
user_list = myCursor.fetchall()

#GENRE_LIST
query1= 'SELECT (genreName) FROM genre ORDER BY genreName'
myCursor.execute(query1)
genre_list= myCursor.fetchall()

#LANGUAGE_LIST
query2= 'SELECT languageName FROM language ORDER BY languageName'
myCursor.execute(query2)
lang_list= myCursor.fetchall()

#COUNTRY_LIST
query3= 'SELECT countryName FROM country ORDER BY countryName'
myCursor.execute(query3)
country_list= myCursor.fetchall()

#DIRECTOR_LIST
query4= 'SELECT dirName FROM director'
myCursor.execute(query4)
dir_list=myCursor.fetchall()

#TITLE_LIST
query5= 'SELECT title FROM movie'
myCursor.execute(query5)
title_list=myCursor.fetchall()

#YEAR_LIST
query6= 'SELECT DISTINCT(year) FROM movie ORDER BY year'
myCursor.execute(query6)
year_list=myCursor.fetchall()

#SERVICE_LIST
query7= 'SELECT serviceName FROM service'
myCursor.execute(query7)
service_list=myCursor.fetchall()

user_select_window()

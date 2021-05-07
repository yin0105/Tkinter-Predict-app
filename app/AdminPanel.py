#import modules
import tkinter.filedialog
import numpy as np
import pandas as pd
import numpy as np
import csv, threading, json, os
import tkinter as tk

from pathlib import Path
from storykey import storykey
from tire import GeneticRisk
from multiprocessing import Process
from PIL import ImageTk
import PIL
from numpy.lib.function_base import append
from numpy.lib.polynomial import polyfit
from pandas.core import frame
from styleframe import StyleFrame, utils
from tkmagicgrid import *
from tkinter import ttk
from os import curdir
from tkinter import *
from datetime import datetime


def display_in_center(win, w, h):
    positionRight = int(win.winfo_screenwidth()/2 - w/2)
    positionDown = int(win.winfo_screenheight()/2 - h/2)
    win.geometry("{}x{}+{}+{}".format(w, h, positionRight, positionDown))

class ProcessParallel(object):
    """
    To Process the  functions parallely

    """    
    def __init__(self, *jobs):
        """
        """
        self.jobs = jobs
        self.processes = []

    def fork_processes(self):
        """
        Creates the process objects for given function deligates
        """
        for job in self.jobs:
            proc  = Process(target=job)
            self.processes.append(proc)

    def start_all(self):
        """
        Starts the functions process all together.
        """
        for proc in self.processes:
            proc.start()

    def join_all(self):
        """
        Waits untill all the functions executed.
        """
        for proc in self.processes:
            proc.join()

try:
    sys.stdout.write("\n")
    sys.stdout.flush()
except:
    class dummyStream:
        ''' dummyStream behaves like a stream but does nothing. '''
        def __init__(self): pass
        def write(self,data): pass
        def read(self,data): pass
        def flush(self): pass
        def close(self): pass

    # and now redirect all default streams to this dummyStream:
    sys.stdout = dummyStream()
    sys.stderr = dummyStream()
    sys.stdin = dummyStream()
    sys.__stdout__ = dummyStream()
    sys.__stderr__ = dummyStream()
    sys.__stdin__ = dummyStream()

# Designing window for registration
def register():
    global register_screen
    register_screen = Toplevel(main_screen)

    ico_path = curdir+"\\media\\my_icon.ico"
    register_screen.iconbitmap(ico_path)
    register_screen.title("Register")
    display_in_center(user_not_found_screen, 300, 250)
 
    global username
    global password
    global username_entry
    global password_entry
    global username_data
    global password_data
    global start_code
    global end_code
    global username_data
    global password_data
    global start_code
    global end_code
    username_data = StringVar()
    password_data = StringVar()
    start_code = StringVar()
    end_code = StringVar()

    username = StringVar()
    password = StringVar()
 
    Label(register_screen, text="Please enter details below", bg="blue").pack()
    Label(register_screen, text="").pack()
    username_lable = Label(register_screen, text="Username * ")
    username_lable.pack()
    username_entry = Entry(register_screen, textvariable=username)
    username_entry.pack()
    password_lable = Label(register_screen, text="Password * ")
    
    password_lable.pack()
    password_entry = Entry(register_screen, textvariable=password, show='*')
    password_entry.bind('<Return>', register_user)
    password_entry.pack()
    Label(register_screen, text="").pack()
    Button(register_screen, text="Register", width=10, height=1, bg="blue", command = register_user).pack()
 
 
# Designing window for login
def login():
    global login_screen
    login_screen = Toplevel(main_screen)
    login_screen.title("Login")
    display_in_center(login_screen, 300, 250)

    ico_path = curdir+"\\media\\my_icon.ico"
    login_screen.iconbitmap(ico_path)
    Label(login_screen, text="Please enter details below to login").pack()
    Label(login_screen, text="").pack()
 
    global username_verify
    global password_verify
 
    username_verify = StringVar()
    password_verify = StringVar()
 
    global username_login_entry
    global password_login_entry
 
    Label(login_screen, text="Username * ").pack()
    username_login_entry = Entry(login_screen, textvariable=username_verify)
    
    username_login_entry.pack()
    Label(login_screen, text="").pack()
    Label(login_screen, text="Password * ").pack()
    password_login_entry = Entry(login_screen, textvariable=password_verify, show= '*')
    password_login_entry.bind('<Return>', login_verify) 
    password_login_entry.pack()
    Label(login_screen, text="").pack()
    Button(login_screen, text="Login", width=10, height=1, command = login_verify).pack()

    username_login_entry.focus_set()
 

# Implementing event on register button
def register_user(event=None):
    username_info = username.get()
    password_info = password.get()
 
    file = open("user_credential_database/" + username_info, "w")
    file.write(username_info + "\n")
    file.write(password_info)
    file.close()
 
    username_entry.delete(0, END)
    password_entry.delete(0, END)
 
    Label(register_screen, text="Registration Success", fg="green", font=("calibri", 11)).pack()
    register_screen.after(700,register_screen.destroy)
 

# Implementing event on login button 
def login_verify(event=None):
    username1 = username_verify.get()
    password1 = password_verify.get()
    username_login_entry.delete(0, END)
    password_login_entry.delete(0, END)
    current_directory = os.getcwd()
    user_credential_directory = current_directory + '/'+"user_credential_database/"
 
    list_of_files = os.listdir(user_credential_directory)
    if username1 in list_of_files:
        file1 = open(user_credential_directory + username1, "r")
        verify = file1.read().splitlines()
        if password1 in verify:
            login_sucess()
        else:
            password_not_recognised()
    else:
        user_not_found()
 

# Designing popup for login success
def login_sucess():  
    login_screen.destroy()
    main_screen.destroy()
    welcome_screen()

    
def del_and_open():
    welcome_screen.destroy()
    application_window()

    
class application_window:

    def __init__(self):
        self.root = Tk()
        frame = self.root
      
        ico_path = curdir+"\\media\\my_icon.ico"
        frame.iconbitmap(ico_path)
        frame.title("Predictive AI Application Window")
        display_in_center(frame, 1000, 800)
        self.current_dir = curdir
        b1 = tkinter.Button(frame, text='Select Master Sheet',width=15, height=2, command=self.get_path_master).place(x=30, y=50)
        b2 = tkinter.Button(frame, text='Select Multiple Test Sheets (use ctrl + click to select)',width=40, height=2, command=self.get_path_test).place(x=300,y=50)
        self.progressbar = ttk.Progressbar(frame, mode='determinate',cursor='spider',length=300)
        self.progressbar.grid(column=1, row=0, sticky=W)
        self.progressbar["maximum"] = 100 
        
        self.progressbar["value"] = 0
        """photo_login = PhotoImage(file = curdir+"\predict.png")
        Button(text = '     Predict Now!', height="80", width="200",  image = photo_login, 
                        compound = LEFT, command = lambda:self.start_submit_thread(None)).place(x=90,y=150)"""

        
        b3 = tkinter.Button(frame, text='Predict Now!',width=15, height=2 ,command= lambda:self.start_submit_thread(None)).place(x=90,y=150)
        "b2.pack(fill='x')"

        
    def get_path_master(self):
        if not os.path.exists('AI External-Outputs/path_info.txt'):
            check_from = curdir
        else:
            file = open("AI External-Outputs/path_info.txt","r")
            for lines in file.read().splitlines():
                if lines[0] == "M":
                    check_from = os.path.dirname(lines[1:])
            file.close() 
        
        self.master_sheet_filepath = tkinter.filedialog.askopenfilename(parent=self.root, initialdir= check_from ,title='Please Choose Master Sheet',filetypes=[('Excel File', '.xlsx'),('CSV Excel file', '.csv')])


    def get_path_test(self):
        if not os.path.exists('AI External-Outputs/path_info.txt'):
            check_from = curdir
        else:
            file = open("AI External-Outputs/path_info.txt","r")
            for lines in file.read().splitlines():
                if lines[0] == "T":
                    check_from = os.path.dirname(lines[1:])
            file.close() 
        
        self.test_sheet_filepaths = list(tkinter.filedialog.askopenfilenames(parent=self.root, initialdir=check_from,title='Please Choose Test Sheet',filetypes=[('Excel File', '.xlsx'),('CSV Excel file', '.csv')]))

        """print(f)"""


    def get_prediction(self):
        def read_master_sheet(filepath):
            sf = StyleFrame.read_excel(filepath , read_style=True, use_openpyxl_styles=False)
            return sf

        def df_column_uniquify(df):
            df_columns = df.columns
            new_columns = []
            for item in df_columns:
                counter = 0
                newitem = item
                while newitem in new_columns:
                    counter += 1
                    newitem = "{}_{}".format(item, counter)
                new_columns.append(newitem)
            df.columns = new_columns
            return df


        def read_data(filepath):
            df = pd.read_excel(filepath)
            return df

        def get_standard_matrix(sf):

            f = open('Value-json/hyperparam.json') 
            hyperparam = json.load(f)

            """

            def only_cells_with_red_text(cell):
                if cell!=cell:
                    return hyperparam['empty']
                
                if cell.style.bg_color in {utils.colors.red, 'FFFF0000'}:
                    return 150
            

                if cell.style.font_color in {utils.colors.green, 'FF00B050'}:
                    return hyperparam['green']


                elif cell.style.font_color in {utils.colors.yellow, '00FFFF00'}:
                    return hyperparam['yellow']

                elif cell.style.font_color in {utils.colors.purple, '800080'}:
                    return hyperparam['purple']

                
                elif cell.style.font_color in {utils.colors.red, 'FFFF0000'}:
                    return hyperparam['red']


                elif cell.style.font_color in {utils.colors.blue, 'FF0070C0'}:
                    return hyperparam['blue']
                
                
                elif cell.style.font_color in {utils.colors.black, '00000000'}:
                    return hyperparam['black']

                else:
                    return 100

            
            
            def only_cells_with_red_text_emp(cell):
                if cell!=cell:
                    return 0
                
                if cell.style.bg_color in {utils.colors.red, 'FFFF0000'}:
                    return 150
            
                if cell.style.font_color in {utils.colors.green, 'FF00B050'}:
                    return hyperparam['green']


                elif cell.style.font_color in {utils.colors.yellow, '00FFFF00'}:
                    return hyperparam['yellow']

                elif cell.style.font_color in {utils.colors.purple, '800080'}:
                    return hyperparam['purple']

                
                elif cell.style.font_color in {utils.colors.red, 'FFFF0000'}:
                    return hyperparam['red']


                elif cell.style.font_color in {utils.colors.blue, 'FF0070C0'}:
                    return hyperparam['blue']
                
                
                elif cell.style.font_color in {utils.colors.black, '00000000'}:
                    return hyperparam['black']


                else:
                    return 100


            """
  
            def only_cells_with_red_text(cell):
                if cell!=cell:
                    return hyperparam['empty']

                elif '#' in str(cell.value) and '(' in str(cell.value):
                    check = cell.value
                    check = check[:-1]
                    cert = check.split('(')
                    cer = float(cert[1])
                    return cer
                else:
                    if '(' in str(cell.value):
                        if cell.style.bg_color in {utils.colors.red, 'FFFF0000'}:
                            return 150
                        if cell.style.font_color in {utils.colors.green, 'FF00B050'}:
                            check = cell.value
                            check = check[:-1]
                            cert = check.split('(')
                            cer = cert[1].split(',')
                        
                            if cer[0] == 'C':
                                return hyperparam['green']
                            elif cer[0] == 'V':
                                return float(cer[1])
                        elif cell.style.font_color in {utils.colors.yellow, '00FFFF00'}:
                            check = cell.value
                            check = check[:-1]
                            cert = check.split('(')
                            cer = cert[1].split(',')
                            
                            if cer[0] == 'C':
                                return hyperparam['yellow']
                            elif cer[0] == 'V':
                                return float(cer[1])
                        elif cell.style.font_color in {utils.colors.purple, '800080'}:
                            check = cell.value
                            check = check[:-1]
                            cert = check.split('(')
                            cer = cert[1].split(',')
                            #print(cer)
                            if cer[0] == 'C':
                                return hyperparam['purple']
                            elif cer[0] == 'V':
                                return float(cer[1])
                        elif cell.style.font_color in {utils.colors.red, 'FFFF0000'}:
                            check = cell.value
                            check = check[:-1]
                            cert = check.split('(')

                            cer = cert[1].split(',')
                            if cer[0] == 'C':
                                return hyperparam['red']
                            elif cer[0] == 'V':
                                return float(cer[1])
                        elif cell.style.font_color in {utils.colors.blue, 'FF0070C0'}:
                            check = cell.value
                            check = check[:-1]
                            cert = check.split('(')
                            cer = cert[1].split(',')
                            if cer[0] == 'C':
                                return hyperparam['blue']
                            elif cer[0] == 'V':
                                return float(cer[1])
                        elif cell.style.font_color in {utils.colors.black, '00000000'}:
                            check = cell.value
                            check = check[:-1]
                            cert = check.split('(')
                            cer = cert[1].split(',')
                            if cer[0] == 'C':
                                return hyperparam['black']
                            elif cer[0] == 'V':
                                return float(cer[1])
                        else:
                            check = cell.value
                            check = check[:-1]
                            cert = check.split('(')
                            cer = cert[1].split(',')
                            if cer[0] == 'C':
                                return hyperparam['black']
                            elif cer[0] == 'V':
                                return float(cer[1])
                    else:
                        return 0.00000001
            
            
            def only_cells_with_red_text_emp(cell):
                if cell!=cell:
                    return 0
                elif '(' in str(cell.value):
                    if cell.style.bg_color in {utils.colors.red, 'FFFF0000'}:
                        return 150

                    if cell.style.font_color in {utils.colors.green, 'FF00B050'}:
                        check = cell.value
                        check = check[:-1]
                        cert = check.split('(')
                        cer = cert[1].split(',')
                        if cer[0] == 'C':
                            return hyperparam['green']
                        elif cer[0] == 'V':
                            return float(cer[1])

                    elif cell.style.font_color in {utils.colors.yellow, '00FFFF00'}:
                        check = cell.value
                        check = check[:-1]
                        cert = check.split('(')
                        cer = cert[1].split(',')
                        if cer[0] == 'C':
                            return hyperparam['yellow']
                        elif cer[0] == 'V':
                            return float(cer[1])

                    elif cell.style.font_color in {utils.colors.purple, '800080'}:
                        check = cell.value
                        check = check[:-1]
                        cert = check.split('(')
                        cer = cert[1].split(',')
                        if cer[0] == 'C':
                            return hyperparam['purple']
                        elif cer[0] == 'V':
                            return float(cer[1])
                    
                    elif cell.style.font_color in {utils.colors.red, 'FFFF0000'}:
                        check = cell.value
                        check = check[:-1]
                        cert = check.split('(')
                        cer = cert[1].split(',')
                        if cer[0] == 'C':
                            return hyperparam['red']
                        elif cer[0] == 'V':
                            return float(cer[1])

                    elif cell.style.font_color in {utils.colors.blue, 'FF0070C0'}:
                        check = cell.value
                        check = check[:-1]
                        cert = check.split('(')
                        cer = cert[1].split(',')
                        if cer[0] == 'C':
                            return hyperparam['blue']
                        elif cer[0] == 'V':
                            return float(cer[1])
                    
                    elif cell.style.font_color in {utils.colors.black, '00000000'}:
                        check = cell.value
                        check = check[:-1]
                        cert = check.split('(')
                        cer = cert[1].split(',')
                        if cer[0] == 'C':
                            return hyperparam['black']
                        elif cer[0] == 'V':
                            return float(cer[1])

                    else:
                        check = cell.value
                        check = check[:-1]
                        cert = check.split('(')
                        cer = cert[1].split(',')
                        if cer[0] == 'C':
                            return hyperparam['black']
                        elif cer[0] == 'V':
                            return float(cer[1])
                else:
                    return 0.0000001
            
            sf_2 = StyleFrame(sf.applymap(only_cells_with_red_text))
            sf_3 = StyleFrame(sf.applymap(only_cells_with_red_text_emp))

            # passing a tuple to pandas.dropna is deprecated since pandas 0.23.0, but this can be
            # avoided by simply calling dropna twice, once with axis=0 and once with axis=1
            def get_sum(sf_3):
                sf_3.to_excel(curdir+'/AI Internal-Outputs/output_0.xlsx').save()
                df = read_data(curdir+'/AI Internal-Outputs/output_0.xlsx')
                code_dict = []
                lent = 0
                for col in df.columns:
                    if 'Code' in col:
                        lent = lent + 1
                
                for i in range(1,lent):
                    code_dict.append("Code "+str(i))
                qf=[]
                df = df.fillna(0)
                for col in code_dict:
                
                    if any(i == 150 for i in df[col].values):
                        qf.append(col)
                
                qualifying_dict = {}
                df = df.iloc[3:,6:]
                for col_n in qf:
                    idx = int(col_n.split()[1])
                    df_n = df.iloc[:,idx-1]
                    qualifying_dict[col_n] = df_n.values
                standard_matrix = df.values

                def sumColumn(matrix):
                    return np.sum(matrix, axis=0) 

                return standard_matrix

            sf_2.to_excel(curdir+'/AI Internal-Outputs/output.xlsx').save()
            df = read_data(curdir+'/AI Internal-Outputs/output.xlsx')
            code_dict = []
            lent = 0
            for col in df.columns:
                if 'Code' in col:
                    lent = lent + 1

            for i in range(1,lent):
                code_dict.append("Code "+str(i))
            qf=[]
            df = df.fillna(0)
            for col in code_dict:
            
                if any(i == 150 for i in df[col].values):
                    qf.append(col)
            
            qualifying_dict = {}
     
            df = df.iloc[3:,6:]
            for col_n in qf:
                idx = int(col_n.split()[1])
                df_n = df.iloc[:,idx-1]
                qualifying_dict[col_n] = df_n.values
            
            standard_matrix = df.values
            return standard_matrix,qualifying_dict,get_sum(sf_3),lent


        def get_age_decision(age,lent):
            code_dict = []
            for i in range(1,lent):
                code_dict.append("Code "+str(i))
            
            dicte = dict.fromkeys(code_dict, 0)
            prediction_codes = []
            if age<35:
                dicte['Code 1']=120
                prediction_codes.append("Code 1")
            if 30<age<50:
                dicte['Code 2']=100
                prediction_codes.append("Code 2")
            if 10<age<58:
                dicte['Code 3']=100
                dicte['Code 5']=100
                dicte['Code 7']=100
                dicte['Code 13']=100
                dicte['Code 14']=100
                dicte['Code 15']=100
                prediction_codes.append("Code 3")
                prediction_codes.append("Code 5")
                prediction_codes.append("Code 7")
                prediction_codes.append("Code 13")
                prediction_codes.append("Code 14")
                prediction_codes.append("Code 15")
            if age<55:
                dicte['Code 12']=100
                prediction_codes.append("Code 12")

            if 10<age<68:
                dicte['Code 16']=100
                prediction_codes.append("Code 16")

            if age<45:
                dicte['Code 18']=100
                prediction_codes.append("Code 45")

            if 20<age<52:
                dicte['Code 28']=100
                prediction_codes.append("Code 28")

            if 45<age<58:
                dicte['Code 30']=100
                dicte['Code 31']=100
                prediction_codes.append("Code 30")
                prediction_codes.append("Code 31")

            if 12<age<60:
                dicte['Code 33']=100
                prediction_codes.append("Code 33")
            if 12<age<58:
                dicte['Code 35']=100
                prediction_codes.append("Code 35")
            if 10<age<60:
                dicte['Code 37']=100
                dicte['Code 38']=100
                prediction_codes.append("Code 37")
                prediction_codes.append("Code 38")
            if age:
                prediction_codes.append("Code 4")
                prediction_codes.append("Code 6")
                prediction_codes.append("Code 8")
                prediction_codes.append("Code 9")
                prediction_codes.append("Code 10")
                prediction_codes.append("Code 11")
                prediction_codes.append("Code 17")
                prediction_codes.append("Code 19")
                prediction_codes.append("Code 20")
                prediction_codes.append("Code 21")
                prediction_codes.append("Code 22")
                prediction_codes.append("Code 23")
                prediction_codes.append("Code 24")
                prediction_codes.append("Code 25")
                prediction_codes.append("Code 26")
                prediction_codes.append("Code 27")
                prediction_codes.append("Code 29")
                prediction_codes.append("Code 32")
                prediction_codes.append("Code 34")
                prediction_codes.append("Code 36")
                dicte["Code 4"]=100
                dicte["Code 6"]=100
                dicte["Code 8"]=100
                dicte["Code 9"]=100
                dicte["Code 10"]=100
                dicte["Code 11"]=100
                dicte["Code 17"]=100
                dicte["Code 19"]=100
                dicte["Code 20"]=100
                dicte["Code 21"]=100
                dicte["Code 22"]=100
                dicte["Code 23"]=100
                dicte["Code 24"]=100
                dicte["Code 25"]=100
                dicte["Code 26"]=100
                dicte["Code 27"]=100
                dicte["Code 29"]=100
                dicte["Code 32"]=100
                dicte["Code 34"]=100
                dicte["Code 36"]=100

            return dicte,prediction_codes


        def get_percentile(score_arr,sum_std_mat,idx_file,df_attempt):

            """
            ptile = [ (len(list(np.where(np.array(x)<=i)[0]))/len(x))*100  for i in x]
            """
            cnt = 0
            
            master_attempt = np.where(sum_std_mat ==0,0,1)
            score_mul = df_attempt.T @ master_attempt
            score_mul = [i * 120 for i in score_mul]
        
            unique_score = score_mul
            max_v = np.max(score_arr)
            inx = max_v
            comp_std = []
            for inx,val in enumerate(score_arr):
                try:
                    bck = (val/unique_score[idx_file[-inx-1]])*100
                except:
                    bck = 127.7789
                bck = bck/10
                comp_std.append(bck)
                if val>0:
                    cnt+=1
                    inx = val
            if max_v == 0:
                max_v = 1
            mulk = (max_v - inx)/max_v

            scorecard = [(((i/max_v)*100)-(cnt*mulk)*2.2132) for i in score_arr]
            return scorecard,comp_std

        def get_qualify(attempt,qualify_dict,lent):
            code_dict = []
            for i in range(1,lent):
                code_dict.append("Code "+str(i))
            
            hell_dict = dict.fromkeys(code_dict, 1)
            for key,val in qualify_dict.items():
                check = np.where(np.logical_and(val==150, attempt==1))[0]
                
                if len(check)>0:
                    hell_dict[key]= 1
                else:
                    hell_dict[key]= -100000

            return hell_dict

        def get_test_output(df, col_number):
            chl = 0
            chlt = 0
            for inx,rows in df.iterrows():
                if rows['Sub-Feature'] == "external factor":
                    chl = inx
            for inx,rows in df.iterrows():
                if rows['Sub-Feature'] == "DropDowns":
                    chlt = inx

            df_check = df.iloc[chl+1:chlt-7]
            df = df[[col_number]]
            ethinicity = df.iloc[4:5].values[0]
            age = df.iloc[5:6].values[0]
            age = age[0]
            ethinicity = str(ethinicity[0])

            df_check = df_check.fillna(0)
            to_check_array = df_check[col_number].values
            return to_check_array,age,ethinicity


        def get_top_5_predictions(to_check_array,age,standard_matrix,qualifying_dict,sum_std_mat,ethnicity,col_number,lent,mat_master_dict,to_check_dict):
            
            """ dicte,prediction_codes = get_age_decision(age)
            to_check_array_match = np.where(to_check_array == 0, 0, 1)
            tat_val_match = np.dot(to_check_array_match.T,standard_matrix)
            for idx,val in enumerate(tat_val_match):
            code_idx = "Code "+str(idx+1)
            tat_val_match[idx] = tat_val_match[idx]*dicte[code_idx] 
            to_check_array_n_match = np.where(to_check_array == 0, -0.001, 0)
            tat_val_n_match = np.dot(to_check_array_n_match.T,standard_matrix)

            for idx,val in enumerate(tat_val_n_match):
            code_idx = "Code "+str(idx+1)
            tat_val_n_match[idx] = tat_val_n_match[idx]*dicte[code_idx] 
            tat_val = tat_val_match + tat_val_n_match
            top_2_idx = np.argsort(tat_val)[-5:]
            top_2_val = [tat_val[i] for i in reversed(top_2_idx)]
            accuarcy = [val/sum(top_2_val) for val in top_2_val]
            predictions = ["Code " + str(idx+1) for idx in reversed(top_2_idx)]
            return predictions,accuarcy,get_scores(top_2_val) """

            def mydot(v1, v2):
                return sum([x*y for x,y in zip(v1, v2)])

            def matmulvec(M, v):
                return [mydot(r,v) for r in M]

            def matprod(x, y):
                I = range(len(x))
                J = range(len(y[0]))
                K = range(len(x[0]))
                matmul = []
                for i in I:
                    matmulprod = []
                    for j in J:
                        for k in K:
                            matmulprod.append(sum(x[i][k]*y[k][j]))
                    matmul.append(matmulprod)
                return matmul  

            def py_matmul(a, b):
                ca = len(a)
                ra = 1
                rb, cb = b.shape
                assert ca == rb, f"{ca} != {rb}"
                
                output = np.zeros(shape=(ra, cb))
                for i in range(ra):
                    for j in range(cb):
                        for k in range(rb):
                            output[i, j] += a[i, k] * b[k, j]
                            
                return output

            consumption_dict = {}
            consumption_dict['Finetuning Logic'] = "Not Consumed"
            consumption_dict['Qualifying criteria'] = "Not Used"
            consumption_dict['Age logic'] = "Not Consumed"
            consumption_dict['Insurance settlement history'] = "Not Consumed"
            consumption_dict['Ethnicity Logic'] = "Not Consumed"
            consumption_dict['Layer Logic'] = "Not Consumed"
            f = open('Value-json/hyperparam.json') 
            hyperparam = json.load(f)
            st = standard_matrix.T
            mat_dict = []
            
            to_check_array = np.where(to_check_array == 0, hyperparam['alpha'], 1)
            rnums = []
            for inx,num in enumerate(to_check_array):
                rnum = "(R{},{})".format(inx+5,num)
                rnums.append(rnum)
                
            to_check_dict[col_number] = rnums

            with open("Input Sheets/mat_dict.txt",'r') as file:
                line = file.read()
                inner_list = [elt.strip() for elt in line.split(',')]

            f = open('Value-json/logic_activation.json') 
            activation = json.load(f)
            if activation['matmul_logic'] == "active":
                for number in inner_list:
                    if col_number == int(number):
                        for ind in range(len(st)):
                            code_idx = "C"+str(ind+1)
                            ajio = np.multiply(to_check_array,st[ind])
                            tax_p = []
                            for aj in range(len(ajio)):
                                tax_p.append('{}(R{},{})'.format(ajio[aj],aj+5,code_idx))
                            
                            mat_dict.append(tax_p) 
            
            mat_master_dict[col_number] = np.array(mat_dict).T
                
            standard_matrix = standard_matrix
            for inx in range(len(to_check_array)):
                if to_check_array[inx] < 0:
                    for idx,val in enumerate(standard_matrix[inx]):
                        if val < 0:
                            standard_matrix[inx][idx] = 0

            tat_val = np.dot(to_check_array.T,standard_matrix)
            qualify_dict = get_qualify(to_check_array,qualifying_dict,lent)
            col_number =col_number
            intial_logic = {}
            for idx,val in enumerate(tat_val):
                code_idx = "Code "+str(idx+1)
                f = open('Value-json/logic_activation.json') 
                activation = json.load(f)
                if qualify_dict[code_idx] <0:
                    if activation['qualifying_criteria'] == 'active':
                        consumption_dict['Qualifying criteria'] = "Used"
                        tat_val[idx] = -1000000
                    else:
                        pass
                else:
                    if activation['age_logic'] == 'active':
                        if dicte[code_idx] == 0:
                            consumption_dict['Age logic'] = "Consumed"
                            tat_val[idx] = -1000000
                        else:
                            pass
                    else:
                        pass
                intial_logic[code_idx] = tat_val[idx]
            
            f = open('Value-json/logic_activation.json') 
            activation = json.load(f)

            if activation['settlement_logic'] == 'active':
                df = pd.read_excel(os.curdir + '/Logic Container/Insurance settlement history.xlsx')
                for idx,rows in df.iterrows():
                    if rows['Age']!=rows['Age']:
                        break
                    else:
                        age_r = rows['Age'].split('-')
                        age_start = int(age_r[0])
                        age_end = int(age_r[1])

                        if age_start <= age <= age_end:
                            total = 0
                            val_arr = (rows[1:].values)
                            for val in val_arr:
                                if '#' in str(val):
                                    pass
                                else:
                                    total = total + val

                            for inx,score in enumerate(tat_val):
                                code_idx = "Code "+str(inx+1)
                                if inx!=3122239:
                                    if '#' in str(rows[code_idx]):
                                        pass
                                    else:
                                        prob = float(rows[code_idx])/float(total)
                                        consumption_dict['Insurance settlement history'] = "Consumed"
                                        tat_val[inx] = tat_val[inx] * prob
                                else:
                                    continue
            
            settlement_logic = {}

            for inx,score in enumerate(tat_val):
                code_idx = "Code "+str(inx+1)
                settlement_logic[code_idx] = tat_val[inx]

            f = open('Value-json/logic_activation.json') 
            activation = json.load(f)

            if activation['ethnicity_logic'] == 'active':

                df = pd.read_excel(os.curdir + '/Logic Container/Ethnicity Logic.xlsx')
                cols = df.columns
                for inx,rows in df.iterrows():
                    if rows['Ethnicity']!=rows['Ethnicity']:
                        break
                    else:
                        if ethnicity == rows['Ethnicity']:
                            for inx,score in enumerate(tat_val):
                                code_idx = "Code "+str(inx+1)
                                if inx!=311229:
                                    prob = rows[code_idx]
                                    consumption_dict['Ethnicity Logic'] = "Consumed"
                                    tat_val[inx] = tat_val[inx] * prob 
                                else:
                                    pass
                        else:
                            for inx,score in enumerate(tat_val):
                                code_idx = "Code "+str(inx+1)

                                if inx!=311129:
                                    prob = 1
                                    consumption_dict['Ethnicity Logic'] = "Consumed"
                                    tat_val[inx] = tat_val[inx] * prob 
                                else:
                                    pass
            ethnicity_logic = {}

            for inx,score in enumerate(tat_val):
                code_idx = "Code "+str(inx+1)
                ethnicity_logic[code_idx] = tat_val[inx]
            
            f = open('Value-json/logic_activation.json') 
            activation = json.load(f)

            if activation['finetuning_logic'] == 'active':

                df = pd.read_excel(os.curdir + '/Logic Container/Fine tuning logic.xlsx')
                cols = df.columns
                for inx,rows in df.iterrows():
                    if rows['Age']!=rows['Age']:
                        break
                    else:
                        age_r = rows['Age'].split('-')
                        age_start = int(age_r[0])
                        age_end = int(age_r[1])

                        if age_start <= age <= age_end:
                            
                            for inx,score in enumerate(tat_val):
                                code_idx = "Code "+str(inx+1)

                                if inx!=31119:


                                    if '#' not in str(rows[code_idx]):
                                        
        
                                        prob = rows[code_idx]
                          
                                        consumption_dict['Finetuning Logic'] = "Consumed"

                                        tat_val[inx] = tat_val[inx] * prob
                                    else:
                                        tat_val[inx] = -100000

                            

                                    

                                    
                        

                                else:
                                    continue




            
            finetuning_logic = {}


            for inx,score in enumerate(tat_val):
                code_idx = "Code "+str(inx+1)
                finetuning_logic[code_idx] = tat_val[inx]

            


            f = open('Value-json/logic_activation.json') 
            activation = json.load(f)


            if activation['layer_logic'] == 'active':

                df = pd.read_excel(os.curdir + '/Logic Container/Layer Logic.xlsx')

    
            
                layer = 0

                for idx,rows in df.iterrows():
                    layer = layer + 1
                    if layer == 1:
                        initial_prediction_weight = rows['Weightage']
                    elif layer ==2:
                        settlement_logic_weight = rows['Weightage']
                    elif layer == 3:
                        ethnicity_logic_weight = rows['Weightage']
                    elif layer == 4:
                        finetuning_logic_weight = rows['Weightage']
                    else:
                        pass

                
                for inx,score in enumerate(tat_val):
                    code_idx = "Code "+str(inx+1)
                    tat_val[inx] = intial_logic[code_idx]*(initial_prediction_weight +  settlement_logic_weight*(settlement_logic[code_idx]/intial_logic[code_idx]) + ethnicity_logic_weight*(ethnicity_logic[code_idx]/settlement_logic[code_idx]) + finetuning_logic_weight*(finetuning_logic[code_idx]/ethnicity_logic[code_idx]))
                    consumption_dict['Layer Logic'] = "Consumed"
                
                



                   
                   



        
            
            final_logic = {}


            for inx,score in enumerate(tat_val):
                code_idx = "Code "+str(inx+1)
                final_logic[code_idx] = tat_val[inx]




            




            
            def get_logic_pred(dicte):
                new_dicte = {k: v for k, v in sorted(dicte.items(), key=lambda item: item[1], reverse=True)}
                cnt = 0
                logic_pred = []
                for idx,value in new_dicte.items():
                    cnt = +1

                    
                    logic_pred.append(idx)
                return logic_pred


            intial_logic_pred = get_logic_pred(intial_logic)
            ethnicity_logic_pred = get_logic_pred(ethnicity_logic)
            settlement_logic_pred = get_logic_pred(settlement_logic)
            
            finetuning_logic_pred = get_logic_pred(finetuning_logic)
            final_logic_pred = get_logic_pred(final_logic)
            consumption_metric = [col_number,json.dumps(consumption_dict)]
            prediction_metric = [col_number,json.dumps(intial_logic),intial_logic_pred,json.dumps(settlement_logic),settlement_logic_pred,json.dumps(ethnicity_logic),ethnicity_logic_pred,json.dumps(finetuning_logic),finetuning_logic_pred,json.dumps(final_logic),final_logic_pred]





            
            predictions = list(final_logic_pred)[:5]
            top_2_val = [int(final_logic[i]) for i in (predictions)]
            top_2_idx = []
            for val in predictions:
                wer = val.split()
                top_2_idx.append(int(wer[1]))

            #print(tat_val)
            #accuarcy = [val/sum(top_2_val) for val in top_2_val]
            #predictions = ["Code " + str(idx+1) for idx in reversed(top_2_idx)]

            score_relat,score_std = get_percentile(top_2_val,sum_std_mat,top_2_idx,to_check_array)
            return predictions,score_relat,score_std,prediction_metric,consumption_metric,mat_master_dict,to_check_dict
            


        def save_master_log(master_sheet_filepath):
            df = pd.read_excel(master_sheet_filepath)
            df_w = df.fillna(0)
           
            df_w = df_w.iloc[3:,:]
   
            weightage = list(df_w.iloc[:,4].values)

            df = pd.read_excel(master_sheet_filepath)
            df_s = df.fillna(0)
            df_s = df_s.iloc[3:,:]

            
            scores = df_s.iloc[:,5].values
            scores = np.where(scores == 'B',-1,scores)
            scores = np.where(scores == 'A',1,scores)
            #scores = np.prod(scores)
            #weightage.append(scores)
            np.savetxt('AI Internal-Outputs/master_log_weightage.txt', weightage)
            np.savetxt('AI Internal-Outputs/master_log_score.txt',scores)
        def get_recommendation(df_attempt):
            b = np.loadtxt('AI Internal-Outputs/master_log_weightage.txt')
            c = np.loadtxt('AI Internal-Outputs/master_log_score.txt')

            scores = (np.multiply(c,df_attempt)).flatten()
            sc_a = 0
            sc_b = 0
            for sc in scores:
                if sc==-1:
                    sc_b+=1
                elif sc == 1:
                    sc_a+=1
                else :
                    pass
            if sc_b == 0:
                if sc_a ==0:
                    score = "No Score Defined"
                else:
                    score = 'A'
            else:
                score = 'B'

            self.weightage = b

        
            mul = (np.multiply(self.weightage,df_attempt)).flatten()

            #mul = [(i+5)/2 for i in mul if i != 0]
        
        
                
            cum_score = np.sum(mul)
            #print(cum_score)
    
            #print(cum_score)
            if cum_score < 0 :
                cum_score = 0
            elif cum_score > 5:
                cum_score = 5

            elif 0<=cum_score<=1:
                cum_score = 0
            elif 1<cum_score<=2:
                cum_score = 1
            elif 2<cum_score<=3:
                cum_score = 2
            elif 3<cum_score<=4:
                cum_score = 3
            elif 4<cum_score<5:
                cum_score = 4
            else:
                cum_score = 5
            



            
            
            filepath = curdir + "/Input Sheets/recommendation_sheet.csv"
            df = pd.read_csv(filepath)
            #df_k = df.fillna(" ")
            x = df.iloc[1:,1:].values
            x = x.flatten()

            self.recom_tot_val = []
            for value in x:
                if value!=value:
                    pass
                else:
                    #print(value)
                    self.recom_tot_val.append(value)  

            score_a = df.iloc[6,:]
            score_b = df.iloc[7,:]

            for idx,row in df.iterrows():
                if idx == int(cum_score):
                    
                    recom = [row['Intepretation-1']] 
                    if score=="No Score Defined":
                        recom.append(row['Intepretation-2'])
                        recom.append(row['Intepretation-3'])
                    else :
                        if score=='A':
                            recom.append(score_a['Intepretation-2'])
                            recom.append(score_a['Intepretation-3'])

                        else:
                            recom.append(score_b['Intepretation-2'])
                            recom.append(score_b['Intepretation-3'])   

                        
            
            return recom,cum_score,score,mul
                


        def execute(df,col_number,mat_master_dict,to_check_dict):

            
            sf = read_master_sheet(self.master_sheet_filepath)
            save_master_log(self.master_sheet_filepath)
            standard_matrix,qualifying_dict,sum_std_mat,lent = get_standard_matrix(sf)
            to_check_array,age,ethnicity = get_test_output(df,col_number)
            predictions,score_relat,score_std,prediction_metric,consumption_metric,mat_master_dict,to_check_dict = get_top_5_predictions(to_check_array,age,standard_matrix,qualifying_dict,sum_std_mat,ethnicity,col_number,lent,mat_master_dict,to_check_dict)
  
            
            #print("Age of the user is = ",age)
            #print("TOP 5 PREDICTIONS ARE :")
            #print(predictions)
            #print("With Cumilitave scores of :")
            #print(scores)
            return age,predictions,score_relat,score_std,ethnicity,prediction_metric,consumption_metric,mat_master_dict,lent,to_check_dict


        def execute_single_files():
            global total_files, rows_of_file, cur_file_num, cur_row_num, aver_time, total_completed_rows, start_time
            
            start_time = datetime.now()

            print("____________*** Prediction Al ***_____________________")
            print("Please make sure master sheet and test sheet are uploaded")
            print(" ")

            total_files = len(self.test_sheet_filepaths)
            cur_file_num = 0
            for test_sheet_filepath in self.test_sheet_filepaths:
                cur_file_num += 1
                self.test_sheet_filepath = test_sheet_filepath

                file1 = open("AI External-Outputs/path_info.txt", "w")

                file1.write("M"+self.master_sheet_filepath)
                file1.write(" \n") 
            
                file1.write("T"+self.test_sheet_filepath)
                file1.write(" \n")
                file1.close()
        
                test_df = read_data(self.test_sheet_filepath)
                test_df = df_column_uniquify(test_df)
                temp_df = test_df.iloc[:,4:]

                col_name = temp_df.columns
                print("col_name = ", col_name)
                code_values = temp_df.iloc[0].values
                prediction_output = []
                accuracy_1 = 0
                accuracy_2 = 0
                self.cnt = 0
    
                # Progress bar widget 
                prediction_metrics = []
                consumption_metrics = []
                mat_master_dict = {}
                to_check_dict = {}

#################################                 
                # file = open("AI External-Outputs/path_info.txt","r")
                # for lines in file.read().splitlines():
                #     if lines[0] == "T":
                #         test_filepath = lines[1:]
                # file.close() 
                test_filepath = self.test_sheet_filepath
##################                
                
                t_filename = Path(test_filepath).stem
                cols_names = ['Column Reference Code','Actual Code','Age','Ethnicity','Predcition Codes','Relative Confidence Percentage','Standard Confidence Percentage','Story','Recommendations','5 yr Risk','10 yr Risk','Lifetime Risk']
                df = pd.DataFrame(columns =cols_names)
                df.to_csv("AI External-Outputs/Prediction_output_{}.csv".format(t_filename),index=False)

                rows_of_file = len(col_name)
                cur_row_num = 0
                for idx,col in enumerate(col_name):
                    cur_row_num += 1
                    # if idx > 1 : break
                    print("idx = ", idx, " , col = ", col)
                    age,prediction,score_relat,score_std,ethnicity,prediction_metric,consumption_metric,mat_master_dict,lent,to_check_dict = execute(test_df,col,mat_master_dict,to_check_dict)
                    consumption_metrics.append(consumption_metric)
                    prediction_metrics.append(prediction_metric)
                    prediction_output = [col,code_values[idx], age,ethnicity, prediction,score_relat,score_std,'story','Recommendations','5 yr risk','10 yr risk','lifetime risk']
                    if code_values[idx]!=code_values[idx]:
                        code_values[idx] = "Not Provided"
                    if col!=col:
                        col = "Not Provided"
                    if age!=age:
                        age = "Not Provided"

                    if ethnicity!=ethnicity:
                        ethnicity = "Not Provided"




                        
                    print("-----------------------------------------CASE NUMBER = {}------------------------------------------------------".format(col))
                    print()

                    print('For Case Number {} with Age {}yrs and Ethnicity {}, has an Actual Provided Code as {} However AI Top 5 Predcition Codes are {} with Relative Confidence Percentage as {}'.format(col,age,ethnicity,code_values[idx],prediction,score_relat))
                    print()
                    print("******************************************************************************************************************************************************************************************************************************************")

                
                

                    self.cnt = self.cnt+1
                    if code_values[idx] in [prediction[0],prediction[1]]:
                    
                        accuracy_2 = accuracy_2+1
                    if code_values[idx] == prediction[0]:

                        accuracy_1 = accuracy_1+1
                    
                    df = pd.DataFrame(consumption_metrics, columns =['Column Reference Code','Logic Consumption Dictonary'])
############################                    
                    # file = open("AI External-Outputs/path_info.txt","r")
                    # for lines in file.read().splitlines():
                    #     if lines[0] == "T":
                    #         test_filepath = lines[1:]
                    # file.close() 
############################                    
                    t_filename = Path(test_filepath).stem

                    with open("Input Sheets/mat_dict.txt",'r') as file:
                        line = file.read()
                        inner_list = [elt.strip() for elt in line.split(',')]
                    inner_list = inner_list[:-1]

                    with open("AI External-Outputs/matmul_{}.csv".format(t_filename),'w') as f:
                        w = csv.writer(f)
                        code_dict = []

                        for i in range(1,lent):
                            code_dict.append("Code "+str(i))
                        
                        w.writerow(code_dict)
                    
                        
                        for key,val in mat_master_dict.items():
                            w.writerow([key])
                            w.writerows(val)

                    with open("AI External-Outputs/attempt_sheet_{}.csv".format(t_filename),'w') as f:
                        w = csv.writer(f)

     
                    
                        
                        for key,val in to_check_dict.items():
                            w.writerow([key])
                            w.writerows([val])

                    df.to_csv("AI External-Outputs/Consumption_metric_{}.csv".format(t_filename))
                    
                    df = pd.DataFrame(prediction_metrics, columns =['Column Reference Code','Intial Score','Intial Prediction','Settlement Logic','Settlement Prediction','Ethnicity Logic','Ethnicity Prediction','Fine Tuning Logic','FineTuning Prediction','Final Logic','Final Prediction'])  
                    
                    df.to_csv("AI External-Outputs/Prediction_metric_{}.csv".format(t_filename))

                    # file = open("AI External-Outputs/path_info.txt","r")
                    # for lines in file.read().splitlines():
                    #     if lines[0] == "T":
                    #         test_filepath = lines[1:]
                    # file.close() 
                    total_df= pd.read_excel(test_filepath)
                    chl = 0
                    chlt = 0
                    for inxt,rows in total_df.iterrows():
                        if rows['Sub-Feature'] == "external factor":
                            chl = inxt
                    
                    for inxt,rows in total_df.iterrows():
                        if rows['Sub-Feature'] == "endFeatures":
                            chlt = inxt
                 
                    df_ops = total_df[[col]]
                    df_ops = df_ops.fillna(0)
                    df_process = total_df.fillna(method='ffill')
                    df_attempt = df_ops.where(df_ops == 0, 1)
  
                    df_attempt = (df_attempt.iloc[chl:chlt-1,:]).values
                    df_attempt = df_attempt.flatten()
                    recommendation,cum_score,score,mul = get_recommendation(df_attempt)
                    df = pd.read_csv("AI External-Outputs/Prediction_output_{}.csv".format(t_filename))
                    dicte= {}
                    for inx,items in enumerate(prediction_output):
                        dicte[cols_names[inx]] = items
                    dicte['Recommendations'] = recommendation
                    df = df.append(dicte,ignore_index=True)
                    df.to_csv("AI External-Outputs/Prediction_output_{}.csv".format(t_filename),index=False)
      
                    #print("Accurate is ",accuracy)
                    if self.cnt==0:
                        self.cnt= 1
                    
                
                    self.accuracy_2 = (accuracy_2/self.cnt)*100
                    self.accuracy_1 = (accuracy_1/self.cnt)*100
                    gr = GeneticRisk()
                    sk = storykey()
                    a = threading.Thread(target = gr.execute(self.test_sheet_filepath,col))
                    a.start()
                    a.join()


                    sk.execute(self.test_sheet_filepath,col,idx)
                    total_completed_rows += 1
                    aver_time = (datetime.now() - start_time).total_seconds() / total_completed_rows 

        execute_single_files() 

    def exit_the_window():
        self.user_root.destroy()


    def display(self):
        def add_user_verify():
            if not os.path.exists('user_pass_database'):
                os.makedirs('user_pass_database')

            

            username_info = username_data_entry.get()
            password_info = password_data_entry.get()
            start_code_info = start_code_entry.get()
            end_code_info = end_code_entry.get()
        
            file = open("user_pass_database/" + username_info + ".txt", "w")
            file.write(username_info + "\n")
            file.write(password_info + "\n")
            file.write(start_code_info + "\n")
            file.write(end_code_info + "\n")

            file.close()
        
            username_data_entry.delete(0, END)
            password_data_entry.delete(0, END)
            start_code_entry.delete(0, END)
            end_code_entry.delete(0, END)


        
            Label(self.user_root, text="Added Successfully", fg="green", font=("calibri", 11)).pack()
            Button(self.user_root, text="Exit", width=10, height=1, command = self.user_root.destroy()).pack()



        def add_user_data():
            global username_data
            global password_data
            global start_code
            global end_code
            global username_data_entry
            global password_data_entry
            global start_code_entry
            global end_code_entry
            username_data = StringVar()
            password_data = StringVar()
            start_code = StringVar()
            end_code = StringVar()



            self.user_root = tkinter.Tk()
            # self.user_root.geometry("500x500")
            display_in_center(self.user_root, 500, 500)

            Label(self.user_root, text="Username * ").pack()
            username_data_entry = Entry(self.user_root, textvariable=username_data)
            username_data_entry.pack()
            Label(self.user_root, text="").pack()
            Label(self.user_root, text="Password * ").pack()
            password_data_entry = Entry(self.user_root, textvariable=password_data)
            password_data_entry.pack()
            Label(self.user_root, text="").pack()
            Label(self.user_root, text="Start Unique Code").pack()
            start_code_entry = Entry(self.user_root, textvariable=start_code)
            start_code_entry.pack()
            Label(self.user_root, text="").pack()
            Label(self.user_root, text="End Unique Code").pack()
            end_code_entry = Entry(self.user_root, textvariable=end_code)
            end_code_entry.pack()
            Label(self.user_root, text="").pack()
            Button(self.user_root, text="Add user data", width=10, height=1, command = add_user_verify).pack()
            

        def display_prediction():
            root = tkinter.Tk()
            # root.geometry("1024x1024")
            display_in_center(root, 1000, 800)

            ico_path = curdir+"\\media\\my_icon.ico"
            root.iconbitmap(ico_path)
            grid = MagicGrid(root)
            grid.pack(side="top", expand=2, fill="both")

            # open file
            file = open("AI External-Outputs/path_info.txt","r")
            for lines in file.read().splitlines():
                if lines[0] == "T":
                    test_filepath = lines[1:]
            file.close() 
            
            t_filename = Path(test_filepath).stem
            with open(self.current_dir+"/AI External-Outputs/Prediction_output_{}.csv".format(t_filename), newline = "") as file:
                reader = csv.reader(file)
                parsed_rows = 0

                # r and c tell us where to grid the labels
                for row in reader:
                    if parsed_rows == 0:
                        # Display the first row as a header
                        grid.add_header(*row)
                    else:
                        grid.add_row(*row)
                    parsed_rows += 1

                root.mainloop()
        root = Tk() 


        # ico_path = curdir+"\\media\\my_icon.ico"
        # root.iconbitmap(ico_path)

        # specify size of window. 
        # root.geometry("1024x1024") 
        display_in_center(root, 1000, 300)

        # Create text widget and specify size. 
        T = Text(root, height = 5, width = 52) 

        # Create label 
        


        l = Label(root, text = "Prediction by AI are saved") 
        l.config(font =("Courier", 14)) 

        # Create button for next text. 
        b1 = Button(root, text = "Display the Predictions", command = display_prediction) 

        # Create an Exit button. 
        b2 = Button(root, text = "Exit", 
                    command = root.destroy) 

        b3 = Button(root, text = "Add User Data", command = add_user_data) 
        
        T.insert(END, "Total Number of user Tested = ")
        T.insert(END, str(self.cnt)+'\n')
        
        T.insert(END, "Accuracy for being in top 2 predictions = ")
        T.insert(END, str(self.accuracy_2)+'\n')
        T.insert(END, "Accuracy for being the top predictions = ")
        T.insert(END, str(self.accuracy_1)+'\n')

        l.pack() 
        T.pack() 
        b1.pack() 
        b2.pack() 
        b3.pack()





        


        # Insert The Fact. 

        

    def start_submit_thread(self,event):
        global submit_thread
        submit_thread = threading.Thread(target=self.get_prediction)
        submit_thread.daemon = True
        self.progressbar.start()
        submit_thread.start()
        
        self.root.after(100, self.check_submit_thread)

    def check_submit_thread(self):
        global total_files, rows_of_file, cur_file_num, cur_row_num, aver_time, total_completed_rows
        if submit_thread.is_alive():
            if total_completed_rows  == 0 :
                remain_time = "It is calculating remaining time."
            else:
                remain_time = aver_time * (rows_of_file - cur_row_num + rows_of_file * (total_files - cur_file_num)) - ((datetime.now() - start_time).total_seconds() - total_completed_rows * aver_time)
                if remain_time < 0: remain_time = 0
                r_hour = int(remain_time // 3600)
                r_min = int((remain_time % 3600) // 60)
                r_sec = int(remain_time % 60)
                remain_time = ""
                if r_hour > 0: 
                    remain_time = "{} hour ".format(r_hour)
                if r_min > 0:
                    remain_time += "{} min ".format(r_min)
                if r_sec > 0:
                    remain_time += "{} sec ".format(r_sec)
            self.progressbar["value"] = int(((cur_file_num - 1) / total_files + (cur_row_num - 1) / rows_of_file / total_files) * 100)
            Label(self.root,text=("{} % :   {} remained.".format(self.progressbar["value"], remain_time))).grid(row=1, column=0, columnspan=2, ipadx=50)

            self.progressbar.update()
            self.root.after(50, self.check_submit_thread)
        else:
            print("*************nb yes")
            self.progressbar.stop()
            self.display()
    


        
    


# Designing popup for login invalid password
 
def password_not_recognised():
    global password_not_recog_screen
    password_not_recog_screen = Toplevel(login_screen)

    ico_path = curdir+"\\media\\my_icon.ico"
    password_not_recog_screen.iconbitmap(ico_path)
    
    password_not_recog_screen.title("Success")
    # password_not_recog_screen.geometry("150x100")
    display_in_center(password_not_recog_screen, 150, 100)
    Label(password_not_recog_screen, text="Invalid Password ").pack()
    Button(password_not_recog_screen, text="OK", command=delete_password_not_recognised).pack()
 
# Designing popup for user not found
 
def user_not_found():
    global user_not_found_screen
    user_not_found_screen = Toplevel(login_screen)

    ico_path = curdir+"\\media\\my_icon.ico"
    login_screen.iconbitmap(ico_path)
    
    
    user_not_found_screen.title("Success")
    # user_not_found_screen.geometry("150x100")
    display_in_center(user_not_found_screen, 150, 100)
    Label(user_not_found_screen, text="User Not Found").pack()
    Button(user_not_found_screen, text="OK", command=delete_user_not_found_screen).pack()
    user_not_found.after(500, delete_user_not_found_screen)


# Deleting popups
def delete_login_success():
    login_screen.destroy()
    main_screen.destroy()
 
 
def delete_password_not_recognised():
    password_not_recog_screen.destroy()
 
 
def delete_user_not_found_screen():
    user_not_found_screen.destroy()
 
 
# Designing Main(first) window
def welcome_screen():
    global welcome_screen
    welcome_screen = Tk()

    image = PIL.Image.open("logo.jpg")
    width, height = image.size
    new_width = 600
    new_hight = int(height / width * new_width)
    image = image.resize((new_width, new_hight))
    img = ImageTk.PhotoImage(image)
    welcome_screen.overrideredirect(True)
    Label(image=img).pack()
    display_in_center(welcome_screen, new_width, new_hight)

    try:
        welcome_screen.after(500, del_and_open)
    except:
        pass
    welcome_screen.mainloop()

   
def main_account_screen():
    if not os.path.exists('user_credential_database'):
        os.makedirs('user_credential_database')
    global main_screen
    main_screen = Tk()

    ico_path = curdir+"\\media\\my_icon.ico"
    main_screen.iconbitmap(ico_path)
    main_screen.title("Account Login")
    Label(text="PREDECTIVE AI", bg="blue", width="300", height="2", font=("Calibri", 13)).pack()
    Label(text="").pack()
    Button(text="Login", height="2", width="30", command = login).pack()
    Label(text="").pack()
    Button(text="Register", height="2", width="30", command=register).pack()

    display_in_center(main_screen, 300, 250)
    main_screen.mainloop()

total_files = 1
rows_of_file = 1
cur_file_num = 1
cur_row_num = 1
total_completed_rows = 0
main_account_screen()


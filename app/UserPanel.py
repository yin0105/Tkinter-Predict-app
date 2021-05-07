 
from os import curdir
from tkinter import *
import os
import tkinter.filedialog
import numpy as np
from styleframe import StyleFrame, utils
import math
import pandas as pd
import numpy as np

import csv
import matplotlib
from tkmagicgrid import *
from PIL import ImageTk, Image
from tkinter import ttk
import uuid
from itertools import count
from tkinter.tix import ScrolledWindow
import json
from pathlib import Path
# Designing window for registration




def register():
    global register_screen
    register_screen = Toplevel(main_screen)
    curdir = os.getcwd()
    ico_path = curdir+"\media\my_icon.ico"
    register_screen.iconbitmap(ico_path)
    register_screen.title("Register")
    register_screen.geometry("300x250")
 
    global username
    global password
    global username_entry
    global password_entry
    username = StringVar()
    password = StringVar()
 
    Label(register_screen, text="Please enter details below", bg="black", fg="grey").pack()
    Label(register_screen, text="").pack()
    username_lable = Label(register_screen, text="Username * ")
    username_lable.pack()
    username_entry = Entry(register_screen, textvariable=username)
    username_entry.pack()
    password_lable = Label(register_screen, text="Password * ")
    password_lable.pack()
    password_entry = Entry(register_screen, textvariable=password, show='*')
    password_entry.pack()
    Label(register_screen, text="").pack()
    
    Button(register_screen, text="Register", width=10, height=1, fg="white",bg="blue", command = register_user).pack()
 
 
# Designing window for login 
 
def login():
    global login_screen
    login_screen = Toplevel(main_screen)
    login_screen.title("Login")
    login_screen.geometry("300x250")
    curdir = os.getcwd()
    ico_path = curdir+"\media\my_icon.ico"
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
 
# Implementing event on register button
 
def register_user():
 
    username_info = username.get()
    password_info = password.get()
 
    file = open("user_pass_database/" + username_info, "w")
    file.write(username_info + "\n")
    file.write(password_info)
    file.close()
 
    username_entry.delete(0, END)
    password_entry.delete(0, END)
 
    Label(register_screen, text="Registration Success", fg="green", font=("calibri", 11)).pack()
 
# Implementing event on login button 
 
def login_verify(event=None):
    username1 = username_verify.get()
    password1 = password_verify.get()
    username_login_entry.delete(0, END)
    password_login_entry.delete(0, END)
    current_directory = os.getcwd()
    user_credential_directory = current_directory + '/'+"user_pass_database/"
 
    list_of_files = os.listdir(user_credential_directory)
    
    if username1+".txt" in list_of_files:
        file1 = open(user_credential_directory + username1 + ".txt", "r")
        verify = file1.read().splitlines()
        global p_username 
        p_username = verify[0]
        global p_password
        p_password = verify[1]
        global p_start_code
        p_start_code = verify[2]
        global p_end_code
        p_end_code = verify[3] 
        if password1 in verify:
            login_sucess()
 
        else:
            password_not_recognised()
 
    else:
        user_not_found()
 
# Designing popup for login success
 
def login_sucess():
    global login_success_screen
 
    login_success_screen = Toplevel(login_screen)
    curdir = os.getcwd()
    ico_path = curdir+"\media\my_icon.ico"
    login_success_screen.iconbitmap(ico_path)
    login_success_screen.title("Success")
    login_success_screen.geometry("150x100")
    Label(login_success_screen, text="Login Success").pack()
    Button(login_success_screen, text="OK", command=del_and_open).pack()
    login_success_screen.after(500, del_and_open)


def del_and_open(event=None):
    delete_login_success()







def password_not_recognised():
    global password_not_recog_screen
    password_not_recog_screen = Toplevel(login_screen)
    curdir = os.getcwd()
    ico_path = curdir+"\media\my_icon.ico"
    password_not_recog_screen.iconbitmap(ico_path)
    
    password_not_recog_screen.title("Success")
    password_not_recog_screen.geometry("150x100")
    Label(password_not_recog_screen, text="Invalid Password ").pack()
    Button(password_not_recog_screen, text="OK", command=delete_password_not_recognised).pack()
 
# Designing popup for user not found
 
def user_not_found():
    global user_not_found_screen
    user_not_found_screen = Toplevel(login_screen)
    curdir = os.getcwd()
    ico_path = curdir+"\media\my_icon.ico"
    login_screen.iconbitmap(ico_path)
    
    
    user_not_found_screen.title("Success")
    user_not_found_screen.geometry("150x100")
    Label(user_not_found_screen, text="User Not Found").pack()
    Button(user_not_found_screen, text="OK", command=delete_user_not_found_screen).pack()
    user_not_found.after(500, delete_user_not_found_screen)
 
# Deleting popups
class ImageLabel(Label):
    """a label that displays images, and plays them if they are gifs"""
    def load(self, im):
        if isinstance(im, str):
            im = Image.open(im)
        self.loc = 0
        self.frames = []

        try:
            for i in count(1):
                self.frames.append(ImageTk.PhotoImage(im.copy()))
                im.seek(i)
        except EOFError:
            pass

        try:
            self.delay = im.info['duration']
        except:
            self.delay = 100

        if len(self.frames) == 1:
            self.config(image=self.frames[0],borderwidth=0,highlightthickness = 0,pady=0,padx=0)
        else:
            self.next_frame()

    def unload(self):
        self.config(image="")
        self.frames = None

    def next_frame(self):
        if self.frames:
            self.loc += 1
            self.loc %= len(self.frames)
            self.config(image=self.frames[self.loc],borderwidth=0,highlightthickness = 0,pady=0,padx=0)
            self.after(self.delay, self.next_frame)

def delete_login_success():
    login_success_screen.destroy()
    login_screen.destroy()
    main_screen.destroy()
    app = application_window()
    app.execute()


 
 
def delete_password_not_recognised():
    password_not_recog_screen.destroy()
 
 
def delete_user_not_found_screen():
    user_not_found_screen.destroy()
 
 
# Designing Main(first) window

class application_window():

    def __init__(self):
        self.username = p_username
        self.password = p_password
        self.p_start_code = int(p_start_code)
        self.p_end_code = int(p_end_code)
        self.case_option = 9008
        self.pred_ch_1 = "Null"
        self.pred_ch_2 = "Null"
        self.pred_ch_3 = "Null"
        self.recom_ch_1 = "Null"
        self.recom_ch_2 = "Null"
        self.recom_ch_3 = "Null"




    def get_recommendation(self,df_attempt):
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



    def save_recommendation_log(self,case_num,cum_score,score,mul):
        if not os.path.exists('AI External-Outputs/recommendation_log.csv'):
            pass
        else:
            os.remove("AI External-Outputs/recommendation_log.csv")


        #df = pd.read_csv('recommendation_log.csv', delim_whitespace=True)
        df = pd.DataFrame()
        #df.set_index('S/N', inplace=True) 


        preset = [case_num,cum_score,score]
        mul = mul.tolist()

        zac = (preset+mul)
        #preset = preset.append(mul)
        print(zac)
        #print(preset)
        df[case_num] = zac
        self.df_glob = pd.concat([self.df_glob,df], axis=1)
    
        #print(df)
        self.df_glob.to_csv('AI External-Outputs/recommendation_log.csv', header=False, index=False)

        
      


    def get_prediction(self,case_num):
        file = open("AI External-Outputs/path_info.txt","r")
        for lines in file.read().splitlines():
            if lines[0] == "T":
                test_filepath = lines[1:]
        file.close() 
        
        t_filename = Path(test_filepath).stem
        
        f_pred = curdir + ("/AI External-Outputs/Prediction_output_{}.csv".format(t_filename))
        pred = pd.read_csv(f_pred)
        pred_re = pred.loc[pred['Column Reference Code']==case_num]
        
        pred_co = (pred_re['Predcition Codes'].values)[0]
        pred_co = [elt.strip() for elt in pred_co.split(',')]
        pred_co = pred_co[0:3]
        pred_per = (pred_re['Relative Confidence Percentage'].values)[0]
        pred_per = [elt.strip() for elt in pred_per.split(',')]
        pred_per = pred_per[0:3]
        pred_per_s = (pred_re['Standard Confidence Percentage'].values)[0]
        pred_per_s = [elt.strip() for elt in pred_per_s.split(',')]
        pred_per_s = pred_per_s[0:3]
        return pred_co,pred_per,pred_per_s


    def read_output_sheet(self):
        file = open("AI External-Outputs/path_info.txt","r")
        for lines in file.read().splitlines():
            if lines[0] == "T":
                self.filepath = lines[1:]
        file.close() 
        self.total_df = pd.read_excel(self.filepath)

    def save_user_data_and_load_pred(self):
        self.dicte = {'Username' : self.username,
                            'Case num' : self.case_option[-4:],
                            'User_prediction_1' : self.pred_ch_1,
                            'User_prediction_2' : self.pred_ch_2,
                            'User_prediction_3' : self.pred_ch_3,
                            'User_recommendation_1' : self.recom_ch_1, 
                            'User_recommendation_2' : self.recom_ch_2,
                            'User_recommendation_3' : self.recom_ch_3,
                                'AI_prediction_1' : self.log_pred[int(self.case_option[-4:])]["Prediction 1 :"], 
                                'AI_prediction_2' : self.log_pred[int(self.case_option[-4:])]["Prediction 2 :"],
                                'AI_prediction_3' : self.log_pred[int(self.case_option[-4:])]["Prediction 3 :"],
                                'AI_recommendation_1' : self.log_pred[int(self.case_option[-4:])]["Recommendation 1 :"],
                                'AI_recommendation_2' : self.log_pred[int(self.case_option[-4:])]["Recommendation 2 :"],
                                'AI_recommendation_3' : self.log_pred[int(self.case_option[-4:])]["Recommendation 3 :"]}
        root = Tk()
        ico_path = curdir+"\media\my_icon.ico"
        root.iconbitmap(ico_path)
        root.geometry("850x850")
        root.title("VALIDATE RESPONSES")
        label = Label(root, text="VALIDATE AI PREDICTION & RESPONSES ", font="LARGE_FONT")
        label.pack(pady=10,padx=1)
        label_sub = Label(root, text="For "+self.case_option,font="Helvetica 18 bold")
        label_sub.pack()
        f = open('Value-json/code_value_map.json') 
        self.code_value_data = json.load(f)

        def get_value(val):

            val = val.split(',')
            print(val)        

            key = val[0]
            valt = str(val[1])
            valte = str(val[2])
            key_s = key[4:-2]
            value = valt[2:-2]
            if value[0]=='[':
                value = value[1:]
            valuet = valte[2:-2]
            if valuet[0]=='[':
                valuet = valuet[1:]
        
            
            if key_s[0]=='C':
                return str(self.code_value_data.get(key_s))+" with Relative Confidence  = "+value+"%"+" and with Standard Confidence  = "+valuet+"%"
            else:
                key_s = key[3:-2]
                return str(self.code_value_data.get(key_s))+" with Relative Confidence  = "+value+"%"+" and with Standard Confidence  = "+valuet+"%"

            


        label1 = Label(root, text =' AI prediction 1 is '+ get_value(str(self.log_pred[int(self.case_option[-4:])]["Prediction 1 :"])))
        label1.pack(pady=10,padx=10)

        var_1 = StringVar(master=root)
        var_1.set("Agree")

        R1 = ttk.Radiobutton(root, text = "Agree", variable = var_1, value = "Agree")
        R2 = ttk.Radiobutton(root, text = "Disagree", variable = var_1, value = "Disagree")
     
        label1.pack(anchor='w')
        R1.pack(anchor='w')
        R2.pack(anchor='w')

        label2 = Label(root, text ='AI prediction 2 is '+ get_value(str(self.log_pred[int(self.case_option[-4:])]["Prediction 2 :"])))
        label2.pack(pady=10,padx=10)

        var_2 = StringVar(master=root)
   
        var_2.set("Agree")
        R11 = ttk.Radiobutton(root, text = "Agree", variable = var_2, value = "Agree")
        R21 = ttk.Radiobutton(root, text = "Disagree", variable = var_2, value = "Disagree")

        label2.pack(anchor='w')
        R11.pack(anchor='w')
        R21.pack(anchor='w')

        label3 = Label(root, text =' AI prediction 3 is '+ get_value(str(self.log_pred[int(self.case_option[-4:])]["Prediction 3 :"])))
        label3.pack(pady=10,padx=10)
        var_3 = StringVar(master=root)
        var_3.set("Agree")

        R12 = ttk.Radiobutton(root, text = "Agree", variable = var_3, value = "Agree")
        R22 = ttk.Radiobutton(root, text = "Disagree", variable = var_3, value = "Disagree")




     
        label3.pack(anchor='w')
        R12.pack(anchor='w')
        R22.pack(anchor='w')

        label4 = Label(root, text =' AI recommendation 1 is ' + str(self.log_pred[int(self.case_option[-4:])]["Recommendation 1 :"]))
        label4.pack(pady=10,padx=10)


        var_4 = StringVar(master=root)
        var_4.set("Agree")

        R13 = ttk.Radiobutton(root, text = "Agree", variable = var_4, value = "Agree")
        R23 = ttk.Radiobutton(root, text = "Disagree", variable = var_4, value = "Disagree")

     
        label4.pack(anchor='w')
        R13.pack(anchor='w')
        R23.pack(anchor='w')

        label5 = Label(root, text =  ' AI recommendation 2 is ' + str(self.log_pred[int(self.case_option[-4:])]["Recommendation 2 :"]))
        label5.pack(pady=10,padx=10)


        var_5 = StringVar(master=root)
        var_5.set("Agree")

        R14 = ttk.Radiobutton(root, text = "Agree", variable = var_5, value = "Agree")
        R24 = ttk.Radiobutton(root, text = "Disagree", variable = var_5, value = "Disagree")

     
        label5.pack(anchor='w')
        R14.pack(anchor='w')
        R24.pack(anchor='w')

        label6 = Label(root, text = ' AI recommendation 3 is ' + str(self.log_pred[int(self.case_option[-4:])]["Recommendation 3 :"]))
        label6.pack(pady=10,padx=10) 


        var_6 = StringVar(master=root)
        var_6.set("Agree")

        R15 = ttk.Radiobutton(root, text = "Agree", variable = var_6, value = "Agree")
        R25 = ttk.Radiobutton(root, text = "Disagree", variable = var_6, value = "Disagree")

     
        label6.pack(anchor='w')
        R15.pack(anchor='w')
        R25.pack(anchor='w')
        def navigation_bar():
            root.destroy()
        def get_submit_and_save():
            var1 = var_1.get()
            var2 = var_2.get()
            var3 = var_3.get()
            var4 = var_4.get()
            var5 = var_5.get()
            var6 = var_6.get()

            self.dicte['AI_prediction_1'] = [self.log_pred[int(self.case_option[-4:])]["Prediction 1 :"],var1] 
            self.dicte['AI_prediction_2'] = [self.log_pred[int(self.case_option[-4:])]["Prediction 2 :"],var2]
            self.dicte['AI_prediction_3'] = [self.log_pred[int(self.case_option[-4:])]["Prediction 3 :"],var3]
            self.dicte['AI_recommendation_1'] = [self.log_pred[int(self.case_option[-4:])]["Recommendation 1 :"],var4]
            self.dicte['AI_recommendation_2'] = [self.log_pred[int(self.case_option[-4:])]["Recommendation 2 :"],var5]
            self.dicte['AI_recommendation_3'] = [self.log_pred[int(self.case_option[-4:])]["Recommendation 3 :"],var6]
            
            with open(r'AI External-Outputs/user_log_data_chunk.csv', 'a', newline='') as csvfile:
                fieldnames = ['Username','Case num', 'User_prediction_1','User_prediction_2','User_prediction_3','User_recommendation_1','User_recommendation_2','User_recommendation_3', 'AI_prediction_1','AI_prediction_2','AI_prediction_3','AI_recommendation_1','AI_recommendation_2','AI_recommendation_3']
                writer = csv.writer(csvfile)
                writer.writerow(fieldnames)
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

                writer.writerow(self.dicte)
            root.destroy()

        ResultsButton = Button(root, text = "Submit" , command=get_submit_and_save)
        ResultsButton.pack(padx=30,pady=10)
        
        button1 = ttk.Button(root, text="Back to Home",
                        command=navigation_bar)
        button1.pack()

        progressbar = ttk.Progressbar(root, orient= HORIZONTAL, length= 200)
        progressbar.pack()
        progressbar.config(mode = 'determinate', maximum = 15.0, value =  15.0)


   



        

    def display_user_options_window(self):
        global img
        root = Tk()
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        root.geometry("800x800+%d+%d" % (screen_width/2-275, screen_height/2-125))
        root.configure(background='white')
        #root.attributes('-topmost', True)
        #root.lift()
        #root.attributes("-fullscreen", True)  
        #root.configure(bg='white')
        ico_path = curdir+"\media\my_icon.ico"
        root.iconbitmap(ico_path)

     
        root.title("Predective AI")
        bg_path = curdir + "\media/ai.gif"
        lbl = ImageLabel(root)
        lbl.pack()
        lbl.load(bg_path)

      

        


        #label.grid(column=1, row=1, sticky=(W,E))
        
        
        def case_numb_call(obj):
            self.case_option = case_numb.get()
        def codechoosen_1_call(obj):
            self.pred_ch_1 = codechoosen_1.get()
        def codechoosen_2_call(obj):
            self.pred_ch_2 = codechoosen_2.get()
        def codechoosen_3_call(obj):
            self.pred_ch_3 = codechoosen_3.get()
        def recomchoosen_1_call(obj):
            self.recom_ch_1 = recomchoosen_1.get()
        def recomchoosen_2_call(obj):
            self.recom_ch_2 = recomchoosen_2.get()
        def recomchoosen_3_call(obj):
            self.recom_ch_3 = recomchoosen_3.get()





        ttk.Label(root, text = "Case Num:",  
        font = ("Times New Roman", 10)).pack() 
  
        n = StringVar() 
        case_numb = ttk.Combobox(root, width = 27,  
                                    textvariable = n) 
        case_numb.bind('<<ComboboxSelected>>',case_numb_call)
        
        # Adding combobox drop down list 
        case_numb['values'] = ["Case no. : "+str(i) for i in range(int(self.p_start_code),int(self.p_end_code))]
        
        case_numb.pack()
        case_numb.current(1)
        
        

        
        # Shows february as a default value 
    

        ttk.Label(root, text = "Prediction 1:",  
        font = ("Times New Roman", 10)).pack()
  
        n = StringVar() 
        codechoosen_1 = ttk.Combobox(root, width = 27,  
                                    textvariable = n) 
        

        code_dict = ["Code "+str(i) for i in range(1,39)]
        f = open('Value-json/code_value_map.json')
        code_json = json.load(f)
        code_value_map = [str(code_json[i]) for i in code_dict]
        
        
        recom_dict = ["Recommendation "+str(i) for i in range(1,31)]


        # Adding combobox drop down list 
        codechoosen_1.bind('<<ComboboxSelected>>',codechoosen_1_call)
        codechoosen_1['values'] = code_value_map
        
        
        codechoosen_1.pack()


        ttk.Label(root, text = "Prediction 2:",  
        font = ("Times New Roman", 10)).pack() 
  
        n = StringVar() 
        codechoosen_2 = ttk.Combobox(root, width = 27,  
                                    textvariable = n) 

        codechoosen_2.bind('<<ComboboxSelected>>',codechoosen_2_call)
        
        # Adding combobox drop down list 
        codechoosen_2['values'] = code_value_map
        
        codechoosen_2.pack()
        codechoosen_2.current(0)

        ttk.Label(root, text = "Prediction 3:",  
        font = ("Times New Roman", 10)).pack()
  
        n = StringVar() 
        codechoosen_3 = ttk.Combobox(root, width = 27,  
                                    textvariable = n) 
        
        # Adding combobox drop down list 
        codechoosen_3.bind('<<ComboboxSelected>>',codechoosen_3_call)
        codechoosen_3['values'] = code_value_map

        
        codechoosen_3.pack()
        
        # Shows february as a default value 
        codechoosen_3.current(0)  
        ttk.Label(root, text = "Recommendation 1:",  
        font = ("Times New Roman", 10)).pack()
  
        n = StringVar() 
        recomchoosen_1 = ttk.Combobox(root, width = 27,  
                                    textvariable = n) 

        recomchoosen_1.bind('<<ComboboxSelected>>',recomchoosen_1_call)
        
        recom_val = open("Input Sheets/recom_value_map_1.txt").read()
        recom_value = recom_val.splitlines()
        # Adding combobox drop down list 
        recomchoosen_1['values'] = recom_value 
        
        recomchoosen_1.pack()
        
        # Shows february as a default value 
        recomchoosen_1.current(0)  
        ttk.Label(root, text = "Recommendation 2:",  
        font = ("Times New Roman", 10)).pack()
  
        n = StringVar() 
        recomchoosen_2 = ttk.Combobox(root, width = 27,  
                                    textvariable = n) 
        recomchoosen_2.bind('<<ComboboxSelected>>',recomchoosen_2_call)
        # Adding combobox drop down list 
        recom_val = open("Input Sheets/recom_value_map_2.txt").read()
        recom_value = recom_val.splitlines()
        recomchoosen_2['values']  = recom_value
        recomchoosen_2.pack()
        
        # Shows february as a default value 
        recomchoosen_2.current(0)
        ttk.Label(root, text = "Recommendation 3:",  
        font = ("Times New Roman", 10)).pack()
  
        n = StringVar() 
        recomchoosen_3 = ttk.Combobox(root, width = 27,  
                                    textvariable = n) 
        
        recomchoosen_3.bind('<<ComboboxSelected>>',recomchoosen_3_call)
        
        # Adding combobox drop down list 
        recom_val = open("Input Sheets/recom_value_map_3.txt").read()
        recom_value = recom_val.splitlines()
        recomchoosen_3['values'] = recom_value
        
        recomchoosen_3.pack()
        
        # Shows february as a default value 
        recomchoosen_3.current(0)

        b = ttk.Button(root, text='See AI Predictions', style='Kim.TButton',command=self.save_user_data_and_load_pred)
        b.pack()



        """

        Checkbutton1 = IntVar()   
        Checkbutton2 = IntVar()   
        Checkbutton3 = IntVar() 
        
        Button1 = Checkbutton(root, text = "Tutorial",  
                            variable = Checkbutton1, 
                            onvalue = 1, 
                            offvalue = 0, 
                            height = 2, 
                            width = 10) 
        
        Button2 = Checkbutton(root, text = "Student", 
                            variable = Checkbutton2, 
                            onvalue = 1, 
                            offvalue = 0, 
                            height = 2, 
                            width = 10) 
        
        Button3 = Checkbutton(root, text = "Courses", 
                            variable = Checkbutton3, 
                            onvalue = 1, 
                            offvalue = 0, 
                            height = 2, 
                            width = 10)   

        Button1.pack()
        Button2.pack()
        Button3.pack()

        """


    def read_cases(self):
        
        self.log_user = {}
        self.log_pred = {}
        for case_num in range(self.p_start_code,self.p_end_code):
            log = {}
            log['case_num'] = case_num
            df_ops = self.total_df[[case_num]]
            df_ops = df_ops.fillna(0)
            df_process = self.total_df.fillna(method='ffill')
            df_attempt = df_ops.where(df_ops == 0, 1)
            df_attempt = (df_attempt.iloc[4:,:]).values
            df_attempt = df_attempt.flatten()
            recommendation,cum_score,score,mul = self.get_recommendation(df_attempt)
            self.save_recommendation_log(case_num,cum_score,score,mul)

            
            
            
            pred_codes,pred_per,pred_per_s = self.get_prediction(case_num)
            self.log_pred[case_num] = { "Prediction 1 :" : (pred_codes[0],pred_per[0],pred_per_s[0]),
                                   "Prediction 2 :"  : (pred_codes[1],pred_per[1],pred_per_s[1]),
                                   "Prediction 3 :" : (pred_codes[2],pred_per[2],pred_per_s[2]),
                                   "Recommendation 1 :" : recommendation[0],
                                   "Recommendation 2 :" : recommendation[1],
                                   "Recommendation 3 :" : recommendation[2]
                                   

            }

            
            features = df_process.iloc[4:,1].values
        
            
            age = df_ops.iloc[3].values
            age = age[0]
            log['age'] = age
            choices = df_ops.iloc[4:,:].values
            feature_choice_dict = {}
            for idx,val in enumerate(choices):
                if val==0:
                    pass
                else:
                    
                    feature_choice_dict[features[idx]] = json.dumps(val[0])
            #print(feature_choice_dict)
            log['Feature Mappings'] = feature_choice_dict
            self.log_user[case_num] = log
    

    def display_user_log(self,user_log):

        def json_tree(tree, parent, dictionary):

            #print(dictionary)
            for key in dictionary:
                uid = uuid.uuid4()
                if isinstance(dictionary[key], dict):
                    
                    tree.insert(parent, 'end', uid, text="Case no. : " + str(key))
                    json_tree(tree, uid, dictionary[key])
                elif isinstance(dictionary[key], list):
                    tree.insert(parent, 'end', uid, text=key + '[]')
                    json_tree(tree,
                            uid,
                            dict([(i, x) for i, x in enumerate(dictionary[key])]))
                else:
                    value = dictionary[key]
                    if value is None:
                        value = 'None'
                    if key=="case_num":
                        tree.insert(parent, 'end', uid, text="Case Unique ID", value=value)
                    else:
                        tree.insert(parent, 'end', uid, text=key, value=value)

        def show_data(data):
            # Setup the root UI
            
            root = Tk()
            
        


            ico_path = curdir+"\media\my_icon.ico"
            root.iconbitmap(ico_path)
 
            root.title("Predective AI")
            

            root.columnconfigure(0, weight=100)
            root.rowconfigure(0, weight=100)
            root.resizable(width=0, height=0)
            """
            main_frame = Frame(root, width=1000, height=1000, background="bisque")
            main_frame.pack(fill=BOTH, expand=2)
            my_canvas = Canvas(main_frame,width=1000, height=1000)
            my_canvas.pack(side=LEFT, fill=BOTH, expand=1)
            my_scrollbar = ttk.Scrollbar(main_frame, orient=VERTICAL, command=my_canvas.yview)
            my_scrollbar.pack(side=RIGHT, fill=Y)
            my_canvas.configure(yscrollcommand=my_scrollbar.set)
            my_canvas.bind('<Configure>', lambda e: my_canvas.configure(scrollregion= my_canvas.bbox("all")))
            second_frame = Frame(my_canvas, width=1000, height=1000, background="bisque")
            my_canvas.create_window((0,0),window =second_frame, anchor="nw")

           """


            # Setup the Frames
            tree_frame = ttk.Frame(root,width=1000, padding="1")
            tree_frame.grid(row=0, column=0, sticky=NSEW)
            tree_frame.pack()
            # Setup the Tree
            tree = ttk.Treeview(tree_frame, columns=('Values'), selectmode='browse')
            tree.column('Values', anchor='nw',width= 500, stretch=True)
            
           


            json_tree(tree, '', data)
            tree.pack(side='left',fill="both",expand=True)
            vsb = Scrollbar(root, orient="vertical", command=tree.yview)
            vsb.pack(side='right', fill='y')

            tree.configure(yscrollcommand=vsb.set)

            # Limit windows minimum dimensions
            root.update_idletasks()
            root.minsize(800, 600)
            root.geometry("800x700")
            #root.attributes("-fullscreen", True) 
            root.mainloop()


        show_data(user_log)

            


            


      

    def execute(self):
        self.df_glob = pd.DataFrame(data=["Case_num","CumScore","Score(AorB)"])

        self.read_output_sheet()
        self.read_cases()
        self.display_user_options_window()
        self.display_user_log(self.log_user)
        
        #self.display_user_log(self.log_pred)







            

    

    


    
        


   
def main_account_screen():
    if not os.path.exists('user_pass_database'):
        os.makedirs('user_pass_database')
    global main_screen
    main_screen = Tk()
    curdir = os.getcwd()

    bg_path = curdir+"\media\my_bg.png"
    #C = Canvas(main_screen, bg="blue", height=1024, width=1024)
    img = ImageTk.PhotoImage(Image.open(bg_path))
    ico_path = curdir+"\media\my_icon.ico"
    main_screen.iconbitmap(ico_path)
    main_screen.geometry("1024x1021")
    main_screen.title("Account Login")
    Label(image=img, width="1024", height="300").pack()
    Label(text="").pack()
    photo_login = PhotoImage(file = curdir+"\media\\login.png") 
    photo_register = PhotoImage(file = curdir+"\media\\register.png") 
    
    # Resizing image to fit on button 
    #photo_login = photo_login.subsample(5, 5)
    #photo_register = photo_register.subsample(5, 5)  
    
    # here, image option is used to 
    # set image on button 
    # compound option is used to align 
    # image on LEFT side of button 
    Button(text = '    Login', height="60", width="160",  image = photo_login, 
                        compound = LEFT, command = login).pack() 
    
    Label(text="").pack()
    Button(text = '    Register', height="60", width="160",  image = photo_register, 
                        compound = LEFT, command = register).pack() 
    #C.pack()
 
    main_screen.mainloop()

main_account_screen()


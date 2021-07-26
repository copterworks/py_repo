#------------------------------------------------------------------------
#Origin: uPy0011.py
#guide: C:\SrcCodes\Py\Py_sqlite\py_sqlite_begin_03.py
#chr(39) single quote
#
#put wrap properties
#https://stackoverflow.com/questions/32577726/python-3-tkinter-how-to-word-wrap-text-in-tkinter-text
#wrap ='NONE' wrap = WORD
#------------------------------------------------------------------------
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import tkinter.font as font
import random
import sqlite3
from datetime import date
import datetime
from tkinter import filedialog
import os
import glob

#------------------functions external of a class-------------------

def centerup_screen(mast, wid, hei):
    sw = mast.winfo_screenwidth()
    sh = mast.winfo_screenheight()
    xh = int((sw - wid)/2)
    yv = int((sh - hei)/2)
    return  ( wid, hei, xh, yv )

def clr_quotespace( str_item):    
    sub = pair_quote( str_item, '"' )
    strb = sub.replace(" ", "")              
    return strb
  
def clearComma( mvalue ) :
     return mvalue.replace(",", "")
        
def count_occurence( mStr, mchar ):      
    mStr =mStr.strip( )
    lnz = len(mStr)
    if mchar in mStr:
         cnt = 0
         mrk =mStr.find(mchar)
         while mrk != -1:              
                cnt = cnt + 1
                mStr = mStr[mStr.find(mchar)+1:]
                mrk =mStr.find(mchar)
    else:
         cnt =0
    return cnt
   
def file_is_text( mfile ):
    # determine before opening file if file is a text file
    in_file = open(mfile, "r")         
    try:       
        data = in_file.read(100)     
        text =str(data)
        if '\n' in text:
             res= True
        else:
             res = False          
    except:
            res = False        
    in_file.close()   
    return res 
           
def giveout_filename():                                          
        tim = datetime.datetime.now()
        dt = tim.strftime("%Y%m%d")
        et = tim.strftime( "%S%M")
        ck = random.randrange(65, 91)
        cl  = random.randrange(65, 91)
        return (  "F" + str(dt) +  str(et) +  chr(ck) +  chr(cl ) + ".txt" )
        
def format_cmd( cmd ):
        lst = cmd.split( " " )
        tcollec = ""
        for u in lst:
           if  u.strip()  !=  "":
              tcollec = tcollec +  u + " "
        tcollec =   tcollec.strip()
        return tcollec
    
def  gen_recp():
        nx =  hex( random.randint( 0x2710,0xFFFF))
        nu = hex( random.randint( 0x2710,0xFFFF))
        nw =hex( random.randint( 0x2710,0xFFFF))
        ny = hex( random.randint( 0x2710,0xFFFF))
        return (  (nx[2:]).upper() +  (nu[2:]).upper()  +  (nw[2:]).upper()   )

def lcSort( lottofmt ):
      larr =   lottofmt.split("-")
      larr.sort()
      nlst = ""
      for u in range(len(larr)):
            nlst =  nlst + larr[u] +  "-"
      nlst =  nlst[:-1]
      return  nlst

def pair_quote( mStr, mchar ):                     
      cq = count_occurence( mStr, mchar )
      lnz = len(mStr)  
      res = ""   
      if cq == 2:
            fq = mStr.find(mchar) + 1   
            collecx = mStr[ fq:]                     
            cx =collecx.find(mchar)
            collec= collecx[ cx:]
            res = collecx.replace(collec, "")
      return res

def  record_id():
        ch = random.randrange(65, 91)
        dg =  str(random.randrange(1, 1000)).zfill(3)
        dh =  str(random.randrange(1, 1000)).zfill(3)
        ck = random.randrange(65, 91)
        dk = str(random.randrange(1, 100)).zfill(2)
        return (  chr(ch) + dg.strip() + dh.strip() + "-" + chr(ck) +  str(int( dg) * int( dh)).zfill(6)+ dk.strip() )
        
def toSqliteDateformat( mdat ):             #mdat = "mm/dd/yyyy" to yyyy-mm-dd
     la = mdat.split("/")
     yr = la[2]
     mo = la[0].zfill(2)
     da = la[1].zfill(2)
     return yr + "-" + mo + "-" + da

def strType(xstr):
    try:
        int(xstr)
        return 'int'
    except:
        try:
            float(xstr)
            return 'float'
        except:
            try:
               complex(xstr)
               return 'complex'
            except:
               return 'str'


                   
def getLst_Topics( ):                                   # returns a list
    dat= open(  "G:/SrcCodes/exe/xguides.txt", "r").read( )     
    g_arr = dat.split("\n")
    lstcmb = [  ]
    for ix in range(0,len(g_arr)):
        arr= g_arr[ix].split("#")
        if arr[0].strip() != "":
            lstcmb.append(arr[0])                       
    return lstcmb
        
def getgroupTbl( selected_topic ):
    dat= open(  "G:/SrcCodes/exe/xguides.txt", "r").read( )     
    g_arr = dat.split("\n")
    res = ""
    for ix in range(0,len(g_arr)):
        if  selected_topic in g_arr[ix]:
            tmp = g_arr[ix]
            arr = tmp.split("#")
            res = arr[1]
            break
    return res   
           
def getmemo_result( ptbl, notestag ):            
    conn = sqlite3.connect( "C:/Data/Au3db/GUIDE_db.db" )            
    cursor = conn.cursor()             
    cursor.execute("SELECT NOTES_TAG, GUIDE_NOTES, RECTAG, ORD_NO  FROM "  +  ptbl +   " WHERE NOTES_TAG = '" +  notestag + "'  ")         
    res = cursor.fetchone() 
    conn.close   
    return res
    
def getlast_order(  ptbl ):
    conn = sqlite3.connect( "C:/Data/Au3db/GUIDE_db.db" )            
    cursor = conn.cursor()             
    cursor.execute("SELECT NOTES_TAG, GUIDE_NOTES, RECTAG, ORD_NO  FROM "  +  ptbl +   " ORDER BY ORD_NO DESC  ")         
    res = cursor.fetchone() 
    conn.close   
    last = int( res[3])
    return last
       
                 
class WinApp(Frame):

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master
        self.def_Dir = ""
        self.init_window()
        self.functions_binding_key()
        self.functions_configurations()

    def init_window(self):
        self.master.title("Memo Store")
        self.pack(fill=BOTH, expand=1)
        self.def_Dir = (os.getcwd()).replace(chr(92), chr(47))  
        
        self.filechoic  =   ttk.Combobox( self,  width=54,   values=[    ],      state="disabled")              # readonly",normal, disabled
        self.filechoic.place(x= 27, y=1)
 
        self.filedtls  =   ttk.Combobox( self,  width=54,   values=[    ],      state="disabled")                 
        self.filedtls.place(x= 27, y=26)
                
        self.recId  =  Label(self, text="",  fg ='#BDBDF3',  anchor=W)
        self.recId.place(x=960, y=26)
        
        self.filechoic.bind("<<ComboboxSelected>>", self.cmbselect)
        
        self.filedtls.bind("<<ComboboxSelected>>", self.cmbshowselect)
              
        self.ent  =  Label(self, text="Entry:", anchor=W)
        self.ent.place(x=25, y=670)

        self.param  =  Entry(self, text="" , width =80)
        self.param.place(x=68, y=670)
        
        self.param.bind("<Return>",  self.interpret_cmd)
        
        self.ordNo  =  Entry(self, text="" , fg ='#BDBDF3',   justify='center', width =6)
        self.ordNo.place(x=554, y=670)

        myfont = font.Font(family='Times', size=9, weight='bold', slant='roman', underline = 0 )
        self.statusbar = Label(self, text="ready...", bd=1, font=myfont,  fg='red', relief=SUNKEN, anchor=W)
        self.statusbar.pack(side=BOTTOM, fill=X)

        self.aButton = Button(self, text="Update", bg='antiquewhite', fg ='black', command = self.updateSave  )
        self.aButton.place(x=20, y=700, width =70)

        self.bButton = Button(self, text="New Save", bg='antiquewhite', command = self.newentrysave )
        self.bButton.place(x=100, y=700, width =70)
  
        self.cButton = Button(self, text="Renumber", bg='antiquewhite',  command = self.renumberOrder)
        self.cButton.place(x=180, y=700, width =70)
        
        self.jButton = Button(self, text="Quit", bg='antiquewhite'  , command = self.client_exit)
        self.jButton.place(x=920, y=700, width =70)

        self.addedWidgets()
        #self.text.bind("<Return>",  self.response_cmd)

    def addedWidgets(self):
        self.fram = Frame( )
        self.scrollbarv = Scrollbar(self.fram, orient=VERTICAL)
        self.scrollbarh = Scrollbar(self.fram, orient=HORIZONTAL)
        self.scrollbarv.pack(side="right", fill="y")
        self.scrollbarh.pack(side="bottom", fill="x")
        self.text =Text(self.fram,  height = 37, width=126, bg='#EAEBE2', wrap = "none",  xscrollcommand=self.scrollbarh.set, yscrollcommand=self.scrollbarv.set)
        self.scrollbarh.config(command=self.text.xview)
        self.scrollbarv.config(command=self.text.yview)
        self.text.pack(side="top", fill="x")
        self.fram.place(x=30, y=55)
        
    def functions_configurations(self):                         
        self.menu = Menu(self.text.master, tearoff = 0)
        self.menu.add_command(label="Open Topics", command = self.opentopics )    
        self.menu.add_separator( )    
        self.menu.add_command(label="Wrap text", command = self.wrapSet  )   
        self.menu.add_separator( )    
        self.menu.add_command(label="Clear Display", command = self.clearEntry  )        
        self.menu.add_command(label="Delete Entry",  command = self.deleteentry )     
    
    def show_menu_(self, event):             
        self.menu.post( event.x_root, event.y_root )        
          
    def functions_binding_key(self):
        self.text.bind("<Button-3>",self.show_menu_)
          
    def  opentopics(self):
        self.statusbar['text'] = " ready..."       
        lstcmb = getLst_Topics( )              
        self.filechoic["state"] = "normal"
        self.filechoic["values"] = lstcmb
        self.filechoic["state"] = "readonly"                                                                                 
        self.param.delete(0, END)  
        self.param.focus()         
          
    def cmbselect(self, event):
        self.statusbar['text'] = " ready..."
        self.text.delete('1.0', END)                   
        self.param.delete(0, END)  
        grp = self.filechoic.get( )           
        tbl = getgroupTbl( grp )          
        conn = sqlite3.connect( "C:/Data/Au3db/GUIDE_db.db" )            
        cursor = conn.cursor()
        cursor.execute("SELECT NOTES_TAG, RECTAG FROM "  +  tbl +   " ORDER BY ORD_NO DESC" )           # list of  Tables on open database
        ntags = cursor.fetchall()    
        if ntags != None: 
            nwl = [ ]
            for ix in range(0,len(ntags)):
                nwl.append( ntags[ix][0])          
            self.filedtls["state"] = "normal"
            self.filedtls["values"] = nwl
            self.filedtls["state"] = "readonly"
            if len(nwl) > 0:
                self.filedtls.current(0)
                grp = self.filechoic.get( )           
                tbl = getgroupTbl( grp )     
                grpi = self.filedtls.get()       
                res =getmemo_result( tbl, grpi )               
                if res != None:     
                    dat =res[1]
                    dat = dat.replace(chr(96), chr(39))         
                    self.recId["text"]= res[2]                                 
                    self.text.insert( END,  dat )  
                    self.ordNo.delete(0, END)
                    self.ordNo.insert(END, res[3])
                    
         
    def cmbshowselect(self, event):
        self.text.delete('1.0', END)                            
        self.param.delete(0, END)  
        grp = self.filechoic.get( )           
        tbl = getgroupTbl( grp )     
        grpi = self.filedtls.get()       
        res =getmemo_result( tbl, grpi )               
        if res != None:                  
            dat =res[1]
            self.recId["text"] = res[2]     
            dat = dat.replace(chr(96), chr(39))          
            self.text.insert( END,  dat )  
            self.ordNo.delete(0, END)
            self.ordNo.insert(END, res[3])
            
    def deleteentry(self):
            if self.recId["text"] != "":
                grp = self.filechoic.get( )           
                tbl = getgroupTbl( grp )     
                grpi = self.filedtls.get()   
                rectg =  self.recId["text"]               
                ask = messagebox.askquestion("Confirm","Are you sure to proceed deletion ?")             
                if  ask == 'yes':           
                    conn = sqlite3.connect( "C:/Data/Au3db/GUIDE_db.db" )            
                    cursor = conn.cursor()
                    cursor.execute( "DELETE FROM "  +  tbl  +  "    WHERE  RECTAG = '"   + rectg   +   "'   "       )          
                    conn.commit()
                    conn.close()
                    self.statusbar['text'] = " one record deleted..."
                 
    def updateSave(self):                     
            if self.recId["text"] != "":
                ordn = self.ordNo.get( )  
                grp = self.filechoic.get( )           
                tbl = getgroupTbl( grp )     
                grpi = self.filedtls.get()                       
                dat = self.text.get('0.0', END)
                ask = messagebox.askquestion("Confirm","Are you sure want to update this entry ?")             
                if  ask == 'yes':  
                    conn = sqlite3.connect( "C:/Data/Au3db/GUIDE_db.db" )            
                    cursor = conn.cursor()
                    dat = dat.replace(chr(39), chr(96))
                    cursor.execute( "UPDATE  "  +  tbl  +  " SET  GUIDE_NOTES =   '"  +   dat  + "', ORD_NO = " + ordn + "   WHERE  NOTES_TAG = '"   + grpi   +   "'   "       )          
                    conn.commit()
                    conn.close()
                    self.statusbar['text'] = " record updated..." 
            else:
                messagebox.showerror('Error Message',  "you can not update a new entry."   )    
            
    def clearEntry( self ):        
        self.recId["text"] =""  
        self.text.delete('1.0', END)    
        self.param.delete(0, END)
        self.ordNo.delete(0, END)        
        self.filedtls["values"] = [ " " ]
        self.filedtls.current(0)
        self.statusbar['text'] = " you may now enter entries for a new one."
        
    def wrapSet( self ):        
        if   self.text["wrap"] ==  "none":    
            self.text.config(wrap = WORD)   
            self.statusbar['text'] = " wrap is on. "    
        else:
            self.text.config(wrap = "none")              
            self.statusbar['text'] = "  ready..."     
          
    def newentrysave(self):      
        if self.recId["text"]  == "":            
            slst = [  ]                                         #list storage
            grp = self.filechoic.get( )                          
            tbl = getgroupTbl( grp )                            # table  to work on
            ordn = getlast_order(  tbl ) + 5                    # ORD_NO
            rect = gen_recp()                                   # RECTAG
            notetag = self.param.get()                   #NOTES_TAG
            if notetag == "":
                messagebox.showerror('Error Message',  "you have not entered subject title."   )    
                return 0
            else:
                if  chr(39) in  notetag:
                    messagebox.showerror('Error Message',  "you are not allowed to use ' on entry of entered subject title."   )    
                    return 0
            #notetag = notetag.replace(chr(39), chr(96)) 
            dat = self.text.get('0.0', END)        
            dat = dat.replace(chr(39), chr(96))    # GUIDE_NOTES
            slst.append(ordn)
            slst.append(notetag)
            slst.append(dat)
            slst.append(rect)
            ask = messagebox.askquestion("Confirm","Are you sure to save as new entry ?")             
            if  ask == 'yes':       
                conn = sqlite3.connect( "C:/Data/Au3db/GUIDE_db.db" )            
                cursor = conn.cursor()      
                cursor.execute( "INSERT INTO " + tbl + "( ORD_NO, NOTES_TAG, GUIDE_NOTES, RECTAG) VALUES( ?, ?, ?, ?  )",     slst )
                conn.commit()
                conn.close 
                self.statusbar['text'] = "a new entry saved..."
        else:       
            messagebox.showerror('Error Message',  "you are not allowed to save an existing record."   )
             
    def renumberOrder(self):
        if self.recId["text"] != "":
            grp = self.filechoic.get( )                          
            tbl = getgroupTbl( grp )        
            conn = sqlite3.connect( "C:/Data/Au3db/GUIDE_db.db" )            
            cursor = conn.cursor()      
            cursor.execute( "SELECT ORD_NO, NOTES_TAG, RECTAG FROM " + tbl + "  ORDER BY  ORD_NO " )
            rectg = cursor.fetchall()                        
            nwl = [  ]                            
            for u in range(0,len(rectg)):
                nwl.append( rectg[u][2])             # collect all rectag
            conn.close 
            ask = messagebox.askquestion("Confirm","Are you sure to renumber order of all entries ?")             
            if  ask == 'yes':   
                conn = sqlite3.connect( "C:/Data/Au3db/GUIDE_db.db" )            
                cursor = conn.cursor()      
                ordnum = 1
                for ux in range(0,len(nwl)):                
                    cursor.execute( "UPDATE " + tbl + " SET  ORD_NO = " + str(ordnum)   +  " WHERE RECTAG = '" +  nwl[ux]  + "'   " )                                  
                    conn.commit()
                    ordnum = ordnum + 4  
                conn.close 
                self.statusbar['text'] = "renumber of all order done."
                  
    def interpret_cmd(self, event):
        cmd =   (self.param.get()).strip()
        cmd = format_cmd( cmd ).lower()   
             
        if  "save to " in cmd:                      # retain this 
             nt = len(cmd)
             fln = cmd[8:nt]             
             filep =clr_quotespace( fln )
             data =  self.text.get("1.0", END)
             arr = data.split("\n")                                                   
             f_= open(  filep, "w")
             for u in range(0,len(arr)):
                 f_.write(arr[u] )
             f_.close()
             self.param.delete(0, END)

        if  "load from " in cmd:                       # retain this 
             nt = len(cmd)
             filn = cmd[10:nt]
             filep =clr_quotespace( filn )
             try:
                  dat= open(  filep, "r").read( )
                  self.text.delete('1.0', END)
                  self.text.insert(END,  dat )
                  self.param.delete(0, END)
             except:
                  err = "Unexpected error:", sys.exc_info()[0]
                  self.statusbar['text'] = err
         
        if "list of files" in cmd:             
             self.text.delete('1.0', END)
             flst = glob.glob('*.*')
             for filep in flst:
                   self.text.insert(END,   filep + "\n"  )
             self.statusbar['text'] = "list of files in current directory."            
             self.text.focus()             
                     
        if "current dir"  in cmd:                  
             if len(cmd) == 11:          
                self.text.delete(1.0, END)     
                self.text.insert(END,  (os.getcwd()).replace(chr(92), chr(47))   )
                
        if "change dir"  in cmd:                  
             if len(cmd) == 10:                   
                nwdir = filedialog.askdirectory()
                try:
                    os.chdir( nwdir )  
                    self.datab["text"] = ""                  
                    self.text.delete(1.0, END)     
                    self.text.insert(END, "new directory: " +  nwdir)
                except:    
                    messagebox.showerror( "Error" , "current directory not changed.")
                
        if "default dir"  in cmd:                  
             if len(cmd) == 11:                                   
                os.chdir( self.def_Dir  )  
                self.datab["text"] = ""             
                self.text.delete(1.0, END)     
                self.text.insert(END, "back to default directory. ")
         
    def client_exit(self):
        messagebox.showinfo('Bye', 'Program exits')
        self.quit()                  

def main( ):
    root = Tk()
    scd = centerup_screen(root, 1080, 750)
    root.geometry('%dx%d+%d+%d' % (scd))
    root.iconbitmap("icons06.ico")
    root.resizable(width=FALSE, height=FALSE)
    #create an interactive file session
    App = WinApp(root)
    root.mainloop()

if __name__=="__main__": 
    main() 


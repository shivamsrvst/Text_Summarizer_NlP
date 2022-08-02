import time
import tkinter as tk
import tkinter.filedialog
from tkinter import *
from tkinter import ttk
from tkinter.scrolledtext import *

timestr = time.strftime("%d %m %Y-%H%M%S")

#NLP
from spacymodel import text_summarizer

#web scrapping
from bs4 import BeautifulSoup
from urllib.request import urlopen

window=Tk()
window.title("Summary Generator")
window.geometry('700x500')




#style
style=ttk.Style(window)
style.configure('lefttab.TNotebook',tabposition='wn')

#tabs
tab_control=ttk.Notebook(window,style='lefttab.TNotebook')

tab1=ttk.Frame(tab_control)
tab2=ttk.Frame(tab_control)
tab3=ttk.Frame(tab_control)



#add tabs to notebook
tab_control.add(tab1, text=f'{"Home":^20s}')
tab_control.add(tab2, text=f'{"File":^20s}')
tab_control.add(tab3, text=f'{"URL":^20s}')

#labels
label1 = Label(tab1, text= 'Summarizer',padx=5, pady=5)
label1.grid(column=0, row=0)
 
label2 = Label(tab2, text= 'File Processing',padx=5, pady=5)
label2.grid(column=0, row=0)

label3 = Label(tab3, text= 'URL',padx=5, pady=5)
label3.grid(column=0, row=0)

tab_control.pack(expand=1,fill='both')


#Functions
def get_summary():
    raw_text = str(entry.get('1.0',tk.END))
    final_text = text_summarizer(raw_text)
    print(final_text)
    result = '\nSummary:  {}'.format(final_text)
    tab1_display.insert(tk.END,result)

def save_summary():
    raw_text=entry.get('1.0',tk.END)
    final_text=text_summarizer(raw_text)
    file_name= 'Generated_summary'+timestr+'.txt'
    with open(file_name,'w') as f:
        f.write(final_text)
    

# Clearing the data
def clear_text():
    entry.delete('1.0',END)

def clear_display_result():
    tab1_display.delete('1.0',END)

def clear_text_file():
        displayed_file.delete('1.0',END)

def clear_text_result():
        tab2_display_text.delete('1.0',END)

def clear_url_entry():
        url_entry.delete(0,END)

def clear_url_display():
    tab3_display_text.delete('1.0',END)



#file tab
def openfiles():
    file1 = tkinter.filedialog.askopenfilename(filetypes=(("Text Files",".txt"),("All files","*")))
    read_text = open(file1,encoding="utf-8").read()
    displayed_file.insert(tk.END,read_text)

def get_file_summary():
    raw_text = displayed_file.get('1.0',tk.END)
    final_text = text_summarizer(raw_text)
    result = '\nSummary:{}'.format(final_text)
    tab2_display_text.insert(tk.END,result)

#URL tab
def get_text():
    raw_text = str(url_entry.get())
    page = urlopen(raw_text)
    soup = BeautifulSoup(page)
    fetched_text = ' '.join(map(lambda p:p.text,soup.find_all('p')))
    url_display.insert(tk.END,fetched_text)

def get_url_summary():
    raw_text = url_display.get('1.0',tk.END)
    final_text = text_summarizer(raw_text)
    result = '\nSummary:{}'.format(final_text)
    tab3_display_text.insert(tk.END,result)

#Main Home Tab
l1 = Label(tab1, text='Enter text to Summarize',padx=5, pady=5)
l1.grid(column=0, row=1)
entry=ScrolledText(tab1,height=10)
entry.grid(row=2,column=0,columnspan=2,padx=5,pady=5)

#buttons
button1=Button(tab1,text="Reset",command=clear_text, width=12,bg='#25add3',fg='#fff')
button1.grid(row=4,column=0,padx=10,pady=10)

button2=Button(tab1,text="Summarize",command=get_summary, width=12,bg='#d325cd',fg='#fff')
button2.grid(row=4,column=1,padx=10,pady=10)

button3=Button(tab1,text="Clear Result", command=clear_display_result,width=12,bg='#7B49F4',fg='#fff')
button3.grid(row=5,column=0,padx=10,pady=10)

button4=Button(tab1,text="Save",command=save_summary, width=12,bg='#AA4A44',fg='#fff')
button4.grid(row=5,column=1,padx=10,pady=10)


#display screen
tab1_display = ScrolledText(tab1,height=10)
tab1_display.grid(row=7,column=0, columnspan=3,padx=5,pady=5)


#File Processing Tab
l1=Label(tab2,text="Open File To Summarize")
l1.grid(row=1,column=1)

displayed_file = ScrolledText(tab2,height=7)# Initial was Text(tab2)
displayed_file.grid(row=2,column=0, columnspan=3,padx=5,pady=3)

# BUTTONS FOR SECOND TAB/FILE READING TAB
b0=Button(tab2,text="Open File", width=12,command=openfiles,bg='#c5cae9')
b0.grid(row=3,column=0,padx=10,pady=10)

b1=Button(tab2,text="Reset ", width=12,command=clear_text_file,bg="#25D366")
b1.grid(row=3,column=1,padx=10,pady=10)

b2=Button(tab2,text="Summarize", width=12,command=get_file_summary,bg='#03A7D4',fg='#fff')
b2.grid(row=3,column=2,padx=10,pady=10)

b3=Button(tab2,text="Clear Result", width=12,command=clear_text_result,bg='#7B49F4',fg='#fff')
b3.grid(row=5,column=1,padx=10,pady=10)

b4=Button(tab2,text="Close", width=12,command=window.destroy,bg='#AA4A44',fg='#fff')
b4.grid(row=5,column=2,padx=10,pady=10)

# Display Screen
# tab2_display_text = Text(tab2)
tab2_display_text = ScrolledText(tab2,height=10)
tab2_display_text.grid(row=7,column=0, columnspan=3,padx=5,pady=5)


#URL
l1=Label(tab3,text="Enter URL To Summarize")
l1.grid(row=1,column=0)

raw_entry=StringVar()
url_entry=Entry(tab3,textvariable=raw_entry,width=50)
url_entry.grid(row=1,column=1)

# BUTTONS
button1=Button(tab3,text="Reset",command=clear_url_entry, width=12,bg='#25D366',fg='#fff')
button1.grid(row=4,column=0,padx=10,pady=10)

button2=Button(tab3,text="Get Text",command=get_text, width=12,bg='#AA4A44',fg='#fff')
button2.grid(row=4,column=1,padx=10,pady=10)

button3=Button(tab3,text="Clear Result", command=clear_url_display,width=12,bg='#7B49F4',fg='#fff')
button3.grid(row=5,column=0,padx=10,pady=10)

button4=Button(tab3,text="Summarize",command=get_url_summary, width=12,bg='#03A7D4',fg='#fff')
button4.grid(row=5,column=1,padx=10,pady=10)

# Display Screen For Result
url_display = ScrolledText(tab3,height=10)
url_display.grid(row=7,column=0, columnspan=3,padx=5,pady=5)


tab3_display_text = ScrolledText(tab3,height=10)
tab3_display_text.grid(row=10,column=0, columnspan=3,padx=5,pady=5)


# Allows you to edit
tab2_display_text.config(state=NORMAL)






window.mainloop()
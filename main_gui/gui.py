from Tkinter import *
import Tkinter as tk
import sys
import os
from analyzefun import analyze

class StorageApp(tk.Tk):
                
    def __init__(self):
        tk.Tk.__init__(self)
        frame = Frame(self, width=10, height=50)
        frame.pack(side=LEFT)

        rframe = Frame(self, width=10, height=50)
        rframe.pack(side = RIGHT)
        
        self.title('Energy Storage Application')
        self.label = Label(frame, text="PG&E Territories")
        self.label.pack(pady=10)
        
        terr = PhotoImage(file= os.getcwd()+'/baseterr.gif')
        self.label = Label(frame, image=terr)
        self.label.image = terr # keep a reference!! or else it will not show up
        self.label.pack(padx=15,pady=10)
           
        self.label = Label(rframe, text="Select PG&E Territory:")
        self.label.pack(pady=10)
        OPTIONS = ["R","S","T","W","X"]
        global tty
        tty = StringVar(self) #territory
        tty.set('-') # default value
        self.label = apply(OptionMenu, (rframe, tty) + tuple(OPTIONS))
        self.label.pack(padx=15)
                
        #life is slider 1
        global ltime
        ltime = IntVar()
        self.s1 = Scale(rframe,from_=0, to=15, label ='Powerwall Lifetime:',
                        length=200, orient=HORIZONTAL, variable=ltime)
        self.s1.pack(padx=15,pady=10)
        
        #discount rate is slider 2
        global drate
        drate = DoubleVar()
        self.s2 = Scale(rframe,from_=0, to=20, label ='Project Discount Rate (%):',
                        length=200, orient=HORIZONTAL, variable=drate)
        self.s2.pack(padx=15,pady=10)
        
        #price escalation is slider 3
        global utilp
        utilp = DoubleVar()
        self.s3 = Scale(rframe,from_=0, to=5, label ='PG&E Price Escalation (%/yr):',
                        length=200, orient=HORIZONTAL, variable=utilp)
        self.s3.pack(padx=15,pady=10)

        
        self.sel_button = Button(rframe, text='Show NPV', command=self.calc_npv)
        self.sel_button.pack(pady=10)
        self.text = Text(rframe,width=30, height=10,bg="#eee")
        self.text.pack(padx=15,expand=1,fill=BOTH)

        sys.stdout = TextRedirector(self.text,"stdout")
        
        self.clear_button = Button(rframe, text="Clear", command=self.clear_text)
        self.clear_button.pack(padx=15,pady=5)
        
        self.close_button = Button(rframe, text="Close", command=self.quit)
        self.close_button.pack(padx=15,pady=5)

    def calc_npv(self):
        npv = analyze(tty.get(),ltime.get(),drate.get()/100.0,(utilp.get()/100)+1)
        print 'NPV: $%d' % (npv[0])
        
    def clear_text(self):
        self.text.delete('1.0', END)

class TextRedirector(object):
    def __init__(self,widget,tag="stdout"):
        self.widget = widget
        self.tag = tag
    def write(self, str):
        self.widget.configure(state="normal")
        self.widget.insert("end", str, (self.tag,))

my_gui = StorageApp()
my_gui.mainloop()
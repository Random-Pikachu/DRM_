from encryptor import encryptPDF
import customtkinter as ctk
from customtkinter import filedialog
from datetime import datetime
from tkinter import messagebox


class dateView(ctk.CTkFrame):
    def __init__(self, master, target_var):
        super().__init__(master, fg_color='transparent')
        self.target_var = target_var


        #variables
        self.year = ctk.StringVar()
        self.month = ctk.StringVar()
        self.date = ctk.StringVar()
        self.hour = ctk.StringVar()
        self.minute = ctk.StringVar()
        self.second = ctk.StringVar()

        #dropdown for each variable 
        year_ = ctk.CTkOptionMenu(self, variable=self.year, values=[str(y) for y  in range(2020, 2035)], dropdown_font=('Poppins', 16), width=80)
        month_ = ctk.CTkOptionMenu(self, variable=self.month, values=[f"{m:02}" for m  in range(1, 13)], dropdown_font=('Poppins', 16), width=60)
        date_ = ctk.CTkOptionMenu(self, variable=self.date, values=[f"{d:02}" for d  in range(1, 32)], dropdown_font=('Poppins', 16), width=60)
        hour_ = ctk.CTkOptionMenu(self, variable=self.hour, values=[f"{h:02}" for h in range(0, 24)], dropdown_font=('Poppins', 16), width=60)
        minute_ = ctk.CTkOptionMenu(self, variable=self.minute, values=[f"{m:02}" for m  in range(0, 60)], dropdown_font=('Poppins', 16), width=60)
        second_ = ctk.CTkOptionMenu(self, variable=self.second, values=[f"{s:02}" for s  in range(0, 60)], dropdown_font=('Poppins', 16), width=60)


        year_.grid(row=0, column=0, padx=2)
        month_.grid(row=0, column=1, padx=2)
        date_.grid(row=0, column=2, padx=2)
        hour_.grid(row=0, column=3, padx=(10, 2))
        minute_.grid(row=0, column=4, padx=2)
        second_.grid(row=0, column=5, padx=2)

        set_btn = ctk.CTkButton(self, text='Select', font=('Poppins', 17),fg_color="#2b6cb0", command=self.setDateTime)
        set_btn.grid(row=0, column=6, padx=2)

    def setDateTime(self):
        dt = f'{self.year.get()}-{self.month.get()}-{self.date.get()} {self.hour.get()}:{self.minute.get()}:{self.second.get()}'
        
        self.target_var.set(dt)


class senderView(ctk.CTkFrame):  
    def __init__(self, master = None): #constructor
        super().__init__(master, fg_color='transparent')
        self.pack(pady=15, fill='both', expand=True)
        
        # variables in encryptPdf = fileNameDir, email, startTime, endTime, outputPath
        self.fileNameDir = ctk.StringVar()
        self.email = ctk.StringVar()
        self.startTime = ctk.StringVar()
        self.endTime = ctk.StringVar()
        self.outputPath = ctk.StringVar()
        self.createForm()


    def createForm(self):
        # Creating UI for fileNameDir inp

        #Frame for directory inp 
        dirFrame = ctk.CTkFrame(self, fg_color="transparent")
        dirFrame.pack(pady=(0, 0))
        
        #Lable for frame1
        dirLabel = ctk.CTkLabel(dirFrame, text="PDF Path: ", font=('Poppins', 16), width=30, anchor='w')
        dirLabel.grid(row=0, column = 0, padx=(0,10), sticky='w')

        #entry for frame1
        dirEntry = ctk.CTkEntry(dirFrame, textvariable=self.fileNameDir, width=350, font=('Poppins', 16), placeholder_text='path')
        dirEntry.grid(row=0, column = 1, padx=(0, 10), sticky = 'ew')

        #browse button frame1
        dirBrowse = ctk.CTkButton(dirFrame, text='Browse File', font=('Poppins', 16),fg_color="#2b6cb0", command=lambda: self.selectDir(self.fileNameDir))
        dirBrowse.grid(row=0, column=2, padx=(0,10), sticky='e')

        dirFrame.grid_columnconfigure(1, weight=1)
        


        #frame for startTime inp 
        startFrame = ctk.CTkFrame(self, fg_color="transparent")
        startFrame.pack(pady=(5,5))
        
        #Lable for startTime
        startLabel = ctk.CTkLabel(startFrame, text="Start Time: ", font=('Poppins', 16), width=30, anchor='w')
        startLabel.grid(row=0, column = 0, padx=(0,10), sticky='w')

        

        #browse button startTime
        dateView(startFrame, target_var=self.startTime).grid(row=0, column=1, columnspan=2, sticky='w')

        #entry for startTime
        # startEntry = ctk.CTkEntry(startFrame, textvariable=self.startTime, width=200, font=('Poppins', 16), placeholder_text='yyyy-mm-dd hh:mm:ss', state='readonly')
        # startEntry.grid(row=1, column=1, columnspan=2, pady=(10, 0), sticky='w')

        startFrame.grid_columnconfigure(1, weight=1)


        #frame for end time
        endFrame = ctk.CTkFrame(self, fg_color="transparent")
        endFrame.pack(pady=(5,5))
        startLabel = ctk.CTkLabel(endFrame, text="Start Time: ", font=('Poppins', 16), width=30, anchor='w')
        startLabel.grid(row=0, column = 0, padx=(0,10), sticky='w')
        dateView(endFrame, target_var=self.endTime).grid(row=0, column=1, columnspan=2, sticky='w')
        endFrame.grid_columnconfigure(1, weight=1)

        #frame for email
        emailFrame = ctk.CTkFrame(self, fg_color='transparent')
        emailFrame.pack(pady=(5,5))
        emailLabel = ctk.CTkLabel(emailFrame, text="Email: ", font=('Poppins', 16), anchor='w', width=30)
        emailLabel.grid(row =0, column=0, padx=(0,10), sticky='w')
        emailEntry = ctk.CTkEntry(emailFrame, textvariable=self.email, width=350, font=('Poppins', 16))
        emailEntry.grid(row= 0, column =1, sticky='ew', padx=(0,10))
        emailEntry.grid_columnconfigure(1, weight=1)

        #frame for outputPath
        outputFrame = ctk.CTkFrame(self, fg_color='transparent')
        outputFrame.pack(pady=(5,5))
        outputLabel = ctk.CTkLabel(outputFrame, text='Output Path[Optional]: ', font=('Poppins', 16), width=30, anchor='w')
        outputLabel.grid(row = 0, column=0, padx=(0,10), sticky='w')
        outputEntry = ctk.CTkEntry(outputFrame, font=('Poppins', 16), width=350, textvariable=self.outputPath)
        outputEntry.grid(row=0, column = 1, padx=(0,10), sticky='ew')
        outputBrowse = ctk.CTkButton(outputFrame, command=lambda: self.selectDir(self.outputPath), text='Browse File', font=('Poppins', 16),fg_color="#2b6cb0")
        outputBrowse.grid(row = 0, column=2, padx=(0,10), sticky='e')

        outputFrame.grid_columnconfigure(1, weight=1)


        ctk.CTkButton(self, text='Encrypt File', command=self.handleEncrypt, font=('Poppins', 16),fg_color="#2b6cb0").pack(pady=40)


    def selectDir(self, target_var):
        if target_var==self.fileNameDir:
            dirPath = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
        
        elif target_var==self.outputPath:
            dirPath = filedialog.askdirectory()
        
        else:
            dirPath = None

        if dirPath: 
            target_var.set(dirPath)

    def handleEncrypt(self):
        try:
            if not all ([self.fileNameDir.get(), self.startTime.get(), self.endTime.get(), self.email.get()]):
                raise ValueError("Fill all the required fields")

            drm_path = encryptPDF(
                fileNameDir=self.fileNameDir.get(),
                startTime=self.startTime.get(),
                endTime=self.endTime.get(),
                email=self.email.get(),
                outputPath=self.outputPath.get()
            )

            messagebox.showinfo(message=f"Success, package created at: \n{drm_path}", title="Success")
        
        except Exception as e:
            messagebox.showerror("Error", str(e))
        

def run_gui():
    ctk.set_appearance_mode('light')
    ctk.set_default_color_theme('blue')
    app = ctk.CTk()
    app.geometry('800x600')

    senderView(master=app)
    app.mainloop()


if __name__ == '__main__':
    run_gui()
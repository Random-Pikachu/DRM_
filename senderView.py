# from encryptor import encryptPDF
import customtkinter as ctk
from customtkinter import filedialog
# ctk.set_appearance_mode('dark')
# ctk.set_default_color_theme('blue')
# default_font = ('Raleway', 18)

# app = ctk.CTk()
# app.geometry('500x600')
# app.title("Sender")

# label = ctk.CTkLabel(app, text="Hello!", font=default_font)
# label.pack(pady=40)

# name = ctk.CTkEntry(app, placeholder_text="Enter the name", font=default_font)
# name.pack()

# def onClick():
#     Name = name.get()
#     print(f"Name: {Name}")


# submit = ctk.CTkButton(app, corner_radius=9, text="Submit", font=('Raleway', 16),width=50, height=30, command=onClick)
# submit.pack(pady=10)


# app.mainloop()

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

        #Step 1: Create frame 
        rowFrame = ctk.CTkFrame(self, fg_color="transparent")
        rowFrame.pack(pady=50)
        
        #Lable for frame1
        dirLabel = ctk.CTkLabel(rowFrame, text="PDF Path: ", font=('Poppins', 18), width=30, anchor='w')
        dirLabel.grid(row=0, column = 0, padx=(0,10), sticky='w')

        #entry for frame1
        dirEntry = ctk.CTkEntry(rowFrame, textvariable=self.fileNameDir, width=350, font=('Poppins', 18), placeholder_text='path')
        dirEntry.grid(row=0, column = 1, padx=(0, 10), sticky = 'ew')

        #browse button frame1
        dirBrowse = ctk.CTkButton(rowFrame, text='Browse File', font=('Poppins', 17),fg_color="#2b6cb0", command=self.selectDir)
        dirBrowse.grid(row=0, column=2, padx=(0,10), sticky='e')

        rowFrame.grid_columnconfigure(1, weight=1)

    
    def selectDir(self):
        dirPath = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
        if dirPath: 
            self.fileNameDir.set(dirPath)

        

def run_gui():
    ctk.set_appearance_mode('light')
    ctk.set_default_color_theme('blue')
    app = ctk.CTk()
    app.geometry('800x600')

    senderView(master=app)
    app.mainloop()


if __name__ == '__main__':
    run_gui()
import customtkinter as ctk
import decryptor
from customtkinter import filedialog
from tkinter import messagebox
from customtkinter import CTkToplevel

class receiverView(ctk.CTkFrame):
    def __init__(self, master=None):
        super().__init__(master, fg_color='transparent')

        self.pack(pady=15, fill='both', expand = True)

        #variables in main
        self.drm_path = ctk.StringVar()
        self.createForm()

    
    def createForm(self):
        drm_dirFrame = ctk.CTkFrame(self, fg_color='transparent')
        drm_dirFrame.pack(pady=(50,0))
        drm_dirLabel = ctk.CTkLabel(drm_dirFrame, text=".drm Path", font=('Poppins', 16), width = 30, anchor ='w')
        drm_dirLabel.grid(row = 0, column = 0, sticky='w', padx=(0,10))
        drm_dirEntry = ctk.CTkEntry(drm_dirFrame, font=('Poppins', 16), width=350, textvariable=self.drm_path)
        drm_dirEntry.grid(row = 0, column = 1, sticky='ew', padx=(0,10))
        drm_dirBrowse = ctk.CTkButton(drm_dirFrame,text="Browse", font=('Poppins', 16),fg_color="#2b6cb0", command=self.selectFile)
        drm_dirBrowse.grid(row =0, column=2, sticky='e', padx=(0,10))
        drm_dirFrame.grid_columnconfigure(1, weight=1)


        decryptBtn = ctk.CTkButton(self,text="Decrypt", font=('Poppins', 16),fg_color="#2b6cb0", command=self.decryptDRMFile)
        decryptBtn.pack(pady=25)


    def selectFile(self):
        dir_path = filedialog.askopenfilename(filetypes=[('DRM Files', '*.drm')])

        if dir_path:
            self.drm_path.set(dir_path)

    def askPasswordDialog(self):
        emailDialog = ctk.CTkInputDialog(text="Enter the email: ", title='Test', font=('Poppins', 13))
        return emailDialog.get_input()
        

    def decryptDRMFile(self):
        try:
            if not self.drm_path.get():
                raise ValueError("Please enter the .drm path")
                return

            decryptor.decrypt_drm_file(drm_path=self.drm_path.get(), ask_pass= self.askPasswordDialog)
            
            

        except Exception as e:
            messagebox.showerror(message=f'{e}', title='error')




def run_gui():
    ctk.set_appearance_mode('light')
    ctk.set_default_color_theme('blue')
    app = ctk.CTk()
    app.geometry('800x600')

    receiverView(master=app)
    app.mainloop()


if __name__ == '__main__':
    run_gui()
        

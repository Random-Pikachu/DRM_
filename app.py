import customtkinter as ctk
from senderView import senderView 
from decryptorView import receiverView

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("DRM PDF Viewer")
        self.geometry("800x600")
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")

        self.radio_var = ctk.StringVar(value="sender")

        radio_frame = ctk.CTkFrame(self, fg_color="transparent")
        radio_frame.pack(pady=40)

        ctk.CTkRadioButton(radio_frame, text="Sender View", variable=self.radio_var, value="sender", command=self.switch_view, font=('Poppins', 16)).pack(side="left", padx=10)
        ctk.CTkRadioButton(radio_frame, text="Receiver", variable=self.radio_var, value="hi", command=self.switch_view, font=('Poppins', 16)).pack(side="left", padx=10)

        self.view_container = ctk.CTkFrame(self, fg_color="transparent")
        self.view_container.pack(fill="both", expand=True)

        self.current_view = None
        self.switch_view()

    def switch_view(self):
        if self.current_view:
            self.current_view.destroy()

        selected = self.radio_var.get()
        if selected == "sender":
            self.current_view = senderView(master=self.view_container)
        else:
            self.current_view = receiverView(master=self.view_container)

        self.current_view.pack(fill="both", expand=True)

if __name__ == "__main__":
    app = App()
    app.mainloop()

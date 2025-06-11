import fitz
import tkinter as tk
from PIL import Image, ImageTk
import io
#to open the pdf from a path

page_num = 0
num_pages = 0
doc = None

def open_path(pdf_path):
    doc=fitz.open(pdf_path)
    n_pag=doc.page_count
    return doc, n_pag

def launchViewer(file_path):
    global page_num
    
    doc, num_pages = open_path(file_path)

    root =tk.Tk()
    root.title("PDF Viewer")
    #disable print copy share
    def do_n(event=None):
        return "break"
    root.bind("<Button-3>", do_n)

    root.bind_all("<Control-c>", do_n)
    root.bind_all("<Control-x>", do_n)
    root.bind_all("<Control-v>", do_n)
    root.bind_all("<Control-p>", do_n)
    root.bind_all("<Control-s>", do_n)
    root.bind_all("<Control-Shift-S>", do_n)


    page_num = 0

    panel = tk.Label(root)
    panel.pack()

    page_label = tk.Label(root, text="")
    page_label.pack()

    def show_page(num):
        page = doc[num]
        pix = page.get_pixmap(matrix=fitz.Matrix(1,1))  # Render at 2x resolution
        img = Image.open(io.BytesIO(pix.tobytes("ppm")))  # Convert to PIL image
        img_tk = ImageTk.PhotoImage(img)
        panel.config(image=img_tk)
        panel.image = img_tk  # Keep reference to avoid garbage collection
        page_label.config(text=f"Page {num+1} / {num_pages}")

    def next_page():
        global page_num
        if page_num < num_pages - 1:
            page_num += 1
            show_page(page_num)

    def prev_page():
        global page_num
        if page_num > 0:
            page_num -= 1
            show_page(page_num)

    btn_frame = tk.Frame(root)
    btn_frame.pack()

    btn_prev = tk.Button(btn_frame, text="Previous", command=prev_page)
    btn_prev.pack(side=tk.LEFT, padx=5, pady=5)

    btn_next = tk.Button(btn_frame, text="Next", command=next_page)
    btn_next.pack(side=tk.LEFT, padx=5, pady=5)

    show_page(page_num)
    root.mainloop()
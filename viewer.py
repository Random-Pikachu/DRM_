import fitz
import tkinter as tk
from PIL import Image, ImageTk
import io

def open_path(pdf_path):
    doc = fitz.open(pdf_path)
    n_pag = doc.page_count
    return doc, n_pag

def launchViewer(file_path):
    doc, num_pages = open_path(file_path)
    current_page = 0
    image_store = {"photo": None}
    zoom_level = {"scale": 2.0}
    fit_to_window = {"enabled": False}

    viewer_win = tk.Toplevel()
    viewer_win.title("Secure PDF Viewer")
    viewer_win.geometry("1000x800")

    def disable_actions(event=None):
        return "break"

    viewer_win.bind("<Button-3>", disable_actions)
    viewer_win.bind_all("<Control-c>", disable_actions)
    viewer_win.bind_all("<Control-v>", disable_actions)
    viewer_win.bind_all("<Control-x>", disable_actions)
    viewer_win.bind_all("<Control-s>", disable_actions)
    viewer_win.bind_all("<Control-p>", disable_actions)

    def toggle_fullscreen(event=None):
        is_fullscreen = viewer_win.attributes("-fullscreen")
        viewer_win.attributes("-fullscreen", not is_fullscreen)

    def exit_fullscreen(event=None):
        viewer_win.attributes("-fullscreen", False)

    viewer_win.bind("<F11>", toggle_fullscreen)
    viewer_win.bind("<Escape>", exit_fullscreen)

    # Canvas + Scrollbars
    canvas_frame = tk.Frame(viewer_win)
    canvas_frame.grid(row=0, column=0, sticky="nsew")

    canvas = tk.Canvas(canvas_frame, bg="gray")
    v_scroll = tk.Scrollbar(canvas_frame, orient=tk.VERTICAL, command=canvas.yview)
    canvas.configure(yscrollcommand=v_scroll.set)

    v_scroll.pack(side=tk.RIGHT, fill=tk.Y)
    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    image_label = tk.Label(canvas)
    image_window = canvas.create_window((0, 0), window=image_label, anchor="n")

    def show_page(page_number):
        page = doc[page_number]
        scale = zoom_level["scale"]

        if fit_to_window["enabled"]:
            page_rect = page.rect
            canvas_width = canvas.winfo_width() or 800
            scale = canvas_width / page_rect.width

        pix = page.get_pixmap(matrix=fitz.Matrix(scale, scale))
        img = Image.open(io.BytesIO(pix.tobytes("ppm")))
        photo = ImageTk.PhotoImage(img)

        image_label.config(image=photo)
        image_store["photo"] = photo

        canvas.update_idletasks()
        canvas_width = canvas.winfo_width()
        x_offset = max((canvas_width - photo.width()) // 2, 0)
        canvas.coords(image_window, x_offset, 0)
        canvas.config(scrollregion=canvas.bbox("all"))

        page_label.config(text=f"Page {page_number + 1} / {num_pages}")

    def next_page():
        nonlocal current_page
        if current_page < num_pages - 1:
            current_page += 1
            show_page(current_page)

    def prev_page():
        nonlocal current_page
        if current_page > 0:
            current_page -= 1
            show_page(current_page)

    def zoom_in():
        zoom_level["scale"] += 0.25
        fit_to_window["enabled"] = False
        show_page(current_page)

    def zoom_out():
        if zoom_level["scale"] > 0.5:
            zoom_level["scale"] -= 0.25
            fit_to_window["enabled"] = False
            show_page(current_page)

    def toggle_fit():
        fit_to_window["enabled"] = not fit_to_window["enabled"]
        show_page(current_page)

    # Mouse wheel scrolling
    def _on_mousewheel(event):
        canvas.yview_scroll(-1 * (event.delta // 120), "units")

    def _on_linux_scroll(event):
        canvas.yview_scroll(-1 if event.num == 4 else 1, "units")

    canvas.bind_all("<MouseWheel>", _on_mousewheel)  # Windows/macOS
    canvas.bind_all("<Button-4>", _on_linux_scroll)  # Linux up
    canvas.bind_all("<Button-5>", _on_linux_scroll)  # Linux down

    # Controls
    controls = tk.Frame(viewer_win)
    controls.grid(row=1, column=0, pady=10)

    page_label = tk.Label(controls, text="")
    page_label.pack(side=tk.LEFT, padx=10)

    tk.Button(controls, text="Previous", command=prev_page).pack(side=tk.LEFT, padx=5)
    tk.Button(controls, text="Next", command=next_page).pack(side=tk.LEFT, padx=5)
    tk.Button(controls, text="Zoom In", command=zoom_in).pack(side=tk.LEFT, padx=5)
    tk.Button(controls, text="Zoom Out", command=zoom_out).pack(side=tk.LEFT, padx=5)
    tk.Button(controls, text="Fit to Window", command=toggle_fit).pack(side=tk.LEFT, padx=5)

    # Resize handling
    viewer_win.grid_rowconfigure(0, weight=1)
    viewer_win.grid_columnconfigure(0, weight=1)

    def center_on_resize(event):
        if image_store["photo"]:
            photo = image_store["photo"]
            canvas_width = canvas.winfo_width()
            x_offset = max((canvas_width - photo.width()) // 2, 0)
            canvas.coords(image_window, x_offset, 0)

    canvas.bind("<Configure>", center_on_resize)

    show_page(current_page)

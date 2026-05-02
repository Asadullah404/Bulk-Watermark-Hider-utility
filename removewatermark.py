import cv2
import os
import numpy as np
from pathlib import Path
import threading
import tkinter as tk
from tkinter import filedialog, messagebox

# Auto-install dependencies if missing
try:
    import customtkinter as ctk
except ImportError:
    import sys
    import subprocess
    print("Installing customtkinter for enterprise UI...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "customtkinter", "packaging"])
    import customtkinter as ctk

try:
    from PIL import Image, ImageTk
except ImportError:
    import sys
    import subprocess
    print("Installing Pillow...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "Pillow"])
    from PIL import Image, ImageTk

# --- App Configuration ---
ctk.set_appearance_mode("Dark")  # Divine dark mode
ctk.set_default_color_theme("blue")  # Modern blue accents

class ModernWatermarkApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # --- Window Setup ---
        self.title("Sipra-Productions Private Limited | Pro Image Studio")
        self.geometry("800x750")
        self.resizable(False, True)

        self.folders = []
        self.logo_path = None

        # --- Grid Layout ---
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # --- Header ---
        self.header_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.header_frame.grid(row=0, column=0, padx=30, pady=(25, 10), sticky="ew")
        
        self.title_label = ctk.CTkLabel(
            self.header_frame, 
            text="Sipra-Productions", 
            font=ctk.CTkFont(family="Helvetica", size=32, weight="bold")
        )
        self.title_label.pack(anchor="w")
        
        self.subtitle_label = ctk.CTkLabel(
            self.header_frame, 
            text="PRIVATE LIMITED • DIVINE WATERMARKING & CONVERSION ENGINE", 
            font=ctk.CTkFont(family="Helvetica", size=13, slant="italic", weight="bold"), 
            text_color="#1f538d"
        )
        self.subtitle_label.pack(anchor="w")

        # --- Main Content Frame (Card style) ---
        self.main_frame = ctk.CTkFrame(self, corner_radius=15)
        self.main_frame.grid(row=1, column=0, padx=30, pady=10, sticky="nsew")
        self.main_frame.grid_columnconfigure(0, weight=1)

        # 1. Folders Section
        self.folder_label = ctk.CTkLabel(self.main_frame, text="1. Select Target Folders", font=ctk.CTkFont(size=16, weight="bold"))
        self.folder_label.grid(row=0, column=0, padx=25, pady=(25, 5), sticky="w")

        self.folder_listbox = tk.Listbox(
            self.main_frame, height=5, 
            bg="#242424", fg="white", 
            selectbackground="#1f538d", borderwidth=0, 
            highlightthickness=1, highlightcolor="#1f538d", 
            font=("Helvetica", 13)
        )
        self.folder_listbox.grid(row=1, column=0, padx=25, pady=5, sticky="ew")

        self.folder_btn_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.folder_btn_frame.grid(row=2, column=0, padx=25, pady=(0, 15), sticky="e")
        
        self.btn_add_folder = ctk.CTkButton(self.folder_btn_frame, text="+ Add Folder", command=self.add_folder, width=130, corner_radius=8)
        self.btn_add_folder.pack(side="left", padx=(0, 10))
        
        self.btn_rem_folder = ctk.CTkButton(self.folder_btn_frame, text="Remove Selected", command=self.remove_folder, width=130, fg_color="#8B0000", hover_color="#5c0000", corner_radius=8)
        self.btn_rem_folder.pack(side="left")

        # 2. Logo Section
        self.logo_label = ctk.CTkLabel(self.main_frame, text="2. Watermark Logo (Optional)", font=ctk.CTkFont(size=16, weight="bold"))
        self.logo_label.grid(row=3, column=0, padx=25, pady=(15, 5), sticky="w")

        self.logo_inner_frame = ctk.CTkFrame(self.main_frame, fg_color="#1a1a1a", corner_radius=8)
        self.logo_inner_frame.grid(row=4, column=0, padx=25, pady=5, sticky="ew")
        
        self.logo_lbl = ctk.CTkLabel(self.logo_inner_frame, text="No premium logo selected...", font=ctk.CTkFont(slant="italic"), text_color="gray")
        self.logo_lbl.pack(side="left", padx=20, pady=12)

        self.btn_browse_logo = ctk.CTkButton(self.logo_inner_frame, text="Browse Logo", command=self.browse_logo, width=120, corner_radius=8)
        self.btn_browse_logo.pack(side="right", padx=10, pady=12)

        self.btn_clear_logo = ctk.CTkButton(self.logo_inner_frame, text="Clear", command=self.clear_logo, width=80, fg_color="#555555", hover_color="#333333", corner_radius=8)
        self.btn_clear_logo.pack(side="right", padx=5, pady=12)

        # 3. Text Fallback Section
        self.text_label = ctk.CTkLabel(self.main_frame, text="3. Fallback Text Watermark", font=ctk.CTkFont(size=16, weight="bold"))
        self.text_label.grid(row=5, column=0, padx=25, pady=(15, 5), sticky="w")

        self.text_inner_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.text_inner_frame.grid(row=6, column=0, padx=25, pady=(0, 25), sticky="ew")

        self.text_desc = ctk.CTkLabel(self.text_inner_frame, text="Dynamic text to use if no logo is provided:", text_color="gray")
        self.text_desc.pack(side="left", padx=(0, 15))

        self.text_var = ctk.StringVar(value="AS")
        self.text_entry = ctk.CTkEntry(self.text_inner_frame, textvariable=self.text_var, width=180, corner_radius=8)
        self.text_entry.pack(side="left")

        # --- Footer / Action Frame ---
        self.action_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.action_frame.grid(row=2, column=0, padx=30, pady=(0, 25), sticky="ew")
        self.action_frame.grid_columnconfigure(0, weight=1)

        self.progress_bar = ctk.CTkProgressBar(self.action_frame, mode="determinate", height=10, corner_radius=5)
        self.progress_bar.grid(row=0, column=0, padx=5, pady=(10, 8), sticky="ew")
        self.progress_bar.set(0)

        self.status_lbl = ctk.CTkLabel(self.action_frame, text="System Ready.", text_color="gray", font=ctk.CTkFont(size=12))
        self.status_lbl.grid(row=1, column=0, pady=(0, 15))

        self.btn_run = ctk.CTkButton(
            self.action_frame, 
            text="START DIVINE PROCESSING", 
            command=self.start_processing, 
            font=ctk.CTkFont(size=18, weight="bold"), 
            height=55, 
            corner_radius=12,
            fg_color="#006400", 
            hover_color="#004d00"
        )
        self.btn_run.grid(row=2, column=0, pady=(0, 5), sticky="ew", padx=5)

    def add_folder(self):
        folder = filedialog.askdirectory(title="Select Folder containing Images")
        if folder and folder not in self.folders:
            self.folders.append(folder)
            self.folder_listbox.insert(tk.END, folder)

    def remove_folder(self):
        selected = self.folder_listbox.curselection()
        if selected:
            idx = selected[0]
            self.folder_listbox.delete(idx)
            self.folders.pop(idx)

    def browse_logo(self):
        filetypes = [("Image files", "*.png *.jpg *.jpeg")]
        filepath = filedialog.askopenfilename(title="Select Premium Logo", filetypes=filetypes)
        if filepath:
            self.logo_path = filepath
            self.logo_lbl.configure(text=Path(filepath).name, text_color="white")

    def clear_logo(self):
        self.logo_path = None
        self.logo_lbl.configure(text="No premium logo selected...", text_color="gray")

    def start_processing(self):
        if not self.folders:
            messagebox.showwarning("Notice", "Please add at least one folder to process.")
            return
            
        self.btn_run.configure(state="disabled", text="PROCESSING... PLEASE WAIT")
        self.status_lbl.configure(text="Initializing divine processing engine...")
        self.progress_bar.set(0)
        
        text_wm = self.text_var.get()
        
        # Run in separate thread so UI doesn't freeze
        threading.Thread(target=self.process_folders, args=(text_wm,), daemon=True).start()

    def process_folders(self, text_wm):
        valid_extensions = ('.jpg', '.jpeg', '.png')
        logo_img = None
        
        if self.logo_path and os.path.exists(self.logo_path):
            logo_img = cv2.imread(self.logo_path, cv2.IMREAD_UNCHANGED)

        total_files = 0
        all_files = []
        for folder in self.folders:
            if not os.path.exists(folder): continue
            for filename in os.listdir(folder):
                if filename.lower().endswith(valid_extensions):
                    all_files.append((folder, filename))
        
        total_files = len(all_files)
        if total_files == 0:
            self.after(0, self.finish_processing, "No valid images found in the selected folders.")
            return

        for idx, (folder, filename) in enumerate(all_files):
            img_path = os.path.join(folder, filename)
            img = cv2.imread(img_path)
            
            if img is None:
                continue
                
            height, width = img.shape[:2]
            
            # Draw Logo or Text
            if logo_img is not None:
                self.apply_logo(img, logo_img, width, height)
            else:
                self.apply_text(img, text_wm, width, height)
                
            # Save logic
            folder_path = Path(folder)
            output_dir = folder_path.parent / f"{folder_path.name}_processed"
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)
                
            file_stem = Path(filename).stem
            output_path = os.path.join(output_dir, f"{file_stem}.webp")
            
            cv2.imwrite(output_path, img, [cv2.IMWRITE_WEBP_QUALITY, 90])
            
            # Update progress
            progress = (idx + 1) / total_files
            self.after(0, self.update_progress, progress, f"Processed {idx+1}/{total_files}: {filename}")

        self.after(0, self.finish_processing, "Divine Processing Completed Successfully!")

    def update_progress(self, val, text):
        self.progress_bar.set(val)
        self.status_lbl.configure(text=text)

    def apply_logo(self, img, logo, img_w, img_h):
        # Resize logo to fit reasonably (15% of image width)
        scale = (img_w * 0.15) / logo.shape[1]
        new_w = int(logo.shape[1] * scale)
        new_h = int(logo.shape[0] * scale)
        
        if new_w <= 0 or new_h <= 0: return # fallback if image is tiny
        
        resized_logo = cv2.resize(logo, (new_w, new_h))
        
        # Position at bottom right with offset
        offset = 40
        y1 = img_h - new_h - offset
        y2 = img_h - offset
        x1 = img_w - new_w - offset
        x2 = img_w - offset
        
        # Ensure it's within bounds
        if y1 < 0 or x1 < 0:
            y1 = max(0, img_h - new_h)
            y2 = y1 + new_h
            x1 = max(0, img_w - new_w)
            x2 = x1 + new_w
            
        # Blend logo
        if resized_logo.shape[2] == 4:
            # Logo has alpha channel
            alpha_s = resized_logo[:, :, 3] / 255.0
            alpha_l = 1.0 - alpha_s
            
            for c in range(0, 3):
                img[y1:y2, x1:x2, c] = (alpha_s * resized_logo[:, :, c] + alpha_l * img[y1:y2, x1:x2, c])
        else:
            # No alpha channel, just paste
            img[y1:y2, x1:x2] = resized_logo

    def apply_text(self, img, text, img_w, img_h):
        radius = 35
        offset = 45
        center_x = img_w - offset
        center_y = img_h - offset
        
        if center_x < 0 or center_y < 0: return # Too small
        
        cv2.circle(img, (center_x, center_y), radius, (0, 0, 0), -1)
        
        font = cv2.FONT_HERSHEY_DUPLEX
        if text:
            text_size = cv2.getTextSize(text, font, 0.8, 2)[0]
            text_x = center_x - (text_size[0] // 2)
            text_y = center_y + (text_size[1] // 2)
            cv2.putText(img, text, (text_x, text_y), font, 0.8, (255, 255, 255), 2, cv2.LINE_AA)

    def finish_processing(self, msg):
        self.status_lbl.configure(text=msg)
        self.btn_run.configure(state="normal", text="START DIVINE PROCESSING")
        messagebox.showinfo("Operation Complete", msg)

if __name__ == "__main__":
    app = ModernWatermarkApp()
    app.mainloop()
import os
import time
import threading
import tkinter as tk
from tkinter import ttk, filedialog, scrolledtext, messagebox
import pandas as pd
import requests
from urllib.parse import urlparse
import concurrent.futures

class ImageDownloaderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Fast Image Downloader Pro")
        self.root.geometry("650x700")
        self.root.resizable(False, False)
        
        # --- Variables ---
        self.xlsx_path = tk.StringVar()
        self.output_folder = tk.StringVar()
        self.url_column = tk.StringVar(value="URL")
        self.batch_size = tk.IntVar(value=50)
        self.wait_time = tk.IntVar(value=5)
        self.workers = tk.IntVar(value=10) # How many images to download at the exact same time
        
        self.downloaded_count = 0
        self.total_count = 0
        
        self.setup_ui()

    def setup_ui(self):
        # Frame for Inputs
        input_frame = ttk.LabelFrame(self.root, text="Settings", padding=(10, 10))
        input_frame.pack(fill="x", padx=10, pady=10)

        # Excel File Path
        ttk.Label(input_frame, text="Excel File (.xlsx):").grid(row=0, column=0, sticky="w", pady=5)
        ttk.Entry(input_frame, textvariable=self.xlsx_path, width=50).grid(row=0, column=1, padx=5)
        ttk.Button(input_frame, text="Browse", command=self.browse_file).grid(row=0, column=2)

        # Output Folder Path
        ttk.Label(input_frame, text="Output Folder:").grid(row=1, column=0, sticky="w", pady=5)
        ttk.Entry(input_frame, textvariable=self.output_folder, width=50).grid(row=1, column=1, padx=5)
        ttk.Button(input_frame, text="Browse", command=self.browse_folder).grid(row=1, column=2)

        # Column Name
        ttk.Label(input_frame, text="URL Column Name:").grid(row=2, column=0, sticky="w", pady=5)
        ttk.Entry(input_frame, textvariable=self.url_column, width=20).grid(row=2, column=1, sticky="w", padx=5)

        # Speed and Limit Settings
        settings_frame = ttk.Frame(input_frame)
        settings_frame.grid(row=3, column=0, columnspan=3, sticky="w", pady=10)
        
        ttk.Label(settings_frame, text="Batch Size:").grid(row=0, column=0, sticky="w")
        ttk.Entry(settings_frame, textvariable=self.batch_size, width=5).grid(row=0, column=1, padx=(5, 15))
        
        ttk.Label(settings_frame, text="Wait Time (sec):").grid(row=0, column=2, sticky="w")
        ttk.Entry(settings_frame, textvariable=self.wait_time, width=5).grid(row=0, column=3, padx=(5, 15))
        
        ttk.Label(settings_frame, text="Concurrent Workers:").grid(row=0, column=4, sticky="w")
        ttk.Entry(settings_frame, textvariable=self.workers, width=5).grid(row=0, column=5, padx=(5, 5))

        # Start Button
        self.start_btn = ttk.Button(self.root, text="Start Download", command=self.start_download_thread)
        self.start_btn.pack(pady=10)

        # Progress Section
        progress_frame = ttk.LabelFrame(self.root, text="Progress", padding=(10, 10))
        progress_frame.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        self.status_label = ttk.Label(progress_frame, text="Idle", font=("Helvetica", 10, "bold"))
        self.status_label.pack(anchor="w", pady=(0, 5))

        self.progress_bar = ttk.Progressbar(progress_frame, orient="horizontal", mode="determinate")
        self.progress_bar.pack(fill="x", pady=5)

        # Log Console
        self.log_area = scrolledtext.ScrolledText(progress_frame, height=15, state='disabled', bg="#f4f4f4")
        self.log_area.pack(fill="both", expand=True, pady=5)

    def browse_file(self):
        filename = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx;*.xls")])
        if filename:
            self.xlsx_path.set(filename)

    def browse_folder(self):
        foldername = filedialog.askdirectory()
        if foldername:
            self.output_folder.set(foldername)

    def log(self, message):
        """Thread-safe way to update the log text area."""
        self.root.after(0, self._append_log, message)

    def _append_log(self, message):
        self.log_area.config(state='normal')
        self.log_area.insert(tk.END, message + "\n")
        self.log_area.see(tk.END)
        self.log_area.config(state='disabled')

    def update_progress(self, increment=1):
        """Thread-safe way to update the progress bar."""
        self.root.after(0, self._step_progress, increment)

    def _step_progress(self, increment):
        self.downloaded_count += increment
        self.progress_bar['value'] = self.downloaded_count
        self.status_label.config(text=f"Downloading... {self.downloaded_count} / {self.total_count} completed")

    def update_status(self, text):
        self.root.after(0, lambda: self.status_label.config(text=text))

    def start_download_thread(self):
        # Validate Inputs
        if not self.xlsx_path.get() or not self.output_folder.get():
            messagebox.showerror("Error", "Please select both the Excel file and Output folder.")
            return
        if not self.url_column.get():
            messagebox.showerror("Error", "Please enter the URL column name.")
            return

        # Disable button to prevent multiple clicks
        self.start_btn.config(state="disabled")
        self.log_area.config(state='normal')
        self.log_area.delete(1.0, tk.END)  # Clear logs
        self.log_area.config(state='disabled')
        
        self.downloaded_count = 0
        self.progress_bar['value'] = 0

        # Start background thread to keep UI responsive
        threading.Thread(target=self.process_downloads, daemon=True).start()

    def download_worker(self, index, url, output_folder, headers):
        """This function handles the download of a SINGLE image."""
        try:
            response = requests.get(url, headers=headers, stream=True, timeout=15)
            response.raise_for_status()
            
            parsed_url = urlparse(url)
            filename = os.path.basename(parsed_url.path)
            if not filename:
                filename = "image.jpg"
                
            safe_filename = f"row_{index + 2}_{filename}"
            filepath = os.path.join(output_folder, safe_filename)
            
            with open(filepath, 'wb') as file:
                for chunk in response.iter_content(chunk_size=8192):
                    file.write(chunk)
                    
            return True, f"[Row {index + 2}] Downloaded: {safe_filename}"
        except Exception as e:
            return False, f"[Row {index + 2}] ERROR: {e}"

    def process_downloads(self):
        self.log("Initializing...")
        try:
            df = pd.read_excel(self.xlsx_path.get())
        except Exception as e:
            self.log(f"Error reading Excel file: {e}")
            self.root.after(0, lambda: self.start_btn.config(state="normal"))
            return

        col_name = self.url_column.get()
        if col_name not in df.columns:
            self.log(f"Error: Column '{col_name}' not found. Available columns: {', '.join(df.columns)}")
            self.root.after(0, lambda: self.start_btn.config(state="normal"))
            return

        output_dir = self.output_folder.get()
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
            self.log(f"Created output folder: {output_dir}")

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'
        }

        # Filter out valid items to download
        valid_items = []
        for index, row in df.iterrows():
            url = str(row[col_name]).strip()
            if pd.isna(row[col_name]) or url.lower() == 'nan' or not url:
                continue
            valid_items.append((index, url))

        self.total_count = len(valid_items)
        
        if self.total_count == 0:
            self.log("No valid URLs found in the specified column.")
            self.root.after(0, lambda: self.start_btn.config(state="normal"))
            return

        self.root.after(0, lambda: self.progress_bar.config(maximum=self.total_count))
        self.log(f"Found {self.total_count} images to download.\nStarting...")

        batch_size = self.batch_size.get()
        wait_time = self.wait_time.get()
        max_workers = self.workers.get()

        # Process downloads in batches to respect the user's anti-ban waiting period
        for i in range(0, self.total_count, batch_size):
            chunk = valid_items[i : i + batch_size]
            
            # Use ThreadPoolExecutor to download multiple files AT THE SAME TIME
            with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
                # Submit all tasks in the current batch
                future_to_url = {
                    executor.submit(self.download_worker, item[0], item[1], output_dir, headers): item 
                    for item in chunk
                }
                
                # As each individual image finishes downloading, update the log & progress bar
                for future in concurrent.futures.as_completed(future_to_url):
                    success, msg = future.result()
                    self.log(msg)
                    self.update_progress(1)

            # Check if we need to pause before the next batch
            if i + batch_size < self.total_count:
                self.update_status(f"[PAUSED] Waiting {wait_time} seconds to prevent IP blocks...")
                self.log(f"\n--- Batch complete. Pausing for {wait_time} seconds... ---\n")
                time.sleep(wait_time)
                self.update_status(f"Downloading... {self.downloaded_count} / {self.total_count} completed")

        self.update_status("Download Complete!")
        self.log("\n--- All downloads finished successfully! ---")
        messagebox.showinfo("Success", f"Successfully downloaded {self.downloaded_count} images.")
        
        # Re-enable start button
        self.root.after(0, lambda: self.start_btn.config(state="normal"))


if __name__ == "__main__":
    # Initialize the GUI Window
    root = tk.Tk()
    app = ImageDownloaderApp(root)
    
    # Run the Application
    root.mainloop()
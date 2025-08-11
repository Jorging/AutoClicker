import tkinter as tk
from tkinter import ttk, messagebox
import threading
import time
import pyautogui
import keyboard

class AutoClickerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Jorgin")
        self.root.geometry("300x150")
        self.root.resizable(False, False)

        # Default settings
        self.hotkey = "f8"
        self.repeat_mode = "count"  # or "until_stopped"
        self.repeat_count = 10
        self.interval = 0.1  # seconds

        self.is_clicking = False
        self.click_thread = None

        # UI Main window
        self.main_button = ttk.Button(root, text=f"Press {self.hotkey.upper()} to click", command=self.toggle_clicking)
        self.main_button.pack(expand=True, fill="both", padx=20, pady=20)

        self.options_button = ttk.Button(root, text="Options", command=self.open_options)
        self.options_button.pack(pady=(0,10))

        # Register hotkey
        keyboard.add_hotkey(self.hotkey, self.toggle_clicking)

    def toggle_clicking(self):
        if self.is_clicking:
            self.stop_clicking()
        else:
            self.start_clicking()

    def start_clicking(self):
        if self.is_clicking:
            return
        self.is_clicking = True
        self.main_button.config(text="Clicking... Press to Stop")
        self.click_thread = threading.Thread(target=self.click_loop, daemon=True)
        self.click_thread.start()

    def stop_clicking(self):
        self.is_clicking = False
        self.main_button.config(text=f"Press {self.hotkey.upper()} to click")

    def click_loop(self):
        count = 0
        while self.is_clicking:
            pyautogui.click()
            count += 1
            if self.repeat_mode == "count" and count >= self.repeat_count:
                self.stop_clicking()
                break
            time.sleep(self.interval)

    def open_options(self):
        OptionsWindow(self)

    def update_hotkey(self, new_hotkey):
        try:
            keyboard.remove_hotkey(self.hotkey)
        except KeyError:
            pass  # No previous hotkey registered
        self.hotkey = new_hotkey.lower()
        keyboard.add_hotkey(self.hotkey, self.toggle_clicking)
        self.main_button.config(text=f"Press {self.hotkey.upper()} to click")

    def update_settings(self, repeat_mode, repeat_count, interval_seconds):
        self.repeat_mode = repeat_mode
        self.repeat_count = repeat_count
        self.interval = interval_seconds


class OptionsWindow(tk.Toplevel):
    def __init__(self, parent: AutoClickerApp):
        super().__init__(parent.root)
        self.parent = parent
        self.title("Options")
        self.geometry("350x300")
        self.resizable(False, False)

        # Repeat mode
        self.repeat_mode_var = tk.StringVar(value=self.parent.repeat_mode)
        ttk.Label(self, text="Repeat Mode:").pack(anchor="w", padx=10, pady=(10,0))

        frame_repeat = ttk.Frame(self)
        frame_repeat.pack(anchor="w", padx=20, pady=(0,10))

        self.rb_count = ttk.Radiobutton(frame_repeat, text="Repeat count", variable=self.repeat_mode_var, value="count", command=self.toggle_repeat_count)
        self.rb_count.grid(row=0, column=0, sticky="w")

        self.rb_until = ttk.Radiobutton(frame_repeat, text="Repeat until stopped", variable=self.repeat_mode_var, value="until_stopped", command=self.toggle_repeat_count)
        self.rb_until.grid(row=1, column=0, sticky="w")

        # Repeat count input
        self.repeat_count_var = tk.StringVar(value=str(self.parent.repeat_count))
        self.repeat_count_entry = ttk.Entry(frame_repeat, width=10, textvariable=self.repeat_count_var)
        self.repeat_count_entry.grid(row=0, column=1, padx=10)

        # Interval inputs
        ttk.Label(self, text="Interval between clicks:").pack(anchor="w", padx=10, pady=(10,0))

        frame_interval = ttk.Frame(self)
        frame_interval.pack(anchor="w", padx=20, pady=(0,10))

        self.interval_h_var = tk.StringVar(value="0")
        self.interval_m_var = tk.StringVar(value="0")
        self.interval_s_var = tk.StringVar(value=str(int(self.parent.interval)))
        self.interval_ms_var = tk.StringVar(value=str(int((self.parent.interval - int(self.parent.interval))*1000)))

        ttk.Label(frame_interval, text="Hours").grid(row=0, column=0)
        ttk.Label(frame_interval, text="Minutes").grid(row=0, column=1)
        ttk.Label(frame_interval, text="Seconds").grid(row=0, column=2)
        ttk.Label(frame_interval, text="Milliseconds").grid(row=0, column=3)

        self.interval_h_entry = ttk.Entry(frame_interval, width=5, textvariable=self.interval_h_var)
        self.interval_h_entry.grid(row=1, column=0, padx=5)

        self.interval_m_entry = ttk.Entry(frame_interval, width=5, textvariable=self.interval_m_var)
        self.interval_m_entry.grid(row=1, column=1, padx=5)

        self.interval_s_entry = ttk.Entry(frame_interval, width=5, textvariable=self.interval_s_var)
        self.interval_s_entry.grid(row=1, column=2, padx=5)

        self.interval_ms_entry = ttk.Entry(frame_interval, width=7, textvariable=self.interval_ms_var)
        self.interval_ms_entry.grid(row=1, column=3, padx=5)

        # Hotkey input
        ttk.Label(self, text="Hotkey (single key):").pack(anchor="w", padx=10, pady=(10,0))
        self.hotkey_var = tk.StringVar(value=self.parent.hotkey.upper())
        self.hotkey_entry = ttk.Entry(self, width=10, textvariable=self.hotkey_var)
        self.hotkey_entry.pack(anchor="w", padx=20, pady=(0,10))

        # Save button
        btn_save = ttk.Button(self, text="Save", command=self.save_options)
        btn_save.pack(pady=10)

        self.toggle_repeat_count()

    def toggle_repeat_count(self):
        if self.repeat_mode_var.get() == "count":
            self.repeat_count_entry.config(state="normal")
        else:
            self.repeat_count_entry.config(state="disabled")

    def save_options(self):
        # Validate repeat count
        repeat_mode = self.repeat_mode_var.get()
        repeat_count = 0
        if repeat_mode == "count":
            try:
                repeat_count = int(self.repeat_count_var.get())
                if repeat_count < 1:
                    raise ValueError
            except ValueError:
                messagebox.showerror("Error", "Repeat count must be a positive integer.")
                return

        # Validate interval inputs
        try:
            h = int(self.interval_h_var.get())
            m = int(self.interval_m_var.get())
            s = int(self.interval_s_var.get())
            ms = int(self.interval_ms_var.get())

            if h < 0 or m < 0 or s < 0 or ms < 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Interval values must be non-negative integers.")
            return

        total_seconds = h*3600 + m*60 + s + ms/1000
        if total_seconds <= 0:
            messagebox.showerror("Error", "Interval must be greater than zero.")
            return

        # Validate hotkey (simplified: must be 1 char or function key name)
        hotkey = self.hotkey_var.get().lower()
        if not hotkey:
            messagebox.showerror("Error", "Hotkey cannot be empty.")
            return
        # You could add more validation here for allowed keys

        # Update settings in parent
        self.parent.update_settings(repeat_mode, repeat_count, total_seconds)
        self.parent.update_hotkey(hotkey)

        self.destroy()
        messagebox.showinfo("Success", "Options saved!")

def main():
    root = tk.Tk()
    app = AutoClickerApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()

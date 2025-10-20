import tkinter as tk
from tkinter import ttk, messagebox
import tkinter.font as tkfont

class StoreManagementApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Store Management - PIN Login")
        self.root.geometry("400x600")
        self.root.configure(bg='#f6f7f8')
        
        # Configure styles
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Demo PIN
        self.DEMO_PIN = '123456'
        self.current_pin = ['', '', '', '', '', '']
        
        self.setup_login_screen()
        
    def setup_login_screen(self):
        # Clear the window
        for widget in self.root.winfo_children():
            widget.destroy()
            
        # Header
        header_frame = tk.Frame(self.root, bg='#f6f7f8', height=80)
        header_frame.pack(fill='x', padx=20, pady=20)
        
        title_label = tk.Label(
            header_frame, 
            text="Store Management", 
            font=('Arial', 18, 'bold'),
            bg='#f6f7f8',
            fg='#101922'
        )
        title_label.pack()
        
        # Main content
        main_frame = tk.Frame(self.root, bg='#f6f7f8')
        main_frame.pack(expand=True, fill='both', padx=40, pady=20)
        
        # Lock icon (using text)
        icon_frame = tk.Frame(main_frame, bg='#e3f2fd', width=80, height=80)
        icon_frame.pack(pady=(0, 20))
        icon_frame.pack_propagate(False)
        
        lock_label = tk.Label(
            icon_frame,
            text="🔒",
            font=('Arial', 30),
            bg='#e3f2fd'
        )
        lock_label.pack(expand=True)
        
        # Title and subtitle
        title = tk.Label(
            main_frame,
            text="Enter your PIN",
            font=('Arial', 20, 'bold'),
            bg='#f6f7f8',
            fg='#101922'
        )
        title.pack(pady=(0, 10))
        
        subtitle = tk.Label(
            main_frame,
            text="Please enter your 6-digit PIN to continue.",
            font=('Arial', 12),
            bg='#f6f7f8',
            fg='#6b7280'
        )
        subtitle.pack(pady=(0, 30))
        
        # PIN input frame
        pin_frame = tk.Frame(main_frame, bg='#f6f7f8')
        pin_frame.pack(pady=(0, 30))
        
        self.pin_entries = []
        for i in range(6):
            entry = tk.Entry(
                pin_frame,
                width=3,
                font=('Arial', 20, 'bold'),
                justify='center',
                relief='solid',
                borderwidth=2,
                validate='key',
                validatecommand=(self.root.register(self.validate_pin_input), '%P', str(i))
            )
            entry.pack(side='left', padx=5)
            entry.bind('<KeyPress>', lambda e, idx=i: self.on_key_press(e, idx))
            self.pin_entries.append(entry)
            
        # Login button
        self.login_btn = tk.Button(
            main_frame,
            text="Login",
            font=('Arial', 12, 'bold'),
            bg='#1173d4',
            fg='white',
            width=20,
            height=2,
            relief='flat',
            state='disabled',
            command=self.attempt_login
        )
        self.login_btn.pack(pady=(0, 20))
        
        # Demo info
        demo_label = tk.Label(
            main_frame,
            text="Demo PIN: 123456",
            font=('Arial', 10),
            bg='#f6f7f8',
            fg='#6b7280'
        )
        demo_label.pack()
        
        demo_btn = tk.Button(
            main_frame,
            text="Use Demo PIN",
            font=('Arial', 10),
            bg='#f6f7f8',
            fg='#1173d4',
            relief='flat',
            cursor='hand2',
            command=self.fill_demo_pin
        )
        demo_btn.pack()
        
        # Footer
        footer_frame = tk.Frame(self.root, bg='#f6f7f8')
        footer_frame.pack(side='bottom', fill='x', pady=20)
        
        footer_label = tk.Label(
            footer_frame,
            text="© 2024 Store Management System",
            font=('Arial', 9),
            bg='#f6f7f8',
            fg='#9ca3af'
        )
        footer_label.pack()
        
        # Focus first entry
        self.pin_entries[0].focus()
        
    def validate_pin_input(self, value, index):
        # Only allow single digits
        if len(value) <= 1 and (value.isdigit() or value == ''):
            return True
        return False
        
    def on_key_press(self, event, index):
        if event.char.isdigit() and len(event.widget.get()) == 0:
            # Move to next entry after typing
            self.root.after(10, lambda: self.move_to_next(index))
        elif event.keysym == 'BackSpace' and len(event.widget.get()) == 0 and index > 0:
            # Move to previous entry on backspace
            self.pin_entries[index - 1].focus()
            
    def move_to_next(self, index):
        self.update_current_pin()
        if index < 5:
            self.pin_entries[index + 1].focus()
        self.update_login_button()
        
    def update_current_pin(self):
        for i, entry in enumerate(self.pin_entries):
            self.current_pin[i] = entry.get()
            
    def update_login_button(self):
        self.update_current_pin()
        is_complete = all(digit != '' for digit in self.current_pin)
        self.login_btn.config(state='normal' if is_complete else 'disabled')
        
    def fill_demo_pin(self):
        for i, digit in enumerate(self.DEMO_PIN):
            self.pin_entries[i].delete(0, tk.END)
            self.pin_entries[i].insert(0, digit)
        self.update_login_button()
        
    def attempt_login(self):
        self.update_current_pin()
        entered_pin = ''.join(self.current_pin)
        
        if entered_pin == self.DEMO_PIN:
            self.show_dashboard()
        else:
            messagebox.showerror("Error", "Invalid PIN. Please try again.")
            self.clear_pin()
            
    def clear_pin(self):
        for entry in self.pin_entries:
            entry.delete(0, tk.END)
        self.current_pin = ['', '', '', '', '', '']
        self.pin_entries[0].focus()
        self.update_login_button()
        
    def show_dashboard(self):
        # Clear the window
        for widget in self.root.winfo_children():
            widget.destroy()
            
        self.root.geometry("800x600")
        
        # Header
        header_frame = tk.Frame(self.root, bg='#1173d4', height=60)
        header_frame.pack(fill='x')
        header_frame.pack_propagate(False)
        
        title_label = tk.Label(
            header_frame,
            text="Store Management Dashboard",
            font=('Arial', 16, 'bold'),
            bg='#1173d4',
            fg='white'
        )
        title_label.pack(expand=True)
        
        logout_btn = tk.Button(
            header_frame,
            text="Logout",
            font=('Arial', 10),
            bg='white',
            fg='#1173d4',
            command=self.setup_login_screen
        )
        logout_btn.place(relx=0.95, rely=0.5, anchor='e')
        
        # Dashboard content
        dashboard_frame = tk.Frame(self.root, bg='#f6f7f8')
        dashboard_frame.pack(expand=True, fill='both', padx=20, pady=20)
        
        welcome_label = tk.Label(
            dashboard_frame,
            text="Welcome to Store Management System!",
            font=('Arial', 18, 'bold'),
            bg='#f6f7f8',
            fg='#101922'
        )
        welcome_label.pack(pady=50)
        
        # Stats frame
        stats_frame = tk.Frame(dashboard_frame, bg='#f6f7f8')
        stats_frame.pack(pady=20)
        
        stats = [
            ("Today's Sales", "$2,847"),
            ("Active Orders", "12"),
            ("Total Items", "156"),
            ("Total Customers", "89")
        ]
        
        for i, (label, value) in enumerate(stats):
            stat_frame = tk.Frame(stats_frame, bg='white', relief='solid', borderwidth=1, padx=20, pady=15)
            stat_frame.grid(row=i//2, column=i%2, padx=10, pady=10, sticky='ew')
            
            tk.Label(stat_frame, text=label, font=('Arial', 10), bg='white', fg='#6b7280').pack()
            tk.Label(stat_frame, text=value, font=('Arial', 16, 'bold'), bg='white', fg='#101922').pack()
            
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = StoreManagementApp()
    app.run()
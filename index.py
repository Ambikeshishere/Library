import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import datetime
import sqlite3

class Book:
    def __init__(self, title, quantity, price_per_hour):
        self.title = title
        self.quantity = quantity
        self.price_per_hour = price_per_hour

class IssuedBook:
    def __init__(self, book_title, customer_name, customer_contact, hours, issue_time):
        self.book_title = book_title
        self.customer_name = customer_name
        self.customer_contact = customer_contact
        self.hours = hours
        self.issue_time = issue_time

class LibraryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Library Management System")
        self.root.geometry("1200x700")
        self.root.configure(bg="#f0f0f0")
        self.init_db()
        self.header = tk.Label(self.root, text="Stark Library", font=("Helvetica", 36, 'bold'), bg="#3498db", fg="white", padx=20, pady=20)
        self.header.pack(fill=tk.X)
        self.books = []
        self.issued_books = []
        self.sidebar_frame_left = tk.Frame(self.root, width=200, bg="#dfe6e9")
        self.sidebar_frame_left.pack(side=tk.LEFT, fill=tk.Y)
        self.sidebar_frame_right = tk.Frame(self.root, width=200, bg="#dfe6e9")
        self.sidebar_frame_right.pack(side=tk.RIGHT, fill=tk.Y)
        self.sidebar_label_left = tk.Label(self.sidebar_frame_left, text="Available Books", font=("Helvetica", 16, 'bold'), bg="#dfe6e9")
        self.sidebar_label_left.pack(pady=10)
        self.search_entry = tk.Entry(self.sidebar_frame_left, font=("Helvetica", 14))
        self.search_entry.pack(pady=10, padx=5)
        self.search_entry.bind("<KeyRelease>", self.update_available_books)
        self.available_books_listbox = tk.Listbox(self.sidebar_frame_left, font=("Helvetica", 14))
        self.available_books_listbox.pack(expand=True, fill=tk.BOTH, padx=5, pady=5)
        self.sidebar_label_right = tk.Label(self.sidebar_frame_right, text="Issued Books", font=("Helvetica", 16, 'bold'), bg="#dfe6e9")
        self.sidebar_label_right.pack(pady=10)
        self.issued_books_listbox = tk.Listbox(self.sidebar_frame_right, font=("Helvetica", 14))
        self.issued_books_listbox.pack(expand=True, fill=tk.BOTH, padx=5, pady=5)
        self.tab_frame = ttk.Frame(self.root)
        self.tab_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.notebook = ttk.Notebook(self.tab_frame)
        self.notebook.pack(pady=10, expand=True, fill='both')
        self.create_add_book_tab()
        self.create_issue_book_tab()
        self.create_return_book_tab()
        self.create_search_book_tab()
        self.load_books_from_db()
        self.update_issued_books()

    def init_db(self):
        self.conn = sqlite3.connect('library.db')
        self.cursor = self.conn.cursor()
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS books (
                title TEXT PRIMARY KEY,
                quantity INTEGER,
                price_per_hour REAL
            )
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS issued_books (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                book_title TEXT,
                customer_name TEXT,
                customer_contact TEXT,
                hours INTEGER,
                issue_time TEXT
            )
        ''')
        self.conn.commit()

    def load_books_from_db(self):
        self.cursor.execute("SELECT title, quantity, price_per_hour FROM books")
        self.books = [Book(row[0], row[1], row[2]) for row in self.cursor.fetchall()]

    def add_book_to_db(self, title, quantity, price_per_hour):
        self.cursor.execute("INSERT INTO books (title, quantity, price_per_hour) VALUES (?, ?, ?)",
                            (title, quantity, price_per_hour))
        self.conn.commit()

    def issue_book_to_db(self, issued_book):
        self.cursor.execute("INSERT INTO issued_books (book_title, customer_name, customer_contact, hours, issue_time) VALUES (?, ?, ?, ?, ?)",
                            (issued_book.book_title, issued_book.customer_name, issued_book.customer_contact, issued_book.hours, issued_book.issue_time.isoformat()))
        self.conn.commit()

    def return_book_in_db(self, book_title):
        self.cursor.execute("DELETE FROM issued_books WHERE book_title = ?", (book_title,))
        self.conn.commit()

    def create_add_book_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Add Book")
        tk.Label(tab, text="Book Title:", font=("Helvetica", 16)).pack(pady=10, padx=10)
        self.title_entry = tk.Entry(tab, font=("Helvetica", 16))
        self.title_entry.pack(pady=10, padx=10)
        tk.Label(tab, text="Quantity:", font=("Helvetica", 16)).pack(pady=10, padx=10)
        self.quantity_entry = tk.Entry(tab, font=("Helvetica", 16))
        self.quantity_entry.pack(pady=10, padx=10)
        tk.Label(tab, text="Price per Hour ($):", font=("Helvetica", 16)).pack(pady=10, padx=10)
        self.price_entry = tk.Entry(tab, font=("Helvetica", 16))
        self.price_entry.pack(pady=10, padx=10)
        tk.Button(tab, text="Add Book", font=("Helvetica", 16), bg="#27ae60", fg="white", command=self.add_book).pack(pady=20)

    def add_book(self):
        title = self.title_entry.get()
        quantity = self.quantity_entry.get()
        price_per_hour = self.price_entry.get()
        if title and quantity.isdigit() and price_per_hour.replace('.', '', 1).isdigit():
            new_book = Book(title, int(quantity), float(price_per_hour))
            self.books.append(new_book)
            self.add_book_to_db(title, int(quantity), float(price_per_hour))
            messagebox.showinfo("Success", f"Book '{title}' added successfully.")
            self.title_entry.delete(0, tk.END)
            self.quantity_entry.delete(0, tk.END)
            self.price_entry.delete(0, tk.END)
            self.update_available_books()
        else:
            messagebox.showerror("Error", "Invalid input!")

    def create_issue_book_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Issue Book")
        tk.Label(tab, text="Book Title:", font=("Helvetica", 16)).pack(pady=10, padx=10)
        self.issue_book_entry = tk.Entry(tab, font=("Helvetica", 16))
        self.issue_book_entry.pack(pady=10, padx=10)
        tk.Label(tab, text="Customer Name:", font=("Helvetica", 16)).pack(pady=10, padx=10)
        self.customer_name_entry = tk.Entry(tab, font=("Helvetica", 16))
        self.customer_name_entry.pack(pady=10, padx=10)
        tk.Label(tab, text="Customer Contact:", font=("Helvetica", 16)).pack(pady=10, padx=10)
        self.customer_contact_entry = tk.Entry(tab, font=("Helvetica", 16))
        self.customer_contact_entry.pack(pady=10, padx=10)
        tk.Label(tab, text="Hours:", font=("Helvetica", 16)).pack(pady=10, padx=10)
        self.hours_entry = tk.Entry(tab, font=("Helvetica", 16))
        self.hours_entry.pack(pady=10, padx=10)
        tk.Button(tab, text="Issue Book", font=("Helvetica", 16), bg="#3498db", fg="white", command=self.issue_book).pack(pady=20)

    def issue_book(self):
        book_title = self.issue_book_entry.get()
        customer_name = self.customer_name_entry.get()
        customer_contact = self.customer_contact_entry.get()
        hours = self.hours_entry.get()
        book = next((b for b in self.books if b.title == book_title), None)
        if book and book.quantity > 0 and hours.isdigit() and int(hours) > 0:
            book.quantity -= 1
            issue_time = datetime.datetime.now()
            issued_book = IssuedBook(book_title, customer_name, customer_contact, int(hours), issue_time)
            self.issued_books.append(issued_book)
            self.issue_book_to_db(issued_book)
            messagebox.showinfo("Success", f"Book '{book_title}' issued to {customer_name} for {hours} hours.")
            self.issue_book_entry.delete(0, tk.END)
            self.customer_name_entry.delete(0, tk.END)
            self.customer_contact_entry.delete(0, tk.END)
            self.hours_entry.delete(0, tk.END)
            self.update_available_books()
            self.update_issued_books()
        else:
            messagebox.showerror("Error", "Invalid book title, no copies available, or invalid hours!")

    def create_return_book_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Return Book")
        tk.Label(tab, text="Book Title:", font=("Helvetica", 16)).pack(pady=10, padx=10)
        self.return_book_entry = tk.Entry(tab, font=("Helvetica", 16))
        self.return_book_entry.pack(pady=10, padx=10)
        tk.Button(tab, text="Return Book", font=("Helvetica", 16), bg="#c0392b", fg="white", command=self.return_book).pack(pady=20)

    def return_book(self):
        book_title = self.return_book_entry.get()
        for issued_book in self.issued_books:
            if issued_book.book_title == book_title:
                self.issued_books.remove(issued_book)
                book = next((b for b in self.books if b.title == book_title), None)
                if book:
                    book.quantity += 1
                issue_duration = datetime.datetime.now() - issued_book.issue_time
                hours_issued = issue_duration.total_seconds() // 3600
                total_price = hours_issued * book.price_per_hour
                self.return_book_in_db(book_title)
                messagebox.showinfo("Success", f"Book '{book_title}' returned. Total cost: ${total_price:.2f}")
                self.return_book_entry.delete(0, tk.END)
                self.update_available_books()
                self.update_issued_books()
                return
        messagebox.showerror("Error", f"Book '{book_title}' is not issued.")

    def create_search_book_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Search Book")
        tk.Label(tab, text="Book Title:", font=("Helvetica", 16)).pack(pady=10, padx=10)
        self.search_book_entry = tk.Entry(tab, font=("Helvetica", 16))
        self.search_book_entry.pack(pady=10, padx=10)
        tk.Button(tab, text="Search Book", font=("Helvetica", 16), bg="#8e44ad", fg="white", command=self.search_book).pack(pady=20)

    def search_book(self):
        book_title = self.search_book_entry.get()
        book = next((b for b in self.books if b.title == book_title), None)
        if book:
            messagebox.showinfo("Book Found", f"'{book_title}' has {book.quantity} copies available.")
        else:
            messagebox.showerror("Not Found", f"No book found with the title '{book_title}'")

    def update_available_books(self, event=None):
        search_query = self.search_entry.get().lower()
        self.available_books_listbox.delete(0, tk.END)
        for book in self.books:
            if search_query in book.title.lower() or not search_query:
                self.available_books_listbox.insert(tk.END, f"{book.title} - {book.quantity} available")

    def update_issued_books(self):
        self.issued_books_listbox.delete(0, tk.END)
        for issued_book in self.issued_books:
            self.issued_books_listbox.insert(tk.END, f"Book - {issued_book.book_title}")

    def __del__(self):
        self.conn.close()

if __name__ == "__main__":
    root = tk.Tk()
    app = LibraryApp(root)
    root.mainloop()

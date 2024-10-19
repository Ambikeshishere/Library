import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import datetime

class Book:
    def __init__(self, title, quantity, price_per_hour):
        self.title = title
        self.quantity = quantity
        self.price_per_hour = price_per_hour

class LibraryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Library Management System")
        self.root.geometry("800x600")
        self.root.configure(bg="#f0f0f0")

        self.books = []  # List to store all books
        self.issued_books = {}  # Dictionary to store issued books with issue time

        # Create the tabbed interface using ttk Notebook
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(pady=10, expand=True)

        # Create tabs
        self.create_add_book_tab()
        self.create_issue_book_tab()
        self.create_return_book_tab()
        self.create_search_book_tab()
        self.create_book_list_tab()

    # Tab 1: Add Book Tab
    def create_add_book_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Add Book")

        # Add book title
        tk.Label(tab, text="Book Title:", font=("Helvetica", 12)).pack(pady=10)
        self.title_entry = tk.Entry(tab, font=("Helvetica", 12))
        self.title_entry.pack(pady=10)

        # Add quantity entry
        tk.Label(tab, text="Quantity:", font=("Helvetica", 12)).pack(pady=10)
        self.quantity_entry = tk.Entry(tab, font=("Helvetica", 12))
        self.quantity_entry.pack(pady=10)

        # Add price per hour entry
        tk.Label(tab, text="Price per Hour ($):", font=("Helvetica", 12)).pack(pady=10)
        self.price_entry = tk.Entry(tab, font=("Helvetica", 12))
        self.price_entry.pack(pady=10)

        # Button to add book
        tk.Button(tab, text="Add Book", font=("Helvetica", 12), bg="#27ae60", fg="white", command=self.add_book).pack(pady=20)

    def add_book(self):
        title = self.title_entry.get()
        quantity = self.quantity_entry.get()
        price_per_hour = self.price_entry.get()
        if title and quantity.isdigit() and price_per_hour.isdigit():
            new_book = Book(title, int(quantity), float(price_per_hour))
            self.books.append(new_book)
            messagebox.showinfo("Success", f"Book '{title}' added successfully.")
            self.title_entry.delete(0, tk.END)
            self.quantity_entry.delete(0, tk.END)
            self.price_entry.delete(0, tk.END)
            self.update_book_list()  # Update the book list after adding a book
        else:
            messagebox.showerror("Error", "Invalid input!")

    # Tab 2: Issue Book Tab
    def create_issue_book_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Issue Book")

        # Add book title entry
        tk.Label(tab, text="Book Title:", font=("Helvetica", 12)).pack(pady=10)
        self.issue_book_entry = tk.Entry(tab, font=("Helvetica", 12))
        self.issue_book_entry.pack(pady=10)

        # Add hours to issue entry
        tk.Label(tab, text="Hours to Issue:", font=("Helvetica", 12)).pack(pady=10)
        self.hours_entry = tk.Entry(tab, font=("Helvetica", 12))
        self.hours_entry.pack(pady=10)

        # Button to issue book
        tk.Button(tab, text="Issue Book", font=("Helvetica", 12), bg="#2980b9", fg="white", command=self.issue_book).pack(pady=20)

    def issue_book(self):
        book_title = self.issue_book_entry.get()
        hours = self.hours_entry.get()
        book = next((b for b in self.books if b.title == book_title), None)

        if book and book.quantity > 0 and hours.isdigit():
            book.quantity -= 1
            issue_time = datetime.datetime.now()
            self.issued_books[book_title] = {
                'hours': int(hours),
                'price_per_hour': book.price_per_hour,
                'issue_time': issue_time
            }
            messagebox.showinfo("Success", f"Book '{book_title}' issued for {hours} hours.")
            self.issue_book_entry.delete(0, tk.END)
            self.hours_entry.delete(0, tk.END)
            self.update_book_list()  # Update the book list after issuing a book
        else:
            messagebox.showerror("Error", "Invalid book title, no copies available, or invalid hours!")

    # Tab 3: Return Book Tab
    def create_return_book_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Return Book")

        # Add book title entry
        tk.Label(tab, text="Book Title:", font=("Helvetica", 12)).pack(pady=10)
        self.return_book_entry = tk.Entry(tab, font=("Helvetica", 12))
        self.return_book_entry.pack(pady=10)

        # Button to return book
        tk.Button(tab, text="Return Book", font=("Helvetica", 12), bg="#c0392b", fg="white", command=self.return_book).pack(pady=20)

    def return_book(self):
        book_title = self.return_book_entry.get()
        if book_title in self.issued_books:
            issue_info = self.issued_books.pop(book_title)
            book = next((b for b in self.books if b.title == book_title), None)
            if book:
                book.quantity += 1

            # Calculate the total price
            issue_duration = datetime.datetime.now() - issue_info['issue_time']
            hours_issued = issue_duration.total_seconds() // 3600
            total_price = hours_issued * issue_info['price_per_hour']

            messagebox.showinfo("Success", f"Book '{book_title}' returned. Total cost: ${total_price:.2f}")
            self.return_book_entry.delete(0, tk.END)
            self.update_book_list()  # Update the book list after returning a book
        else:
            messagebox.showerror("Error", f"Book '{book_title}' is not issued.")

    # Tab 4: Search Book Tab
    def create_search_book_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Search Book")

        # Add book title entry
        tk.Label(tab, text="Book Title:", font=("Helvetica", 12)).pack(pady=10)
        self.search_book_entry = tk.Entry(tab, font=("Helvetica", 12))
        self.search_book_entry.pack(pady=10)

        # Button to search book
        tk.Button(tab, text="Search Book", font=("Helvetica", 12), bg="#8e44ad", fg="white", command=self.search_book).pack(pady=20)

    def search_book(self):
        book_title = self.search_book_entry.get()
        book = next((b for b in self.books if b.title == book_title), None)
        if book:
            messagebox.showinfo("Book Found", f"'{book_title}' has {book.quantity} copies available.")
        else:
            messagebox.showerror("Not Found", f"No book found with the title '{book_title}'")

    # Tab 5: Book List Tab
    def create_book_list_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Book List")

        self.book_list_frame = tk.Frame(tab)
        self.book_list_frame.pack(fill=tk.BOTH, expand=True)

        # Initially show empty list
        self.update_book_list()

    def update_book_list(self):
        for widget in self.book_list_frame.winfo_children():
            widget.destroy()  # Clear existing widgets

        # If no books are present, show a message
        if not self.books:
            tk.Label(self.book_list_frame, text="No books available", font=("Helvetica", 12)).pack(pady=10)
        else:
            for book in self.books:
                tk.Label(self.book_list_frame, text=f"Title: {book.title} | Available Copies: {book.quantity} | Price per hour: ${book.price_per_hour}",
                         font=("Helvetica", 12)).pack(pady=5)


# Run the application
root = tk.Tk()
app = LibraryApp(root)
root.mainloop

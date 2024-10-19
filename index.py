import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import datetime

class Person:
    def __init__(self, name, card_id):
        self.name = name
        self.card_id = card_id
        self.issued_books = []  # List to store issued books for the person

class LibraryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Library Management System")
        self.root.geometry("700x550")
        self.root.configure(bg="#f0f0f0")

        self.books = []  # To store books
        self.people = {}  # Dictionary to store people with card_id as the key
        self.issued_books = {}  # To track issued books (by book title)

        # Main UI setup
        self.create_main_ui()

    def create_main_ui(self):
        # Create a stylish title for the app
        title_frame = tk.Frame(self.root, bg="#2c3e50")
        title_frame.pack(fill=tk.X, pady=10)

        title_label = tk.Label(title_frame, text="Library Management System",
                               font=("Helvetica", 18, "bold"), fg="white", bg="#2c3e50")
        title_label.pack(pady=10)

        # Create a frame for menu buttons
        menu_frame = tk.LabelFrame(self.root, text="Main Menu", font=("Helvetica", 14),
                                   labelanchor="n", padx=20, pady=20, bg="#ecf0f1")
        menu_frame.pack(pady=20)

        # Buttons for main actions
        btn_style = {'font': ("Helvetica", 12), 'width': 20, 'padx': 10, 'pady': 10, 'bg': "#3498db", 'fg': "white"}

        add_book_btn = tk.Button(menu_frame, text="Add Book", **btn_style, command=self.add_book_window)
        add_book_btn.pack(pady=10)

        issue_book_btn = tk.Button(menu_frame, text="Issue Book", **btn_style, command=self.issue_book_window)
        issue_book_btn.pack(pady=10)

        return_book_btn = tk.Button(menu_frame, text="Return Book", **btn_style, command=self.return_book_window)
        return_book_btn.pack(pady=10)

        create_card_btn = tk.Button(menu_frame, text="Create Library Card", **btn_style, command=self.create_card_window)
        create_card_btn.pack(pady=10)

        view_issued_books_btn = tk.Button(menu_frame, text="View Issued Books", **btn_style, command=self.view_issued_books)
        view_issued_books_btn.pack(pady=10)

    def add_book_window(self):
        add_win = tk.Toplevel(self.root)
        add_win.title("Add a Book")
        add_win.geometry("400x300")
        add_win.configure(bg="#f0f0f0")

        # Add book title
        tk.Label(add_win, text="Book Title:", font=("Helvetica", 12), bg="#f0f0f0").pack(pady=10)
        title_entry = tk.Entry(add_win, font=("Helvetica", 12))
        title_entry.pack(pady=10)

        # Add price entry
        tk.Label(add_win, text="Price:", font=("Helvetica", 12), bg="#f0f0f0").pack(pady=10)
        price_entry = tk.Entry(add_win, font=("Helvetica", 12))
        price_entry.pack(pady=10)

        # Button to submit book details
        def add_book():
            title = title_entry.get()
            price = price_entry.get()
            if title and price.isdigit():
                self.books.append({'title': title, 'price': float(price)})
                messagebox.showinfo("Success", f"Book '{title}' added successfully.")
                add_win.destroy()
            else:
                messagebox.showerror("Error", "Invalid input!")

        tk.Button(add_win, text="Add Book", font=("Helvetica", 12), bg="#27ae60", fg="white",
                  command=add_book).pack(pady=20)

    def issue_book_window(self):
        issue_win = tk.Toplevel(self.root)
        issue_win.title("Issue a Book")
        issue_win.geometry("400x400")
        issue_win.configure(bg="#f0f0f0")

        # Add card ID entry
        tk.Label(issue_win, text="Library Card ID:", font=("Helvetica", 12), bg="#f0f0f0").pack(pady=10)
        card_entry = tk.Entry(issue_win, font=("Helvetica", 12))
        card_entry.pack(pady=10)

        # Add book title entry
        tk.Label(issue_win, text="Book Title:", font=("Helvetica", 12), bg="#f0f0f0").pack(pady=10)
        book_entry = tk.Entry(issue_win, font=("Helvetica", 12))
        book_entry.pack(pady=10)

        # Button to issue book
        def issue_book():
            card_id = card_entry.get()
            book_title = book_entry.get()
            person = self.people.get(card_id, None)
            book = next((b for b in self.books if b['title'] == book_title), None)

            if person and book and book_title not in self.issued_books:
                self.issued_books[book_title] = {
                    'person': person.name,
                    'price': book['price'],
                    'issue_time': datetime.datetime.now()
                }
                person.issued_books.append(book_title)
                messagebox.showinfo("Success", f"Book '{book_title}' issued to {person.name}.")
                issue_win.destroy()
            else:
                messagebox.showerror("Error", f"Invalid card ID or book title, or book already issued.")

        tk.Button(issue_win, text="Issue Book", font=("Helvetica", 12), bg="#2980b9", fg="white",
                  command=issue_book).pack(pady=20)

    def return_book_window(self):
        return_win = tk.Toplevel(self.root)
        return_win.title("Return a Book")
        return_win.geometry("400x300")
        return_win.configure(bg="#f0f0f0")

        # Add book title entry
        tk.Label(return_win, text="Book Title:", font=("Helvetica", 12), bg="#f0f0f0").pack(pady=10)
        book_entry = tk.Entry(return_win, font=("Helvetica", 12))
        book_entry.pack(pady=10)

        # Button to return book
        def return_book():
            book_title = book_entry.get()
            if book_title in self.issued_books:
                person_name = self.issued_books[book_title]['person']
                # Remove from person's issued books list
                person = next((p for p in self.people.values() if p.name == person_name), None)
                if person:
                    person.issued_books.remove(book_title)
                del self.issued_books[book_title]
                messagebox.showinfo("Success", f"Book '{book_title}' returned successfully.")
                return_win.destroy()
            else:
                messagebox.showerror("Error", f"Book '{book_title}' is not issued.")

        tk.Button(return_win, text="Return Book", font=("Helvetica", 12), bg="#c0392b", fg="white",
                  command=return_book).pack(pady=20)

    def create_card_window(self):
        card_win = tk.Toplevel(self.root)
        card_win.title("Create Library Card")
        card_win.geometry("400x300")
        card_win.configure(bg="#f0f0f0")

        # Add name entry
        tk.Label(card_win, text="Person's Name:", font=("Helvetica", 12), bg="#f0f0f0").pack(pady=10)
        name_entry = tk.Entry(card_win, font=("Helvetica", 12))
        name_entry.pack(pady=10)

        # Generate and assign a unique card ID
        def create_card():
            name = name_entry.get()
            card_id = str(len(self.people) + 1)  # Simple card ID generation based on the count of people
            if name:
                new_person = Person(name, card_id)
                self.people[card_id] = new_person
                messagebox.showinfo("Success", f"Library Card created for {name}. Card ID: {card_id}")
                card_win.destroy()
            else:
                messagebox.showerror("Error", "Invalid name!")

        tk.Button(card_win, text="Create Card", font=("Helvetica", 12), bg="#27ae60", fg="white",
                  command=create_card).pack(pady=20)

    def view_issued_books(self):
        issued_win = tk.Toplevel(self.root)
        issued_win.title("Issued Books")
        issued_win.geometry("500x400")
        issued_win.configure(bg="#f0f0f0")

        # Create a frame to hold the issued books
        issued_frame = tk.Frame(issued_win, bg="#f0f0f0")
        issued_frame.pack(pady=20)

        if not self.issued_books:
            tk.Label(issued_win, text="No books are currently issued.", font=("Helvetica", 12), bg="#f0f0f0").pack(pady=20)
        else:
            for title, details in self.issued_books.items():
                tk.Label(issued_frame, text=f"Book: {title} | Issued to: {details['person']} | "
                                            f"Price: ${details['price']} | Issue Date/Time: {details['issue_time']}",
                         font=("Helvetica", 12), bg="#f0f0f0").pack(pady=5)


# Run the application
3



root = tk.Tk()
app = LibraryApp(root)
root.mainloop()

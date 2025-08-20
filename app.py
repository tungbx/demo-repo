import json
import os
from datetime import datetime


class Book:
    def __init__(self, book_id, title, author, year, copies=1):
        self.book_id = book_id
        self.title = title
        self.author = author
        self.year = year
        self.copies = copies
        self.borrowed = 0

    def borrow(self):
        if self.available_copies() > 0:
            self.borrowed += 1
            return True
        return False

    def return_book(self):
        if self.borrowed > 0:
            self.borrowed -= 1
            return True
        return False

    def available_copies(self):
        return self.copies - self.borrowed

    def to_dict(self):
        return {
            "book_id": self.book_id,
            "title": self.title,
            "author": self.author,
            "year": self.year,
            "copies": self.copies,
            "borrowed": self.borrowed
        }

    @staticmethod
    def from_dict(data):
        book = Book(data["book_id"], data["title"], data["author"], data["year"], data["copies"])
        book.borrowed = data.get("borrowed", 0)
        return book


class Library:
    def __init__(self, db_file="library.json"):
        self.db_file = db_file
        self.books = {}
        self.load_data()

    def add_book(self, book):
        if book.book_id in self.books:
            print(f"⚠️ Book with ID {book.book_id} already exists.")
        else:
            self.books[book.book_id] = book
            print(f"✅ Added book: {book.title}")

    def search_book(self, keyword):
        results = []
        for book in self.books.values():
            if keyword.lower() in book.title.lower() or keyword.lower() in book.author.lower():
                results.append(book)
        return results

    def borrow_book(self, book_id):
        if book_id in self.books:
            if self.books[book_id].borrow():
                print(f"📕 Borrowed: {self.books[book_id].title}")
            else:
                print("❌ No copies available.")
        else:
            print("❌ Book not found.")

    def return_book(self, book_id):
        if book_id in self.books:
            if self.books[book_id].return_book():
                print(f"📗 Returned: {self.books[book_id].title}")
            else:
                print("⚠️ No borrowed copies to return.")
        else:
            print("❌ Book not found.")

    def list_books(self):
        print("\n===== 📚 Library Books =====")
        if not self.books:
            print("⚠️ No books in library.")
        for book in self.books.values():
            print(f"[{book.book_id}] {book.title} - {book.author} ({book.year}) "
                  f"Copies: {book.copies}, Available: {book.available_copies()}")
        print("============================\n")

    def save_data(self):
        data = {book_id: book.to_dict() for book_id, book in self.books.items()}
        with open(self.db_file, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

    def load_data(self):
        if os.path.exists(self.db_file):
            with open(self.db_file, "r", encoding="utf-8") as f:
                data = json.load(f)
                self.books = {book_id: Book.from_dict(bdata) for book_id, bdata in data.items()}
        else:
            self.books = {}

    def stats(self):
        total_books = sum(book.copies for book in self.books.values())
        total_borrowed = sum(book.borrowed for book in self.books.values())
        print("\n===== 📊 Statistics =====")
        print(f"Total distinct books: {len(self.books)}")
        print(f"Total copies: {total_books}")
        print(f"Borrowed copies: {total_borrowed}")
        print(f"Available copies: {total_books - total_borrowed}")
        print("=========================\n")


def menu():
    print("""
======= 📖 Library Menu =======
1. Add new book
2. Search book
3. Borrow book
4. Return book
5. List all books
6. Show statistics
7. Save and Exit
===============================
""")


def main():
    library = Library()
    while True:
        menu()
        choice = input("👉 Enter choice: ").strip()
        if choice == "1":
            try:
                book_id = input("Enter book ID: ")
                title = input("Enter title: ")
                author = input("Enter author: ")
                year = int(input("Enter year: "))
                copies = int(input("Enter number of copies: "))
                book = Book(book_id, title, author, year, copies)
                library.add_book(book)
            except ValueError:
                print("⚠️ Invalid input.")
        elif choice == "2":
            keyword = input("Enter keyword: ")
            results = library.search_book(keyword)
            if results:
                print("\nSearch results:")
                for book in results:
                    print(f"[{book.book_id}] {book.title} - {book.author} ({book.year})")
            else:
                print("❌ No matching books found.")
        elif choice == "3":
            book_id = input("Enter book ID to borrow: ")
            library.borrow_book(book_id)
        elif choice == "4":
            book_id = input("Enter book ID to return: ")
            library.return_book(book_id)
        elif choice == "5":
            library.list_books()
        elif choice == "6":
            library.stats()
        elif choice == "7":
            library.save_data()
            print("💾 Data saved. Exiting...")
            break
        else:
            print("⚠️ Invalid choice. Try again.")


if __name__ == "__main__":
    main()

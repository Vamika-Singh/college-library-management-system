"""
Library Management System
A terminal-based library management system for a college library.

Uses OOP concepts:
- Class and Object
- Encapsulation (private members with getters/setters)
- Inheritance (Person -> Student, Librarian)
- Polymorphism (method overriding - display_details)
- Abstraction (LibraryOperations abstract class)
- Constructors (__init__)
- Exception Handling (custom exceptions)
"""

import sys
from abc import ABC, abstractmethod

# Ensure terminal supports UTF-8 characters on all platforms (especially Windows CMD/PowerShell)
if sys.platform.startswith("win"):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except AttributeError:
        pass



# ──────────────────────────────────────────────
# Custom Exceptions
# ──────────────────────────────────────────────

class BookNotFoundException(Exception):
    """Raised when a book is not found in the library."""
    def __init__(self, book_id):
        super().__init__(f"Book with ID {book_id} not found.")


class BookAlreadyIssuedException(Exception):
    """Raised when trying to issue a book that is already issued."""
    def __init__(self, book_id):
        super().__init__(f"Book with ID {book_id} is already issued.")


class StudentNotFoundException(Exception):
    """Raised when a student is not found."""
    def __init__(self, student_id):
        super().__init__(f"Student with ID {student_id} not found.")


class BorrowLimitExceededException(Exception):
    """Raised when a student tries to borrow more than 3 books."""
    def __init__(self, student_name):
        super().__init__(f"Student '{student_name}' has already borrowed the maximum of 3 books.")


class BookNotBorrowedByStudentException(Exception):
    """Raised when a student tries to return a book they didn't borrow."""
    def __init__(self, student_name, book_id):
        super().__init__(f"Student '{student_name}' has not borrowed Book ID {book_id}.")


class InvalidIDException(Exception):
    """Raised when an invalid ID is entered."""
    def __init__(self, id_value):
        super().__init__(f"Invalid ID entered: '{id_value}'. ID must be a positive integer.")


# ──────────────────────────────────────────────
# Book Class (Encapsulation + Constructor)
# ──────────────────────────────────────────────

class Book:
    """Represents a book in the library."""

    def __init__(self, book_id, book_name, author_name):
        """Constructor to initialize a Book object."""
        self.__book_id = book_id            # Private
        self.__book_name = book_name        # Private
        self.__author_name = author_name    # Private
        self.__is_available = True          # Private — True = Available, False = Issued

    # --- Getters ---
    def get_book_id(self):
        return self.__book_id

    def get_book_name(self):
        return self.__book_name

    def get_author_name(self):
        return self.__author_name

    def is_available(self):
        return self.__is_available

    # --- Setters ---
    def set_book_name(self, name):
        self.__book_name = name

    def set_author_name(self, author):
        self.__author_name = author

    def set_availability(self, status):
        """Change availability status."""
        self.__is_available = status

    def display_details(self):
        """Display book details."""
        status = "Available" if self.__is_available else "Issued"
        print(f"  Book ID    : {self.__book_id}")
        print(f"  Book Name  : {self.__book_name}")
        print(f"  Author     : {self.__author_name}")
        print(f"  Status     : {status}")

    def __str__(self):
        status = "Available" if self.__is_available else "Issued"
        return f"[{self.__book_id}] {self.__book_name} by {self.__author_name} — {status}"


# ──────────────────────────────────────────────
# Person Class — Parent (Inheritance base)
# ──────────────────────────────────────────────

class Person:
    """Parent class with common properties: id and name."""

    def __init__(self, person_id, name):
        """Constructor to initialize common Person properties."""
        self._id = person_id    # Protected
        self._name = name       # Protected

    # --- Getters ---
    def get_id(self):
        return self._id

    def get_name(self):
        return self._name

    # --- Setters ---
    def set_name(self, name):
        self._name = name

    def display_details(self):
        """Base display — overridden by child classes (Polymorphism)."""
        print(f"  ID   : {self._id}")
        print(f"  Name : {self._name}")


# ──────────────────────────────────────────────
# Student Class — Inherits Person (Polymorphism)
# ──────────────────────────────────────────────

class Student(Person):
    """Represents a student who can borrow books. Inherits from Person."""

    MAX_BORROW_LIMIT = 3

    def __init__(self, student_id, name, department):
        """Constructor to initialize a Student object."""
        super().__init__(student_id, name)
        self.__department = department          # Private
        self.__borrowed_books = []              # Private — list of Book objects

    # --- Getters ---
    def get_department(self):
        return self.__department

    def get_borrowed_books(self):
        return list(self.__borrowed_books)  # Return a copy

    # --- Setters ---
    def set_department(self, department):
        self.__department = department

    def borrow_book(self, book):
        """Borrow a book (adds to borrowed list)."""
        if len(self.__borrowed_books) >= Student.MAX_BORROW_LIMIT:
            raise BorrowLimitExceededException(self._name)
        if not book.is_available():
            raise BookAlreadyIssuedException(book.get_book_id())
        self.__borrowed_books.append(book)
        book.set_availability(False)

    def return_book(self, book_id):
        """Return a book by its ID."""
        for book in self.__borrowed_books:
            if book.get_book_id() == book_id:
                self.__borrowed_books.remove(book)
                book.set_availability(True)
                return book
        raise BookNotBorrowedByStudentException(self._name, book_id)

    def display_details(self):
        """Overridden method — Polymorphism (Student version)."""
        print(f"  Student ID   : {self._id}")
        print(f"  Student Name : {self._name}")
        print(f"  Department   : {self.__department}")
        if self.__borrowed_books:
            print(f"  Borrowed Books ({len(self.__borrowed_books)}/{Student.MAX_BORROW_LIMIT}):")
            for book in self.__borrowed_books:
                print(f"    - {book}")
        else:
            print(f"  Borrowed Books : None")


# ──────────────────────────────────────────────
# Librarian Class — Inherits Person (Polymorphism)
# ──────────────────────────────────────────────

class Librarian(Person):
    """Represents a librarian. Inherits from Person."""

    def __init__(self, librarian_id, name):
        """Constructor to initialize a Librarian object."""
        super().__init__(librarian_id, name)

    def display_details(self):
        """Overridden method — Polymorphism (Librarian version)."""
        print(f"  Librarian ID   : {self._id}")
        print(f"  Librarian Name : {self._name}")
        print(f"  Role           : Library Administrator")


# ──────────────────────────────────────────────
# LibraryOperations — Abstract Class (Abstraction)
# ──────────────────────────────────────────────

class LibraryOperations(ABC):
    """Abstract class defining core library operations."""

    @abstractmethod
    def issue_book(self, book_id, student_id):
        """Issue a book to a student."""
        pass

    @abstractmethod
    def return_book(self, book_id, student_id):
        """Accept a returned book from a student."""
        pass


# ──────────────────────────────────────────────
# Library Class — Implements LibraryOperations
# ──────────────────────────────────────────────

class Library(LibraryOperations):
    """
    Main Library class that manages books, students, and operations.
    Implements the LibraryOperations abstract class.
    """

    def __init__(self):
        """Constructor to initialize the Library."""
        self.__books = {}       # Private — {book_id: Book}
        self.__students = {}    # Private — {student_id: Student}
        self.__librarian = Librarian(1, "Admin Librarian")

    # --- Getters ---
    def get_librarian(self):
        return self.__librarian

    # ──── Book Management ────

    def add_book(self, book_id, book_name, author_name):
        """Add a new book to the library."""
        if book_id in self.__books:
            print(f"\n  ⚠  Book with ID {book_id} already exists.")
            return
        book = Book(book_id, book_name, author_name)
        self.__books[book_id] = book
        print(f"\n  ✓  Book '{book_name}' added successfully.")

    def view_all_books(self):
        """Display all books in the library."""
        if not self.__books:
            print("\n  No books in the library.")
            return
        print(f"\n  {'='*50}")
        print(f"  {'ALL BOOKS IN LIBRARY':^50}")
        print(f"  {'='*50}")
        for book in self.__books.values():
            print(f"  {'-'*50}")
            book.display_details()
        print(f"  {'-'*50}")
        print(f"  Total books: {len(self.__books)}")

    def find_book(self, book_id):
        """Find a book by its ID."""
        if book_id not in self.__books:
            raise BookNotFoundException(book_id)
        return self.__books[book_id]

    # ──── Student Management ────

    def add_student(self, student_id, name, department):
        """Add a new student."""
        if student_id in self.__students:
            print(f"\n  ⚠  Student with ID {student_id} already exists.")
            return
        student = Student(student_id, name, department)
        self.__students[student_id] = student
        print(f"\n  ✓  Student '{name}' added successfully.")

    def find_student(self, student_id):
        """Find a student by their ID."""
        if student_id not in self.__students:
            raise StudentNotFoundException(student_id)
        return self.__students[student_id]

    def view_student_details(self, student_id):
        """Display a student's details."""
        student = self.find_student(student_id)
        print(f"\n  {'='*50}")
        print(f"  {'STUDENT DETAILS':^50}")
        print(f"  {'='*50}")
        student.display_details()
        print(f"  {'='*50}")

    # ──── LibraryOperations Implementation (Abstraction) ────

    def issue_book(self, book_id, student_id):
        """Issue a book to a student. Implements abstract method."""
        book = self.find_book(book_id)
        student = self.find_student(student_id)
        student.borrow_book(book)
        print(f"\n  ✓  Book '{book.get_book_name()}' issued to student '{student.get_name()}'.")

    def return_book(self, book_id, student_id):
        """Accept a returned book. Implements abstract method."""
        self.find_book(book_id)  # Verify book exists in library
        student = self.find_student(student_id)
        returned_book = student.return_book(book_id)
        print(f"\n  ✓  Book '{returned_book.get_book_name()}' returned by student '{student.get_name()}'.")


# ──────────────────────────────────────────────
# Helper: Validate and parse integer ID
# ──────────────────────────────────────────────

def get_valid_id(prompt):
    """Prompt user for a valid positive integer ID."""
    raw = input(prompt).strip()
    try:
        value = int(raw)
        if value <= 0:
            raise InvalidIDException(raw)
        return value
    except ValueError:
        raise InvalidIDException(raw)


# ──────────────────────────────────────────────
# Main Menu — Terminal Interface
# ──────────────────────────────────────────────

def display_menu():
    """Display the main menu."""
    print("\n" + "=" * 54)
    print("  ╔══════════════════════════════════════════════════╗")
    print("  ║          LIBRARY MANAGEMENT SYSTEM               ║")
    print("  ╚══════════════════════════════════════════════════╝")
    print("=" * 54)
    print("  1. Add Book")
    print("  2. View All Books")
    print("  3. Add Student")
    print("  4. Issue Book")
    print("  5. Return Book")
    print("  6. View Student Details")
    print("  7. View Librarian Details")
    print("  8. Search Book by ID")
    print("  9. Exit")
    print("=" * 54)


def main():
    """Main function — entry point of the program."""
    library = Library()

    while True:
        display_menu()
        choice = input("  Enter your choice (1-9): ").strip()

        try:
            if choice == "1":
                # ── Add Book ──
                print("\n  --- Add a New Book ---")
                book_id = get_valid_id("  Enter Book ID: ")
                book_name = input("  Enter Book Name: ").strip()
                if not book_name:
                    print("\n  ⚠  Book name cannot be empty.")
                    continue
                author_name = input("  Enter Author Name: ").strip()
                if not author_name:
                    print("\n  ⚠  Author name cannot be empty.")
                    continue
                library.add_book(book_id, book_name, author_name)

            elif choice == "2":
                # ── View All Books ──
                library.view_all_books()

            elif choice == "3":
                # ── Add Student ──
                print("\n  --- Add a New Student ---")
                student_id = get_valid_id("  Enter Student ID: ")
                student_name = input("  Enter Student Name: ").strip()
                if not student_name:
                    print("\n  ⚠  Student name cannot be empty.")
                    continue
                department = input("  Enter Department: ").strip()
                if not department:
                    print("\n  ⚠  Department cannot be empty.")
                    continue
                library.add_student(student_id, student_name, department)

            elif choice == "4":
                # ── Issue Book ──
                print("\n  --- Issue a Book ---")
                book_id = get_valid_id("  Enter Book ID to issue: ")
                student_id = get_valid_id("  Enter Student ID: ")
                library.issue_book(book_id, student_id)

            elif choice == "5":
                # ── Return Book ──
                print("\n  --- Return a Book ---")
                book_id = get_valid_id("  Enter Book ID to return: ")
                student_id = get_valid_id("  Enter Student ID: ")
                library.return_book(book_id, student_id)

            elif choice == "6":
                # ── View Student Details ──
                print("\n  --- View Student Details ---")
                student_id = get_valid_id("  Enter Student ID: ")
                library.view_student_details(student_id)

            elif choice == "7":
                # ── View Librarian Details ──
                print(f"\n  {'='*50}")
                print(f"  {'LIBRARIAN DETAILS':^50}")
                print(f"  {'='*50}")
                library.get_librarian().display_details()
                print(f"  {'='*50}")

            elif choice == "8":
                # ── Search Book by ID ──
                print("\n  --- Search Book by ID ---")
                book_id = get_valid_id("  Enter Book ID: ")
                book = library.find_book(book_id)
                print(f"\n  {'='*50}")
                print(f"  {'BOOK DETAILS':^50}")
                print(f"  {'='*50}")
                book.display_details()
                print(f"  {'='*50}")

            elif choice == "9":
                # ── Exit ──
                print("\n  Thank you for using the Library Management System!")
                print("  Goodbye!\n")
                break

            else:
                print("\n  ⚠  Invalid choice. Please enter a number between 1 and 9.")

        except BookNotFoundException as e:
            print(f"\n  ✗  Error: {e}")
        except BookAlreadyIssuedException as e:
            print(f"\n  ✗  Error: {e}")
        except StudentNotFoundException as e:
            print(f"\n  ✗  Error: {e}")
        except BorrowLimitExceededException as e:
            print(f"\n  ✗  Error: {e}")
        except BookNotBorrowedByStudentException as e:
            print(f"\n  ✗  Error: {e}")
        except InvalidIDException as e:
            print(f"\n  ✗  Error: {e}")
        except KeyboardInterrupt:
            print("\n\n  Program interrupted. Goodbye!\n")
            break


if __name__ == "__main__":
    main()

# 📚 College Library Management System

A beautiful, robust, and clean **terminal-based Library Management System** designed for a college library. 

This project is built from the ground up using **Object-Oriented Programming (OOP) concepts in Python** and features custom exception handling, a rich text-based CLI (with fallback UTF-8 encoding support for cross-platform stability), and a comprehensive programmatic test suite.

---

## 🌟 Key Features

- **Book Management**: Add, search, and view all books with detailed availability statuses.
- **Student Management**: Add students, maintain their department information, and track borrowed books.
- **Librarian Administration**: Display admin credentials and manage transaction operations.
- **Issue & Return System**: Easily issue books to students and accept returns, automatically managing book availability.
- **Robust Validation**: Enforces positive integer IDs, non-empty fields, and checks borrowing rules.
- **Cross-Platform UTF-8 Console Support**: Automatically detects and adjusts console encoding on Windows platforms to display nice borders and status icons safely without crashing.

---

## 🛠️ Object-Oriented Programming (OOP) Breakdown

This application serves as an excellent demonstration of standard software engineering OOP practices in Python:

### 1. Class and Object
Every entity in the system is represented as a Class, from which active instances (Objects) are created:
- **`Book`**: Represents physical book items in the library.
- **`Student`**: Represents college student members who borrow books.
- **`Librarian`**: Represents library administrators managing the system.
- **`Library`**: Represents the main coordinating body implementing operations.

### 2. Encapsulation (Private & Protected Members)
Data hiding and state protection are strictly enforced:
- **Private Members (`__`)**: `Book` properties (like `__book_id`, `__book_name`, `__author_name`, `__is_available`) and `Student` properties (like `__department`, `__borrowed_books`) are private. They cannot be modified directly from outside the class.
- **Getters & Setters**: Exposed safe methods (like `get_book_id()`, `is_available()`, `set_availability(status)`) are used to access or modify these private variables securely.
- **Protected Members (`_`)**: The base class `Person` uses protected variables `_id` and `_name` to allow direct access from child classes (`Student` and `Librarian`) while signaling they shouldn't be touched by external modules.

### 3. Inheritance
To avoid code duplication and establish hierarchical relationships:
- The base class `Person` encapsulates common attributes of individuals (like `_id` and `_name`).
- Both **`Student`** and **`Librarian`** inherit from **`Person`**, utilizing `super().__init__(id, name)` to initialize the parent constructor and reuse its properties.

```python
class Person:
    def __init__(self, person_id, name):
        self._id = person_id
        self._name = name

class Student(Person):
    def __init__(self, student_id, name, department):
        super().__init__(student_id, name)
        self.__department = department
        # ...
```

### 4. Polymorphism (Method Overriding)
Different classes respond to the same method name in their own specialized way:
- The `display_details()` method is defined in `Person` and overridden in both `Student` and `Librarian` to print custom, relevant information for each role:
  - `Librarian.display_details()` prints administrative role information.
  - `Student.display_details()` lists their department and a breakdown of their currently borrowed books.

### 5. Abstraction
Using Python's Built-in Abstract Base Classes (`abc` module):
- **`LibraryOperations`** is defined as an abstract class inheriting from `ABC`.
- It defines abstract methods `issue_book` and `return_book` decorated with `@abstractmethod`.
- The main **`Library`** class implements these abstract methods, guaranteeing the interface contract is strictly obeyed.

```python
from abc import ABC, abstractmethod

class LibraryOperations(ABC):
    @abstractmethod
    def issue_book(self, book_id, student_id):
        pass

    @abstractmethod
    def return_book(self, book_id, student_id):
        pass
```

---

## ⚠️ Custom Exceptions and Business Logic

The system utilizes a custom exception hierarchy to handle business logic constraints and input validation gracefully. All exceptions inherit from Python's base `Exception`:

| Exception Class | Raised When... |
| :--- | :--- |
| `BookNotFoundException` | Searching or issuing a book that does not exist in the library. |
| `BookAlreadyIssuedException` | Attempting to borrow a book that is currently marked as unavailable. |
| `StudentNotFoundException` | Attempting to fetch details or issue a book to an unregistered student ID. |
| `BorrowLimitExceededException` | A student attempts to borrow a book when they already have **3 books** checked out (defined by `MAX_BORROW_LIMIT`). |
| `BookNotBorrowedByStudentException` | A student tries to return a book that they never borrowed. |
| `InvalidIDException` | Entering non-integer text or non-positive values for Book or Student IDs. |

---

## 📂 Project Structure

```
library-management-system/
├── main.py            # Main application containing classes and interactive terminal menu
├── test_library.py    # Automated programmatic test suite verifying OOP logic and exceptions
└── README.md          # Comprehensive documentation (this file!)
```

---

## 🚀 Getting Started

### Prerequisites
- Python 3.7 or higher installed on your system.

### Running the Interactive Console App
Run the main file in your terminal to start the interactive management console:
```bash
python main.py
```

You will see a beautiful terminal menu:
```text
======================================================
  ╔══════════════════════════════════════════════════╗
  ║          LIBRARY MANAGEMENT SYSTEM               ║
  ╚══════════════════════════════════════════════════╝
======================================================
  1. Add Book
  2. View All Books
  3. Add Student
  4. Issue Book
  5. Return Book
  6. View Student Details
  7. View Librarian Details
  8. Search Book by ID
  9. Exit
======================================================
  Enter your choice (1-9):
```

### Running the Programmatic Test Suite
An automated verification script is included to immediately test and prove all class structures, encapsulation rules, limits, and custom exceptions programmatically:
```bash
python test_library.py
```

---

## 📝 License
This project is open-source and free to use under the MIT License. Feel free to clone, modify, and showcase this project on your GitHub portfolio!

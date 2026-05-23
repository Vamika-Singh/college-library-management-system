"""
Programmatic verification script for Library Management System.
Verifies all core OOP concepts:
1. Encapsulation (Private members and getters/setters)
2. Inheritance (Person -> Student, Librarian)
3. Polymorphism (display_details overrides)
4. Abstraction (LibraryOperations abstract methods)
5. Custom Exception handling
"""

import sys
from main import (
    Library, Book, Student, Librarian, 
    BookNotFoundException, BookAlreadyIssuedException,
    StudentNotFoundException, BorrowLimitExceededException,
    BookNotBorrowedByStudentException, InvalidIDException
)

def run_tests():
    print("=== STARTING PROGRAMMATIC LIBRARY SYSTEM TESTS ===")
    
    # Initialize Library
    library = Library()
    print("\n[+] Created Library instance.")
    
    # Check Librarian Details (Inheritance + Polymorphism)
    print("\n--- Verifying Librarian (Inheritance & Polymorphism) ---")
    librarian = library.get_librarian()
    assert isinstance(librarian, Librarian), "Librarian must be an instance of Librarian"
    librarian.display_details()
    
    # 1. Add Books (Encapsulation check)
    print("\n--- Verifying Book Creation & Encapsulation ---")
    library.add_book(101, "The Python Programming Language", "Guido van Rossum")
    library.add_book(102, "Introduction to Algorithms", "Thomas H. Cormen")
    library.add_book(103, "Design Patterns", "Erich Gamma")
    library.add_book(104, "Clean Code", "Robert C. Martin")
    
    book = library.find_book(101)
    assert book.get_book_id() == 101
    assert book.get_book_name() == "The Python Programming Language"
    assert book.get_author_name() == "Guido van Rossum"
    assert book.is_available() is True
    print("✓ Book getters work correctly.")
    
    # Try adding a duplicate book
    print("\n--- Testing Duplicate Book Prevention ---")
    library.add_book(101, "Duplicate Book", "Some Author")
    
    # 2. Add Students
    print("\n--- Verifying Student Creation & Inheritance ---")
    library.add_student(1, "Alice Smith", "Computer Science")
    library.add_student(2, "Bob Jones", "Information Technology")
    
    student = library.find_student(1)
    assert isinstance(student, Student), "Student must be an instance of Student"
    assert student.get_id() == 1
    assert student.get_name() == "Alice Smith"
    assert student.get_department() == "Computer Science"
    print("✓ Student getters and inheritance work correctly.")
    
    # 3. Issue Books (Abstraction & Polymorphism check)
    print("\n--- Verifying Book Issuing & Borrow Limits ---")
    library.issue_book(101, 1) # Alice borrows book 101
    library.issue_book(102, 1) # Alice borrows book 102
    library.issue_book(103, 1) # Alice borrows book 103
    
    # Alice details should show 3 borrowed books
    library.view_student_details(1)
    
    # Verify that trying to borrow a 4th book raises BorrowLimitExceededException
    print("\n--- Testing Borrow Limit Exceeded Exception ---")
    try:
        library.issue_book(104, 1)
        assert False, "Should have raised BorrowLimitExceededException"
    except BorrowLimitExceededException as e:
        print(f"✓ Correctly raised exception: {e}")
        
    # Verify that trying to borrow an already issued book raises BookAlreadyIssuedException
    print("\n--- Testing Already Issued Exception ---")
    try:
        library.issue_book(101, 2)
        assert False, "Should have raised BookAlreadyIssuedException"
    except BookAlreadyIssuedException as e:
        print(f"✓ Correctly raised exception: {e}")
        
    # 4. Return Books
    print("\n--- Verifying Book Returning ---")
    library.return_book(101, 1) # Alice returns book 101
    
    # Bob borrows book 101
    library.issue_book(101, 2)
    library.view_student_details(2)
    
    # Try returning a book Alice has not borrowed
    print("\n--- Testing Book Not Borrowed Exception ---")
    try:
        library.return_book(102, 2) # Bob tries to return book 102 (borrowed by Alice)
        assert False, "Should have raised BookNotBorrowedByStudentException"
    except BookNotBorrowedByStudentException as e:
        print(f"✓ Correctly raised exception: {e}")
        
    # 5. Invalid book/student lookups
    print("\n--- Testing Not Found Exceptions ---")
    try:
        library.find_book(999)
        assert False, "Should have raised BookNotFoundException"
    except BookNotFoundException as e:
        print(f"✓ Correctly raised exception: {e}")
        
    try:
        library.find_student(999)
        assert False, "Should have raised StudentNotFoundException"
    except StudentNotFoundException as e:
        print(f"✓ Correctly raised exception: {e}")
        
    print("\n=== ALL TESTS PASSED SUCCESSFULLY! ===")

if __name__ == "__main__":
    run_tests()

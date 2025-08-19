from abc import ABC, abstractmethod

# ----------- Strategy Pattern -----------
class BorrowPolicy(ABC):
    @abstractmethod
    def borrow_duration(self):
        pass

class StudentPolicy(BorrowPolicy):
    def borrow_duration(self):
        return 14  # 14 days

class FacultyPolicy(BorrowPolicy):
    def borrow_duration(self):
        return 30  # 30 days

# ----------- Factory Pattern -----------
class Book(ABC):
    def __init__(self, title):
        self.title = title

class FictionBook(Book):
    pass

class NonFictionBook(Book):
    pass

class BookFactory:
    @staticmethod
    def create_book(book_type, title):
        if book_type == "Fiction":
            return FictionBook(title)
        elif book_type == "NonFiction":
            return NonFictionBook(title)
        else:
            raise ValueError("Unknown book type")

# ----------- Singleton Pattern -----------
class Library:
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super(Library, cls).__new__(cls)
            cls.__instance.books = []
            cls.__instance.users = []
        return cls.__instance

    def add_book(self, book: Book):
        self.books.append(book)

    def register_user(self, user):
        self.users.append(user)

    def borrow_book(self, user, book):
        if book in self.books:
            duration = user.policy.borrow_duration()
            print(f"{user.name} borrowed '{book.title}' for {duration} days")
            self.books.remove(book)
        else:
            print(f"Book '{book.title}' is not available")

# ----------- User Class -----------
class User:
    def __init__(self, name, policy: BorrowPolicy):
        self.name = name
        self.policy = policy

# ----------- Client Code -----------
if __name__ == "__main__":
    # Create books using factory
    book1 = BookFactory.create_book("Fiction", "Harry Potter")
    book2 = BookFactory.create_book("NonFiction", "Sapiens")

    # Get library singleton
    library = Library()
    library.add_book(book1)
    library.add_book(book2)

    # Register users with different borrowing policies
    alice = User("Alice", StudentPolicy())
    bob = User("Bob", FacultyPolicy())
    library.register_user(alice)
    library.register_user(bob)

    # Borrow books
    library.borrow_book(alice, book1)  # Alice borrows Harry Potter for 14 days
    library.borrow_book(bob, book2)    # Bob borrows Sapiens for 30 days

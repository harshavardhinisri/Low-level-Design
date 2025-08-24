from abc import ABC, abstractmethod
import threading

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

# ----------- Borrow Policy Factory -----------
class BorrowPolicyFactory:
    policy_map = {
        "student": StudentPolicy,
        "faculty": FacultyPolicy
    }

    @staticmethod
    def create_policy(policy_type: str) -> BorrowPolicy:
        policy_cls = BorrowPolicyFactory.policy_map.get(policy_type.lower())
        if not policy_cls:
            raise ValueError(f"Unknown policy type: {policy_type}")
        return policy_cls()

# ----------- Factory Pattern -----------
class Book(ABC):
    def __init__(self, title):
        self.title = title

class FictionBook(Book):
    pass

class NonFictionBook(Book):
    pass

class BookFactory:
    book_map = {
        "fiction": FictionBook,
        "nonfiction": NonFictionBook
    }

    @staticmethod
    def create_book(book_type: str, title: str) -> Book:
        book_cls = BookFactory.book_map.get(book_type.lower())
        if not book_cls:
            raise ValueError(f"Unknown book type: {book_type}")
        return book_cls(title)

# ----------- Singleton Pattern -----------
class Library:
    __instance = None
    __lock = threading.Lock()

    def __init__(self):
        if Library.__instance is not None:
            raise Exception("Use get_instance() instead of creating Library directly")
        self.__books = []
        self.__users = []

    @classmethod
    def get_instance(cls):
        if cls.__instance is None:
            with cls.__lock:
                if cls.__instance is None:
                    cls.__instance = super(Library, cls).__new__(cls)
                    cls.__instance.__books = []
                    cls.__instance.__users = []
        return cls.__instance

    def add_book(self, book: Book):
        self.__books.append(book)

    def register_user(self, user):
        self.__users.append(user)

    def borrow_book(self, user, book):
        if book in self.__books:
            duration = user.policy.borrow_duration()
            print(f"{user.name} borrowed '{book.title}' for {duration} days")
            self.__books.remove(book)
        else:
            print(f"Book '{book.title}' is not available")

# ----------- User Factory -----------
class User:
    def __init__(self, name: str, policy: BorrowPolicy):
        self.name = name
        self.policy = policy

class UserFactory:
    @staticmethod
    def create_user(name: str, policy_type: str) -> User:
        policy = BorrowPolicyFactory.create_policy(policy_type)
        return User(name, policy)

# ----------- Client Code (No direct object creation) -----------
if __name__ == "__main__":
    library = Library.get_instance()  # Singleton accessor

    # Create books via factory
    books_to_add = [
        ("fiction", "Harry Potter"),
        ("nonfiction", "Sapiens")
    ]
    for book_type, title in books_to_add:
        library.add_book(BookFactory.create_book(book_type, title))

    # Create users via factory
    users_to_register = [
        ("Alice", "student"),
        ("Bob", "faculty")
    ]
    users = []
    for name, policy_type in users_to_register:
        user = UserFactory.create_user(name, policy_type)
        library.register_user(user)
        users.append(user)

    # Borrow books
    library.borrow_book(users[0], BookFactory.create_book("fiction", "Harry Potter"))
    library.borrow_book(users[1], BookFactory.create_book("nonfiction", "Sapiens"))

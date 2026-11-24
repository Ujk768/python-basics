from abc import ABC, abstractmethod
from collections import deque
from datetime import datetime, timedelta
from enum import Enum


# ---------------------------------------------------------------- errors
class LibraryError(Exception):
    """Base class so callers can catch every library problem at once."""


class CopyNotAvailableError(LibraryError):
    pass


class BorrowLimitExceededError(LibraryError):
    pass


class LoanNotFoundError(LibraryError):
    pass


class LoanAlreadyClosedError(LibraryError):
    pass


class CopyAlreadyLoanedError(LibraryError):
    pass


class InvalidCopyTransitionError(LibraryError):
    pass


class ReservationError(LibraryError):
    pass


# ---------------------------------------------------------------- enums
class CopyStatus(Enum):
    AVAILABLE = "available"
    BORROWED = "borrowed"
    RESERVED = "reserved"
    LOST = "lost"


class MembershipType(Enum):
    REGULAR = "regular"
    PREMIUM = "premium"
    STUDENT = "student"


# ---------------------------------------------------------------- entities
class Book:
    def __init__(self, title: str, author: str, year: int, isbn: str):
        self.title = title
        self.author = author
        self.year = year
        self.isbn = isbn


class BookCopy:
    def __init__(self, book: Book, copy_id: str):
        self.book = book
        self.copy_id = copy_id
        self.status = CopyStatus.AVAILABLE

    def mark_borrowed(self):
        if self.status != CopyStatus.AVAILABLE:
            raise CopyNotAvailableError(
                f"Copy {self.copy_id} is {self.status.value}, cannot be borrowed"
            )
        self.status = CopyStatus.BORROWED

    def mark_available(self):
        # Legal sources: BORROWED (returned) and RESERVED (hold released)
        if self.status not in (CopyStatus.BORROWED, CopyStatus.RESERVED):
            raise InvalidCopyTransitionError(
                f"Copy {self.copy_id} is {self.status.value}, cannot be made available"
            )
        self.status = CopyStatus.AVAILABLE

    def mark_reserved(self):
        # A hold is placed on a copy that has just become free
        if self.status != CopyStatus.AVAILABLE:
            raise InvalidCopyTransitionError(
                f"Copy {self.copy_id} is {self.status.value}, cannot be reserved"
            )
        self.status = CopyStatus.RESERVED

    def mark_lost(self):
        self.status = CopyStatus.LOST


class Member:
    LIMITS = {
        MembershipType.STUDENT: 3,
        MembershipType.REGULAR: 5,
        MembershipType.PREMIUM: 10,
    }

    def __init__(self, name: str, member_id: str, membership_type: MembershipType):
        self.name = name
        self.member_id = member_id
        self.membership_type = membership_type
        self.borrow_limit = self.LIMITS[self.membership_type]


class Loan:
    def __init__(self, book_copy: BookCopy, member: Member,
                 loan_date: datetime, due_date: datetime):
        self.book_copy = book_copy
        self.member = member
        self.loan_date = loan_date
        self.due_date = due_date
        self.return_date = None

    @property
    def is_active(self) -> bool:
        return self.return_date is None

    def close(self, return_date: datetime) -> None:
        if not self.is_active:
            raise LoanAlreadyClosedError("Loan already closed")
        self.return_date = return_date

    def days_overdue(self, as_of: datetime) -> int:
        return max(0, (as_of - self.due_date).days)


# ---------------------------------------------------------------- fines (Strategy)
class Fine(ABC):
    @abstractmethod
    def calculate_fine(self, days_overdue: int):
        pass


class FlatPerDayRate(Fine):
    def __init__(self, fine_amount: int):
        self.fine_amount = fine_amount

    def calculate_fine(self, days_overdue: int):
        return self.fine_amount * days_overdue


class TieredFine(Fine):
    """First `tier_days` days at `low_rate`, later days at `high_rate`, capped."""

    def __init__(self, low_rate: int, high_rate: int, tier_days: int, cap: int):
        self.low_rate = low_rate
        self.high_rate = high_rate
        self.tier_days = tier_days
        self.cap = cap

    def calculate_fine(self, days_overdue: int):
        low_days = min(days_overdue, self.tier_days)
        high_days = max(0, days_overdue - self.tier_days)
        return min(self.cap, low_days * self.low_rate + high_days * self.high_rate)


# ---------------------------------------------------------------- registry
class LoanRegistry:
    def __init__(self):
        self.active_by_copy = {}    # copy_id   -> Loan
        self.active_by_member = {}  # member_id -> [Loan]

    def add(self, loan: Loan):
        copy_id = loan.book_copy.copy_id
        if copy_id in self.active_by_copy:
            raise CopyAlreadyLoanedError(f"Copy {copy_id} is already on loan")
        self.active_by_copy[copy_id] = loan
        self.active_by_member.setdefault(loan.member.member_id, []).append(loan)

    def close(self, copy_id: str) -> Loan:
        loan = self.active_by_copy.pop(copy_id, None)
        if loan is None:
            raise LoanNotFoundError(f"Copy {copy_id} has no active loan")
        member_id = loan.member.member_id
        member_loans = self.active_by_member[member_id]
        member_loans.remove(loan)
        if not member_loans:
            del self.active_by_member[member_id]
        return loan

    def get_active_loan(self, copy_id: str):
        return self.active_by_copy.get(copy_id)

    def active_count(self, member: Member) -> int:
        return len(self.active_by_member.get(member.member_id, []))


# ---------------------------------------------------------------- reservations
class ReservationManager:
    """FIFO queue of waiting members per book (by ISBN), plus holds on copies."""

    def __init__(self):
        self.queues = {}  # isbn -> deque[Member]
        self.holds = {}   # copy_id -> Member

    def enqueue(self, member: Member, isbn: str):
        queue = self.queues.setdefault(isbn, deque())
        if member in queue:
            raise ReservationError(f"{member.name} is already waiting for this book")
        queue.append(member)

    def pop_next(self, isbn: str):
        queue = self.queues.get(isbn)
        if not queue:
            return None
        member = queue.popleft()
        if not queue:
            del self.queues[isbn]
        return member

    def place_hold(self, copy_id: str, member: Member):
        self.holds[copy_id] = member

    def held_for(self, copy_id: str):
        return self.holds.get(copy_id)

    def release_hold(self, copy_id: str):
        self.holds.pop(copy_id, None)


# ---------------------------------------------------------------- library (coordinator)
class Library:
    def __init__(self, loan_registry: LoanRegistry, fine: Fine,
                 reservations: ReservationManager = None, loan_period_days: int = 14):
        self.loan_registry = loan_registry
        self.fine = fine
        self.reservations = reservations or ReservationManager()
        self.loan_period = timedelta(days=loan_period_days)
        self.books = {}          # isbn -> Book
        self.copies = {}         # copy_id -> BookCopy
        self.notifications = []  # (member, message); stand-in for a real notifier

    # ---- catalog
    def add_book(self, book: Book):
        self.books[book.isbn] = book

    def add_copy(self, copy: BookCopy):
        if copy.book.isbn not in self.books:
            self.add_book(copy.book)
        self.copies[copy.copy_id] = copy

    def copies_of(self, isbn: str):
        return [c for c in self.copies.values() if c.book.isbn == isbn]

    def search_by_title(self, query: str):
        q = query.lower()
        return [b for b in self.books.values() if q in b.title.lower()]

    def search_by_author(self, query: str):
        q = query.lower()
        return [b for b in self.books.values() if q in b.author.lower()]

    def _get_copy(self, copy_id: str) -> BookCopy:
        copy = self.copies.get(copy_id)
        if copy is None:
            raise LibraryError(f"Unknown copy {copy_id}")
        return copy

    # ---- borrow
    def borrow(self, member: Member, copy_id: str, borrowed_on: datetime = None) -> Loan:
        borrowed_on = borrowed_on or datetime.now()
        copy = self._get_copy(copy_id)

        # 1. checks first; nothing is changed until all of them pass
        if copy.status == CopyStatus.RESERVED:
            if self.reservations.held_for(copy_id) is not member:
                raise CopyNotAvailableError(f"Copy {copy_id} is on hold for another member")
        elif copy.status != CopyStatus.AVAILABLE:
            raise CopyNotAvailableError(f"Copy {copy_id} is {copy.status.value}")

        if self.loan_registry.active_count(member) >= member.borrow_limit:
            raise BorrowLimitExceededError(
                f"{member.name} has reached the limit of {member.borrow_limit} loans"
            )

        # 2. state changes
        loan = Loan(copy, member, borrowed_on, borrowed_on + self.loan_period)
        self.loan_registry.add(loan)
        if copy.status == CopyStatus.RESERVED:
            self.reservations.release_hold(copy_id)
            copy.mark_available()
        copy.mark_borrowed()
        return loan

    # ---- return
    def return_copy(self, copy_id: str, returned_on: datetime = None):
        returned_on = returned_on or datetime.now()

        loan = self.loan_registry.close(copy_id)   # raises if never borrowed
        loan.close(returned_on)
        fine = self.fine.calculate_fine(loan.days_overdue(returned_on))

        copy = loan.book_copy
        copy.mark_available()

        next_member = self.reservations.pop_next(copy.book.isbn)
        if next_member is not None:
            copy.mark_reserved()
            self.reservations.place_hold(copy_id, next_member)
            self.notifications.append(
                (next_member, f"'{copy.book.title}' is ready for you (copy {copy_id})")
            )
        return fine

    # ---- reserve
    def reserve(self, member: Member, isbn: str):
        copies = self.copies_of(isbn)
        if not copies:
            raise ReservationError("No copies of this book exist")
        if any(c.status == CopyStatus.AVAILABLE for c in copies):
            raise ReservationError("A copy is available now; borrow it instead")
        self.reservations.enqueue(member, isbn)


# ---------------------------------------------------------------- self-test
if __name__ == "__main__":
    def raises(exc, fn, *args, **kwargs):
        try:
            fn(*args, **kwargs)
        except exc:
            return True
        return False

    t0 = datetime(2026, 1, 1)
    lib = Library(LoanRegistry(), FlatPerDayRate(2))

    dune = Book("Dune", "Frank Herbert", 1965, "isbn-1")
    emma = Book("Emma", "Jane Austen", 1815, "isbn-2")
    for i in range(1, 5):
        lib.add_copy(BookCopy(dune, f"D{i}"))
    lib.add_copy(BookCopy(emma, "E1"))

    alice = Member("Alice", "M1", MembershipType.STUDENT)   # limit 3
    bob = Member("Bob", "M2", MembershipType.REGULAR)
    carol = Member("Carol", "M3", MembershipType.REGULAR)
    dave = Member("Dave", "M4", MembershipType.REGULAR)

    # borrow basics
    lib.borrow(alice, "D1", t0)
    assert lib.copies["D1"].status == CopyStatus.BORROWED
    assert raises(CopyNotAvailableError, lib.borrow, bob, "D1", t0)

    # limit
    lib.borrow(alice, "D2", t0)
    lib.borrow(alice, "D3", t0)
    assert raises(BorrowLimitExceededError, lib.borrow, alice, "D4", t0)
    assert lib.loan_registry.active_count(alice) == 3

    # returns and fines
    assert lib.return_copy("D1", t0 + timedelta(days=14)) == 0           # on time
    assert lib.return_copy("D2", t0 + timedelta(days=19)) == 10          # 5 days * 2
    assert lib.loan_registry.active_count(alice) == 1
    assert lib.loan_registry.get_active_loan("D1") is None
    assert lib.loan_registry.get_active_loan("D3") is not None
    assert raises(LoanNotFoundError, lib.return_copy, "D4", t0)          # never borrowed
    lib.return_copy("D3", t0 + timedelta(days=1))
    assert "M1" not in lib.loan_registry.active_by_member                # key cleaned up

    # reservations
    lib.borrow(bob, "E1", t0)
    lib.reserve(carol, "isbn-2")
    assert raises(ReservationError, lib.reserve, carol, "isbn-2")        # no duplicates
    assert raises(ReservationError, lib.reserve, dave, "isbn-1")         # Dune copies free
    lib.return_copy("E1", t0 + timedelta(days=3))
    assert lib.copies["E1"].status == CopyStatus.RESERVED
    assert lib.notifications[-1][0] is carol
    assert raises(CopyNotAvailableError, lib.borrow, dave, "E1", t0)     # held for Carol
    lib.borrow(carol, "E1", t0 + timedelta(days=4))
    assert lib.copies["E1"].status == CopyStatus.BORROWED

    # fine strategies are swappable
    tiered = TieredFine(low_rate=1, high_rate=3, tier_days=5, cap=20)
    assert tiered.calculate_fine(3) == 3
    assert tiered.calculate_fine(7) == 5 + 6
    assert tiered.calculate_fine(100) == 20

    # search
    assert [b.title for b in lib.search_by_author("austen")] == ["Emma"]

    print("All checks passed")
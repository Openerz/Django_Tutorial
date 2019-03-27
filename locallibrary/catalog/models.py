from django.contrib.auth.models import User
from django.db import models
from datetime import date

@property
def is_overdue(self):
    if self.due_back and date.today() > self.due_back:
        return True
    return False

# Create your models here.
class Genre(models.Model):
    """Model representing a book genre."""
    name = models.CharField(max_length=200, help_text="Enter a book genre (e.g. Science Fiction")

    def __str__(self): # 최소한, 모든 모델마다 표준 파이썬 클래스의 메소드인 __str__() 을 정의하여 각각의 object 가 사람이 읽을 수 있는 문자열을 반환(return)하도록 합니다.
        """String for representing(대표적인) the Model object."""
        return self.name

class Language(models.Model):
    """Model representing a Language (e.g. English, French, Japanese, etc.)"""
    name = models.CharField(max_length=200,
                            help_text="Enter the book's natural language (e.g. English, French, Japanese etc.)")

    def __str__(self):
        """String for representing the Model object (in Admin site etc.)"""
        return self.name

from django.urls import reverse  # Used to generate URLs by reversing the URL patterns


class Book(models.Model):
    """Model representing a book (but not a specific copy of a book)."""
    title = models.CharField(max_length=200)
    author = models.ForeignKey('Author', on_delete=models.SET_NULL, null=True)
    # null=True 는 어떤 저자도 선택되지 않았다면 데이터베이스에 Null 값을 저장하도록 하고,
    # on_delete=models.SET_NULL 은 관련된 저자(author) 레코드가 삭제되었을 때 저자(author)의 값을 Null 로 설정할 겁니다.
    # 장르는 책이 여러 개의 장르를 가지고, 장르도 여러 개의 책을 가질 수 있는 다-대-다 필드(ManyToManyField)입니다. 저자는 ForeignKey 로 선언됩니다.
    # Foreign Key used because book can only have one author, but authors can have multiple books
    # Author as a string rather than object because it hasn't been declared yet in the file.

    summary = models.TextField(max_length=1000, help_text='Enter a brief(짧은) description of the book')
    isbn = models.CharField('ISBN', max_length=13,
                            help_text='13 Character <a href="https://www.isbn-international.org/content/what-isbn">ISBN number</a>')

    # ManyToManyField used because genre can contain many books. Books can cover many genres.
    # Genre class has already been defined so we can specify the object above.
    genre = models.ManyToManyField(Genre, help_text='Select a genre for this book')

    def __str__(self):
        """String for representing the Model object."""
        return self.title

    def get_absolute_url(self):
        """Returns the url to access a detail record for this book."""
        return reverse('book-detail', args=[str(self.id)])

    def display_genre(self):
        """Create a string for the Genre. This is required to display genre in Admin."""
        return ', '.join(genre.name for genre in self.genre.all()[:3])

    display_genre.short_description = 'Genre'

import uuid # Required for unique book instances

class BookInstance(models.Model):
    """Model representing a specific copy of a book (i.e. that can be borrowed from the library)."""
    """ ForeignKey : 연관된 Book 을 식별하기 위해(각각의 책은 많은 복사본을 가질 수 있지만, 복사본은 하나의 Book 만을 가질 수 있음).
        CharField  : 책의 출판사(imprint)(특정한 발간일)을 나타내기 위해."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text='Unique ID for this particular book across whole library')
    # UUIDField 는 id 필드가 이 모델의 primary_key 로 설정되는 데 사용됩니다.
    # 이 타입의 필드는 각 인스턴스에 전역적으로 고유한 값을 할당합니다 (도서관에서 찾을 수 있는 모든 책 마다 하나씩). * UUID : Unique User Identifier
    book = models.ForeignKey('Book', on_delete=models.SET_NULL, null=True)
    imprint = models.CharField(max_length=200)
    due_back = models.DateField(null=True, blank=True)
    #due_back 은 만기일을 정할 때 사용.
    LOAN_STATUS = (
        ('m', 'Maintenance'), # 유지관리
        ('o', 'On loan'), # 대여됨
        ('a', 'Available'), # 이용가능
        ('r', 'Reserved'), # 예약됨
    )

    status = models.CharField(     # 선택/선택 목록(choice/selection list)을 정의하는 CharField 입니다.
        max_length=1,
        choices=LOAN_STATUS,
        blank=True,
        default='m',
        help_text='Book availability',
    )

    class Meta:
        ordering = ['due_back']

    def __str__(self):
        """String for representing the Model object."""
        return f'{self.id} ({self.book.title})' # f' = 문자열 보간 구문 ? 결과 문자열에 서식이 지정된 식 결과를 포함하는 읽기 쉽고 편리한 구문을 제공

    borrower = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)


class Author(models.Model):
    """Model representing an author."""
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField('Died', null=True, blank=True)

    class Meta: # 메타데이터 옵션들은 모델에 무슨 데이터베이스를 사용해야만 하는가 그리고 데이터가 어떻게 저장되는가를 제어합니다.
        ordering = ['last_name', 'first_name']

    def get_absolute_url(self): # 개별 저자를 나타내기 위한 URL 을 가져오기 위해 author-detail URL 매핑을 반대로 합니다.
        """Returns the url to access a particular author instance."""
        return reverse('author-detail', args=[str(self.id)])

    def __str__(self):
        """String for representing the Model object."""
        return f'{self.last_name}, {self.first_name}'

from django.contrib import admin

# Register your models here.

from .models import Book, System_Person, Booksys_Person, Read_Person, Lend_Stream

admin.site.register(Book)
admin.site.register(System_Person)
admin.site.register(Booksys_Person)
admin.site.register(Read_Person)
admin.site.register(Lend_Stream)
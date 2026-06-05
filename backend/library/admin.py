from django.contrib import admin
from .models import StudentExtra, Book, IssuedBook

@admin.register(StudentExtra)
class StudentExtraAdmin(admin.ModelAdmin):
    list_display = ['get_name', 'enrollment', 'branch']

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['name', 'isbn', 'author', 'category']
    list_filter = ['category']
    search_fields = ['name', 'author', 'isbn']

@admin.register(IssuedBook)
class IssuedBookAdmin(admin.ModelAdmin):
    list_display = ['enrollment', 'isbn', 'issuedate', 'expirydate', 'status']
    list_filter = ['status']

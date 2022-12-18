from django.contrib import admin
from . models import Category, Author, Book, Member, IssueBook

# Register your models here.


class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'category',
                    'is_referrence_only', 'status']


class MemberAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'membership_date', 'membership_status']


class IssueBookAdmin(admin.ModelAdmin):
    list_display = ['borrower', 'book', 'issue_date',
                    'expired_date', 'fine_per_day']


admin.site.register(Category)
admin.site.register(Author)
admin.site.register(Book, BookAdmin)
admin.site.register(Member, MemberAdmin)
admin.site.register(IssueBook, IssueBookAdmin)

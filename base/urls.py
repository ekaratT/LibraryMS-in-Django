from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='books'),
    path('books', views.books, name='books'),
    path('add_book', views.add_book, name='add_book'),
    path('single_book/<int:id>', views.single_book, name='single_book'),
    path('edit_book/<int:id>', views.edit_book, name='edit_book'),
    path('delete_book/<int:id>', views.delete_book, name='delete_book'),
    path('issue_book/<int:id>', views.issue_book, name='issue_book'),
    path('issued_books', views.issued_book_view, name='issued_books'),
    path('edit_issued_book/<int:id>',
         views.edit_issued_book, name='edit_issued_book'),
    path('delete_issued_books/<int:id>',
         views.delete_issued_book, name='delete_issued_book'),
    path('members', views.members, name='members'),
    path('member_home', views.member_home, name='member_home'),

    path('single_member/<int:id>', views.single_member, name='single_member'),
    path('edit_member/<int:id>', views.edit_member, name='edit_member'),
    path('delete_member/<int:id>', views.delete_member, name='delete_member'),
    path('register', views.register_member, name='register'),
    path('login', views.login_user, name='login'),
    path('logout', views.logout_user, name='logout')
]

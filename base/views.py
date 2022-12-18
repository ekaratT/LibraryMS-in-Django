from django.shortcuts import render, redirect
from .models import Book, Member, IssueBook, Category, Author
from . forms import CreateUserForm, IssueBookForm, CreateBookForm, EditMemberForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.models import Group
from datetime import datetime, timedelta
from django.contrib.auth.decorators import login_required
from .decorator import admin_site_only, allowed_user
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage




# Create your views here.

def index(request):
    return render(request, 'base/index.html')


@login_required(login_url='login')
@allowed_user(allow_roles=['admin', 'staff'])
def books(request):
    books = Book.objects.all()

    page = request.GET.get('page')
    paginator = Paginator(books, 5) # Show 5 books per page.

    try:
        books_obj = paginator.page(page)
    except PageNotAnInteger:
        page = 1
        books_obj = paginator.page(page)
    except EmptyPage:
        page = paginator.num_pages
        books_obj = paginator.page(page)

    context = {'books_obj': books_obj, 'paginator': paginator}
    return render(request, 'base/books.html', context)


@login_required(login_url='login')
@allowed_user(allow_roles=['admin', 'staff'])
def add_book(request):
    page = 'add_book'
    authors = Author.objects.all()
    categories = Category.objects.all()
    form = CreateBookForm()
    if request.method == 'POST':
        category_name = request.POST.get('category')
        author_name = request.POST.get('author')
        author_name = author_name.split()
        if len(author_name) > 2:
            messages.error(request, 'Missing spaces in Author field')
        first_name, last_name = author_name
        author_name, created = Author.objects.get_or_create(first_name=first_name, last_name=last_name)
        category_name, created = Category.objects.get_or_create(category_name=category_name)

        Book.objects.create(
            isbn=request.POST.get('isbn'),
            title=request.POST.get('title'),
            author=author_name,
            category=category_name,
            is_referrence_only=True if request.POST.get('is_referrence_only') == 'on' else False,
            status=request.POST.get('status')
        )
        
        messages.success(request, 'Book was added successfully')
        return redirect('books')
    context = {'form': form, 'page': page, 'authors': authors, 'categories': categories}
    return render(request, 'base/book_form.html', context)


@login_required(login_url='login')
@allowed_user(allow_roles=['admin', 'staff'])
def single_book(request, id):
    book = Book.objects.get(pk=id)
    return HttpResponseRedirect(reverse('books'))


@login_required(login_url='login')
@allowed_user(allow_roles=['admin', 'staff'])
def edit_book(request, id):
    book = Book.objects.get(pk=id)
    form = CreateBookForm(instance=book)
    if request.method == 'POST':
        form = CreateBookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            messages.success(request, 'Changes were saved successfully')
            return redirect('books')
    context = {'form': form}
    return render(request, 'base/book_form.html', context)


@login_required(login_url='login')
@allowed_user(allow_roles=['admin', 'staff'])
def delete_book(request, id):
    book = Book.objects.get(pk=id)
    if request.method == 'POST':
        book.delete()
        messages.success(request, 'Book was deleted successfully')
    return HttpResponseRedirect(reverse('books'))


@login_required(login_url='login')
@allowed_user(allow_roles=['admin', 'staff'])
def issue_book(request, id):
    page = 'issue_book'
    book = Book.objects.get(pk=id)
    borrowers = Member.objects.all()

    form = IssueBookForm(instance=book)
    if request.method == 'POST':
        IssueBook.objects.create(
            borrower=Member.objects.get(name=request.POST.get('borrower')),
            book=Book.objects.get(title=request.POST.get('book')),
            fine_per_day=request.POST.get('fine_per_day'),
            over_due=True if request.POST.get('over_due') == 'on' else False,
        )

        messages.success(request, 'Book was issued successfully')
        return redirect('issued_books')
    context = {'form': form, 'page': page, 'borrowers': borrowers, 'book': book}
    return render(request, 'base/issue_book_form.html', context)
    

# Just in case for some reason admin needs to change fine per book
@login_required(login_url='login')
@allowed_user(allow_roles=['admin', 'staff'])
def edit_issued_book(request, id):
    issued_book = IssueBook.objects.get(pk=id)
    form = IssueBookForm(instance=issued_book)
    if request.method == 'POST':
        form = IssueBookForm(request.POST, instance=issued_book)
        if form.is_valid():
            form.save()
            messages.success(request, 'Changes were saved successfully')
        return redirect('issued_books')
    context = {'form': form, 'issued_book': issued_book}
    return render(request, 'base/issue_book_form.html', context)


@login_required(login_url='login')
@allowed_user(allow_roles=['admin', 'staff'])
def delete_issued_book(request, id):
    book = IssueBook.objects.get(pk=id)
    if request.method == 'POST':
        book.delete()
    return HttpResponseRedirect(reverse('issued_books'))


# To view all book that have been issued.
@login_required(login_url='login')
@allowed_user(allow_roles=['admin', 'staff'])
def issued_book_view(request):
    issued_books = IssueBook.objects.all()


    page = request.GET.get('page')
    paginator = Paginator(issued_books, 5) # Show 5 books per page.

    try:
        ibs_obj = paginator.page(page)
    except PageNotAnInteger:
        page = 1
        ibs_obj = paginator.page(page)
    except EmptyPage:
        page = paginator.num_pages
        ibs_obj = paginator.page(page)

    context = {'ibs_obj': ibs_obj, 'paginator':paginator}
    return render(request, 'base/view_issued_book.html', context)


# To view all user/member.
@login_required(login_url='login')
@allowed_user(allow_roles=['admin', 'staff'])
def members(request):
    members = Member.objects.all()

    page = request.GET.get('page')
    paginator = Paginator(members, 5) # Show 5 books per page.

    try:
        member_obj = paginator.page(page)
    except PageNotAnInteger:
        page = 1
        member_obj = paginator.page(page)
    except EmptyPage:
        page = paginator.num_pages
        member_obj = paginator.page(page)

    context = {'member_obj': member_obj, 'paginator':paginator}
    return render(request, 'base/members.html', context)


# To view single member in booststrap modal.
@login_required(login_url='login')
@allowed_user(allow_roles=['admin', 'staff'])
def single_member(request, id):
    mem = Member.objects.get(pk=id)
    borrowed_books = mem.issuebook_set.all()  # type: ignore
    context = {'mem': mem, 'borrowed_books': borrowed_books}
    return HttpResponseRedirect(reverse('members'))



@login_required(login_url='login')
@allowed_user(allow_roles=['admin', 'staff'])
def edit_member(request, id):
    page = 'edit'
    member = Member.objects.get(pk=id)
    member_form = EditMemberForm(instance=member)
    if request.method == 'POST':
        member_form = EditMemberForm(request.POST, instance=member)
        if member_form.is_valid():
            member_form.save()
            messages.success(request, 'Member was updated successfully')
            return redirect('members')
    context = {'form': member_form, 'page': page}
    return render(request, 'base/member_form.html', context)


# To confirm deleting in booststrap modal.
@login_required(login_url='login')
@allowed_user(allow_roles=['admin', 'staff'])
def delete_member(request, id):
    member = User.objects.get(pk=id)
    if request.method == 'POST':
        messages.success(request, 'Member was deleted successfully')
        member.delete()
    return HttpResponseRedirect(reverse('members'))



def login_user(request):
    page = 'login'
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        try:
            user = User.objects.get(username=username)
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                if request.user.is_staff or request.user.is_superuser:
                    # Admin will be redirected to books page after logged in.
                    return redirect('books')
                else:
                    # Member will be redirected to member_home, the page shows books that member borrowed.
                    return redirect('member_home')
            else:
                messages.warning(request, 'Username or password is incorrect')
        except:
            messages.warning(request, 'User does not exist')
        
    return render(request, 'base/member_form.html', {'page': page})


def member_home(request):
    cur_user = request.user
    books = IssueBook.objects.filter(borrower_id=cur_user.id)
    context = {'books': books}
    return render(request, 'base/member_logged_in.html', context)


def logout_user(request):
    logout(request)
    messages.success(request, 'User was logged out')
    return redirect('login')


def register_member(request):
    page = 'register'
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            if user.is_staff:
                group = Group.objects.get(name='staff')
                user.groups.add(group)
            else:
                group = Group.objects.get(name='member')
                user.groups.add(group)

            messages.success(request, 'Account was created')
            return redirect('login')
    context = {'form': form, 'page': page}
    return render(request, 'base/member_form.html', context)



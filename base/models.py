from enum import unique
from django.db import models
from datetime import datetime, timedelta
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.utils import timezone

# Create your models here.


class Author(models.Model):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class Category(models.Model):
    category_name = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.category_name


class Book(models.Model):
    STATUS = [
        ('available', 'Available'),
        ('loned', 'Loned'),
        ('lost', 'Lost'),
    ]

    isbn = models.CharField(max_length=13, unique=True)
    title = models.CharField(max_length=200)
    author = models.ForeignKey(Author, on_delete=models.SET_NULL, null=True)
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True)
    is_referrence_only = models.BooleanField(default=False)
    status = models.CharField(
        max_length=50, choices=STATUS, default='available')
    add_date = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-add_date']


class Member(models.Model):
    STATUS = [
        ('active', 'Active'),
        ('closed', 'Closed'),
        ('blacklist', 'Blacklist'),
    ]
    member = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email = models.EmailField(
        unique=True, max_length=200, null=True, blank=True)
    membership_date = models.DateTimeField(auto_now_add=True)
    membership_status = models.CharField(
        max_length=20, choices=STATUS, default='active')

    def __str__(self):
        return self.name


class IssueBook(models.Model):
    borrower = models.ForeignKey(
        Member, on_delete=models.CASCADE, null=True, blank=True)
    book = models.ForeignKey(
        Book, on_delete=models.CASCADE, null=True, blank=True)
    issue_date = models.DateTimeField(auto_now_add=True)
    expired_date = models.DateTimeField(
        default=timezone.datetime.today() + timedelta(days=15))
    fine_per_day = models.PositiveIntegerField(default=0)
    over_due = models.BooleanField(default=False, null=True, blank=True)

    def __str__(self):
        return f'{self.book} was loaned to {self.borrower}'

    @property
    def get_total_fine(self):
        total_fine = 0
        today = timezone.datetime.today()
        if today > self.expired_date:
            self.over_due = True
            days = today - self.expired_date
            total_fine = self.fine_per_day * days.days
            return total_fine
        return total_fine


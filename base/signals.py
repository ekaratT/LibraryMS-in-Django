import email
from django.db.models.signals import post_save, pre_delete
from django.contrib.auth.models import User
from . models import Member, IssueBook, Book
from datetime import datetime, timedelta



# Create member once user is created.
def create_member(sender, instance, created, **kwarge):
    member = instance
    if created:
        Member.objects.create(
            member=member,
            name=member.first_name,
            email=member.email,
        )


# Update book status to loned if book is loned to the member.
def update_book_status(sender, instance, created, **kwarge):
    book = Book.objects.get(id=instance.book.id)
    if created:
        book.status = 'loned'
        book.save()

# Change book status to available if issued book get deleted.
def change_book_status(sender, instance, *args, **kwarge):
    book = Book.objects.get(id=instance.book.id)
    book.status = 'available'
    book.save()


post_save.connect(create_member, sender=User)
post_save.connect(update_book_status, sender=IssueBook)
pre_delete.connect(change_book_status, sender=IssueBook)


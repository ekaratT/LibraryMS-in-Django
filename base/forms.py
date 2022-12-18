from django.forms import ModelForm
from django.contrib.auth.models import User
from . models import Book, Author, Category, Member, IssueBook
from django.contrib.auth.forms import UserCreationForm


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name',
                  'email', 'is_staff', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super(CreateUserForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            if name == 'is_staff':
                field.widget.attrs.update(
                    {'class': 'form-check form-check-input input mb-2'}
                )
            else:
                field.widget.attrs.update(
                {'class': 'form-control input mb-2', 'placeholder': field.label}
                )


class EditMemberForm(ModelForm):
    class Meta:
        model = Member
        fields = '__all__'
        exclude = ['member']

    def __init__(self, *args, **kwargs):
        super(EditMemberForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update(
                {'class': 'form-control input mb-2', 'placeholder': field.label})


class CreateBookForm(ModelForm):
    class Meta:
        model = Book
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(CreateBookForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            if name == 'is_referrence_only':
                field.widget.attrs.update(
                    {'class': 'form-check form-check-input input mb-2'}
                )
            else:
                field.widget.attrs.update(
                    {'class': 'form-control input mb-2', 'placeholder': field.label}
                )


class IssueBookForm(ModelForm):
    class Meta:
        model = IssueBook
        fields = '__all__'
        exclude = ['expired_date']

    def __init__(self, *args, **kwargs):
        super(IssueBookForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update(
                {'class': 'form-control input mb-2', 'placeholder': field.label})

from django import forms

class BookCreateForm(forms.Form):
    book_url = forms.URLField()
    book_title = forms.CharField(max_length=150)


        
        

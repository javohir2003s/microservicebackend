from django.shortcuts import render, redirect
from rest_framework.generics import ListAPIView, RetrieveAPIView
from .serializers import BookSerializer
from .models import Book
from .adminform import BookCreateForm
from .paginations import CustomPagination
from .parsing import parse_book_data
from django.contrib.admin.views.decorators import staff_member_required


class BookListView(ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    pagination_class = CustomPagination

class BookDetailView(RetrieveAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer


@staff_member_required
def add_book_view(request):
    if request.method == "POST":
        form = BookCreateForm(request.POST)
        if form.is_valid():
            book_title = form.cleaned_data.get('book_title')
            book_url = form.cleaned_data.get('book_url')
            data = parse_book_data(book_title=book_title, book_url=book_url)
            Book.objects.create(
                title=data['title'],
                price=data['price'],
                photo=data['photo'],
                description=data['description']
            )
            return redirect('admin:api_book_changelist')

    else:
        form = BookCreateForm()
    return render(request, 'admin/add_book.html', {'form': form})

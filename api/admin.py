from django.contrib import admin
from django.urls import path
from .views import add_book_view
from django.urls import path
from django.contrib import admin
from django.urls import path
from .views import add_book_view
from .models import Book
from django.db import connections
from django.shortcuts import render

class MySiteAdmin(admin.AdminSite):
    site_header = "Mening maxsus admin sahifam"
    site_title = 'Admin paneli'
    index_title = 'Boshqaruv paneli'

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('add-book/', self.admin_view(add_book_view), name='add-book'),
            path('bot-users/', self.admin_view(self.show_telegram_users), name='telegram_users')
        ]
        return custom_urls + urls
    
    def show_telegram_users(self, request, extra_context=None):
        with connections['telegram_users'].cursor() as cursor:
            cursor.execute("SELECT telegram_id, first_name, last_name, phone_number FROM users")
            rows = cursor.fetchall()

        context = dict(
            self.each_context(request),
            rows=rows,
            app_label='api'

        )
        return render(request, 'admin/telegram_users_changelist.html', context)


        
    def get_index_context(self, request):
        context = super().get_index_context(request)
        context['custom_links'] = [
            {
                'title': 'Add Book',
                'url': self.reverse('myadmin:add-book'),
            },
        ]
        return context
my_admin_site = MySiteAdmin(name='myadmin')


class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'photo')

my_admin_site.register(Book, BookAdmin)
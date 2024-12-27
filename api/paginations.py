from rest_framework.pagination import PageNumberPagination

class CustomPagination(PageNumberPagination):
    page_size = 5  # Har bir sahifada ko'rsatiladigan obyektlar soni
    page_size_query_param = 'page_size'  # URL orqali sahifa o'lchamini belgilash

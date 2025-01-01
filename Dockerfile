# Rasm bazasi sifatida rasmiy Python tasvirini tanlang
FROM python:3.12-slim

# Ishchi katalogni o'rnatish
WORKDIR /app

# Talablar faylini nusxalash va o'rnatish
COPY req.txt req.txt
RUN pip install --no-cache-dir -r req.txt

# Loyihani nusxalash
COPY . .

# Gunicorn o'rnatish
RUN pip install gunicorn

# Gunicorn yordamida Django serverini ishga tushirish
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "config.wsgi:application"]
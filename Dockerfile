# Use the official Python image from the Docker Hub
FROM python:3.9

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /app

# Install dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy project
COPY . /app/

EXPOSE 8000

# Run migrations on each boot
CMD ["/bin/sh", "-c", " python manage.py migrate && python manage.py runserver"]
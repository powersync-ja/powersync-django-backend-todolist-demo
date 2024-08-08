from django.utils import timezone
from django.db import migrations
from django.contrib.auth import get_user_model


def create_test_user(apps, schema_editor):
    User = get_user_model()
    User.objects.create_user(
        username='testuser',
        password='testpassword',
        last_login=timezone.now()
    )


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_test_user),
    ]

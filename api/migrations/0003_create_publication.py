# yourappname/migrations/000X_your_migration_name.py

from django.db import migrations

class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_create_test_user'),
    ]

    operations = [
        migrations.RunSQL(
        """
            DO $$
            BEGIN
                IF NOT EXISTS (
                    SELECT 1 FROM pg_publication WHERE pubname = 'powersync'
                ) THEN
                    CREATE PUBLICATION powersync FOR TABLE lists, todos;
                END IF;
            END $$;
            """,
            reverse_sql="""
            DROP PUBLICATION IF EXISTS powersync;
            """
        ),
    ]
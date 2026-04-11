from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('settings_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='systemsettings',
            name='system_online',
            field=models.BooleanField(default=True),
        ),
    ]

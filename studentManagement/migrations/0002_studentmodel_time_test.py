import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('studentManagement', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='studentmodel',
            name='time_test',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
    ]

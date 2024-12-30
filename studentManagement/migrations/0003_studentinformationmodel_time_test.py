import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('studentManagement', '0002_studentmodel_time_test'),
    ]

    operations = [
        migrations.AddField(
            model_name='studentinformationmodel',
            name='time_test',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
    ]

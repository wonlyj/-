from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('studentManagement', '0003_studentinformationmodel_time_test'),
    ]

    operations = [
        migrations.AlterField(
            model_name='studentinformationmodel',
            name='stu_address',
            field=models.CharField(max_length=30, verbose_name='学生地址'),
        ),
    ]

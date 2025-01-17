from django.db import migrations, models

class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CourseModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stu_id', models.CharField(max_length=15, verbose_name='学生id')),
                ('course', models.CharField(max_length=30, verbose_name='课程')),
                ('grade', models.IntegerField(default=60, verbose_name='分数')),
            ],
            options={
                'db_table': 'new_course',
            },
        ),
        migrations.CreateModel(
            name='StudentInformationModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.CharField(max_length=15, verbose_name='用户id')),
                ('stu_id', models.CharField(max_length=15, verbose_name='学生id')),
                ('stu_name', models.CharField(max_length=30, verbose_name='学生姓名')),
                ('stu_phone', models.CharField(max_length=20, verbose_name='学生电话')),
                ('stu_address', models.TextField(verbose_name='学生地址')),
                ('stu_faculty', models.CharField(max_length=20, verbose_name='院系')),
                ('stu_major', models.CharField(max_length=30, verbose_name='专业')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建日期')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='最后修改日期')),
            ],
            options={
                'db_table': 'new_studentinformation',
            },
        ),
        migrations.CreateModel(
            name='StudentModel',
            fields=[
                ('user_id', models.AutoField(primary_key=True, serialize=False)),
                ('username', models.CharField(max_length=10, verbose_name='用户名')),
                ('yourname', models.CharField(max_length=10, verbose_name='姓名')),
                ('password', models.CharField(max_length=10, verbose_name='密码')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建日期')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='最后修改日期')),
            ],
            options={
                'db_table': 'new_student',
            },
        ),
    ]

# Generated by Django 2.2.8 on 2020-02-13 23:34

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='About',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=300)),
                ('description', models.TextField()),
                ('image', models.ImageField(upload_to='pictures')),
                ('name', models.CharField(max_length=300)),
                ('satisfied_students', models.IntegerField()),
                ('courses_offered', models.IntegerField()),
                ('expert_advisors', models.IntegerField()),
                ('schools', models.IntegerField()),
            ],
        ),
    ]

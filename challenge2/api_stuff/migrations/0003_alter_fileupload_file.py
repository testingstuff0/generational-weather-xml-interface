# Generated by Django 3.2.8 on 2021-10-20 02:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api_stuff', '0002_rename_name_fileupload_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fileupload',
            name='file',
            field=models.FileField(upload_to='uploads/'),
        ),
    ]

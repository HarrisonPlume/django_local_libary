# Generated by Django 3.2.5 on 2021-07-14 06:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0053_plating_task_platingtaskinstance'),
    ]

    operations = [
        migrations.AddField(
            model_name='part',
            name='Plating_tasks',
            field=models.ManyToManyField(help_text='                                            Select the nessessary plating                                                tasks', to='catalog.Plating_Task'),
        ),
    ]
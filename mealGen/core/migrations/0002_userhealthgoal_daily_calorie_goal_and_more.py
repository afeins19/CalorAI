# Generated by Django 5.0.4 on 2024-04-22 04:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userhealthgoal',
            name='daily_calorie_goal',
            field=models.IntegerField(help_text='Daily Calorie Goal (log entries within 5 percent of this goal will count)', null=True),
        ),
        migrations.DeleteModel(
            name='UserAPICredentials',
        ),
    ]

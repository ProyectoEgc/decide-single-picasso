# Generated by Django 4.1 on 2023-11-20 19:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('voting', '0004_alter_voting_postproc_alter_voting_tally'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='create_ordination',
            field=models.BooleanField(default=False, verbose_name='Create ordination'),
        ),
        migrations.AddField(
            model_name='question',
            name='type',
            field=models.CharField(choices=[('C', 'Classic question'), ('B', 'Yes/No question')], default='C', max_length=1),
        ),
    ]

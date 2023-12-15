from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):

    dependencies = [
        ('voting', '0003_auto_20180605_0842'),
        ('mixnet', '0003_mixnet_auth_position'),
    ]

    operations = [
        # Remove foreign key constraint
        migrations.RunSQL('ALTER TABLE mixnet_mixnet_auths DROP FOREIGN KEY mixnet_mixnet_auths_auth_id_247a47a8_fk_mixnet_auth_id;'),

        # Now, you can safely delete the models
        migrations.DeleteModel(
            name='Auth',
        ),
        migrations.AlterField(
            model_name='mixnet',
            name='auths',
            field=models.ManyToManyField(related_name='mixnets', to='base.Auth'),
        ),
        migrations.AlterField(
            model_name='mixnet',
            name='key',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='mixnets', to='base.Key'),
        ),
        migrations.AlterField(
            model_name='mixnet',
            name='pubkey',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='mixnets_pub', to='base.Key'),
        ),
        migrations.DeleteModel(
            name='Key',
        ),
    ]

# Generated migration for role field update

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usuario',
            name='rol',
            field=models.CharField(
                choices=[('admin', 'Administrador'), ('docente', 'Docente')],
                default='docente',
                max_length=20
            ),
        ),
    ]

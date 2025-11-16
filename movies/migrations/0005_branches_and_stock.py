from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0004_review_rating'),
    ]

    operations = [
        migrations.CreateModel(
            name='LibraryBranch',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('address', models.CharField(blank=True, max_length=512, null=True)),
                ('latitude', models.DecimalField(blank=True, decimal_places=6, max_digits=9, null=True)),
                ('longitude', models.DecimalField(blank=True, decimal_places=6, max_digits=9, null=True)),
                ('phone', models.CharField(blank=True, max_length=50, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Stock',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('count', models.IntegerField(default=0)),
                ('branch', models.ForeignKey(on_delete=models.deletion.CASCADE, related_name='stocks', to='movies.librarybranch')),
                ('movie', models.ForeignKey(on_delete=models.deletion.CASCADE, related_name='stocks', to='movies.movie')),
            ],
            options={
                'unique_together': {('movie', 'branch')},
            },
        ),
    ]

# Generated by Django 5.0.3 on 2024-04-05 18:12

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Chess_Tournament',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('description', models.TextField()),
                ('rounds', models.IntegerField()),
            ],
            options={
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='Chess_Player',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('surname', models.CharField(max_length=50)),
                ('username', models.CharField(max_length=50)),
                ('rating', models.IntegerField(default=0)),
                ('birth_date', models.DateField(blank=True, null=True)),
                ('white_games', models.IntegerField(default=0)),
                ('tournament', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='chesstour.chess_tournament')),
            ],
            options={
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='Chess_Game',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('round', models.IntegerField()),
                ('result', models.CharField(max_length=50)),
                ('date', models.DateTimeField(blank=True, null=True)),
                ('player1', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='player1', to='chesstour.chess_player')),
                ('player2', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='player2', to='chesstour.chess_player')),
                ('tournament', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='chesstour.chess_tournament')),
            ],
            options={
                'ordering': ('tournament',),
            },
        ),
    ]
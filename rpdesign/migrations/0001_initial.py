# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2018-01-16 07:04
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dname', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Material',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mname', models.CharField(max_length=30)),
                ('type', models.IntegerField(default=1)),
                ('pos', models.IntegerField(default=1)),
            ],
        ),
        migrations.CreateModel(
            name='Patient',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pname', models.CharField(max_length=20)),
                ('idnum', models.CharField(max_length=20)),
                ('P_sexual', models.IntegerField(null=True)),
                ('P_page', models.IntegerField(null=True)),
                ('phonenum', models.CharField(max_length=20, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Remark',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('identy_index', models.CharField(max_length=30)),
                ('left_top_pos', models.CharField(max_length=30)),
                ('remark_pos', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='RPDVisit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('idnum', models.CharField(max_length=30)),
                ('type', models.IntegerField(default=1)),
                ('make_model_date', models.DateField(null=True)),
                ('get_model_date', models.DateField(null=True)),
                ('try_cradled', models.DateField(null=True)),
                ('try_paraffin', models.DateField(null=True)),
                ('try_teeth_arrange', models.DateField(null=True)),
                ('try_stake', models.DateField(null=True)),
                ('try_crown', models.DateField(null=True)),
                ('try_base', models.DateField(null=True)),
                ('finish_date', models.DateField(null=True)),
                ('fee', models.FloatField(null=True)),
                ('gold_use', models.FloatField(null=True)),
                ('model_edge', models.IntegerField(null=True)),
                ('occlusion_state', models.IntegerField(null=True)),
                ('occlusion_record', models.IntegerField(null=True)),
                ('teeth_pre', models.IntegerField(null=True)),
                ('problem', models.TextField(null=True)),
                ('solution', models.TextField(null=True)),
                ('precheck', models.CharField(max_length=20, null=True)),
                ('precheck_date', models.DateField(null=True)),
                ('finalcheck', models.CharField(max_length=20, null=True)),
                ('finalcheck_date', models.DateField(null=True)),
                ('color', models.CharField(max_length=20, null=True)),
                ('model_maker', models.CharField(max_length=20, null=True)),
                ('model_checker', models.CharField(max_length=20, null=True)),
                ('paraffin_maker', models.CharField(max_length=20, null=True)),
                ('paraffin_checker', models.CharField(max_length=20, null=True)),
                ('burnish_maker', models.CharField(max_length=20, null=True)),
                ('burnish_checker', models.CharField(max_length=20, null=True)),
                ('china_arrange_makeer', models.CharField(max_length=20, null=True)),
                ('china_arrange_checker', models.CharField(max_length=20, null=True)),
                ('design_explain', models.TextField(null=True)),
                ('quadraticTops', models.TextField(null=True)),
                ('conntype_hollow', models.BooleanField(default=False)),
                ('tongue_cover', models.BooleanField(default=False)),
                ('maxilla_cover', models.BooleanField(default=False)),
                ('innerPathList', models.TextField(null=True)),
                ('KennedyTop', models.IntegerField(null=True)),
                ('KennedyBot', models.IntegerField(null=True)),
                ('teethlosslistTop', models.TextField(null=True)),
                ('teethlosslistBot', models.TextField(null=True)),
                ('department', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='rpdesign.Department')),
                ('material', models.ManyToManyField(to='rpdesign.Material')),
                ('pid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rpdesign.Patient')),
            ],
        ),
        migrations.CreateModel(
            name='Staff',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('idnum', models.CharField(max_length=20)),
                ('sname', models.CharField(max_length=20)),
                ('phonenum', models.CharField(max_length=20, null=True)),
                ('department', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='rpdesign.Department')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Tooth',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pos', models.IntegerField(null=True)),
                ('tooth_lost', models.IntegerField(null=True)),
                ('tooth_base', models.IntegerField(null=True)),
                ('tooth_clasp', models.IntegerField(null=True)),
                ('tooth_support', models.IntegerField(null=True)),
                ('tongue_blank', models.IntegerField(null=True)),
                ('vid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rpdesign.RPDVisit')),
            ],
        ),
        migrations.CreateModel(
            name='Treatproject',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tname', models.CharField(max_length=20)),
                ('type', models.IntegerField(default=1)),
            ],
        ),
        migrations.AddField(
            model_name='rpdvisit',
            name='project',
            field=models.ManyToManyField(to='rpdesign.Treatproject'),
        ),
        migrations.AddField(
            model_name='rpdvisit',
            name='sid',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rpdesign.Staff'),
        ),
        migrations.AddField(
            model_name='remark',
            name='vid',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rpdesign.RPDVisit'),
        ),
    ]

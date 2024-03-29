# Generated by Django 4.1 on 2022-09-04 08:02

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('assessmentbaseinfo', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AssessmentProject',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('code', models.CharField(max_length=50)),
                ('title', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('creation_time', models.DateTimeField(auto_now_add=True)),
                ('last_modification_date', models.DateTimeField(auto_now=True)),
                ('assessment_profile', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='assessment_projects', to='assessmentbaseinfo.assessmentprofile')),
            ],
        ),
        migrations.CreateModel(
            name='AssessmentResult',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('assessment_project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='assessment_results', to='assessment.assessmentproject')),
            ],
        ),
        migrations.CreateModel(
            name='QualityAttributeValue',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.PositiveIntegerField()),
                ('assessment_results', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='quality_attribute_value', to='assessment.assessmentresult')),
            ],
        ),
        migrations.CreateModel(
            name='MetricValue',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('value', models.PositiveIntegerField(null=True)),
                ('assessment_result', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='metric_values', to='assessment.assessmentresult')),
                ('metric', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='metric_values', to='assessmentbaseinfo.metric')),
            ],
        ),
    ]

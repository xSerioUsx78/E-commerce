# Generated by Django 5.1.6 on 2025-03-16 08:41

import django.db.models.deletion
import model_utils.fields
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('product_app', '0005_alter_product_discount_alter_product_price_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='QuestionAnswer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('content', models.TextField()),
                ('status', model_utils.fields.StatusField(choices=[('pending', 'pending'), ('approved', 'approved'), ('rejected', 'rejected')], default='pending', max_length=100, no_check_for_status=True)),
                ('status_changed_at', model_utils.fields.MonitorField(blank=True, default=None, monitor='status', null=True, when={'approved', 'pending', 'rejected'})),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='questions_answers', to='product_app.product', verbose_name='محصول')),
                ('reply', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='replies', to='question_answer_app.questionanswer')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='questions_answers', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'پرسش و پاسخ',
                'verbose_name_plural': 'پرسش ها و پاسخ ها',
            },
        ),
    ]

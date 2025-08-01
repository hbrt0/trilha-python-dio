# Generated by Django 5.0.4 on 2024-04-08 19:28

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Card",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=20)),
                ("number", models.CharField(max_length=16)),
                ("holder_name", models.CharField(max_length=20)),
                (
                    "network",
                    models.CharField(
                        choices=[("V", "Visa"), ("M", "Mastercard")], max_length=1
                    ),
                ),
                ("expiration_date", models.CharField(max_length=5)),
                ("cvv", models.CharField(max_length=4)),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("P", "Pendente"),
                            ("A", "Aprovado"),
                            ("E", "Enviado"),
                            ("R", "Recebido"),
                        ],
                        default="P",
                        max_length=1,
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="cards",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "ordering": ["-created_at"],
            },
        ),
    ]

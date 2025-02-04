# Generated by Django 5.1.2 on 2024-10-21 03:43

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="StockPrediction",
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
                ("symbol", models.CharField(max_length=10)),
                ("date", models.DateField()),
                (
                    "predicted_price",
                    models.DecimalField(decimal_places=2, max_digits=10),
                ),
                (
                    "actual_price",
                    models.DecimalField(
                        blank=True, decimal_places=2, max_digits=10, null=True
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="StockPrice",
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
                ("symbol", models.CharField(db_index=True, max_length=10)),
                ("date", models.DateField(blank=True, db_index=True, null=True)),
                ("open_price", models.DecimalField(decimal_places=2, max_digits=10)),
                ("close_price", models.DecimalField(decimal_places=2, max_digits=10)),
                ("high_price", models.DecimalField(decimal_places=2, max_digits=10)),
                ("low_price", models.DecimalField(decimal_places=2, max_digits=10)),
                ("volume", models.BigIntegerField()),
            ],
            options={
                "indexes": [
                    models.Index(
                        fields=["symbol", "date"], name="stocks_stoc_symbol_bc0f0a_idx"
                    )
                ],
            },
        ),
    ]

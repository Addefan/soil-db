from django.db import models


class TaxonLevel(models.TextChoices):
    genus = "genus", "Род"
    family = "family", "Семейство"
    order = "order", "Порядок"
    klass = "class", "Класс"
    phylum = "phylum", "Отдел"
    kingdom = "kingdom", "Царство"

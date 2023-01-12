from django.db import models


class TaxonLevel(models.TextChoices):
    kingdom = "kingdom", "Царство"
    phylum = "phylum", "Отдел"
    klass = "class", "Класс"
    order = "order", "Порядок"
    family = "family", "Семейство"
    genus = "genus", "Род"

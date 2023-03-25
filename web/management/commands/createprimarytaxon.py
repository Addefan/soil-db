from django.core.management import BaseCommand
from django.utils.translation import gettext_lazy as _

from web.enums import TaxonLevel
from web.models import Taxon


class Command(BaseCommand):
    def handle(self, *args, **options):
        Taxon.objects.get_or_create(level=TaxonLevel.kingdom, title="Растения", latin_title="Plantae")
        print(_('Царство "Растения" создано'))

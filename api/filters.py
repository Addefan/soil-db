from django.utils.datetime_safe import datetime
from eav.models import Attribute
from rest_framework import filters

from web.mappings import translate


class PlantFilterBackend(filters.BaseFilterBackend):
    taxa_lookup_mapping: dict[str, str] = {
        "genus": "genus__title__in",
        "family": "genus__parent__title__in",
        "order": "genus__parent__parent__title__in",
        "class": "genus__parent__parent__parent__title__in",
        "phylum": "genus__parent__parent__parent__parent__title__in",
    }

    def filter_queryset(self, request, queryset, view):
        attributes = request.query_params

        eav_attributes = {
            eav_attribute.slug: eav_attribute for eav_attribute in Attribute.objects.filter(slug__in=attributes)
        }

        for attribute in attributes:
            values = attributes.getlist(attribute)

            eav_attribute = eav_attributes.get(attribute)
            if eav_attribute:
                if eav_attribute.datatype == Attribute.TYPE_TEXT:
                    queryset = queryset.filter({f"eav__{attribute}__in": values})
                elif eav_attribute.datatype in (Attribute.TYPE_INT, Attribute.TYPE_FLOAT):
                    values = list(map(float, values))
                    queryset = queryset.filter(**{f"eav__{attribute}__range": values})
                elif eav_attribute.datatype == Attribute.TYPE_DATE:
                    values = list(
                        map(lambda x: datetime.strptime(x.split(" (")[0], "%a %b %d %Y %H:%M:%S %Z%z"), values)
                    )
                    queryset = queryset.filter(**{f"eav__{attribute}__range": values})
                continue

            if attribute in self.taxa_lookup_mapping:
                queryset = queryset.filter(**{self.taxa_lookup_mapping[attribute]: values})
                continue

            if attribute in translate:
                queryset = queryset.filter(**{f"{attribute}__in": values})

        return queryset

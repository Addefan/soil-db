from eav.models import Entity, Value
from rest_framework import serializers

from web.models import Plant


class PlantSerializerMixin:
    def fill_in_taxon_fields(self, taxa):
        for taxon in taxa:
            self.instance[self.translation[taxon.level]] = taxon.title
            self.instance[f"{self.translation[taxon.level]} (лат.)"] = taxon.latin_title

    def fill_in_eav_fields(self, eav_fields):
        for field in eav_fields:
            self.instance[field.attribute.name] = field.value

    def fill_in_missing_fields(self, attributes):
        # fill in all missing fields as None
        for attr in attributes:
            self.instance.setdefault(attr.name, None)


class PlantSerializer(serializers.ModelSerializer, PlantSerializerMixin):
    # 'translation' attribute isn't used in serializing
    translation = Plant._taxa
    organization = serializers.StringRelatedField()

    class Meta:
        model = Plant
        fields = ("id", "number", "digitized_at", "latin_name", "name", "organization", "genus")

    def to_representation(self, instance):
        self.instance = super(PlantSerializer, self).to_representation(instance)
        eav_fields = self.context.get("eav_fields").get(self.instance["id"])
        attributes = self.context.get("attributes")
        genus = self.instance.pop("genus")
        # TODO optimize queries, using 'ancestors' method creates N+1 problem
        taxa = self.context.get("taxa").get(genus).ancestors(include_self=True).reverse()
        self.fill_in_taxon_fields(taxa)
        self.fill_in_eav_fields(eav_fields)
        self.fill_in_missing_fields(attributes)
        return self.instance

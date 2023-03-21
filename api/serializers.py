from eav.models import Entity, Value
from rest_framework import serializers

from web.models import Plant


class PlantSerializer(serializers.ModelSerializer):
    # 'translation' attribute isn't used in serializing
    translation = Plant._taxa
    organization = serializers.StringRelatedField()

    class Meta:
        model = Plant
        fields = ("id", "number", "digitized_at", "latin_name", "name", "organization", "genus")

    def to_representation(self, instance):
        instance = super(PlantSerializer, self).to_representation(instance)
        eav_fields = self.context.get("eav_fields").get(instance["id"])
        taxa = self.context.get("taxa")
        genus = instance.pop("genus")
        # TODO optimize queries, using 'ancestors' method creates N+1 problem
        taxa = taxa.get(genus).ancestors(include_self=True).reverse()
        for taxon in taxa:
            instance.setdefault(self.translation[taxon.level], taxon.title)
            instance.setdefault(f"{self.translation[taxon.level]} (лат.)", taxon.latin_title)
        for field in eav_fields:
            instance.setdefault(field.attribute.name, field.value)
        return instance

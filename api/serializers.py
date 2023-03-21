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
        fields = (
            "number",
            "organization",
        )

    def to_representation(self, instance):
        instance = super(PlantSerializer, self).to_representation(instance)
        return self.context.get("data")[instance["number"]]

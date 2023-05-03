from eav.models import Value, Attribute
from rest_framework import serializers

from web.models import Plant, Taxon


class PlantPartialSerializer(serializers.ModelSerializer):
    organization = serializers.StringRelatedField()
    genus = serializers.StringRelatedField()

    class Meta:
        model = Plant
        exclude = ["digitized_at", "id"]


class AttributeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attribute
        fields = ("name",)


class ValueSerializer(serializers.ModelSerializer):
    attribute = AttributeSerializer(read_only=True)
    _datatypes = ("bool", "csv", "date", "float", "int", "json", "text")
    _null_values = (None, {}, "['']")

    class Meta:
        model = Value
        exclude = (
            "id",
            "entity_id",
            "entity_uuid",
            "created",
            "modified",
            "generic_value_id",
            "entity_ct",
            "value_enum",
            "generic_value_ct",
        )

    def to_representation(self, instance):
        instance = super(ValueSerializer, self).to_representation(instance)
        value = None

        for candidate_datatype in self._datatypes:
            candidate_value = f"value_{candidate_datatype}"
            if instance[candidate_value] in self._null_values:
                instance.pop(candidate_value)
            else:
                value = candidate_value
        attribute = instance.pop("attribute")
        instance.setdefault(attribute["name"], instance.pop(value))
        return instance


class TaxonSerializer(serializers.ModelSerializer):
    parent = serializers.SerializerMethodField()

    class Meta:
        model = Taxon
        exclude = ("id",)

    def to_representation(self, instance):
        instance = super(TaxonSerializer, self).to_representation(instance)
        level = instance.pop("level")
        instance[f"{level}_title"] = instance.pop("title")
        instance[f"{level}_latin_title"] = instance.pop("latin_title")
        return instance

    def get_parent(self, obj):
        parent = obj.parent
        if parent is None:
            return
        return TaxonSerializer(parent).data


class PlantSerializer(PlantPartialSerializer):
    genus = TaxonSerializer(read_only=True)
    eav_values = ValueSerializer(read_only=True, many=True)

    @staticmethod
    def taxa_hierarchy_to_representation(taxon):
        taxa_hierarchy = {}
        while taxon is not None:
            parent = taxon.pop("parent")
            taxa_hierarchy.update(taxon)
            taxon = parent
        return taxa_hierarchy

    @staticmethod
    def add_missing_fields(instance, columns):
        """
        All serializers must have the same structure
        so missing fields must be presented in each serializer
        """
        for column in columns:
            instance.setdefault(column, None)
        return instance

    def to_representation(self, instance):
        instance = super(PlantSerializer, self).to_representation(instance)
        eav_values = instance.pop("eav_values")
        for eav_value in eav_values:
            instance.update(eav_value)
        instance.update(self.taxa_hierarchy_to_representation(instance.pop("genus")))
        instance = self.add_missing_fields(instance, self.context["columns"])
        return instance

    class Meta(PlantPartialSerializer.Meta):
        exclude = ["id"]

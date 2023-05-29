from collections import OrderedDict

from eav.models import Value, Attribute
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from rest_framework import serializers

from web.choices import xlsx_columns_choices
from web.models import Plant, Taxon


class PlantPartialSerializer(serializers.ModelSerializer):
    organization = serializers.StringRelatedField()
    genus = serializers.StringRelatedField()

    class Meta:
        model = Plant
        exclude = ["digitized_at", "id"]


class CustomAttributeSerializer(serializers.Serializer):
    name_attr = serializers.CharField()
    type_attr = serializers.CharField()
    slug_name = serializers.CharField(read_only=True)

    def create(self, validated_data):
        attr = Attribute.objects.create(name=validated_data["name_attr"], datatype=validated_data["type_attr"])
        validated_data["slug_name"] = attr.slug
        return validated_data


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
        instance[level] = instance.pop("title")
        instance[f"latin_{level}"] = instance.pop("latin_title")
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
    def clean_serializer(instance, columns):
        """
        All serializers must have the same structure
        so missing fields must be presented and redundant field must be removed in each serializer
        """
        # remove redundant fields
        instance = OrderedDict({key: val for key, val in instance.items() if key in columns})
        # add missing fields
        for column in columns:
            instance.setdefault(column, None)
        return instance

    def to_representation(self, instance):
        instance = super(PlantSerializer, self).to_representation(instance)
        eav_values = instance.pop("eav_values")
        for eav_value in eav_values:
            instance.update(eav_value)
        instance.update(self.taxa_hierarchy_to_representation(instance.pop("genus")))
        instance["organization__name"] = instance.pop("organization")
        instance = self.clean_serializer(
            instance, self.context.get("columns", tuple([choice[0] for choice in xlsx_columns_choices()]))
        )
        return instance

    class Meta(PlantPartialSerializer.Meta):
        exclude = ["id"]


class PasswordSerializer(serializers.Serializer):
    password = serializers.CharField()

    def validate_password(self, password):
        try:
            validate_password(password)
        except ValidationError as error:
            raise serializers.ValidationError(error.messages)
        return password

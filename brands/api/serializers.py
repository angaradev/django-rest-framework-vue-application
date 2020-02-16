from rest_framework import serializers
from brands.models import BrandsDict, BrandDictSup, AngSuppliers


class BrandsDictSerializer(serializers.ModelSerializer):
    brand_supplier = serializers.StringRelatedField(read_only=False)

    class Meta:
        model = BrandsDict
        fields = ['id', 'brand', 'brand_supplier']


class BrandDictSupSerializer(serializers.ModelSerializer):

    class Meta:
        model = BrandDictSup
        fields = '__all__'


# class AngPriceAllSerializer(serializers.ModelSerializer):
#     brand_name = serializers.CharField(max_length=255)
#     ang_brand = serializers.CharField(max_length=255)
#     brand_id = serializers.SerializerMethodField()

#     class Meta:
#         model = BrandDictSup
#         fields = ['brand_name', 'ang_brand', 'brand_id']

#     def get_brand_id(self, instance):
#         return instance.brand_name.id

# Use for checking if brand exists in dictionry

class AngPriceAllSerializerNotExists(serializers.Serializer):
    ang_brand = serializers.CharField(max_length=255)
    count = serializers.IntegerField(required=False)

    class Meta:
        fields = ['ang_brand', 'count']


class CheckDuplicatesSerializer(serializers.ModelSerializer):
    #brand = serializers.CharField()

    class Meta:
        model = BrandsDict
        extra_kwargs = {'brand': {'read_only': False, 'required': False}}
        fields = ['id', 'brand']


###############################################################################


class TrackSerializer(serializers.ModelSerializer):
    class Meta:
        model = BrandDictSup

        fields = ['pk', 'ang_brand']
        extra_kwargs = {'pk': {'read_only': False, 'required': False}}


class AlbumSerializer(serializers.ModelSerializer):
    brand_supplier = TrackSerializer(many=True)

    class Meta:
        model = BrandsDict
        fields = ['id', 'brand', 'brand_supplier']

    def create(self, validated_data):
        tracks_data = validated_data.pop('brand_supplier')
        album = BrandsDict.objects.create(**validated_data)
        for track_data in tracks_data:
            BrandDictSup.objects.create(brand_name=album, **track_data)
        return album

    def update(self, instance, validated_data):

        brand_supplier = validated_data.get('brand_supplier')

        # Delete any pages not included in the request
        ids = [item.get('pk') for item in brand_supplier]
        for b in instance.brand_supplier.all():
            if b.id not in ids:
                BrandDictSup.objects.get(id=b.id).delete()
                # page.delete()

        for i, b in enumerate(brand_supplier):
            item, created = BrandDictSup.objects.update_or_create(
                id=b.get('pk'),
                defaults={
                    'ang_brand': b.get('ang_brand'),
                    'brand_name': instance
                }
            )

        return instance


class SuppliersSerializer(serializers.ModelSerializer):
    class Meta:
        model = AngSuppliers

        fields = ['id', 'name', 'weight']

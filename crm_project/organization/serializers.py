from rest_framework import serializers
from . import models


class OrganizationSerializer(serializers.HyperlinkedModelSerializer):
    created_time = serializers.SerializerMethodField()
    organization_province_name = serializers.SerializerMethodField()
    organization_manufacturedـproducts = serializers.SerializerMethodField()
    expert_creator_url_detail = serializers.SerializerMethodField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        request = kwargs['context']['request']

        if not request.user.is_superuser:
            del self.fields['expert_creator_url_detail']

    def get_expert_creator_url_detail(self, obj):
        return "http://127.0.0.1:8000/api/users/{}/".format(obj.expert_creator.pk)

    def get_organization_manufacturedـproducts(self, obj):
        return obj.manufacturedـproducts.all().values_list('name', flat=True)

    def get_organization_province_name(self, obj):
        return obj.province.name

    def get_created_time(self, obj):
        return obj.created_time.strftime("%Y/%m/%d, %H:%M:%S")

    class Meta:
        model = models.Organization

        fields = [
            'organization_name',
            'organization_phone_number',
            'organization_province_name',
            'workers_size',
            'expert_creator_url_detail',
            'owner_first_name',
            'owner_last_name',
            'owner_second_last_name',
            'owner_phone_number',
            'owner_email',
            'created_time',
            'organization_manufacturedـproducts',
        ]

        read_only_fields = [field.name for field in models.Organization._meta.get_fields()]

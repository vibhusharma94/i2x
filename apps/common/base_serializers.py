from rest_framework import serializers
from apps.common import mixins as common_mixins


class BaseModelSerializer(common_mixins.CustomResponseSerializerMixin, serializers.ModelSerializer):
    """
    Serializer to be used as Base in Other Model serializers in application
    Common code required in All Serializers can be added here or
    In separate mixins and then inherited here
    It also extends from CustomResponseSerializerMixin which re-formats the data as required
    """


class BaseAPISerializer(common_mixins.CustomResponseSerializerMixin, serializers.Serializer):
    """
    Serializer to be used as Base in Other serializers in application
    Common code required in All Serializers can be added here or
    In separate mixins and then inherited here
    It also extends from CustomResponseSerializerMixin which re-formats the data as required
    """


class CustomMessageSerializer(BaseAPISerializer):
    """
    serializer to pass custom message in response
    """
    custom_message = ""

    def __init__(self, *args, **kwargs):
        custom_message = kwargs.pop('custom_message', '')
        self.custom_message = custom_message
        super(CustomMessageSerializer, self).__init__(*args, **kwargs)

    @property
    def data(self):
        # If any child serializer needs to override the data method,
        # it should first call the super class data
        message_dict = {
            "message": self.custom_message
        }
        data = super(CustomMessageSerializer, self).data
        data.update(message_dict)
        return data




class CustomResponseSerializerMixin(object):
    """
    Mixin to format serializer data to a custom response
    All serializers to inherit from this
    """
    @property
    def data(self):
        # If any child serializer needs to override the data method,
        # it should first call the super class data
        data = super(CustomResponseSerializerMixin, self).data
        return {
            'data': data
        }

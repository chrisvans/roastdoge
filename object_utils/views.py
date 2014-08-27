from django.shortcuts import render
from django.views.generic.base import ContextMixin

# Create your views here.

class ObjectDataMixin(ContextMixin):
    """
    This is intended to be appended as a mixin to a listview, and will add to the context 
    the object's model name and module name.
    """

    def get_context_data(self, **kwargs):

        kwargs['objectClassName'] = self.model.__name__
        kwargs['objectClassModule'] = self.model.__module__

        return super(ObjectDataMixin, self).get_context_data(**kwargs)
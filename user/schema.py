from graphene import relay, ObjectType, Field
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from django.contrib.auth import get_user_model

class UserNode(DjangoObjectType):
    class Meta:
        model = get_user_model()
        #only_fields = ['username', 'email', 'first_name', 'last_name', 'image_set']
        interfaces = (relay.Node, )

class Query(object):
    user = Field(UserNode)
    def resolve_user(self, info):
        if info.context.user.is_authenticated:
            return get_user_model().objects.get(id=info.context.user.id)
        else:
            return None

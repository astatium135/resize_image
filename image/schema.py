import graphene
from graphene import relay, ObjectType, Field
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from graphql_relay import from_global_id
from graphene_django.forms.mutation import DjangoModelFormMutation

from django.contrib.auth import get_user_model
from image.models import Image

class ImageNode(DjangoObjectType):
    image = graphene.String()
    width = graphene.Int()
    height = graphene.Int()
    class Meta:
        model = Image
        only_fields = ['id', 'name', 'image', 'image.width']
        filter_fields = ["user",]
        interfaces = (relay.Node, )
    def resolve_image(self, info):
        return self.get_image().url
    def resolve_width(self, info):
        return self.get_image().width
    def resolve_height(self, info):
        return self.get_image().height
    @classmethod
    def get_queryset(cls, queryset, info):
        if info.context.user.is_authenticated:
            return queryset.filter(user=info.context.user)
        else:
            return None

class Query(object):
    image = relay.Node.Field(ImageNode)
    all_images = DjangoFilterConnectionField(ImageNode)

class AddImageByLinkMutation(graphene.Mutation):
    class Arguments:
        link = graphene.String(required=True)
    image = graphene.Field(ImageNode)
    def mutate(self, info, link):
        image = Image.objects.add_by_link(link, info.context.user)
        return AddImageByLinkMutation(image=image)
        
class ImageMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
        width = graphene.Int()
        height = graphene.Int()
    image = graphene.Field(ImageNode)
    def mutate(self, info, **kwargs):
        id = from_global_id(kwargs.get("id"))[1]
        width = kwargs.get("width")
        height = kwargs.get("height")
        try:
            image = Image.objects.get(id=id, user=info.context.user)
        except:
            raise IndexError("Изображение не найдено или нет прав доступа")
        if not(width or height):
            raise ValueError("Должен быть указан хотя бы идин из аргументов: width, height")
        image.change_image(width, height)
        return ImageMutation(image=image)


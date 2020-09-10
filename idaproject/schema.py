import graphene

import user.schema
import image.schema

class Query(graphene.ObjectType,
            user.schema.Query,
            image.schema.Query,):
    hello = graphene.String(default_value="Hi!")

class Mutation(graphene.ObjectType):
    resize_image = image.schema.ImageMutation.Field()
    add_image = image.schema.AddImageByLinkMutation.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)

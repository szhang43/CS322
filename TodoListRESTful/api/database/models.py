from mongoengine import *


class ListItem(EmbeddedDocument):
    description = StringField(required=True)
    priority = StringField()


class TodoList(Document):
    title = StringField()
    items = EmbeddedDocumentListField(ListItem)


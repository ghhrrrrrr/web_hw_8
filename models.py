from mongoengine import EmbeddedDocument, Document
from mongoengine.fields import DateField, BooleanField, EmailField, EmbeddedDocumentField, ListField, StringField, ReferenceField


class Author(Document):
    fullname = StringField()
    born_date = DateField()
    born_location = StringField()
    description = StringField()


class Tag(EmbeddedDocument):
    name = StringField()


class Quote(Document):
    tags = ListField(EmbeddedDocumentField(Tag))
    author = ReferenceField(Author)
    quote = StringField()
    
    
class Contact(Document):
    fullname = StringField()
    email = EmailField()
    is_sent = BooleanField(default=False)

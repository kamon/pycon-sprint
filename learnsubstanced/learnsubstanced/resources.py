import colander
import deform.widget

from persistent import Persistent

from pyramid.security import (
    Allow,
    Everyone,
    )

from substanced.content import content
from substanced.folder import Folder
from substanced.property import PropertySheet
from substanced.root import Root

from substanced.schema import (
    Schema,
    NameSchemaNode
    )
from substanced.util import renamer

# def context_is_a_document(context, request):
#     return request.registry.content.istype(context, 'Document')
# 
# class DocumentSchema(Schema):
#     name = NameSchemaNode(
#         editing=context_is_a_document,
#         )
#     title = colander.SchemaNode(
#         colander.String(),
#         )
#     body = colander.SchemaNode(
#         colander.String(),
#         widget=deform.widget.RichTextWidget()
#         )
# 
# class DocumentPropertySheet(PropertySheet):
#     schema = DocumentSchema()
#     
# @content(
#     'Document',
#     icon='icon-align-left',
#     add_view='add_document', 
#     propertysheets = (
#         ('Basic', DocumentPropertySheet),
#         ),
#     )
# class Document(Persistent):
# 
#     name = renamer()
#     
#     def __init__(self, title='', body=''):
#         self.title = title
#         self.body = body
# 
        
## Contact content type

class ContactSchema(Schema):
    name = NameSchemaNode(
        editing=lambda c, r: r.registry.content.istype(c, 'Contact'),
        )
    
    firstname= colander.SchemaNode(
        colander.String(),
        )

    lastname= colander.SchemaNode(
        colander.String(),
        )

    bio = colander.SchemaNode(
        colander.String(),
        widget=deform.widget.RichTextWidget()
        )

class ContactPropertySheet(PropertySheet):
    schema = ContactSchema()
    
@content(
    'Contact',
    icon='icon-align-left',
    add_view='add_contact', 
    propertysheets = (
        ('Basic', ContactPropertySheet),
        ),
    )
    
class Contact(Persistent):

    name = renamer()
    
    def __init__(self, firstname='', lastname='', bio=''):
        self.firstname = firstname
        self.lastname = lastname
        self.bio = bio


## Directory / Root object

class DirectorySchema(Schema):
    """ The schema representing the directory root. """

    title = colander.SchemaNode(
        colander.String(),
        missing=''
        )
    description = colander.SchemaNode(
        colander.String(),
        missing=''
        )
    
class DirectoryPropertySheet(PropertySheet):
    schema = DirectorySchema()
    
@content(
    'Root',
    icon='icon-home',
    propertysheets = (
        ('', DirectoryPropertySheet),
        ),
    after_create= ('after_create', 'after_create2')
    )
class Directory(Root):
    title = ''
    description = ''

    @property
    def sdi_title(self):
        return self.title

    @sdi_title.setter
    def sdi_title(self, value):
        self.title = value
    
    def after_create2(self, inst, registry):
        acl = getattr(self, '__acl__', [])
        acl.append((Allow, Everyone, 'view'))
        self.__acl__ = acl

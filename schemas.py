from marshmallow import Schema, fields


# dump only means that you send this back
# required = True for posting
class ItemSchema(Schema):
    id = fields.Str(dump_only=True)
    name = fields.Str(required=True)
    price = fields.Float(required=True)
    store_id = fields.Str(required=True)


# schemas for updating an item
class ItemUpdateSchema(Schema):
    name = fields.Str()
    price = fields.Float()


# schemas for the store
class StoreSchema(Schema):
    id = fields.Str(dump_only=True)
    name = fields.Str(required=True)

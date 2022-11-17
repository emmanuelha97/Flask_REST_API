import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from db import items, stores

# blue print used to divide an api into multiple segments

blue_print = Blueprint(
    'items',
    __name__,
    description='Operations on items'
)


@blue_print.route('/item/<string:item_id>')
class Item(MethodView):
    @staticmethod
    def get(item_id):
        item = items.get(item_id)
        if item is None:
            abort(404, message='item not found.')
        return item

    @staticmethod
    def delete(item_id):
        item_id = items.get(item_id)
        if item_id is None:
            return abort(404, message='item not found.')
        del items[item_id]
        return {'message': 'item deleted.'}

    def post(self, store_id):
        raise NotImplemented

    def put(self, store_id):
        raise NotImplemented


@blue_print.route('/item')
class ItemList(MethodView):
    @staticmethod
    def get():
        return {'items': list(items.values())}

    @staticmethod
    def post():
        item_data = request.get_json()
        if (
                'price' not in item_data
                or 'store_id' not in item_data
                or 'name' not in item_data
        ):
            abort(400, message='incorrect object schema sent')

        for item in items.values():
            if (
                    item_data.get('name') == item.get('name')
                    and item_data.get('store_id') == item.get('store_id')
            ):
                abort(400, message=f'item already exist')

        if stores.get(item_data.get('store_id')) is None:
            abort(404, message='store not found.')

        item_id = uuid.uuid4().hex
        item = {**item_data, 'id': item_id}
        item[item_id] = item

        return item, 201

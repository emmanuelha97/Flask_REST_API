import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from db import stores


# blue print used to divide an api into multiple segments

blue_print = Blueprint(
    'stores',
    __name__,
    description='Operations on stores'
)


@blue_print.route('/store/<string:store_id>')
class Store(MethodView):
    @staticmethod
    def get(store_id):
        store_id = stores.get(store_id)
        if store_id is None:
            abort(404, message='store not found.')
        return store_id

    @staticmethod
    def delete(store_id):
        store = stores.get(store_id)
        if store is None:
            return abort(404, message='item not found.')
        del stores[store_id]
        return {'message': 'store deleted.'}

    def post(self, store_id):
        raise NotImplemented

    def put(self, store_id):
        raise NotImplemented


@blue_print.route('/store')
class ItemList(MethodView):
    @staticmethod
    def get():
        return {'stores': list(stores.values())}

    @staticmethod
    def post():
        store_data = request.get_json()
        if 'name' not in store_data:
            abort(400, message='incorrect object schema sent')
        for store in stores.values():
            if store_data.get('name') == store.get('name'):
                abort(400, message=f'store already exist')

        store_id = uuid.uuid4().hex
        store = {**store_data, 'id': store_id}
        stores[store_id] = store
        return store, 201

from flask import Flask
from flask_marshmallow import Marshmallow
from marshmallow import  fields
from flask_restful import Resource, Api, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
api = Api(app)
db = SQLAlchemy(app)
ma = Marshmallow(app)


class NotFoundError(Exception):
    def __init__(self, message, code):
        self.message = message
        self.code = code
        super()


class ListModel(db.Model):
    __tablename__ = 'list'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(80), unique=True, nullable=False)
    itemi = db.relationship("ItemModel")

    def __repr__(self):
        return f'List {self.title}'


class ItemModel(db.Model):
    __tablename__ = 'item'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.String(80), nullable=False)
    status = db.Column(db.Integer, nullable=False)
    list_id = db.Column(db.Integer, db.ForeignKey('list.id'))

class ItemSchema(ma.ModelSchema):
    class Meta:
        model = ItemModel
        include_fk = True

item_schema = ItemSchema()

class ListSchema(ma.ModelSchema):
    itemi = fields.Nested(item_schema, many=True)
    class Meta:
        model = ListModel

list_schema = ListSchema()

@app.errorhandler(NotFoundError)
def handle_exception(e):
    return {'err': e.message}, e.code


@app.before_first_request
def before_first_request():
    db.create_all()


class ListsController(Resource):
    def get(self):
        return {'data': list_schema.dump(ListModel.query.all(), many=True)}

class ListController(Resource):
    def post(self):
        list = list_schema.load(request.get_json())
        try:
            db.session.add(list)
            db.session.commit()
        except:
            return {'err': 'Already exists!'}, 409
        return {'data': list_schema.dump(list)}, 200

class ItemController(Resource):
    def post(self):
        item = item_schema.load(request.get_json())
        list_id = item.list_id
        if not list_id:
            return {'err': 'No list_id provided'}, 400

        list = ListModel.query.filter_by(id=list_id).first()
        if not list:
            return {'err': f'List with id: {list_id} not found!'}, 404

        db.session.add(item)
        db.session.commit()
        return {'data': item_schema.dump(item)}, 200

class ListControllerById(Resource):
    def delete(self, list_id):
        if not list_id:
            return {'err': 'No list_id provided'}, 400

        list = ListModel.query.filter_by(id=list_id).first()
        if not list:
            return {'err': f'List with id: {list_id} not found!'}, 404

        ItemModel.query.filter_by(list_id=list_id).delete()
        db.session.delete(list)
        db.session.commit()
        return {'msg': f'List by id: {list_id} successfully deleted!'}, 200

    def put(self, list_id):
        if not list_id:
            return {'err': 'No list_id provided'}, 400

        list = ListModel.query.filter_by(id=list_id).first()
        if not list:
            return {'err': f'List with id: {list_id} not found!'}, 404

        request_list = list_schema.load(request.get_json())

        list.title = request_list.title
        try:
            db.session.add(list)
            db.session.commit()
        except:
            return {'err': 'Already exists!'}, 409
        return {'msg': f'List by id: {list_id} successfully changed!'}, 200

class ItemControllerById(Resource):
    def delete(self, item_id):
        if not item_id:
            return {'err': 'No item_id provided'}, 400

        item = ItemModel.query.filter_by(id=item_id).first()
        if not item:
            return {'err': f'Item with id: {item_id} not found!'}, 404

        db.session.delete(item)
        db.session.commit()
        return {'msg': f'Item by id: {item_id} successfully deleted!'}, 200

    def put(self, item_id):
        if not item_id:
            return {'err': 'No item_id provided'}, 400

        item = ItemModel.query.filter_by(id=item_id).first()
        if not item:
            return {'err': f'Item with id: {item_id} not found!'}, 404

        request_item = item_schema.load(request.get_json())
        list = ListModel.query.filter_by(id=request_item.list_id).first()
        if not list:
            return {'err': f'List with id: {request_item.list_id} not found!'}, 404

        item.content = request_item.content
        item.status = request_item.status
        item.list_id = request_item.list_id

        try:
            db.session.add(item)
            db.session.commit()
        except:
            return {'err': 'Already exists!'}, 409
        return {'msg': f'Item by id: {item_id} successfully changed!'}, 200


api.add_resource(ListsController, '/liste.json')
api.add_resource(ListController, '/liste')
api.add_resource(ItemController, '/itemi')
api.add_resource(ListControllerById, '/liste/<int:list_id>')
api.add_resource(ItemControllerById, '/itemi/<int:item_id>')

if __name__ == '__main__':
    app.run(debug=True, port=5000, host='0.0.0.0')

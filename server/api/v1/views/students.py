#!/usr/bin/python3
""" objects that handle all default RestFul API actions for students """

# import api
from models.student import Student
from models.user import User
from models import storage
from api.v1.views import api
from flask import abort, jsonify, request, make_response
from flask_restx import Resource, fields
# from api.v1.auth import token_required
from flask_jwt_extended import jwt_required

@api.route('/students', strict_slashes=False)
class Student1(Resource):
    @jwt_required(False)
    def get(self):
        """ returns list of all todo objects """
        all_students = []
        students = storage.all(Student).values()
        for student in students:
            d = student.to_dict()
            del d['_sa_instance_state']
            print(d)
            all_students.append(d)
        return all_students
    
    @api.expect(api.model('student', {
        'email': fields.String,
        'password': fields.String,
        'first_name': fields.String,
        'last_name': fields.String,
    }))
    def post(self):
        """ creates new student """

        data = request.get_json()
        if data is None:
            abort(400, "Not a JSON")
        if 'email' not in data:
            abort(400, "Missing email")
        if 'password' not in data:
            abort(400, "Missing password")
        student = Student()

        for k, v in data.items():
            setattr(student, k, v)
        student.save()
        u = student.to_dict()
        del u['_sa_instance_state']
        print(u)
        return make_response(jsonify(u), 201)



# @api.route('/users/<user_id>/todos', strict_slashes=False)
# @api.doc(security='apikey')
# class Todo2(Resource):
#     resource_fields = api.model('todo', {
#         'title': fields.String,
#         'isCompleted': fields.Boolean,
#     })

#     def get(self, user_id):
#         """ returns list of all todo objects """

#         user = storage.get(User, user_id)
#         if not user:
#             abort(404)

#         todos = []
#         all_todos = storage.all(Todo).values()
#         for todo in all_todos:
#             d = todo.to_dict()
#             del d['_sa_instance_state']
#             if todo.user_id == user_id:
#                 todos.append(d)
#         return jsonify(todos)

    # @api.doc(params={'title': ''})
    # @api.marshal_with(resource_fields, as_list=True)
    # @api.expect(resource_fields)
    # def post(self, user_id):
    #     """ Creates a todo objects """
    #     data = request.get_json()
    #     if not data:
    #         abort(404, 'Not a JSON')
    #     print(data)
    #     user = storage.get(User, user_id)
    #     if not user:
    #         abort(404)

    #     todo = Todo(data)
    #     todo.user_id = user_id
    #     for k, v in data.items():
    #         setattr(todo, k, v)
    #     todo.save()
    #     t = todo.to_dict()
    #     del t['_sa_instance_state']
    #     print(t)
    #     return make_response(jsonify(t), 201)


@api.route('/students/<student_id>', strict_slashes=False)
class Student3(Resource):
    resource_fields = api.model('student', {
        'email': fields.String,
        'password': fields.String,
        'lastname': fields.String,
        'firstname': fields.String,
    })
    def get(self, student_id):
        """ returns list of all todo objects """
        student = storage.get(Student, student_id)

        if not student:
            abort(404)

        t = student.to_dict()
        del t['_sa_instance_state']
        print(t)
        return jsonify(t)

    def delete(self, student_id):
        """ delete a student object """
        student = storage.get(Student, student_id)

        if not student:
            abort(404)

        student.delete()
        storage.save()
        return make_response(jsonify({}), 200)
    
    @api.expect(resource_fields)
    def put(self, student_id):
        """ Updates a student object """
        student = storage.get(Student, student_id)

        if not student:
            abort(404)

        data = request.get_json()

        if not data:
            return make_response(jsonify({"error": "Not a valid JSON"}), 400)

        for k, v in data.items():
            if k != 'id' and k != 'user_id' and k != 'created_at' and k != 'updated_at':
                setattr(student, k, v)
        student.save()
        t = student.to_dict()
        del t['_sa_instance_state']

        return make_response(jsonify(t), 203)

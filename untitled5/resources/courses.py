from flask import jsonify,Blueprint,abort
from flask_restful import (Resource,inputs,Api,reqparse,fields
                           ,marshal,marshal_with,url_for)
import models

course_fields= {
    'id':fields.Integer,
    'title':fields.String,
    'url':fields.String,
    'reviews':fields.List(fields.String)
}

def add_reviews(course):
    course.reviews= [url_for('resources.reviews.review',id=review.id) for review in course.review_set]
    return course

def course_or_404(course_id):
    try:
        course=models.Course.get(models.Course.id==course_id)
    except models.Course.DoesNotExist:
        abort(404,message="Course {} does not exist".format(course_id))
    else:
        return course

class coursesList(Resource):
    def __init__(self):
        self.reqparse=reqparse.RequestParser()
        self.reqparse.add_argument(
                'title',
            required=True,
            help='No Course Title provided',
            location=['form','json']
        )
        self.reqparse.add_argument(
            'url',
            required=True,
            help='No Course URL provided',
            location=['form', 'json'],
            type=inputs.url
        )
        super().__init__()

    def get(self):
        courses=[marshal(add_reviews(course),course_fields) for course in models.Course.select()]
        return jsonify({'courses':courses})

    def post(self):
        args=self.reqparse.parse_args()
        models.Course.create(**args)
        return jsonify({ 'reviews': [{'course': 1 , 'rating':5  }]})

class course(Resource):
    def __init__(self):
        self.reqparse=reqparse.RequestParser()
        self.reqparse.add_argument(
            'string1',
            required=True,
            help='No Course string1 provided',
            location=['form','json']
        )
        self.reqparse.add_argument(
            'string2',
            required=True,
            help='No Course string2 provided',
            location=['form', 'json']
        )

        super().__init__()
    @marshal_with(course_fields)
    def get(self,id):
        return add_reviews(course_or_404(id))
    def put(self,id):
        return jsonify({'course':1 , 'rating':5})
    def delete(self,id):
        return jsonify({'course':1 , 'rating':5})
    def post(self,id):
        args=self.reqparse.parse_args()
        models.Review2.create(**args)
        return jsonify({'course':1 , 'rating':5})

courses_api = Blueprint('resources.courses',__name__)
api = Api (courses_api)
api.add_resource(coursesList,'/api/v1/courses',endpoint='courses')
api.add_resource(course,'/api/v1/courses/<int:id>',endpoint='course')

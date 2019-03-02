from flask import jsonify,Blueprint,abort
from flask_restful import Resource,Api,reqparse,inputs,marshal,marshal_with,url_for,fields
import models

review_fields= {
    'id':fields.Integer,
    'for_course':fields.String,
    'rating':fields.Integer,
    'comment':fields.String(default=''),
    'created_at':fields.DateTime
}

def course_or_404(course_id):
    try:
        course=models.Review.get(models.Review.id==course_id)
    except models.Review.DoesNotExist:
        abort(404)
    else:
        return course

def add_course(review):
    review.for_course=url_for('resources.courses.course',id=review.course.id)
    return review

class ReviewList(Resource):
    def __init__(self):
        self.reqparse=reqparse.RequestParser()
        self.reqparse.add_argument(
            'course',
            type=inputs.positive,
            required=True,
            help='No course  provided',
            location=['form','json']
        )
        self.reqparse.add_argument(
            'rating',
            type=inputs.int_range(1,5),
            required=True,
            help='No rating provided',
            location=['form', 'json']
        )
        self.reqparse.add_argument(
            'comment',
            required=False,
            nullable=True,
            help='No Course URL provided',
            location=['form', 'json'],
            default=''
        )

        super().__init__()

    def get(self):
        return {'reviews' : [marshal(add_course(review), review_fields) for review in models.Review.select()]}

    def post(self):
        args=self.reqparse.parse_args()
        models.Review.create(**args)
        return jsonify({ 'courses': [{'title': 'Python Basics'}]})

class Review(Resource):
    @marshal_with(review_fields)
    def get(self,id):
        return add_course(course_or_404(id))
    def put(self,id):
        return jsonify({'title':'Python Basics'})
    def delete(self,id):
        return jsonify({'title':'Python Basics'})

reviews_api = Blueprint('resources.reviews',__name__)
api=Api(reviews_api)
api.add_resource(ReviewList,'/reviews',endpoint='reviews')
api.add_resource(Review,'/reviews/<int:id>',endpoint='review')





import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

# Functions built based on the functions of the book project (module).

#fuunca que cria a paginacao da pagina, me basei na funcao da paginacao dos livros.
def paginate_question(request, selection):
    
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    
    end = start + QUESTIONS_PER_PAGE
    
    questions = [question.format() for question in selection]
    
    current_questions = questions[start:end]
    
    return current_questions



def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    
    #Cors
    CORS(app)

    #Cors permission
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET,PUT,POST,DELETE,OPTIONS')
        return response

    
    # Function GET requests for all categories.
    @app.route("/categories")
    def get_all_categories():
        categories = Category.query.all()
        typecategories = {}
        for category in categories:
            typecategories[category.id] = category.type

        return jsonify({
            'success': True,
            'categories': typecategories
        })


    #function DELETE request for questiosn delete
    @app.route('/questions/<int:id>', methods=['DELETE'])
    def delete_question(id):
        try:
            question = Question.query.filter_by(id=id).one_or_none()
            if question is None:
                abort(404)
            question.delete()
            selection = Question.query.order_by(Question.id).all()
            currentQuestions = paginate_question(request, selection)
            return jsonify({
                'success': True,
            })
        except Exception as e:
            abort(404)
            
    
    #function POST request for create Questions
    @app.route("/questions", methods=['POST'])
    def add_question():
        body = request.get_json()
        
        Question_new = body.get('question', None)
        Answer_new = body.get('answer', None)
        Category_new = body.get('category', None)
        Difficult_new = body.get('difficulty', None)

        try:
            question_new_answer = Question(question=Question_new, answer=Answer_new,
                                category=Category_new, difficulty=Difficult_new)
            question_new_answer.insert()
            selection = Question.query.order_by(Question.id).all()
            curreQuestions = paginate_question(request, selection)

            return jsonify({
                'success': True,
                'created': question_new_answer.id,
                'questions': curreQuestions,
                'total_questions': len(selection)
            })

        except Exception:
            abort(422)

            
    #Function GET for all questions based in book project
    @app.route('/questions')
    def get_questions():
        try:
            selection = Question.query.order_by(Question.id).all()
            totalQuestions = len(selection)
            curreQuestions = paginate_question(request, selection)
            if (len(curreQuestions) == 0):
                abort(404)

            categories = Category.query.all()
            categoriesDict = {}
            for category in categories:
                categoriesDict[category.id] = category.type

            return jsonify({
                'success': True,
                'questions': curreQuestions,
                'total_questions': totalQuestions,
                'categories': categoriesDict
            })
        except Exception:
            abort(400)
            


    # Function search 
    # I confess that in this role I base myself on the work of other colleagues because I was not able to think of a solution
    @app.route('/search', methods=['GET','POST'])
    def search_questions():
    #search related question with input string
        data = request.get_json()
        if(data['searchTerm']):
            search_term = data['searchTerm']

        related = Question.query.filter(Question.question.ilike('%{}%'.format(search_term))).all()
        if related==[]:
            abort(404)

        curreQuestions = paginate_question(request, related)

        return jsonify({
            'success': True,
            'questions': curreQuestions,
            'total_questions': len(related)
        })

            

    # GET questions based on category.
    @app.route("/categories/<int:id>/questions")
    def questions_in_category(id):
        category = Category.query.filter_by(id=id).one_or_none()
        if category:
            questions = Question.query.filter_by(category=str(id)).all()
            curreQuestions = paginate_question(request, questions)
            return jsonify({
                'success': True,
                'questions': curreQuestions,
                'total_questions': len(questions),
                'current_category': category.type
            })
        else:
            abort(404)

    # Function quizzes 
    # I confess that in this role I base myself on the work of other colleagues because I was not able to think of a solution
    @app.route('/quizzes', methods=['POST'])
    def quiz():
        body = request.get_json()
        quiz = body.get('quiz_category')
        previous = body.get('previous_questions')
        try:
            if (quiz['id'] == 0):
                questionsQuery = Question.query.all()
            else:
                questionsQuery = Question.query.filter_by(
                    category=quiz['id']).all()

            randomIndex = random.randint(0, len(questionsQuery)-1)
            nextQuestion = questionsQuery[randomIndex]
            stillQuestions = True
            while nextQuestion.id not in previous:
                nextQuestion = questionsQuery[randomIndex]
                return jsonify({
                    'success': True,
                    'question': {
                        "answer": nextQuestion.answer,
                        "category": nextQuestion.category,
                        "difficulty": nextQuestion.difficulty,
                        "id": nextQuestion.id,
                        "question": nextQuestion.question
                    },
                    'previousQuestion': previous
                })

        except Exception:
            abort(404)
            
            
            
    ############# Error  #############
    #################################

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            'error': 400,
            "message": "Bad request"
        }), 400

    @app.errorhandler(404)
    def page_not_found(error):
        return jsonify({
            "success": False,
            'error': 404,
            "message": "Page not found"
        }), 404

    @app.errorhandler(422)
    def unprocessable_recource(error):
        return jsonify({
            "success": False,
            'error': 422,
            "message": "Unprocessable recource"
        }), 422

    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify({
            "success": False,
            'error': 500,
            "message": "Internal server error"
        }), 500

    @app.errorhandler(405)
    def invalid_method(error):
        return jsonify({
            "success": False,
            'error': 405,
            "message": "Invalid method!"
        }), 405
    
    

    return app

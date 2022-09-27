# API Development and Documentation Final Project

## Trivia App

Udacity is invested in creating bonding experiences for its employees and students. A bunch of team members got the idea to hold trivia on a regular basis and created a webpage to manage the trivia app and play the game, but their API experience is limited and still needs to be built out.

That's where you come in! Help them finish the trivia app so they can start holding trivia and seeing who's the most knowledgeable of the bunch. The application must:

1. Display questions - both all questions and by category. Questions should show the question, category and difficulty rating by default and can show/hide the answer.
2. Delete questions.
3. Add questions and require that they include question and answer text.
4. Search for questions based on a text query string.
5. Play the quiz game, randomizing either all questions or within a specific category.

Completing this trivia app will give you the ability to structure plan, implement, and test an API - skills essential for enabling your future applications to communicate with others.

## Starting and Submitting the Project

[Fork](https://help.github.com/en/articles/fork-a-repo) the project repository and [clone](https://help.github.com/en/articles/cloning-a-repository) your forked repository to your machine. Work on the project locally and make sure to push all your changes to the remote repository before submitting the link to your repository in the Classroom.

## About the Stack

We started the full stack application for you. It is designed with some key functional areas:

### Backend

The [backend](./backend/README.md) directory contains a partially completed Flask and SQLAlchemy server. You will work primarily in `__init__.py` to define your endpoints and can reference models.py for DB and SQLAlchemy setup. These are the files you'd want to edit in the backend:

1. `backend/flaskr/__init__.py`
2. `backend/test_flaskr.py`

> View the [Backend README](./backend/README.md) for more details.

### Frontend

The [frontend](./frontend/README.md) directory contains a complete React frontend to consume the data from the Flask server. If you have prior experience building a frontend application, you should feel free to edit the endpoints as you see fit for the backend you design. If you do not have prior experience building a frontend application, you should read through the frontend code before starting and make notes regarding:

1. What are the end points and HTTP methods the frontend is expecting to consume?
2. How are the requests from the frontend formatted? Are they expecting certain parameters or payloads?

Pay special attention to what data the frontend is expecting from each API response to help guide how you format your API. The places where you may change the frontend behavior, and where you should be looking for the above information, are marked with `TODO`. These are the files you'd want to edit in the frontend:

1. `frontend/src/components/QuestionView.js`
2. `frontend/src/components/FormView.js`
3. `frontend/src/components/QuizView.js`

By making notes ahead of time, you will practice the core skill of being able to read and understand code and will have a simple plan to follow to build out the endpoints of your backend API.

### API Reference

## Error Handling

Errors are returned as JSON objects in the following format:

```
{
    "success": False, 
    "error": 400,
    "message": "bad request"
}
```

The API will return three error types when requests fail:

1. 400: Bad Request
2. 404: Resource Not Found
3. 422: Unprocessable recource
4. 500: Internal Server Error
5. 405: Invalid method!


### Endpoints

##### GET '/categories'

General:

 - returns a list of questions from the database

- Results are paginated in groups of 10. Include a request argument to choose page number, starting from 1.

- Sample: curl http://127.0.0.1:5000/books

```
{
  "categories": {
    "1": "Science", 
    "2": "Art", 
    "3": "Geography", 
    "4": "History", 
    "5": "Entertainment", 
    "6": "Sports"
  }, 
  "success": true
}
```

#### DELETE /questions/{id}**

General:
- Deletes the question of the given ID if it exists. Returns success value.

Sample ```curl -X DELETE http://127.0.0.1:5000/questions/5 ```

```
{
  "success": true
}
```

##### POST '/questions'
- Create a new question. The new question must have all four information. 
- Example: ```curl http://127.0.0.1:5000/questions -X POST -H "Content-Type: application/json" -d '{"question": "Who is Jorge Darlim?", "answer": "the current student at Ufam", "difficulty": 1, "category": "5"}' ```
```
{
  "created": 47, 
  "questions": [
    {
      "answer": "Apollo 13", 
      "category": 5, 
      "difficulty": 4, 
      "id": 2, 
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
    }, 
    {
      "answer": "Tom Cruise", 
      "category": 5, 
      "difficulty": 4, 
      "id": 4, 
      "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
    }, 
    {
      "answer": "Edward Scissorhands", 
      "category": 5, 
      "difficulty": 3, 
      "id": 6, 
      "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
    }, 
    {
      "answer": "Muhammad Ali", 
      "category": 4, 
      "difficulty": 1, 
      "id": 9, 
      "question": "What boxer's original name is Cassius Clay?"
    }, 
    {
      "answer": "Brazil", 
      "category": 6, 
      "difficulty": 3, 
      "id": 10, 
      "question": "Which is the only team to play in every soccer World Cup tournament?"
    }, 
    {
      "answer": "Uruguay", 
      "category": 6, 
      "difficulty": 4, 
      "id": 11, 
      "question": "Which country won the first ever soccer World Cup in 1930?"
    }, 
    {
      "answer": "George Washington Carver", 
      "category": 4, 
      "difficulty": 2, 
      "id": 12, 
      "question": "Who invented Peanut Butter?"
    }, 
    {
      "answer": "Lake Victoria", 
      "category": 3, 
      "difficulty": 2, 
      "id": 13, 
      "question": "What is the largest lake in Africa?"
    }, 
    {
      "answer": "The Palace of Versailles", 
      "category": 3, 
      "difficulty": 3, 
      "id": 14, 
      "question": "In which royal palace would you find the Hall of Mirrors?"
    }, 
    {
      "answer": "Agra", 
      "category": 3, 
      "difficulty": 2, 
      "id": 15, 
      "question": "The Taj Mahal is located in which Indian city?"
    }
  ], 
  "success": true, 
  "total_questions": 42
}

```

##### POST '/questions/search'
- User type in a string to search for a question and it will return all the questions that contain this string. 
- Example: ```curl http://127.0.0.1:5000/questions/search -X POST -H "Content-Type: application/json" -d '{"searchTerm": "peanut butter"}' ```

```
{
  "questions": [
    {
      "answer": "George Washington Carver", 
      "category": 4, 
      "difficulty": 2, 
      "id": 12, 
      "question": "Who invented Peanut Butter?"
    }
  ], 
  "success": true, 
  "total_questions": 1
}
```

##### GET '/categories/int:id/questions'
- Get questions only in a specific category
- Example: ```curl http://127.0.0.1:5000/categories/2/questions```

```
  "current_category": "Science", 
  "questions": [
    {
      "answer": "The Liver", 
      "category": 1, 
      "difficulty": 4, 
      "id": 20, 
      "question": "What is the heaviest organ in the human body?"
    }, 
    {
      "answer": "Alexander Fleming", 
      "category": 1, 
      "difficulty": 3, 
      "id": 21, 
      "question": "Who discovered penicillin?"
    }, 
    {
      "answer": "Blood", 
      "category": 1, 
      "difficulty": 4, 
      "id": 22, 
      "question": "Hematology is a branch of medicine involving the study of what?"
    }, 
    {
      "answer": "", 
      "category": 1, 
      "difficulty": 1, 
      "id": 24, 
      "question": ""
    }, 
    {
      "answer": "", 
      "category": 1, 
      "difficulty": 1, 
      "id": 25, 
      "question": ""
    }, 
    {
      "answer": "", 
      "category": 1, 
      "difficulty": 1, 
      "id": 26, 
      "question": ""
    }, 
    {
      "answer": "", 
      "category": 1, 
      "difficulty": 1, 
      "id": 27, 
      "question": ""
    }, 
    {
      "answer": "", 
      "category": 1, 
      "difficulty": 1, 
      "id": 28, 
      "question": ""
    }, 
    {
      "answer": "2", 
      "category": 1, 
      "difficulty": 1, 
      "id": 29, 
      "question": "dasda"
    }, 
    {
      "answer": "2", 
      "category": 1, 
      "difficulty": 1, 
      "id": 30, 
      "question": "dasda"
    }
  ], 
  "success": true, 
  "total_questions": 11
  
```

##### POST '/quizzes'
- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Example: ```curl http://127.0.0.1:5000/quizzes -X POST -H "Content-Type: application/json" -d '{"quiz_category":{"type":"Sports","id": "6"}, "previous_questions":[]}'  ```
```
{
  "previousQuestion": [], 
  "question": {
    "answer": "Brazil", 
    "category": 6, 
    "difficulty": 3, 
    "id": 10, 
    "question": "Which is the only team to play in every soccer World Cup tournament?"
  }, 
  "success": true
}
```




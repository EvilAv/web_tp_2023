from django.shortcuts import render
from django.http import HttpResponse


QUESTIONS_DB = [
    {
        'id': i,
        'title': 'Question #' + str(i),
        'text': 'Lorem ipsum dolor sit amet consectetur adipisicing elit. Corrupti incidunt fuga dicta eaque, quae impedit!'
    } for i in range(50)
]

ANSWERS_DB = [
    {
        'title': 'Answer #' + str(i),
        'text': 'Lorem ipsum dolor sit amet consectetur adipisicing elit. Corrupti incidunt fuga dicta eaque, quae impedit!',
        'rate': str(i - 10),
    } for i in range(50)
]


def index(request):
    return render(request, 'index.html', {'questions': QUESTIONS_DB})


def hot(request):
    return render(request, 'index.html', {'questions': QUESTIONS_DB})


def detail_question(request, id):
    return render(request, 'question.html', {'question': QUESTIONS_DB[id], 'answers': ANSWERS_DB})


def questions_by_tag(request, slag):
    return render(request, 'tag.html', {'questions': QUESTIONS_DB, 'tag_name': slag})

def login(request):
    pass
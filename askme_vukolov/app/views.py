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

TAGS_DB = [
    {
        'name': 'tag-' + str(i),
    } for i in range(50)
]


def get_top_tags(rows=3):
    res = []
    idx = 0
    for i in range(rows):
        res.append([])
        for _ in range(4):
            res[i].append(TAGS_DB[idx])
            idx += 1
    return res


def index(request):
    return render(request, 'index.html', {'questions': QUESTIONS_DB,
                                          'tags': get_top_tags(), 'is_logged_in': True})


def hot(request):
    return render(request, 'index.html', {'questions': QUESTIONS_DB,
                                          'tags': get_top_tags(), 'is_logged_in': True})


def detail_question(request, id):
    return render(request, 'question.html', {'question': QUESTIONS_DB[id], 'answers': ANSWERS_DB,
                                             'tags': get_top_tags(), 'is_logged_in': True})


def questions_by_tag(request, slag):
    return render(request, 'tag.html', {'questions': QUESTIONS_DB, 'tag_name': slag,
                                        'tags': get_top_tags(), 'is_logged_in': True})


def login(request):
    return render(request, 'login.html', {'tags': get_top_tags()})


def signup(request):
    return render(request, 'signup.html', {'tags': get_top_tags()})


def ask(request):
    return render(request, 'ask.html', {'tags': get_top_tags(), 'is_logged_in': True})


def user_settings(request):
    return render(request, 'settings.html', {'tags': get_top_tags(), 'is_logged_in': True})
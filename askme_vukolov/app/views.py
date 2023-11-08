from django.shortcuts import render
from django.http import HttpResponse
from django.core.paginator import Paginator, PageNotAnInteger
from .models import Question, Tag, Answer

ANSWERS_DB = [
    {
        'title': 'Answer #' + str(i),
        'text': 'Lorem ipsum dolor sit amet consectetur adipisicing elit. Corrupti incidunt fuga dicta eaque, quae impedit!',
        'rate': str(i - 10),
    } for i in range(50)
]


def get_top_tags(rows=3):
    res = []
    idx = 0
    arr = Tag.objects.popular()
    for i in range(rows):
        res.append([])
        for _ in range(4):
            res[i].append(arr[idx])
            idx += 1
    return res


def paginate(objects_list, request, per_page=10):
    p = Paginator(objects_list, per_page)
    page_idx = request.GET.get('page', 1)
    try:
        page_idx = int(page_idx)
    except ValueError:
        page_idx = 1
    if page_idx < 1:
        page_idx = 1
    elif page_idx > p.num_pages:
        page_idx = p.num_pages
    raw_page = p.page(page_idx)
    correct_page_range = raw_page.paginator.get_elided_page_range(page_idx, on_each_side=2, on_ends=1)
    return {
        'page_obj': raw_page,
        'obj_list': raw_page.object_list,
        'page_range': correct_page_range,
        }


def index(request):
    page = paginate(Question.objects.recent(), request, 15)
    return render(request, 'index.html', {'questions': page['obj_list'],
                                          'tags': get_top_tags(), 'is_logged_in': True,
                                          'page': page})


def hot(request):
    page = paginate(Question.objects.best(), request, 15)
    return render(request, 'index.html', {'questions': page['obj_list'],
                                          'tags': get_top_tags(), 'is_logged_in': True,
                                          'page': page})


def detail_question(request, id):
    page = paginate(Answer.objects.filter(parent__id=id), request, 7)
    return render(request, 'question.html', {'question': Question.objects.get(pk=id), 'answers': page['obj_list'],
                                             'tags': get_top_tags(), 'is_logged_in': True,
                                             'page': page})


def questions_by_tag(request, slag):
    page = paginate(Question.objects.by_tag(slag), request, 15)
    return render(request, 'tag.html', {'questions': page['obj_list'], 'tag_name': slag,
                                        'tags': get_top_tags(), 'is_logged_in': True,
                                        'page': page})


def login(request):
    return render(request, 'login.html', {'tags': get_top_tags()})


def signup(request):
    return render(request, 'signup.html', {'tags': get_top_tags()})


def ask(request):
    return render(request, 'ask.html', {'tags': get_top_tags(), 'is_logged_in': True})


def user_settings(request):
    return render(request, 'settings.html', {'tags': get_top_tags(), 'is_logged_in': True})
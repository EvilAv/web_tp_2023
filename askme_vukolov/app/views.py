from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core.paginator import Paginator, PageNotAnInteger
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .forms import LoginForm, RegisterForm, QuestionFrom, AnswerForm
from .models import Question, Tag, Answer
from django.shortcuts import get_object_or_404, get_list_or_404


def get_top_tags(rows=3):
    res = []
    idx = 0
    arr = Tag.objects.popular()
    for i in range(rows):
        res.append([])
        for _ in range(4):
            if len(arr) <= idx:
                break
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


@login_required(redirect_field_name='continue', login_url='login')
def index(request):
    page = paginate(Question.objects.recent(), request, 15)
    return render(request, 'index.html', {'questions': page['obj_list'],
                                          'tags': get_top_tags(), 'page': page})


@login_required(redirect_field_name='continue', login_url='login')
def hot(request):
    page = paginate(Question.objects.best(), request, 15)
    return render(request, 'index.html', {'questions': page['obj_list'],
                                          'tags': get_top_tags(), 'page': page})


@login_required(redirect_field_name='continue', login_url='login')
def detail_question(request, id):
    question = get_object_or_404(Question, pk=id)
    page = paginate(Answer.objects.filter(parent=question), request, 7)

    if request.method == 'GET':
        answer_form = AnswerForm()
    if request.method == 'POST':
        answer_form = AnswerForm(request.POST)
        if answer_form.is_valid():
            answer = answer_form.save(commit=False)
            answer.author = request.user.profile
            answer.parent = question
            answer.title = "Answer from " + answer.author.nickname
            answer.save()
            return redirect(request.path + '?add=' + str(answer.pk))
        else:
            answer_form.add_error(None, 'Some problems with answer')
    return render(request, 'question.html', {'question': question, 'answers': page['obj_list'],
                                             'tags': get_top_tags(), 'page': page, 'form': answer_form})


@login_required(redirect_field_name='continue', login_url='login')
def questions_by_tag(request, slag):
    questions = get_list_or_404(Question.objects.by_tag(slag))
    page = paginate(questions, request, 7)
    return render(request, 'tag.html', {'questions': page['obj_list'], 'tag_name': slag,
                                        'tags': get_top_tags(), 'page': page})


def login_view(request):
    if request.method == 'GET':
        login_form = LoginForm()
    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user = authenticate(request, **login_form.cleaned_data)
            if user is not None:
                login(request, user)
                next_page = request.GET.get('continue')
                if next_page is None:
                    next_page = reverse('index')
                return redirect(next_page)
            else:
                login_form.add_error(None, 'Sorry, wrong password')
                login_form.add_error('password', '')
        else:
            login_form.add_error(None, 'Some authentication problems')
            login_form.add_error('password', '')

    return render(request, 'login.html', {'tags': get_top_tags(), 'form': login_form})


@login_required(redirect_field_name='continue', login_url='login')
def logout_view(request):
    logout(request)
    return redirect(request.GET.get('continue'))


def signup(request):
    if request.method == 'GET':
        signup_form = RegisterForm()
    if request.method == 'POST':
        signup_form = RegisterForm(request.POST)
        if signup_form.is_valid():
            user = signup_form.save()
            if user:
                login(request, user)
                return redirect(reverse('index'))
            else:
                signup_form.add_error(None, 'Some complex registration problems')
        else:
            signup_form.add_error(None, 'Some registration problems')

    return render(request, 'signup.html', {'tags': get_top_tags(), 'form': signup_form})


@login_required(redirect_field_name='continue', login_url='login')
def ask(request):
    if request.method == 'GET':
        question_form = QuestionFrom()
    if request.method == 'POST':
        question_form = QuestionFrom(request.POST)
        if question_form.is_valid():
            q = question_form.save(commit=False)
            q.author = request.user.profile
            q.save()
            question_form.save_m2m()
            return redirect(reverse('detail_question', args=[q.pk]))
        else:
            question_form.add_error(None, 'Some problems with question')
    return render(request, 'ask.html', {'tags': get_top_tags(), 'form': question_form})


@login_required(redirect_field_name='continue', login_url='login')
def user_settings(request):
    return render(request, 'settings.html', {'tags': get_top_tags()})

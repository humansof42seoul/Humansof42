import json

from django.contrib.auth.decorators import login_required, permission_required
from django.core.serializers.json import DjangoJSONEncoder
from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.http import Http404, HttpResponse, JsonResponse
from django.conf import settings
from django.template.loader import render_to_string

from .models import Interview, Comment
from .forms import InterviewForm, CommentForm


def home(request):
    return render(request, 'interview/index.html')


def about(request):
    return render(request, 'interview/about.html')


def interview_detail(request, pk):
    try:
        interview = Interview.objects.get(pk=pk)
    except Interview.DoesNotExist:
        raise Http404('게시글을 찾을 수 없습니다.')
    is_liked = False
    if interview.likes.filter(id=request.user.id).exists():
        is_liked = True
    comment_form = CommentForm()
    comments = interview.comment_set.all()
    image = interview.image
    return render(request, 'interview/interview_detail.html', {'interview': interview, 'image': image,
                                                               'is_liked': is_liked,
                                                               'comments': comments, 'comment_form': comment_form})


@permission_required('admin', raise_exception=True)
def interview_write(request):
    if request.method == 'POST':
        form = InterviewForm(request.POST)
        if form.is_valid():
            interview = Interview()
            interview.title = form.cleaned_data['title']
            interview.interviewee = form.cleaned_data['interviewee']
            interview.interviewer = form.cleaned_data['interviewer']
            interview.photographer = form.cleaned_data['photographer']
            interview.content = form.cleaned_data['content']
            interview.image = request.FILES['image']
            interview.save()
            return redirect('/interviews/')
    else:
        form = InterviewForm()
    return render(request, 'interview/interview_write.html', {'form': form})


@permission_required('admin', raise_exception=True)
def interview_edit(request, pk):
    try:
        interview = Interview.objects.get(pk=pk)
    except Interview.DoesNotExist:
        raise Http404('게시글을 찾을 수 없습니다.')
    if request.method == "POST":
        form = InterviewForm(request.POST)
        if form.is_valid():
            interview.title = form.cleaned_data['title']
            interview.interviewee = form.cleaned_data['interviewee']
            interview.interviewer = form.cleaned_data['interviewer']
            interview.photographer = form.cleaned_data['photographer']
            interview.content = form.cleaned_data['content']
            interview.save()
            return redirect('/interviews/' + str(pk))
    else:
        form = InterviewForm(instance=interview)
        return render(request, 'interview/interview_edit.html', {'form': form, 'interview': interview})


def interview_list(request):
    # 모든 게시글을 시간 역순(최신것 먼저)으로 가져옴
    interviews = Interview.objects.all().order_by('-id')
    # page = int(request.GET.get('p', 1))
    # paginator = Paginator(all_interviews, 9)
    # interviews = paginator.get_page(page)
    return render(request, 'interview/index.html', {'interviews': interviews})


def like_interview(request):
    if not request.user.is_authenticated:
        return
    if request.method == 'POST':
        pk = request.POST.get('pk')
        interview = get_object_or_404(Interview, id=pk)
        if interview.likes.filter(id=request.user.id).exists():
            interview.likes.remove(request.user)
            is_liked = False
        else:
            interview.likes.add(request.user)
            is_liked = True
        interview.save()
        data = {
            'pk': pk,
            'is_liked': is_liked,
            'total_likes': interview.total_likes(),
        }
        return HttpResponse(json.dumps(data, cls=DjangoJSONEncoder), content_type='application/json')


@login_required(login_url=settings.LOGIN_URL)
def write_comment(request, pk):
    interview = get_object_or_404(Interview, id=pk)
    writer = request.user
    content = request.POST.get('content')
    if content:
        comment = Comment.objects.create(writer=writer, interview=interview, content=content)
        comment.save()
        interview.save()
        data = {
            'writer': writer.login,
            'content': content,
            'created': '방금전',
            'comment_id': comment.id,
        }
        return HttpResponse(json.dumps(data, cls=DjangoJSONEncoder), content_type='application/json')


@login_required(login_url=settings.LOGIN_URL)
def delete_comment(request, pk):
    interview = get_object_or_404(Interview, id=pk)
    comment_id = request.POST.get('comment_id')
    comment = Comment.objects.get(pk=comment_id)
    if request.user == comment.writer:
        comment.delete()
        interview.save()
        data = {
            'comment_id': comment_id,
        }
        return HttpResponse(json.dumps(data, cls=DjangoJSONEncoder), content_type="application/json")

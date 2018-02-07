from django.shortcuts import render, get_object_or_404
# 同理 get_list_or_404()  

from django.template import loader
from django.http import HttpResponse, Http404, HttpResponseRedirect

from django.shortcuts import render

from django.urls import reverse
from .models import Question, Choice

from project.libs.decorator import post_method, get_method


def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]  # 降序，取 5 个
    context = {
        'latest_question_list': latest_question_list,
    }

    '''
    template = loader.get_template('polls/index.html')
    return HttpResponse(template.render(context, request))
    简写如下
    '''
    return render(request, 'polls/index.html', context )

def detail(request, question_id):
    # try:
    #     question = Question.objects.get(pk=question_id)
    # except Question.DoesNotExist:
    #     raise Http404("Question does not exist")
    # return render(request, 'polls/detail.html', {'question': question})

    # 简写
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/detail.html', {'question': question})

def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/results.html', {'question': question})


@post_method
def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
    	# 多个人同时投票时，会导致竞争条件的出现，解决方法https://docs.djangoproject.com/en/2.0/ref/models/expressions/#avoiding-race-conditions-using-f
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.

        # 这里的 reverse 通过给定的 模板名和参数，生成对应的url, 如 '/polls/3/results/'
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))

def action(request, question_id):
    pass
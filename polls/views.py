from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.views import generic
from django.utils import timezone

from polls.models import Question, Choice

""" 版本：函数视图 """
# def index(request):
#     # return HttpResponse("Hello, world. You're at the polls index.")
#     # - - -
#     # latest_question_list = Question.objects.order_by('-pub_date')[:5]
#     # output = ', '.join([q.question_text for q in latest_question_list])
#     # return HttpResponse(output)
#     # - - -
#     # latest_question_list = Question.objects.order_by('-pub_date')[:5]
#     # template = loader.get_template('polls/index.html')
#     # context = {
#     #     'latest_question_list': latest_question_list,
#     # }
#     # return HttpResponse(template.render(context, request))
#     # - - -
#     latest_question_list = Question.objects.order_by('-pub_date')[:5]
#     context = {'latest_question_list': latest_question_list}
#     return render(request, 'polls/index.html', context)


# def detail(request, question_id):
#     # return HttpResponse("You're looking at question %s." % question_id)
#     # - - -
#     # try:
#     #     question = Question.objects.get(pk=question_id)
#     # except Question.DoesNotExist:
#     #     raise Http404("Question does not exist")
#     # return render(request, 'polls/detail.html', {'question': question})
#     # - - -
#     question = get_object_or_404(Question, pk=question_id)
#     return render(request, 'polls/detail.html', {'question': question})
#
#
# def results(request, question_id):
#     # response = "You're looking at the results of question %s."
#     # return HttpResponse(response % question_id)
#     # - - -
#     question = get_object_or_404(Question, pk=question_id)
#     return render(request, 'polls/results.html', {'question': question})
#
#
# def vote(request, question_id):
#     # return HttpResponse("You're voting on question %s." % question_id)
#     # - - -
#     question = get_object_or_404(Question, pk=question_id)
#     try:
#         # request.POST['choice'] returns the ID of the selected choice, as a string.
#         # request.POST values are always strings
#         selected_choice = question.choice_set.get(pk=request.POST['choice'])
#     except (KeyError, Choice.DoesNotExist):
#         # Redisplay the question voting form.
#         return render(request, 'polls/detail.html', {
#             'question': question,
#             'error_message': "You didn't select a choice.",
#         })
#     else:
#         selected_choice.votes += 1
#         selected_choice.save()
#         # Always return an HttpResponseRedirect after successfully dealing
#         # with POST data. This prevents data from being posted twice if a
#         # user hits the Back button.
#
#         # This tip isn’t specific to Django; it’s good Web development practice in general.
#
#         # In this case, using the URLconf we set up in Tutorial 3,
#         # this reverse() call will return a string like '/polls/3/results/'.
#         return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))


""" 版本：类视图(generic views) """


class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    # def get_queryset(self):
    #     """Return the last five published questions."""
    #     return Question.objects.order_by('-pub_date')[:5]

    def get_queryset(self):
        """
        Return the last five published questions (not including those set to be
        published in the future).
        """
        return Question.objects.filter(
            pub_date__lte=timezone.now()
        ).order_by('-pub_date')[:5]


# <https://docs.djangoproject.com/en/3.1/intro/tutorial04/>
# Each generic view needs to know what model it will be acting upon.
# This is provided using the model attribute.

# The DetailView generic view expects the primary key value captured from the URL to be called "pk",
# so we’ve changed question_id to pk for the generic views.
class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'

    # What we have works well; however, even though future questions don’t appear in the index,
    # users can still reach them if they know or guess the right URL.
    # So we need to add a similar constraint to DetailView:
    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'


# - - -
def vote(request, question_id):
    # return HttpResponse("You're voting on question %s." % question_id)
    # - - -
    question = get_object_or_404(Question, pk=question_id)
    try:
        # request.POST['choice'] returns the ID of the selected choice, as a string.
        # request.POST values are always strings
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        # This tip isn’t specific to Django; it’s good Web development practice in general.
        # In this case, using the URLconf we set up in Tutorial 3,
        # this reverse() call will return a string like '/polls/3/results/'.
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))

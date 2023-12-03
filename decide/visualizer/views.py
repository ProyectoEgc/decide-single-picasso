import json
from django.views.generic import TemplateView
from django.conf import settings
from django.http import Http404
from django.shortcuts import render, get_object_or_404
from voting.models import Voting

from base import mods


class VisualizerView(TemplateView):
    template_name = 'visualizer/visualizer.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        voting_id = self.kwargs.get('voting_id')
        context['promedio'] = self.score_average(voting_id)

        vid = kwargs.get('voting_id', 0)

        try:
            r = mods.get('voting', params={'id': vid})
            context['voting'] = json.dumps(r[0])
        except:
            raise Http404

        return context
    
    
    
    def score_average(self, voting_id):
        voting = get_object_or_404(Voting, id=voting_id)
        ac = 0
        number_votes = 0
    
        for opt in voting.postproc:
            option = int(opt['option'])
            votes = int(opt['votes'])
            ac = ac + option*votes
            number_votes = number_votes + votes
    
        promedio = ac / number_votes
    
        return promedio
    



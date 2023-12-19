from django.test import TestCase

from visualizer.views import VisualizerView
from voting.models import Voting, Question

class TestScoreAverageFunction(TestCase):
    def setUp(self):
        self.question = Question.objects.create(id=1,type='S'
        )
        self.question = Question.objects.create(id=2,type='C'
        )
        self.voting = Voting.objects.create(id=1,question_id=1, postproc=[
            {'option': '0', 'number': '2','votes': '0'},
            {'option': '1', 'number': '3','votes': '3'},
            {'option': '2', 'number': '4','votes': '5'},
            {'option': '3', 'number': '5','votes': '0'},
            {'option': '4', 'number': '6','votes': '0'},
            {'option': '5', 'number': '7','votes': '0'},
            {'option': '6', 'number': '8','votes': '0'},
            {'option': '7', 'number': '9','votes': '0'},
            {'option': '8', 'number': '10','votes': '0'},
            {'option': '9', 'number': '11','votes': '0'},
            {'option': '10', 'number': '12','votes': '0'},
        ])
        self.voting = Voting.objects.create(id=2,question_id=2, postproc=[
            {'option': '0', 'number': '1','votes': '0'},
            {'option': '1', 'number': '2','votes': '3'},
        ])

        self.voting = Voting.objects.create(id=3,question_id=1, postproc=[
            {'option': '0', 'number': '2','votes': '0'},
            {'option': '1', 'number': '3','votes': '0'},
            {'option': '2', 'number': '4','votes': '0'},
            {'option': '3', 'number': '5','votes': '0'},
            {'option': '4', 'number': '6','votes': '0'},
            {'option': '5', 'number': '7','votes': '0'},
            {'option': '6', 'number': '8','votes': '0'},
            {'option': '7', 'number': '9','votes': '0'},
            {'option': '8', 'number': '10','votes': '0'},
            {'option': '9', 'number': '11','votes': '0'},
            {'option': '10', 'number': '12','votes': '0'},
        ])

        
    def tearDown(self):
        Voting.objects.filter(id=1).delete()

    def test_score_average_with_positive_votes(self):
        visualizer = VisualizerView()

        resultado = visualizer.score_average(voting_id=1)

        self.assertEqual(resultado, (1*3 + 2*5) / (3 + 5))      

    def test_score_average_not_equal(self):
        visualizer = VisualizerView()

        resultado = visualizer.score_average(voting_id=1)

        self.assertNotEqual(resultado, 200)

    def test_score_average_division_zero(self):
        visualizer = VisualizerView()

        with self.assertRaises(ZeroDivisionError):
            self.assertRaises(visualizer.score_average(voting_id=3))

    def test_score_average_different_question_type(self):
        visualizer = VisualizerView()

        resultado = visualizer.score_average(voting_id=2)

        self.assertEqual(resultado, -1) 

   

    
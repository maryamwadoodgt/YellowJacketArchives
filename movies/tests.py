from django.test import TestCase
from django.urls import reverse
from .models import Movie, LibraryBranch, Stock


class BranchesAPITest(TestCase):
	def setUp(self):
		self.movie = Movie.objects.create(name='Test Book', description='desc', available=True)
		self.branch = LibraryBranch.objects.create(name='Test Branch', latitude=33.77, longitude=-84.39)
		Stock.objects.create(movie=self.movie, branch=self.branch, count=3)

	def test_branches_list(self):
		url = reverse('movies.branches_list')
		resp = self.client.get(url)
		self.assertEqual(resp.status_code, 200)
		data = resp.json()
		self.assertIn('branches', data)
		self.assertTrue(any(b['name'] == 'Test Branch' for b in data['branches']))

	def test_movie_branches(self):
		url = reverse('movies.movie_branches', args=[self.movie.id])
		resp = self.client.get(url)
		self.assertEqual(resp.status_code, 200)
		data = resp.json()
		self.assertEqual(data.get('movie_id'), self.movie.id)
		self.assertTrue(len(data.get('branches', [])) >= 1)

from django.test import TestCase
from django.urls import reverse
from .models import Book


class BookViewsTest(TestCase):
	def setUp(self):
		Book.objects.create(title='Django for Humans', author='Jane Doe', genre='Tech', summary='A friendly guide.', publication_year=2020, available=True)
		Book.objects.create(title='Advanced Django', author='John Smith', genre='Tech', summary='Deep dive.', publication_year=2021, available=False)

	def test_search_by_title(self):
		response = self.client.get(reverse('books.index'), {'search': 'Django for Humans'})
		self.assertEqual(response.status_code, 200)
		self.assertContains(response, 'Django for Humans')

	def test_search_by_author(self):
		response = self.client.get(reverse('books.index'), {'search': 'John Smith'})
		self.assertEqual(response.status_code, 200)
		self.assertContains(response, 'Advanced Django')

	def test_book_detail(self):
		book = Book.objects.first()
		response = self.client.get(reverse('books.show', args=[book.id]))
		self.assertEqual(response.status_code, 200)
		self.assertContains(response, book.title)
		self.assertContains(response, book.author)

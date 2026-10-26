import datetime

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .models import Choice, Question


def create_question(question_text, days):
    """Create a question published the given number of `days` offset to now."""
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)


class QuestionModelTests(TestCase):
    def test_was_published_recently_with_future_question(self):
        """was_published_recently() returns False for questions in the future."""
        future_question = create_question("Future question.", days=30)
        self.assertIs(future_question.was_published_recently(), False)

    def test_was_published_recently_with_old_question(self):
        """was_published_recently() returns False for questions older than 1 day."""
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_question = Question(pub_date=time)
        self.assertIs(old_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        """was_published_recently() returns True for questions within the last day."""
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_question = Question(pub_date=time)
        self.assertIs(recent_question.was_published_recently(), True)

    def test_str(self):
        question = create_question("What's up?", days=0)
        choice = Choice.objects.create(question=question, choice_text="Not much")
        self.assertEqual(str(question), "What's up?")
        self.assertEqual(str(choice), "Not much")


class QuestionIndexViewTests(TestCase):
    def test_no_questions(self):
        response = self.client.get(reverse("polls:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerySetEqual(response.context["latest_question_list"], [])

    def test_shows_latest_five_questions(self):
        questions = [create_question(f"Question {i}.", days=-i) for i in range(6)]
        response = self.client.get(reverse("polls:index"))
        self.assertQuerySetEqual(
            response.context["latest_question_list"], questions[:5]
        )


class QuestionDetailViewTests(TestCase):
    def test_detail_shows_choices(self):
        question = create_question("Past question.", days=-1)
        Choice.objects.create(question=question, choice_text="Yes")
        response = self.client.get(reverse("polls:detail", args=(question.id,)))
        self.assertContains(response, question.question_text)
        self.assertContains(response, "Yes")

    def test_missing_question_returns_404(self):
        response = self.client.get(reverse("polls:detail", args=(999,)))
        self.assertEqual(response.status_code, 404)


class VoteViewTests(TestCase):
    def setUp(self):
        self.question = create_question("Vote question.", days=-1)
        self.choice = Choice.objects.create(question=self.question, choice_text="A")

    def test_vote_increments_and_redirects(self):
        response = self.client.post(
            reverse("polls:vote", args=(self.question.id,)),
            {"choice": self.choice.id},
        )
        self.assertRedirects(
            response, reverse("polls:results", args=(self.question.id,))
        )
        self.choice.refresh_from_db()
        self.assertEqual(self.choice.votes, 1)

    def test_vote_without_choice_shows_error(self):
        response = self.client.post(reverse("polls:vote", args=(self.question.id,)))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "You didn&#x27;t select a choice.")

    def test_results_page(self):
        response = self.client.get(reverse("polls:results", args=(self.question.id,)))
        self.assertContains(response, "A -- 0 votes")

from unittest import TestCase
from app import app
from flask import session
from boggle import Boggle


class FlaskTests(TestCase):
  def test_home_page(self):
    """Checking first visit to homepage if template is loading and session cookie is setting inital values"""
    with app.test_client() as client:
      res = client.get('/')
      html = res.get_data(as_text=True)

      self.assertEqual(res.status_code, 200)
      self.assertIn('<h3>Top Scores</h3>', html)
      self.assertEqual(session['high_scores'], [])
      self.assertEqual(session['gamesplayed'], 0)

  def test_start_game(self):
    """testing the start button post request is setting board as a list and storing in session cookie"""
    with app.test_client() as client:
      res = client.post('/start')

      self.assertEqual(res.status_code, 302)
      self.assertEqual(res.location, 'http://localhost/game')
      self.assertIsInstance(session['board'], list)

  def test_start_redirect_followed(self):
    """Checking start button post request is redirecting to game board"""
    with app.test_client() as client:
      res = client.post('/start', follow_redirects = True)
      html = res.get_data(as_text=True)

      self.assertEqual(res.status_code, 200)
      self.assertIn('<input type="text" name="guess" id="guess" />', html)

  def test_game_logic_ok(self):
    """Checking guess submit with a valid guess"""
    with app.test_client as client:
      with app.client.session_transaction() as change_session:
        change_session['board'] = [['b','o','a','r','d'],['b','o','a','r','d'],['b','o','a','r','d'],['b','o','a','r','d'],['b','o','a','r','d']]
      res = client.post('/logic', data={'guess': 'board'})
      answer = res.get_data(as_text=True)
      self.assertEqual(res.status_code, 200)
      self.assertIn('ok', answer)
  
  def test_game_logic_not_word(self):
    """Checking guess submit with an invalid guess(not a real word)"""
    with app.test_client as client:
      with app.client.session_transaction() as change_session:
        change_session['board'] = [['b','o','a','r','d'],['b','o','a','r','d'],['b','o','a','r','d'],['b','o','a','r','d'],['b','o','a','r','d']]
      res = client.post('/logic', data={'guess': 'asdf'})
      answer = res.get_data(as_text=True)
      self.assertEqual(res.status_code, 200)
      self.assertIn('not-word', answer)
  
  def test_game_logic_not_board(self):
    """Checking guess submit with an invalid guess(valid word, not on board)"""
    with app.test_client as client:
      with app.client.session_transaction() as change_session:
        change_session['board'] = [['b','o','a','r','d'],['b','o','a','r','d'],['b','o','a','r','d'],['b','o','a','r','d'],['b','o','a','r','d']]
      res = client.post('/logic', data={'guess': 'talk'})
      answer = res.get_data(as_text=True)
      self.assertEqual(res.status_code, 200)
      self.assertIn('not-on-board', answer)

  def test_endgame_new_high_score(self):
    """Checking new high score changes list"""
    with app.test_client as client:
      with app.client.session_transaction() as change_session:
        change_session['high_scores'] = [1,2,3]
        change_session['gamesplayed'] = 4
    res = client.post('/endgame', data={'score' = 23})

    self.assertEqual(session['high_scores'], [23,3,2])
    self.assertEqual(session['gamesplayed'], 5)
  
  def test_endgame_not_high_score(self):
    """Checking no new high score not changing list, but sorting descending"""
    with app.test_client as client:
      with app.client.session_transaction() as change_session:
        change_session['high_scores'] = [100,200,300]
        change_session['gamesplayed'] = 4
    res = client.post('/endgame', data={'score' = 23})

    self.assertEqual(session['high_scores'], [300,200,100])
    self.assertEqual(session['gamesplayed'], 5)
  
  def test_endgame_not_enough_high_score(self):
    """Checking only one previous high score, should change list to 2 entries"""
    with app.test_client as client:
      with app.client.session_transaction() as change_session:
        change_session['high_scores'] = [100]
        change_session['gamesplayed'] = 1
    res = client.post('/endgame', data={'score' = 23})

    self.assertEqual(session['high_scores'], [100,23])
    self.assertEqual(session['gamesplayed'], 2)
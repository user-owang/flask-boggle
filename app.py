from boggle import Boggle
from flask import *
boggle_game = Boggle()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'abcdefghijklmnopqrstuvwxyz'


@app.route('/')
def showHome():
  """shows home page with start button"""
  if not session.get('gamesplayed'):
    session['gamesplayed'] = 0
    session['high_scores'] = []
  return render_template('home.html')

@app.route('/start', methods=['POST'])
def startGame():
  """Create board and reset session"""
  board = boggle_game.make_board()
  session['board'] = board
  session['found'] = []
  return redirect('/game')

@app.route('/game')
def showGame():
  """show game board and guess form"""
  return render_template('game.html')
  

@app.route('/logic')
def check_word():
  """check logic"""
  
  guess = request.args['word']
  board = session["board"]
  response = boggle_game.check_valid_word(board, guess)
  
  return jsonify({'result': response})

@app.route('/endgame', methods=['POST'])
def end_game():
  """store last score and check for high score in sessions and store number of games played"""
  print(request.json)
  last_score = request.json['score']
  high_scores = session['high_scores']
  high_scores.append(last_score)
  high_scores.sort(reverse=True)
  if len(high_scores) > 3:
    high_scores.pop(-1)
  session['high_scores'] = high_scores
  session['gamesplayed'] += 1
  return str(request.json)
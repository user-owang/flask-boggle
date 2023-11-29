from boggle import Boggle
from flask import *
boggle_game = Boggle()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'abcdefghijklmnopqrstuvwxyz'


@app.route('/')
def showHome():
  """shows home page with start button"""
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
  
  guess = request.args['guess']
  board = session["board"]
  response = boggle_game.check_valid_word(board, guess)
  
  return jsonify({'result': response})
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
  

@app.route('/logic', methods=['POST'])
def check_word():
  """check logic"""
  guess = request.form['guess']
    
  if session['found'].count(guess) == 0:
    validation_result = boggle_game.check_valid_word(session['board'], guess)
        
    if validation_result == 'ok':
      found = session['found']
      found.append(guess)
      session['found'] = found
      flash('Great guess!', 'good')
    elif validation_result == 'not-on-board':
      flash('That word is not found on the current game board!', 'bad')
    elif validation_result == 'not-word':
      flash('That guess is not a word!', 'bad')
  else:
    flash('You have already guessed that word!', 'bad')
    
  return redirect('/game')
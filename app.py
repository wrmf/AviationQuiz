from flask import Flask, render_template, request, redirect, url_for, session, Blueprint
import sys
from modules.questions import *
from fileIO import *
import pandas as pd
import importlib
import string


TEMPLATES_AUTO_RELOAD = True

MAXQUESTIONS = 10
app = Flask(__name__)

# index page
@app.route("/", methods=[ 'GET', 'POST' ])	# 'GET' and 'POST' are HTML methods that are used in the corresponding html file
def index():
	curruser = session.get('curruser', None)
	theme = session.get('theme', None)
	session['currentQuestion'] = 0  # reset current question counter
	session['numCorrect'] = 0  # reset current question counter
	session['answerString'] = ""  # reset current question counter
	session['listOfQuestions'] = []

	# If theme doesn't exist, set to dark
	if not theme:
		theme = 'Dark'

	if request.method == 'POST':
		# Get the theme
		if request.form.get('toggle-button') == 'Dark':
			session['theme'] = 'Dark'
			theme = session.get('theme', None)
		elif request.form.get('toggle-button') == 'Light':
			session['theme'] = 'Light'
			theme = session.get('theme', None)
		# Go straight to home
		elif request.form.get('skip') == 'Home':
			# Throw error if not logged in
			if not curruser:
				error = 'Currently not logged in.'
				return render_template('index.html', theme=theme, error=error)
			else:
				return redirect(url_for('home'))
	return render_template('index.html', theme=theme, error=None)

@app.route("/codes", methods=[ 'GET', 'POST' ])#, methods=[ 'GET', 'POST' ])	# 'GET' and 'POST' are HTML methods that are used in the corresponding html file
def codes():
	code_df = read_from_code_file()
	answerString = session.get('answerString', None)
	theme = session.get('theme', None)
	ret = get_code_question(session.get('listOfQuestions'), code_df, len(code_df))

	if(session.get('listOfQuestions') is None):
		session['listOfQuestions'] = [ret[0]]
	else:
		Q = session.get('listOfQuestions')
		Q.append(ret[0])
		session['listOfQuestions'] = Q

	numCorrect = session.get('numCorrect', None)
	currentQuestion = session.get('currentQuestion', None)

	if(currentQuestion < 10):

		correctAnswer = session.get('correctAnswer', None)  # Get correct answer

		if request.method == 'GET':
			session['correctAnswer'] = ret[0] #correctAnswer # Set correct answer
		if request.method == 'POST':
			answer = request.form.get('answer', 'No answer')  # Get answer from button press with a default value of "No answer"

			if (answer is not None and correctAnswer is not None and compareString(answer, correctAnswer)):
				numCorrect += 1
				session['numCorrect'] = numCorrect  # Set
				if currentQuestion != 0:
					answerString = answerString + f"{session.get('question', None)}:{answer} ✅ {correctAnswer}\n"
					session['answerString'] = answerString
			else:
				if currentQuestion != 0:
					answerString = answerString + f"{session.get('question', None)}: {answer} ❌ {correctAnswer}\n"
					session['answerString'] = answerString

			currentQuestion += 1  # Increment current question
			session['currentQuestion'] = currentQuestion  # Save to cookies
			session['correctAnswer'] = ret[0]
			session['question'] = ret[1]
	else:
		correctAnswer = session.get('correctAnswer', None)  # Get correct answer
		answer = request.form.get('answer', 'No answer')  # Get answer from button press with a default value of "No answer"

		if (answer is not None and correctAnswer is not None and compareString(answer, correctAnswer)):
			numCorrect += 1
			session['numCorrect'] = numCorrect  # Set
			if currentQuestion != 0:
				answerString = answerString + f"{session.get('question', None)}:{answer} ✅ {correctAnswer}\n"
				session['answerString'] = answerString
		else:
			if currentQuestion != 0:
				answerString = answerString + f"{session.get('question', None)}: {answer} ❌ {correctAnswer}\n"
				session['answerString'] = answerString

		if(answer is not None and correctAnswer is not None and compareString(answer, correctAnswer)):
			numCorrect += 1
			session['numCorrect'] = numCorrect  #Set

		return redirect(url_for('gameComplete'))


	if not theme:
		theme = 'Dark'

	answerArray = answerString.split('\n')
	while(len(answerArray) <= 10):
		answerArray.append('')
	return render_template('codes.html', theme=theme, question=ret[1], correctQ=numCorrect,currQ=currentQuestion, maxQ=MAXQUESTIONS, q0=answerArray[0], q1=answerArray[1], q2=answerArray[2], q3=answerArray[3], q4=answerArray[4], q5=answerArray[5], q6=answerArray[6], q7=answerArray[7], q8=answerArray[8], q9=answerArray[9])

@app.route("/complete/", methods=[ 'GET', 'POST' ])#, methods=[ 'GET', 'POST' ])	# 'GET' and 'POST' are HTML methods that are used in the corresponding html file
def gameComplete():
	theme = session.get('theme', None)

	# If theme doesn't exist, set to dark
	if not theme:
		theme = 'Dark'

	score = int(session.get('numCorrect', None)) #Get current score
	message = f'Congrats, you scored {score}/10' #Message to display on page
	answers = session.get('answerString', None)
	answerArray = answers.split('\n')

	return render_template('complete.html', theme=theme, message=message, q0=answerArray[0], q1=answerArray[1], q2=answerArray[2], q3=answerArray[3], q4=answerArray[4], q5=answerArray[5], q6=answerArray[6], q7=answerArray[7], q8=answerArray[8], q9=answerArray[9]) #Render window

@app.route("/metar", methods=[ 'GET', 'POST' ])
def metar():
	metar_df = read_from_metar_file()
	answerString = session.get('answerString', None)
	theme = session.get('theme', None)
	ret = get_metar_questions(session.get('listOfQuestions'), metar_df, len(metar_df))

	if(session.get('listOfQuestions') is None):
		session['listOfQuestions'] = [ret[0]]
	else:

		Q = session.get('listOfQuestions')
		Q.append(ret[0])
		session['listOfQuestions'] = Q

	numCorrect = session.get('numCorrect', None)
	currentQuestion = session.get('currentQuestion', None)

	if (currentQuestion < 10):

		correctAnswer = session.get('correctAnswer', None)  # Get correct answer

		if request.method == 'GET':
			session['correctAnswer'] = ret[0]  # correctAnswer # Set correct answer
		if request.method == 'POST':
			answer = request.form.get('answer',
									  'No answer')  # Get answer from button press with a default value of "No answer"

			if (answer is not None and correctAnswer is not None and compareMETAR(answer, correctAnswer)):
				numCorrect += 1
				session['numCorrect'] = numCorrect  # Set
				if currentQuestion != 0:
					answerString = answerString + f"{answer} ✅ {correctAnswer}\n"
					session['answerString'] = answerString
			else:
				if currentQuestion != 0:
					answerString = answerString + f"{answer} ❌ {correctAnswer}\n"
					session['answerString'] = answerString

			currentQuestion += 1  # Increment current question
			session['currentQuestion'] = currentQuestion  # Save to cookies
			session['correctAnswer'] = ret[0]
			session['question'] = ret[1]
	else:
		correctAnswer = session.get('correctAnswer', None)  # Get correct answer
		answer = request.form.get('answer',
								  'No answer')  # Get answer from button press with a default value of "No answer"

		if (answer is not None and correctAnswer is not None and compareMETAR(answer, correctAnswer)):
			numCorrect += 1
			session['numCorrect'] = numCorrect  # Set
			if currentQuestion != 0:
				answerString = answerString + f"{answer} ✅ {correctAnswer}\n"
				session['answerString'] = answerString
		else:
			if currentQuestion != 0:
				answerString = answerString + f"{answer} ❌ {correctAnswer}\n"
				session['answerString'] = answerString

		return redirect(url_for('gameComplete'))

	if not theme:
		theme = 'Dark'

	answerArray = answerString.split('\n')
	while (len(answerArray) <= 10):
		answerArray.append('')
	return render_template('metar.html', theme=theme, question=ret[1], correctQ=numCorrect, currQ=currentQuestion,
						   maxQ=MAXQUESTIONS, q0=answerArray[0], q1=answerArray[1], q2=answerArray[2],
						   q3=answerArray[3], q4=answerArray[4], q5=answerArray[5], q6=answerArray[6],
						   q7=answerArray[7], q8=answerArray[8], q9=answerArray[9])

@app.route("/taf", methods=[ 'GET', 'POST' ])
def taf():
	theme = session.get('theme', None)

	if not theme:
		theme = 'Dark'

	taf_df = read_from_taf_file()
	answerString = session.get('answerString', None)
	theme = session.get('theme', None)
	ret = get_taf_questions(session.get('listOfQuestions'), taf_df, len(taf_df))

	if (session.get('listOfQuestions') is None):
		session['listOfQuestions'] = [ret[0]]
	else:
		Q = session.get('listOfQuestions')
		Q.append(ret[0])
		session['listOfQuestions'] = Q

	numCorrect = session.get('numCorrect', None)
	currentQuestion = session.get('currentQuestion', None)

	if (currentQuestion < 10):

		correctAnswer = session.get('correctAnswer', None)  # Get correct answer

		if request.method == 'GET':
			session['correctAnswer'] = ret[0]  # correctAnswer # Set correct answer
		if request.method == 'POST':
			answer = request.form.get('answer',
									  'No answer')  # Get answer from button press with a default value of "No answer"

			if (answer is not None and correctAnswer is not None and compareTAF(answer, correctAnswer)):
				numCorrect += 1
				session['numCorrect'] = numCorrect  # Set
				if currentQuestion != 0:
					answerString = answerString + f"{answer} ✅ {correctAnswer}\n"
					session['answerString'] = answerString
			else:
				if currentQuestion != 0:
					answerString = answerString + f"{answer} ❌ {correctAnswer}\n"
					session['answerString'] = answerString

			currentQuestion += 1  # Increment current question
			session['currentQuestion'] = currentQuestion  # Save to cookies
			session['correctAnswer'] = ret[0]
			session['question'] = ret[1]
	else:
		correctAnswer = session.get('correctAnswer', None)  # Get correct answer
		answer = request.form.get('answer',
								  'No answer')  # Get answer from button press with a default value of "No answer"

		if (answer is not None and correctAnswer is not None and compareTAF(answer, correctAnswer)):
			numCorrect += 1
			session['numCorrect'] = numCorrect  # Set
			if currentQuestion != 0:
				answerString = answerString + f"{answer} ✅ {correctAnswer}\n"
				session['answerString'] = answerString
		else:
			if currentQuestion != 0:
				answerString = answerString + f"{answer} ❌ {correctAnswer}\n"
				session['answerString'] = answerString

		return redirect(url_for('gameComplete'))

	if not theme:
		theme = 'Dark'

	answerArray = answerString.split('\n')
	while (len(answerArray) <= 10):
		answerArray.append('')
	return render_template('taf.html', theme=theme, question=ret[1], correctQ=numCorrect, currQ=currentQuestion,
						   maxQ=MAXQUESTIONS, q0=answerArray[0], q1=answerArray[1], q2=answerArray[2],
						   q3=answerArray[3], q4=answerArray[4], q5=answerArray[5], q6=answerArray[6],
						   q7=answerArray[7], q8=answerArray[8], q9=answerArray[9])

@app.route("/types", methods=[ 'GET', 'POST' ])
def types():
	theme = session.get('theme', None)

	if not theme:
		theme = 'Dark'

	types_df = read_from_type_file()
	answerString = session.get('answerString', None)
	theme = session.get('theme', None)
	ret = get_type_questions(session.get('listOfQuestions'), types_df, len(types_df))


	if (session.get('listOfQuestions') is None):
		session['listOfQuestions'] = [ret[0]]
	else:
		Q = session.get('listOfQuestions')
		Q.append(ret[0])
		session['listOfQuestions'] = Q

	numCorrect = session.get('numCorrect', None)
	currentQuestion = session.get('currentQuestion', None)

	if (currentQuestion < 10):

		correctAnswer = session.get('correctAnswer', None)  # Get correct answer

		if request.method == 'GET':
			session['correctAnswer'] = ret[0]  # correctAnswer # Set correct answer
		if request.method == 'POST':
			answer = request.form.get('answer',
									  'No answer')  # Get answer from button press with a default value of "No answer"

			if (answer is not None and correctAnswer is not None and compareString(answer, correctAnswer)):
				numCorrect += 1
				session['numCorrect'] = numCorrect  # Set
				if currentQuestion != 0:
					answerString = answerString + f"{answer} ✅ {correctAnswer}\n"
					session['answerString'] = answerString
			else:
				if currentQuestion != 0:
					answerString = answerString + f"{answer} ❌ {correctAnswer}\n"
					session['answerString'] = answerString

			currentQuestion += 1  # Increment current question
			session['currentQuestion'] = currentQuestion  # Save to cookies
			session['correctAnswer'] = ret[0]
			session['question'] = ret[1]
	else:
		correctAnswer = session.get('correctAnswer', None)  # Get correct answer
		answer = request.form.get('answer',
								  'No answer')  # Get answer from button press with a default value of "No answer"

		if (answer is not None and correctAnswer is not None and compareString(answer, correctAnswer)):
			numCorrect += 1
			session['numCorrect'] = numCorrect  # Set
			if currentQuestion != 0:
				answerString = answerString + f"{answer} ✅ {correctAnswer}\n"
				session['answerString'] = answerString
		else:
			if currentQuestion != 0:
				answerString = answerString + f"{answer} ❌ {correctAnswer}\n"
				session['answerString'] = answerString

		return redirect(url_for('gameComplete'))

	if not theme:
		theme = 'Dark'

	answerArray = answerString.split('\n')
	while (len(answerArray) <= 10):
		answerArray.append('')
	return render_template('types.html', theme=theme, question=ret[1], correctQ=numCorrect, currQ=currentQuestion,
						   maxQ=MAXQUESTIONS, q0=answerArray[0], q1=answerArray[1], q2=answerArray[2],
						   q3=answerArray[3], q4=answerArray[4], q5=answerArray[5], q6=answerArray[6],
						   q7=answerArray[7], q8=answerArray[8], q9=answerArray[9])

@app.route("/winds", methods=[ 'GET', 'POST' ])
def winds():
	theme = session.get('theme', None)
	if not theme:
		theme = 'Dark'

	return render_template('winds.html', theme=theme) #Render window

def compareString(s1, s2):
	theme = session.get('theme', None)
	if not theme:
		theme = 'Dark'

	remove = string.punctuation + string.whitespace
	return s1.translate(str.maketrans('', '', remove)).lower() == s2.translate(str.maketrans('', '', remove)).lower()

def isDoubleable(s1, s2):
	if len(s1) == 0 or len(s2) == 0:
		return False
	else:
		for c in s1:
			if c.isdigit() or c == '.':
				pass
			else:
				return False

		for c in s2:
			if c.isdigit() or c == '.':
				pass
			else:
				return False

		return True

def compareMETAR(s1, s2):
	theme = session.get('theme', None)
	if not theme:
		theme = 'Dark'

	if isDoubleable(s1, s2):
		return float(s1) == float(s2)
	else:
		remove = string.punctuation + string.whitespace
		return s1.translate(str.maketrans('', '', remove)).lower() == s2.translate(str.maketrans('', '', remove)).lower()

def compareTAF(s1, s2):
	theme = session.get('theme', None)
	if not theme:
		theme = 'Dark'

	if isDoubleable(s1, s2):
		return float(s1) == float(s2)
	else:
		remove = string.punctuation + string.whitespace
		return s1.translate(str.maketrans('', '', remove)).lower() == s2.translate(str.maketrans('', '', remove)).lower()


if __name__ == "__main__":
	port = 5000
	if(len(sys.argv) >= 2):
		port = sys.argv[1]
	app.config['SECRET_KEY'] = 'NA.bcr*xB2KJc7W!7mVHeG!xUC9uQo8qAJj7fE7wr2FbHM8A7kdRRaaN7a-zK9*.vxB92o3s.wgLRV76Z6qWvj9gb@Er*2cThNpe'
	app.run()
	#app.run('0.0.0.0', port) # 5000 is the port for the url, change this when test so that multiple devs can run at same time on different ports
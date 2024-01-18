import random
import pandas as pd
def get_code_question(listOfQuestions, question_df, maxQuestions):
    maxQuestions = len(question_df)

    currentQuestion = random.randint(0, maxQuestions-1)

    if listOfQuestions is not None:
        while question_df["CODE"][currentQuestion] in listOfQuestions:  # Make sure this question has not been asked already this game
            currentQuestion = random.randint(0, maxQuestions-1)

    if(random.randint(0, 10) != 0): #Case for if we are asking FOR the code
        correctAnswer = question_df["CODE"][currentQuestion]
        question = f"What is the airport code for {question_df['LOCATION'][currentQuestion]}?"

        return [correctAnswer, question, question_df["CODE"][currentQuestion]]
    else:
        correctAnswer = question_df["LOCATION"][currentQuestion]
        question = f"What city and state is {question_df['CODE'][currentQuestion]} located in??"

        return [correctAnswer, question, question_df["CODE"][currentQuestion]]

def get_metar_questions(listOfQuestions, question_df, maxQuestions):
    currentQuestion = random.randint(0, maxQuestions - 1)

    if listOfQuestions is not None:
        while question_df["QUESTION"][
            currentQuestion] in listOfQuestions:  # Make sure this question has not been asked already this game
            currentQuestion = random.randint(0, maxQuestions - 1)

    correctAnswer = question_df["ANSWER"][currentQuestion]
    question = question_df["QUESTION"][currentQuestion]

    return [correctAnswer, question]

def get_taf_questions(listOfQuestions, question_df, maxQuestions):
    currentQuestion = random.randint(0, maxQuestions - 1)

    if listOfQuestions is not None:
        while question_df["QUESTION"][
            currentQuestion] in listOfQuestions:  # Make sure this question has not been asked already this game
            currentQuestion = random.randint(0, maxQuestions - 1)

    correctAnswer = question_df["ANSWER"][currentQuestion]
    question = question_df["QUESTION"][currentQuestion]

    return [correctAnswer, question]

def get_type_questions(listOfQuestions, question_df, maxQuestions):
    currentQuestion = random.randint(0, maxQuestions - 1)

    if listOfQuestions is not None:
        while question_df["ICAO_Code"][
            currentQuestion] in listOfQuestions:  # Make sure this question has not been asked already this game
            currentQuestion = random.randint(0, maxQuestions - 1)

    correctAnswer = question_df["ICAO_Code"][currentQuestion]
    question = f'What is the IACO type identifier for an {question_df["Model_FAA"][currentQuestion]}'

    return [correctAnswer, question]
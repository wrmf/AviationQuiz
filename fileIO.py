import pandas as pd

Code_Questions = 'static/codes.csv'
METAR_Questions = 'static/metars.csv'
TAF_Questions = 'static/tafs.csv'
Type_questions = 'static/types.csv'
code_df = pd.DataFrame
metar_df = pd.DataFrame
taf_df = pd.DataFrame


def read_from_code_file():
	text_file = open(Code_Questions, "r")
	temp = text_file.read().split('\n')
	temp = [i.replace(')', '') for i in temp]
	temp = [i.split('(', 1) for i in temp]
	code_df = pd.DataFrame(temp, columns=['LOCATION', 'CODE'])
	return code_df

def read_from_metar_file():
	text_file = open(METAR_Questions, "r")
	temp = text_file.read().split('\n')
	temp = [i.replace('"', '') for i in temp]
	temp = [i.split('*', 1) for i in temp]
	code_df = pd.DataFrame(temp, columns=['QUESTION', 'ANSWER'])
	return code_df

def read_from_taf_file():
	text_file = open(TAF_Questions, "r")
	temp = text_file.read().split('\n')
	temp = [i.replace('"', '') for i in temp]
	temp = [i.split('*', 1) for i in temp]
	code_df = pd.DataFrame(temp, columns=['QUESTION', 'ANSWER'])
	return code_df

def read_from_type_file():
	type_df = pd.read_csv(Type_questions)
	return type_df

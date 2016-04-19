import os
from werkzeug import secure_filename
from flask import Flask, request, redirect, url_for,render_template
from collections import defaultdict
import xml.etree.ElementTree as ET
import urllib2

app = Flask(__name__)

userList=[
		"dispenser","arsenic28","menphim",	"komi0222", 				#"ja3rno","ayihis","fukku",
        "bnsgny",	"CROW",		"okkyun",	"tmbsx",		"yazaten", 	#"is0220rk"
		"ixmel",	"futo",		"IS0283IR",	"moon_remon",	"Rp7rf", 	#"is0248vx","Nanana","satoshi31043","mots555","pikanatsu","kerokero","proru","sarada417","is0268ev","kinono","is0266hx",
        "noy72",	"Taka13"
]


def getUser(id):
    response = urllib2.urlopen('http://judge.u-aizu.ac.jp/onlinejudge/webservice/user?id='+id)
    return response


def updateSolvedDict(id,Dict):
	html=getUser(id)
	#
	tree=ET.parse(html)
	root=tree.getroot()
	#
	for problemNum in root.findall(".//problem/id"):
		Dict[problemNum.text] += 1;
	#
	return Dict


def getProblemsList():
	solved_dict = defaultdict(lambda : 0)
	for user in userList:
		solved_dict = updateSolvedDict( user, solved_dict )
	problems_list = []
	for solved_problem_number in solved_dict :
		problems_list.append( (solved_problem_number, solved_dict[solved_problem_number]) )
	#
	problems_list.sort( key=lambda x:int(x[1])*10000-int(x[0]), reverse=True )
	#
	ret = []
	for elm in problems_list:
		ret.append( {'count':elm[1], 'number':elm[0]} )
	return ret

@app.route('/')
def index():
	problems_list = getProblemsList()
	return render_template('index.html', problems = problems_list)

#@app.route('/user/<usernames>')
#def show_user_profile(usernames):
#	problems_list = getProblemsList()
#	return render_template('index.html', problems = problems_list)


if __name__ == '__main__':
    app.run(debug=True)

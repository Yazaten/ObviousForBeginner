# -*- coding: utf-8 -*-

from collections import defaultdict
import xml.etree.ElementTree as ET
import urllib2
import sys

ME=""

solvedActiveMembers=7

activeList=[
           "komi0222","menphim","ja3rno","dispenser","arsenic28","ayihis","fukku",
           "bnsgny","CROW","is0220rk","okkyun","tmbsx","yazaten",
           "is0248vx","Nanana","satoshi31043","mots555","ixmel","pikanatsu","kerokero","futo","proru","sarada417","is0268ev","IS0283IR","moon_remon","kinono","is0266hx","Rp7rf"
]


def getUser(id):
    response = urllib2.urlopen('http://judge.u-aizu.ac.jp/onlinejudge/webservice/user?id='+id)
    return response



def getSolvedList(id,Dict):
	html=getUser(id)
	#
	tree=ET.parse(html)
	root=tree.getroot()
	#
	for problemNum in root.findall(".//problem/id"):
		Dict[problemNum.text] += 1;
	#
	return Dict


def getAlreadySolvedFromText():
	dict = defaultdict(lambda : 0)
	for line in open('solved.txt', 'r'):
		dict[line[:-1]] += 1;
	return dict


solvedMeDict = defaultdict(lambda : 0)
solvedMeDict = getSolvedList(ME,solvedMeDict)

alreadySolved = getAlreadySolvedFromText()

solvedActiveDict=defaultdict(lambda : 0)

for name in activeList:
    solvedActiveDict=getSolvedList(name,solvedActiveDict)

problemList=[]
for problemNum in solvedActiveDict:
	problemList.append( ( problemNum , solvedActiveDict[ problemNum ] ) )

problemList.sort(key=lambda x:x[1], reverse=True)



print "<!DOCTYPE html>\n<html>\n\t<head>\n\t\t<meta charset=\"utf-8\">\n   <meta http-equiv=\"X-UA-Compatible\" content=\"IE=edge\"><meta name=\"viewport\" content=\"width=device-width, initial-scale=1\"><link href=\"css/bootstrap.min.css\" rel=\"stylesheet\">  \t\t<title>problems</title>\n\t</head>\n\t<body>"
print "<div  class=\"container\"><table class=\"table table-hover table-striped table-condensed\"><thead><tr><th>solved</th><th>problem</th></tr></thead><tbody>"


count=0
for problem in problemList:
	problemNum	= problem[0]
	solvedNum	= problem[1]
	#
	if( solvedNum >= solvedActiveMembers ):
		if alreadySolved[ str(problemNum) ] >= 1 :
			if solvedMeDict[ problemNum ] >= 1 :
				print "<tr class = \"warning\"><td>"+str(solvedNum)+"</td><td>"+  "<a href="+"\"http://judge.u-aizu.ac.jp/onlinejudge/description.jsp?id="+problemNum+"&lang=jp\""+">"+problemNum+"</a>"  +"</td></tr>"
			else:
				print "<tr class = \"info\"><td>"+str(solvedNum)+"</td><td>"+  "<a href="+"\"http://judge.u-aizu.ac.jp/onlinejudge/description.jsp?id="+problemNum+"&lang=jp\""+">"+problemNum+"</a>"  +"</td></tr>"
		#
		elif solvedMeDict[ problemNum ] >= 1 :
			print "<tr class = \"success\"><td>"+str(solvedNum)+"</td><td>"+  "<a href="+"\"http://judge.u-aizu.ac.jp/onlinejudge/description.jsp?id="+problemNum+"&lang=jp\""+">"+problemNum+"</a>"  +"</td></tr>"
		#
		else:
			print "<tr><td>"+str(solvedNum)+"</td><td>"+  "<a href="+"\"http://judge.u-aizu.ac.jp/onlinejudge/description.jsp?id="+problemNum+"&lang=jp\""+">"+problemNum+"</a>"  +"</td></tr>"

print "</tbody></table></div>"
print "<script src=\"https://ajax.googleapis.com/ajax/libs/jquery/1.11.0/jquery.min.js\"></script><script src=\"js/bootstrap.min.js\"></script>"
print "\t</body>\n</html>"
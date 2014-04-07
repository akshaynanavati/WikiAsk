import sys
from corenlp import StanfordCoreNLP
#input_paragraph = sys.argv[1]
#import nltk
para = sys.stdin.read()

#para = """On 13 August 2009, Dempsey signed a contract extension to remain with Fulham through 2013. On August 20, he scored his first goal in European competition, in the newly formed Europa League, netting Fulham's second goal in a 31 win against Amkar Perm in the play-off round. On December 30, La Gazzetta dello Sport named Dempsey as one of the top eleven Premier League players of the season. On January 17, 2010, Dempsey suffered a suspected cruciate knee ligament injury in a 20 away defeat to Blackburn Rovers. On March 11, Dempsey returned, coming on in the last minute of Fulham's loss away to Juventus, and then completed 72 minutes of their away loss to Manchester United in the league. On March 18, Dempsey came off the bench against Juventus in their second-leg, last-16 tie in the Europa League and scored the winner on a long chip shot. Fulham won the game 41 and this game resulted in Fulham winning an award, as well as Dempsey receiving an award for his 'Wonderful' (Quote from the commentator on ESPN" goal."""
#print len(para)
#print len(nltk.sent_tokenize(para))
#exit(0)
s = StanfordCoreNLP()
s.raw_parse(para)
#print 2
print s.raw_parse(para)

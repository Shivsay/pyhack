from .hackernews import HackerNews
from bs4 import BeautifulSoup


hn = HackerNews()

def getTop(id):
    top = hn.get_item(id)
    content = [top.url, top.text]
    #content[0] = top.url
    #content[1] = top.text
    return content

def getComment(id):
     itemObj = hn.get_item(id)
     return itemObj.kids

def parseComment(id):
    commentListItem = hn.get_item(id)
    commentHTMLItem = commentListItem.text
    commentParsedItem = BeautifulSoup(commentHTMLItem, 'html.parser')
    commentItem = commentParsedItem.get_text()
    return commentItem

def getShowStories(): 
    showStories = hn.show_stories(limit=20)
    return showStories


def getTopStories():
    topStories = hn.top_stories(limit=20)
    return topStories

def getjobStories():
    jobStories = hn.job_stories(limit=20)
    return jobStories

def getnewStories():
    newStories = hn.new_stories(limit=20)
    return newStories

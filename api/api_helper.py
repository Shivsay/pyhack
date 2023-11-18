from hackernews import HackerNews
from bs4 import BeautifulSoup


hn = HackerNews()


def getComments(level, comments):
    print("\n")
    level += ('\t')
    if comments is not None:
        for comment in comments:
            commentListItem = hn.get_item(comment)
            commentHTMLItem = commentListItem.text
            commentParsedItem = BeautifulSoup(commentHTMLItem, 'html.parser')
            commentItem = commentParsedItem.get_text()
            print(level, commentItem)
            getComments(level, commentListItem.kids)


def getShowStories():
    showStories = hn.show_stories(limit=1)

    for showStory in showStories:
        print(showStory.title, " - ", showStory.url, "\nComments:\n")
        level = ""
        getComments(level, showStory.kids)
        print("------------------------------------------")


def getTopStories():
    topStories = hn.top_stories(limit=1)

    for topStory in topStories:
        print(topStory.title, " - ", topStory.url, "\nComments:\n")
        level = ""
        getComments(level, topStory.kids)
        print("------------------------------------------")


def getjobStories():
    jobStories = hn.job_stories(limit=1)

    for jobStory in jobStories:
        print(jobStory.title, " - ", jobStory.url, "\nComments:\n")
        level = ""
        getComments(level, jobStory.kids)
        print("------------------------------------------")

def getnewStories():
    newStories = hn.new_stories(limit=1)

    for newStory in newStories:
        print(newStory.title, " - ", newStory.url, "\nComments:\n")
        level = ""
        getComments(level, newStory.kids)
        print("------------------------------------------")



getShowStories()
print("\nNOW TOP:\n")
getTopStories()
getjobStories()
getnewStories()
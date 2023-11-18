from hackernews import HackerNews

hn = HackerNews()


def getComments(level, comments):
    print("\n")
    level += ('\t')
    if comments is not None:
        for comment in comments:
            commentItem = hn.get_item(comment)
            print(level, commentItem.text)
            getComments(level, commentItem.kids)


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


getShowStories()
print("\nNOW TOP:\n")
getTopStories()

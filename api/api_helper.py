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


topStories = hn.show_stories(limit=1)

for topStory in topStories:
    print(topStory.title, " - ", topStory.url, "\nComments:\n")
    level = ""
    getComments(level, topStory.kids)
    print("------------------------------------------")

import json
from urllib.request import urlopen
from bs4 import BeautifulSoup
import time


class ArticleFetcher():
    def fetch(self):
        time.sleep(1)
        # JSON API request
        response = urlopen("https://newsapi.org/v2/top-headlines?sources=spiegel-online&apiKey=XXXXXXXXXXXXXX").read().decode('utf-8')
        responseJson = json.loads(response)
        numberArticles = responseJson.get("articles")
        numberArticles = len(numberArticles)
        # API outputs 10 articles
        # loop index from 0 - 9
        x = 0
        while x < numberArticles:
            # API requests, work for all articles!
            title = responseJson.get("articles")[x].get("title")
            daytime = responseJson.get("articles")[x].get("publishedAt")
            url = responseJson.get("articles")[x].get("url")

            # Infos from API / URL
            category = url.split("/")[3].upper()
            subcategory = url.split("/")[4]
            domain = url.split("/")[2]
            if domain != "www.spiegel.de":
                x += 1
            else:
                # Crawler: Entering the page to get the infos ..
                articlePage = urlopen(url)
                articlePage = BeautifulSoup(articlePage, "html.parser")

                # Keywords (if available)
                if articlePage.find("meta", {"name": "news_keywords"}):
                    meta = articlePage.find("meta", {"name": "news_keywords"})['content']
                else:
                    pass

                # Last modified
                if articlePage.find("meta", {"name": "last-modified"}):
                    lastModified = articlePage.find("meta", {"name": "last-modified"})['content']
                else:
                    lastModified = "Not yet modified"

                # PLUS category just can be read by signe din members
                if category == "PLUS":
                    x += 1
                else:

                    # Comments
                    if articlePage.find("div", {"data-sponlytics-area": "box-comments"}):
                        comments = "Comments: YES"
                    else:
                        comments = "Comments: NO"

                    # Creator & Author
                    authorScript = articlePage.find("script", {"type": "application/ld+json"}).text
                    authorJsonScript = json.loads(authorScript)
                    creator = authorJsonScript.get("creator")
                    creator = ', '.join(str(y) for y in creator)

                    authorJsonScript.get("author")
                    authorList = authorJsonScript.get("author")[0]
                    authorName = authorList.get("name")
                    if authorName == "SPIEGEL ONLINE":
                        authorBlock = articlePage.find("div", {"id": "js-article-column"})
                        authorTag = authorBlock.select("i")[1]
                        author = authorTag.text
                        author = author + " (abbreviation)"
                    elif authorName != "SPIEGEL ONLINE":
                        author = authorList.get("name")
                    else:
                        author = "PROBLEM to identify author"

                    # Loop through all paragraph tags to get the length of written article
                    if articlePage.select("div .spArticleContent"):
                        articleSection = articlePage.select("div .spArticleContent")[0]
                        articleParagraphs = articleSection.select("p")
                        articleText = []
                        i = 0
                        while i < len(articleParagraphs):
                            # print(articleParagraphs[i].text)
                            paragraph = articleParagraphs[i].text
                            articleText.append(paragraph)
                            i += 1

                        articleText = ''.join(articleText)
                        words = len(articleText.split())

                    else:
                        pass

                    x += 1

                print("Author: " + author)
                print("Creator: " + creator)
                print("Title: " + title)
                print("Published: " + str(daytime))
                print("Last Modified: " + str(lastModified))
                print(url)
                print(str(words) + " Words")
                print("Category: " + category + ", " + subcategory.capitalize())
                print("Keywords: " + meta)
                print(comments)
                print("\n")


fetcher = ArticleFetcher()
fetcher.fetch()

# Unique article id? Total article count (unique number in url)

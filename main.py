import csv
import time
import requests
from bs4 import BeautifulSoup
import os

global url, sub, key_wrds, Nodes;
sub = []
key_wrds = []
Nodes = []
header = {'User-Agent': 'Mozilla/5.0'}


class Node:
    def __init__(self, sub, title, author, upvote, comments, link, relation):
        self.sub = sub
        self.title = title
        self.author = author
        self.upvote = upvote
        self.comments = comments
        self.link = link
        self.relation = relation

#  key is the word beinng searched
# if filter = 1 we filter only subreddits with the key word in name
def sub_red(key, filter):
    lst = key.split(" ")
    ser = ''
    for i in lst:
        ser += i+'%20'
    url = 'https://old.reddit.com/search/?q='+key+'&type=sr'
    page = requests.get(url, headers=header)
    soup_ = BeautifulSoup(page.text, 'html.parser')
    attrs = {'class': 'search-result search-result-subreddit'}
    # print(soup_.div.attrs)
    for sr in soup_.find_all('div', attrs=attrs):
        node = sr.find('a', {'class': 'search-title may-blank'})
        if(filter):
            f = 0
            title = node.text.lower()
            if key in title:
                f = 1
            if f == 0:
                continue
        url = node.attrs['href']
        sub.append(url)
        print("r/"+node.text)
        if(len(sub)==2): break

def post(sub, type, filter, sim):
    url = sub+type + "/"
    page = requests.get(url, headers=header)
    soup_ = BeautifulSoup(page.text, 'html.parser')
    attrs = {'class': 'thing'}
    cnt = 0
    print(url)
    print('Tag: ' + type)
    while cnt < 1:
        for post in soup_.find_all('div', attrs=attrs):
            title = post.find('p', attrs={'class': 'title'}).text
            title = title[:- 17]
            rel = []
            f = 0
            if(filter):
                title = title.lower()
                for key in key_wrds:
                    if key in title:
                        f += 1
                        rel.append(key)
                if f == 0:
                    continue
                if (sim == '1'):
                    if f != len(key_wrds):
                        continue
            cnt += 1
            print(cnt, ":")
            post_link = post.attrs['data-url']
            author = "u/" + post.attrs['data-author']
            num_of_comments = post.find('a', attrs={'class': 'comments'})
            if num_of_comments == None:
                num_of_comments = 0
            else:
                num_of_comments = num_of_comments.text.split()[0]

            upvotes = post.find('div', attrs={'class': 'score likes'}).text
            if upvotes == '•':
                upvotes = 0
            print("title: ", title.encode("utf-8"), "\n", "author: ", author, " ", "upvotes: ",
                  upvotes, " ", "comments :", num_of_comments, "\n", "link: ", post_link)
            if(f > 0):
                print("Key_wrds: ",end=" ")
                for i in rel:
                    print(i, end=' ')
                print("\n")
            Nodes.append(Node(sub, title, author, upvotes, num_of_comments, post_link,rel))
            if cnt > 1:
                break
        next_button = soup_.find('span', attrs={'class': 'next-button'})
        if next_button == None:
            break
        next_page_link = next_button.find('a').attrs['href']
        time.sleep(2)
        page = requests.get(next_page_link, headers=header)
        soup_ = BeautifulSoup(page.text, 'html.parser')


if __name__ == '__main__':
    key = input('Enter the Topic: ')
    tag = input("Enter the tag: ")
    print("Enter the key words")

    st = input().split(' ')
    f1, f2 = input("Enter f1, f2 {1,0} : ").split(' ')
    k = input("Enter 1->&& 0->||: ")
    for i in st:
        key_wrds.append(i)
    # getting the subreddits
    sub_red(key, f1)
    # getting related posts
    for s in sub:
        post(s, tag, f2, k)
    for node in Nodes:
        # writing in a CSV file
        file_exists = os.path.isfile('result.csv')
        with open('result.csv', 'a') as f:
            headers = ['Sub', 'Title', 'Author', 'Upvotes',
                       'Number_of_comments', 'Post_link', 'Reations']
            writer = csv.DictWriter(f, fieldnames=headers)
            if not file_exists:
                writer.writeheader()
            writer.writerow({'Title': node.title.encode("utf-8"), 'Author': node.author, 'Upvotes': node.upvote,'Number_of_comments': node.comments, 'Post_link': node.link, 'Reations': node.relation})
        # print(node.title)

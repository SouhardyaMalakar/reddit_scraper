import csv
import time
import requests
from bs4 import BeautifulSoup
import os

global url 
header = {'User-Agent': 'Mozilla/5.0'}         

def fun(sub):
    url='https://old.reddit.com/r/' + sub+"/new/"
    page = requests.get(url, headers=header)
    soup_ = BeautifulSoup(page.text, 'html.parser')
    attrs = {'class': 'thing'}
    cnt=0
    while cnt<100:
        for post in soup_.find_all('div', attrs=attrs):
            related_post = post.find('time', attrs={'class': 'live-timestamp'})
            if related_post is None:
                continue
            else:
                cnt+=1
                print(cnt,":")
                title = post.find('p', attrs={'class': 'title'}).text;
                title=title[:- 17]
                post_link = post.attrs['data-url']
                author = "u/" + post.attrs['data-author']
                num_of_comments = post.find('a', attrs={'class': 'comments'}).text.split()[0]

                if num_of_comments == 'comment':
                    num_of_comments = 0
                upvotes = post.find('div', attrs={'class': 'score likes'}).text
                if upvotes == '•':
                    upvotes = 0
                print(" title: ", title.encode("utf-8"), "\n","author: ", author," ","upvotes: ",upvotes, " ","comments :",num_of_comments,"\n","link: ", post_link,"\n")
                
                # writing in a CSV file
                file_exists = os.path.isfile('result.csv')
                with open('result.csv', 'a') as f:
                    headers = ['Title', 'Author', 'Upvotes', 'Number_of_comments', 'Post_link']
                    writer = csv.DictWriter(f, fieldnames=headers)
                    if not file_exists:
                        writer.writeheader()
                    writer.writerow({ 'Title': title.encode("utf-8"), 'Author': author, 'Upvotes': upvotes,'Number_of_comments': num_of_comments, 'Post_link': post_link})

        next_button = soup_.find('span', attrs={'class': 'next-button'})
        next_page_link = next_button.find('a').attrs['href']
        time.sleep(2)
        page = requests.get(next_page_link, headers=header)
        soup = BeautifulSoup(page.text, 'html.parser')

if __name__ == '__main__':
    sub="askreddit"
    # print("Enter the subreddit you want :")
    # input(sub)
    fun(sub)

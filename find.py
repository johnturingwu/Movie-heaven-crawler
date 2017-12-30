import re,requests,queue

LINK = set()
List = []
times = 10

URL = "http://www.ygdy8.com"
headers = {
    'Referer':'http://www.ygdy8.com/',
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36'
}

def append_url(link):
    try:
        global num
        r = requests.get(URL+link,headers=headers)
        r.encoding=r.apparent_encoding
        web = r.text
        movies = re.findall(r'"(ftp[^\'"]+)"',web)
        name = re.search('<title>.+《(.+)》.+<\/title>',web).group(1)
        tplt = "{0:{2}^10}\t{1:{2}^90}\n"
        for movie in movies:
            List.append(tplt.format(name,movie,chr(12288)))
            num += 1
            print(num)
            print(movie,name)
    except:
        print("error getftp")
        pass

num = 0
def bfs(url):
    Q = queue.Queue()
    Q.put(url)
    global num
    try:
        while not Q.empty():
            url = Q.get()
            r = requests.get(URL+url,headers=headers)
            r.encoding=r.apparent_encoding
            text = r.text
            links = re.findall(r'/html[^"\';]+',text)

            for link in links:
                if link in LINK:
                    continue
                append_url(link)
                LINK.add(link)
                Q.put(link)
                if num>times:
                    return
    except:
        print("error bfs")
        pass

def main():
    url = '/'
    bfs(url)
    file = open('movies.txt','w+',encoding='utf-8')
    url_file = open('urls.txt','w+',encoding='utf-8')
    for strs in List:
        try:
            file.write(strs)
        except:
            print('error file')
            continue
    for link in LINK:
        try:
            url_file.write(URL+link+'\n')
        except:
            continue
    file.close()
    url_file.close()

main()
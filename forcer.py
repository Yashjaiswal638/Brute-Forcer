import threading
import time
import sys
import requests
import pyfiglet

def thr(url, words, codes, l):
    threads = []
    for i in range(l):
        thread = threading.Thread(target=bruteForcer, args = (url[i], words, codes))
        thread.start()
        threads.append(thread)
    
    for t in threads:
        t.join()


# defines user input with various conditions given in the question
def welcome():
    art = pyfiglet.figlet_format("Brute-Forcer\n")
    print(art)


# Function for assigning arguments as userInput
def userInput():

    if not len(sys.argv) <= 4 and len(sys.argv) >=3 :
        return "Invalid arguments"
    else:
        fileInput = sys.argv[2]
        try :
            url = sys.argv[1]
            if url[0] == "[" and url[-1] == "]":
                url = url[1:-1]
        except : url = ""

        try:
            codes = sys.argv[3]
            if codes[0] == "[" and codes[-1] == "]":
                codes = codes[1:-1]
        except:
            codes = []

        words = []

        # Reading wordList file into a list
        try:
            with open(fileInput, 'r') as file:
                data = file.readlines()

            for line in data:
                line = line.rstrip()
                words.append(line)
        except:
            words = "Error"

        if words == "Error" or len(words)<1000 : print("Invalid arguments provided")
        else :
            res = inputProcessing(url, words, codes)
            return res


# Function for processing User Input   
def inputProcessing(url, words, codes):

    try:
        urlM = []
        if not len(url) == 0:
            url = url.split(",")
        else : url = ""

        for u in url:
            if not u.startswith("https://"):
                u = "https://"+u
            if not u[-1] == '/':
                u += '/'
            res = checkConnection(u)
            if res == "Error":
                continue
            urlM.append(u)
    except : pass

    try :

        if not len(codes) == 0:
            codes = codes.split(",")
            codes = [int(x) for x in codes]
        else: codes.append(200)

    except:
        return "Invalid arguments provided"
    l = len(urlM)

    thr(urlM, words, codes, l)


# Main Logic - Brute Force
def bruteForcer(url, words, codes):
    time.sleep(0.2)
    for word in words:
        response = requests.get((url+word), allow_redirects=False)
        c = response.status_code
        if c in codes:
            print(f"{url+word} [Status Code {c}]")
        else : pass
        
        
# Checks for Connection error
def checkConnection(url):
    try:
        check = requests.get(url)
    except requests.exceptions.RequestException as e:
        check = "Error"
    if check == "Error":
        print(f"{url} - Invalid Url\n")
    return check


def main():

    welcome()
    res = userInput()
    if not res == None:
        print(res)

if __name__ == "__main__":
    main()
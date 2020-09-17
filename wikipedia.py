from bs4 import BeautifulSoup
from urllib.request import urlopen
from math import log2

def wikipediasearch(terms = 'blue'):
    #Search two terms simulataneously or search one up. Will help with NWD function
    #See NWD (should I add +1 to total results since indexes start at 0)
    if isinstance(terms, list) and len(terms) > 1:
        word = terms[0]
        for term in terms:
            word += "+" + term
    else:
        word = terms
    
    #Webscrape Parsing
    url = 'https://en.wikipedia.org/w/index.php?title=Special%3ASearch&profile=default&search=' + word + '+&fulltext=Search'
    url = urlopen(url)
    soup = BeautifulSoup(url, 'html.parser')
    results = soup.find_all(attrs = {"class": "results-info"})
    results = str(results[0]) #Convert to string, so we can parse through the html manually and pull out the final result. 
    results = results.split(">Results")[0]
    results = results.split("data-mw-num-results-total=")[1] #Isolates the total results integer
    results = results.strip('""') #Remove quotes from the string integer
    
    return int(results) + 1 #Convert the string to an int and add one since indexes start at 0

def getN(serverType = 'wikipedia'):
    #I suspect the purpose of this function is to establish a baseline based off previous search results.
    # maxN will be used to create a list of objects that should achieve an NWD of 1
    
    #Below will be updated later as a switch statement to choose between which search methods
    if serverType is 'wikipedia':
        search = wikipediasearch
        
    maxN = [['einstein', 'fudge'], ['apple','xyzzy'], ['imbecile', 'newton']]
    cn = []
    for terms in maxN:
        fX = search(terms)
        fw = [search(term) for term in terms]
        cn.append(2**((log2(max(fw)) - log2(fX)) + log2(min(fw))))
    return 1E6*max(cn)

def NWD(terms = ['blue', 'green'], serverType = 'wikipedia'):
    
    #Questions for the future: matlab indexing starts as 1, should Python reflect that because we want the total integer value?
    if not isinstance(terms, list):
        raise TypeError('input terms requires list')
    servers = ['wikipedia']
    
    #Check is serverType is found in list. Currently only supports Wikipedia Search
    if serverType not in servers:
        raise TypeError('input servertype is invalid. Please choose valid serverType')
    
    #Will be updated lik getN
    if serverType is 'wikipedia':
        search = wikipediasearch
        
    N = getN(serverType)
    
    fX =search(terms) #Searching up all terms
    fw = [search(i) for i in terms] #Search up terms invidually
    nwd = (log2(max(fw)) - log2(fX)) / (log2(N) - log2(min(fw)))
    
    return nwd

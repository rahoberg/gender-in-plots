import requests
import io
import re

def query(request):
    request['action'] = 'query'
    request['format'] = 'json'
    request['maxlag']='5'
    lastContinue = {}
    while True:
        # Clone original request
        req = request.copy()
        # Modify it with the values returned in the 'continue' section of the last result.
        req.update(lastContinue)
        # Call API
        result = requests.get('https://en.wikipedia.org/w/api.php', params=req).json()
        if 'error' in result:
            raise RuntimeError(result['error'])
            #print('Error',result['error'])
            #print(lastcontinue)
            #break
        if 'warnings' in result:
            print(result['warnings'])
        if 'query' in result:
            yield result['query']
        if 'continue' not in result:
            break
        lastContinue = result['continue']

def findplots(outfilename,categoryname):
    f=open(outfilename,'w')
    #Look for subheader (so having ==, not ===) containing the word plot
    pattern=r'(?s)(?:(?<!=)==(?!=))[\s\w]*?[pP]lot.*?(?<!=)==(?!=).*?(?:(?:(?<!=)==(?!=))|$)'
    for result in query({'generator': 'categorymembers', 'gcmtitle': categoryname,'formatversion':'2','prop':'revisions','rvprop':'content'}):
        for page in result['pages']:
            plots=re.findall(pattern,page['revisions'][0]['content'])
            if len(plots)>0:
                #remove tabs and newline
                title=re.sub(r'\t|\n',' ',page['title'])
                f.write(title)
                f.write('\n')
                #remove header and any comments from plot
                plot = re.sub(r'(?:(?<!=)==(?!=)).*?[pP]lot.*?(?<!=)==(?!=)|{{.*?}}|<!--.*-->','',plots[0])
                #remove trailing '==' from plot
                plot=re.sub(r'(?<!=)==(?!=)','',plot)
                #removes tabs and newlines
                plot=re.sub(r'\t|\n',' ',plot)
                #plot=plots[0].sub(r'==Plot==|{{.*?}}|<!--.*-->','').sub('==','').sub('
                f.write(plot)
                f.write('\n')
    f.close()


#pattern=r'(?s)(?:(?<!=)==(?!=)).*?[pP]lot.*?(?<!=)==(?!=).*?(?:(?:(?<!=)==(?!=))|$)'
findplots('westernbookplots','Category:Western_(genre)_novels')
#findplots('lonerangerplots','Category:Lone_Ranger_films')
#findplots('tvplots','Category:English-language_television_programs')
#findplots('feministnovels','Category:Feminist_novels')
#findplots('movieplots2','Category:English-language_films')
#findplots('2017movieplots','Category:2017_films')
#findplots('2018movieplots','Category:2018_films')

#for year in range(1990,2017):
#    syear=str(year)
#    findplots(syear+'movieplots','Category:'+syear+'_films')






#Create movie plots file
#g=open('movieplots','w')
#pattern='==Plot==\n(?:.*?\n)+?=='
#for result in query({'generator': 'categorymembers', 'gcmtitle': 'Category:English-language_films','formatversion':'2','prop':'revisions','rvprop':'content'}):
#    for page in result['pages']:
 #       plot=re.findall(pattern,page['revisions'][0]['content'])
 #       if len(plot)>0:
 #           g.write(page['title'],plot[0])
#g.close()

#Do stuff for TV programs
#for result in query({'generator': 'categorymembers', 'gcmtitle': 'Category:English-language_television_programs','formatversion':'2','prop':'revisions','rvprop':'content'}):
#    print(result)

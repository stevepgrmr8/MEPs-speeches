import requests
import re
import bs4
def getspeech(url, file):
    docraw=requests.get(url).text
    start=docraw.find('<table width="100%" border="0" cellpadding="5" cellspacing="0" class="doc_box_header">')
    end=docraw.find('<table width="100%" border="0" cellspacing="0" cellpadding="5">')
    doc=docraw[start:end]
    docbs=bs4.BeautifulSoup(doc).text
    file.write(docbs)
    file.write('\n\n\n =======================\n\n\n')

    
#getting xml file with all IDs of MEPs
#to change the country of MEPs, change "IT" in the next row to the abbreviation of the country you need (have a look at the website)
searchfile=requests.get('http://www.europarl.europa.eu/meps/en/xml.html?country=IT').text
#getting and cleaning all the IDs, generating URLs with lists of speech
listnum=re.findall("<id>\d+</id>", searchfile)
for i in range(len(listnum)):
    listnum[i]=listnum[i].lstrip('<id>')
    listnum[i]=listnum[i].rstrip('</id>')
    listnum[i]='http://www.europarl.europa.eu/meps/en/'+listnum[i]+'/seeall.html?type=CRE'

filebugs=open("Missing_Data.txt", "w+")
filebugs.write('MEPs with more than 100 interventions: \n')

for j in range (len(listnum)):   
    docraw=requests.get(listnum[j]).text
    start=docraw.find('<!-- START : MAIN CONTENT -->')
    end=docraw.find('<!-- END : MAIN CONTENT -->')
    doc=docraw[start:end]
    docbs=bs4.BeautifulSoup(doc)
    #name of the MEP, opening file with the MEP name:
    try:
        name=docbs.find('h2').text
        name=name.replace('\r', '')
        name=name.replace('\t', '')
        name=name.replace('\n', '')
        file=open(name+'.txt', "w+")
        print('downloading '+name+'...')
        #links for speeches:
        links=docbs.findAll('a')
        for k in range(len(links)):
            try:
                links[k]=str(links[k])
                links[k]=links[k].lstrip('''<a href="''')
                links[k]=links[k].partition('''" target=''')[0]
                links[k]=links[k].replace('amp;', '')
                links[k]='h'+links[k]
                getspeech(links[k], file)
                print('Speech num.'+ str(k+1)+' Done...')
            except Exception:
                file.write('ONLY FIRST 100 INTERVENTIONS SHOWN! SOME MORE REMAIN')
                filebugs.write(name+' URL:'+listnum[j]+'\n')
                continue
    except Exception:
        continue
    file.close()
filebugs.close()

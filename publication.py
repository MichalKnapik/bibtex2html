# -*- coding: utf-8 -*-

import re 

class pub:
    """A publication. 
    The data dictionary contains all details of publication. 
    There are two special entries:
    data[bibtexentrylabel] (the name of entry in .bib),
    data[bibtexentrytype]  (ARTICLE, INPROCEEDINGS, etc.)."""
    def __init__(self, data):
        self.data = data #dictionary with publication details

    def __repr__(self):
        return repr(self.data)

    def replaceSpecials(self, txt = None):
        """This function should replace annoying special symbols from bibtex.
        For now, it only throws away some stuff, without replacement.
        If called without txt, returns self.data version with specials removed."""
        if not txt == None:
            partial = re.sub(r'\\[\'\"\~\,\.\`\^]', '', txt) 
            partial = re.sub(r'\\', '', partial) 
            partial = re.sub(r'[\"\{]\s*|\s*[\"\}]','', partial.strip())
            return partial
        else:
            cleanData = {}
            for key in self.data:
                cleanData[key] = self.replaceSpecials(self.data[key])
        return cleanData
            
    def produceHTML(self):
        result = ""
        cleanData = self.replaceSpecials()
        if cleanData.has_key('pubauthor'):
            result += ' <span class="pubauthor"> ' + cleanData['author'] + ': </span> '
        if cleanData.has_key('title'):
            if cleanData.has_key('uri'):
                result += '<a href="{0}" class="puburi"> {1} </a>'.format(cleanData['uri'], cleanData['title'])
            else:
                result += ' <span class="pubtitle"> ' + cleanData['title'] + '</span>'

        result += '<span class="pubdetails">'
        for label in ['booktitle', 'journal', 'pages', 'city', 'country', 'year']:
            if cleanData.has_key(label):
                result +=  ", " 
                if label == 'pages':
                    result += 'pp.'
                result += cleanData[label]
        result += ' </span> '
        return result

class BibException(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

class pubFetcher:

    startpubregex = re.compile(r'\s*@(\w+)\s*{', re.IGNORECASE) 

    def __init__(self):
        self.txt = None
        self.publist = [] #fetched publications
        self.suppressAt = False #allows or disallows for '@' symbol in bibtex

    def publistHTML(self, bibType = None):
        """Prints publications of bibType (all if None) in HTML"""
        #sort publications by year
        def sorter(publ):
            if publ.has_key('year'):
                year = re.search(r'[0-9]+', publ['year'])
                if not year == None:
                    start, end = year.span()
                    return int(publ['year'][start:end])
            else:
                return 0
        self.publist = sorted(self.publist, key = lambda publ: sorter(publ.data), reverse = True)
        #-------------------------
        for publication in self.publist:
            if (bibType == None) or (publication.data['bibtexentrytype'] == bibType):
                print "<li>" + publication.produceHTML() + "</li>"
    
    def loadPubs(self, bibsrc):
        """Loads publications from bibTeX file bibsrc."""
        with open(bibsrc, 'r') as f:
            self.txt = f.read()
            start = 0
            startpub = pubFetcher.startpubregex.search(self.txt, start)
            while not startpub is None:
                pubtype = startpub.groups()[0].upper() #ARTICLE, etc.
                start = startpub.span()[1] #one position after '{'
                pubdata = self.fetchPub(self.txt[start:])
                if not pubdata is None:
                    pubdata['bibtexentrytype'] = pubtype
                    self.publist.append(pub(pubdata))

                startpub = pubFetcher.startpubregex.search(self.txt, start)
            
    def fetchPub(self, inptxt):
        """Tries to read publication from inptxt.
        Returns a generated dict for a publication or None when it fails."""
        ctr, lbrackets, rbrackets = 0, 1, 0

        for letter in inptxt:
            ctr += 1
            if letter == '{':
                lbrackets += 1
            elif letter == '}':
                rbrackets += 1
            elif letter == '@' and self.suppressAt:
                raise BibException("Found '@' in text: {0}".format(inptxt[:ctr]))

            if lbrackets == rbrackets: #actual publication data gathering starts
                pubtxt = inptxt[:(ctr-1)] 
                pubtxt = re.compile(r'\s+').sub(' ', pubtxt) #trim whitespaces
                pubdata = dict()
                pubdata['bibtexentrylabel'], pubtxt = pubtxt.split(',', 1) #bibtex entry label
                fields = re.split(r'[\"\}],', pubtxt)
                if len(fields[-1].strip()) == 0:
                    fields = fields[:-1]
                for field in fields:
                    key, value = field.split('=',1)[0].strip(), field.split('=',1)[1]
                    pubdata[key] = value
                return pubdata

        return None

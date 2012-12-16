# -*- coding: utf-8 -*-

import re 

class pub:
    pass

class BibException(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

class pubFetcher:

    startpubregex = re.compile(r'\s*@\w+\s*{', re.IGNORECASE) 

    def __init__(self):
        self.txt = None
        self.suppressAt = False #allows or disallows for '@' symbol in bibtex
    
    def loadPubs(self, bibsrc):
        with open(bibsrc, 'r') as f:
            self.txt = f.read()
            start = 0
            startpub = pubFetcher.startpubregex.search(self.txt, start)
            while not startpub is None:
                start = startpub.span()[1] #one position after '{'
                self.fetchPub(self.txt[start:])

                startpub = pubFetcher.startpubregex.search(self.txt, start)
            
    def fetchPub(self, inptxt):
        """Tries to read publication from inptxt.
        Returns a generated pub or None when it fails."""
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
                fields = pubtxt.split(',')
                pubdata = dict()
                pubdata['bibtexentrylabel'] = fields[0] #bibtex entry label
                for field in fields[1:-1]:
                    key, value = field.split('=',1)
                    key, value = key.strip(), value.strip()
                    pubdata[key] = value[1:-1] #remove brackets or quotation marks
                return pubdata

        return None

# -*- coding: utf-8 -*-

import argparse
from publication import *

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("bibsrc", help = "BibTeX source file")
    args = parser.parse_args()
    src = vars(args)["bibsrc"]
    
    try:
        fetcher = pubFetcher()
        fetcher.loadPubs(src)

        #an example use of fetcher
        print '<h1 class="journpub">Journal publications</h1><ul>'
        fetcher.publistHTML("ARTICLE")
        print "</ul>" 

        print '<h1 class="procpub">Conference publications</h1><ul>'
        fetcher.publistHTML("INPROCEEDINGS")
        print "</ul>" 
        #------------------------

    except IOError as ioerr:
        print ioerr
    except BibException as biberr:
        print biberr
    

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
        print '<h4 class="journpub">Journal publications</h4><ul>'
        fetcher.publistHTML("ARTICLE")
        print "</ul>" 

        print '<h4 class="procpub">Conference publications</h4><ul>'
        fetcher.publistHTML("INPROCEEDINGS")
        print "</ul>" 
        #------------------------

    except IOError as ioerr:
        print ioerr
    except BibException as biberr:
        print biberr
    

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
    except IOError as ioerr:
        print ioerr
    except BibException as biberr:
        print biberr
    

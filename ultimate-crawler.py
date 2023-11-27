#!/usr/bin/env python3

from requests import get
from bs4 import BeautifulSoup
import requests
import argparse
from progress.bar import Bar

def crawl_them_all():
    only_files = []
    only_dirs = []
    donly_dirs = {}
    out = []
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--target", metavar="", required=True)
    parser.add_argument("-d", "--depth", metavar="", help="It sets how deep it should crawl. Higher values increase the execution time [1, 2, 3]")
    args = parser.parse_args()
    target = args.target
    depth = args.depth
    xyz = get(target, verify=False)
    soup = BeautifulSoup(xyz.text, "lxml")
    if int(depth) <= 3:
        for _ in range(int(depth)):
            if not only_dirs:
                for tag in soup.find_all():
                    next_ones = tag.get('href')
                    if next_ones is not None:
                        if next_ones.startswith("http") or next_ones.startswith("https"):
                            # Get splitted at the slashes
                            # Ignore proto and target
                            # Example bellow
                            # Original one => http://83.136.254.53:44248/wp-content/plugins/mail-masta/lib/css/mm_frontend.css?ver=5.1.6
                            # Parsed one => ['wp-content', 'plugins', 'mail-masta', 'lib', 'css', 'mm_frontend.css?ver=5.1.6']
                            dirs = next_ones.split("/")[3:]
                            for _ in range(len(dirs)):
                                dirs_joined = "/".join(dirs[:_+1])
                                if dirs[:_+1][-1] != "":
                                    if "/" in dirs_joined:
                                        if ".asp" in dirs_joined or ".aspx" in dirs_joined or ".bat" in dirs_joined or ".c" in dirs_joined or ".cfm" in dirs_joined or ".cgi" in dirs_joined or ".css" in dirs_joined or ".com" in dirs_joined or ".dll" in dirs_joined or ".exe" in dirs_joined or ".hta" in dirs_joined or ".htm" in dirs_joined or ".html" in dirs_joined or ".inc" in dirs_joined or ".jhtml" in dirs_joined or ".js" in dirs_joined or ".jsa" in dirs_joined or ".jsp" in dirs_joined or ".log" in dirs_joined or ".mdb" in dirs_joined or ".nsf" in dirs_joined or ".pcap" in dirs_joined or ".php" in dirs_joined or ".php2" in dirs_joined or ".php3" in dirs_joined or ".php4" in dirs_joined or ".php5" in dirs_joined or ".php6" in dirs_joined or ".php7" in dirs_joined or ".phps" in dirs_joined or ".pht" in dirs_joined or ".phtml" in dirs_joined or ".pl" in dirs_joined or ".phar" in dirs_joined or ".reg" in dirs_joined or ".sh" in dirs_joined or ".shtml" in dirs_joined or ".sql" in dirs_joined or ".swf" in dirs_joined or ".txt" in dirs_joined or ".xml" in dirs_joined:
                                            dir_ready = target+"/"+dirs_joined
                                            if dir_ready not in only_files:
                                                only_files.append(dir_ready)
                                        else:
                                            if dirs_joined[-1] != "/":
                                                dir_ready = target+"/"+dirs_joined+"/"
                                                if dir_ready not in donly_dirs:
                                                    #only_dirs.append(dir_ready)
                                                    donly_dirs[dir_ready] = donly_dirs.get(dir_ready, 0) + 1
                                            else:
                                                dir_ready = dirs_joined
                                                print(f"What's this {dir_ready}")
                else:
                    bar = Bar (f"[+] Crawling Initial URLs-",max=sum(donly_dirs.values()), fill="█")
                    for values, dirs in zip(range(sum(donly_dirs.values())), donly_dirs):
                        bar.next()
                        if dirs != "../":
                            try:
                                re = get(dirs, verify=False)
                                soup = BeautifulSoup(re.text, "lxml")
                                for tag in soup.find_all():
                                    next_ones = tag.get('href')
                                    if next_ones is not None:
                                        if next_ones.startswith("http") or next_ones.startswith("https"):
                                            dirs = next_ones.split("/")[3:]
                                            for _ in range(len(dirs)):
                                                dirs_joined = "/".join(dirs[:_+1])
                                                if dirs[:_+1][-1] != "":
                                                    if "/" in dirs_joined:
                                                        if ".asp" in dirs_joined or ".aspx" in dirs_joined or ".bat" in dirs_joined or ".c" in dirs_joined or ".cfm" in dirs_joined or ".cgi" in dirs_joined or ".css" in dirs_joined or ".com" in dirs_joined or ".dll" in dirs_joined or ".exe" in dirs_joined or ".hta" in dirs_joined or ".htm" in dirs_joined or ".html" in dirs_joined or ".inc" in dirs_joined or ".jhtml" in dirs_joined or ".js" in dirs_joined or ".jsa" in dirs_joined or ".jsp" in dirs_joined or ".log" in dirs_joined or ".mdb" in dirs_joined or ".nsf" in dirs_joined or ".pcap" in dirs_joined or ".php" in dirs_joined or ".php2" in dirs_joined or ".php3" in dirs_joined or ".php4" in dirs_joined or ".php5" in dirs_joined or ".php6" in dirs_joined or ".php7" in dirs_joined or ".phps" in dirs_joined or ".pht" in dirs_joined or ".phtml" in dirs_joined or ".pl" in dirs_joined or ".phar" in dirs_joined or ".reg" in dirs_joined or ".sh" in dirs_joined or ".shtml" in dirs_joined or ".sql" in dirs_joined or ".swf" in dirs_joined or ".txt" in dirs_joined or ".xml" in dirs_joined:
                                                            dir_ready = target+"/"+dirs_joined
                                                            if dir_ready not in only_files:
                                                                only_files.append(dir_ready)
                                                        else:
                                                            if dirs_joined[-1] != "/":
                                                                dir_ready = target+"/"+dirs_joined+"/"
                                                                if dir_ready not in only_dirs:
                                                                    only_dirs.append(dir_ready)
                                                            else:
                                                                dir_ready = dirs_joined
                                                                print(f"What's this {dir_ready}")
                                        else:
                                            try:
                                                if next_ones != "../":
                                                    if next_ones[-1] == "/":
                                                        if next_ones not in only_dirs:
                                                            next_ones = dirs+next_ones
                                                            only_dirs.append(next_ones)
                                                    elif ".asp" in next_ones or ".aspx" in next_ones or ".bat" in next_ones or ".c" in next_ones or ".cfm" in next_ones or ".cgi" in next_ones or ".css" in next_ones or ".com" in next_ones or ".dll" in next_ones or ".exe" in next_ones or ".hta" in next_ones or ".htm" in next_ones or ".html" in next_ones or ".inc" in next_ones or ".jhtml" in next_ones or ".js" in next_ones or ".jsa" in next_ones or ".jsp" in next_ones or ".log" in next_ones or ".mdb" in next_ones or ".nsf" in next_ones or ".pcap" in next_ones or ".php" in next_ones or ".php2" in next_ones or ".php3" in next_ones or ".php4" in next_ones or ".php5" in next_ones or ".php6" in next_ones or ".php7" in next_ones or ".phps" in next_ones or ".pht" in next_ones or ".phtml" in next_ones or ".pl" in next_ones or ".phar" in next_ones or ".reg" in next_ones or ".sh" in next_ones or ".shtml" in next_ones or ".sql" in next_ones or ".swf" in next_ones or ".txt" in next_ones or ".xml" in next_ones:
                                                            if dirs[:_+1][-1] != "":
                                                                next_ones = dirs,next_ones
                                                                if next_ones not in only_files:
                                                                    only_files.append(''.join(next_ones))
                                            except IndexError:
                                                pass
                            except requests.exceptions.ConnectionError:
                                print(f"This one failed {dirs}")
                bar.finish()
            break            
    else:
        print(f"[!] Unknown recursion options {depth}") 
        print("[+] Available options [1, 2, 3]")   
                    
                    

    
    for dirs in only_dirs:
        print(f"DIRS-[{dirs}]")

    for files in only_files:
        print(f"FILE-[{files}]")

    

crawl_them_all()

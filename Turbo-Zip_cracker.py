print("""
##   ##   ####    ##                #####    ######   ####    
 ##   ##    ##     ##                ##  ##   ##       ## ##   
 ##   ##    ##     ##                ##  ##   ##       ##  ##  
 ## # ##    ##     ##       ######   #####    ####     ##  ##  
 #######    ##     ##                ####     ##       ##  ##  
 ### ###    ##     ##                ## ##    ##       ## ##   
 ##   ##   ####    ######            ##  ##   ######   #### 
""")

from optparse import OptionParser
import pyzipper
from progress.bar import Bar

def get_wordlist(wordlist_file):
    with open(wordlist_file, 'r') as f:
        return f.read().split('\n')

def extract(file_name, password):
    try:
        with pyzipper.AESZipFile(file_name, 'r') as f:
            f.extractall(pwd=bytes(password, 'utf-8'))
        return True
    except RuntimeError:
        return False

if __name__ == "__main__":
    parser = OptionParser()
    parser.add_option("-f", "--file", dest="filename",
                        help="compressed file", metavar="FILE")
    parser.add_option("-w", "--wordlist", dest="wordlist",
                        help="Select the wordlist", metavar="WORDLIST")

    (options, args) = parser.parse_args()

    password_found = False
    wordlist = get_wordlist(options.wordlist)
    with Bar('Processing', max=len(wordlist)) as bar:
        for p in wordlist:
            if extract(options.filename, p):
                print(f"\n[+] Password found: {p}")
                password_found = True
                break
            bar.next()

    if not password_found:
        print('Zip Password not found, try another wordlist')





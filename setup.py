"""
Setup only works in bash terminals ;)
"""

import os
import sys

def main():
    """
    Good code ahead!
    """
    directory = os.listdir()
    platform = sys.platform
    if platform in ('linux', 'darwin'):
        if 'ise.py' in directory:
            os.system('chmod +x ise.py; mv ise.py ise;')
        elif 'ise' not in directory:
            os.system("echo 'Expected ise.py or ise to be in current directory.'")
            quit()

        os.system("""
        rm -r ~/bin; 
        mkdir ~/bin; 
        cp ise ~/bin; 
        export PATH=$PATH":$HOME/bin"; 
        echo 'export PATH=$PATH":$HOME/bin"' >> .profile; 
        """)
    else:
        sys.stdout.write(platform + ' not supported.\n')
        sys.stdout.flush()

if __name__ == '__main__':
    main()

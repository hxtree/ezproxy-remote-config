'''
Sync EzProxy Config with Google Docs

author:         hxtree
language:       Python
date:           2017-01-04

REQUIRED:
        sudo apt-get install python-pip

INSTALL:
        sudo crontab -e
        */5 * * * * python /DIR/sync.py
'''

import inspect, os, shutil, datetime, time, string,fnmatch, os, sys, ntpath, math, glob
from tendo import singleton
import urllib
import filecmp

__author__ = 'hxtree'

def main():
        reload(sys)

        sys.setdefaultencoding('utf-8')
        
        # allow only one instance of a script
        me = singleton.SingleInstance()
        
        # change the relative directory
        os.chdir('/usr/local/ezproxy')
        
        # get local ini config

        old_file = "/usr/local/ezproxy/config.txt"
        new_file = "/usr/local/ezproxy/new_config.txt"
        download_file = "https://docs.google.com/feeds/download/documents/export/Export?id={{INSERT_ID}}&exportFormat=txt"

        print '<<script start>>'

        # file to be written to
        print "downloading " + new_file
        urllib.urlretrieve(download_file, new_file)

        # check if new file is a reasonable size
        if not os.path.getsize(new_file) > 1000:
                print new_file + ' was under 1000 bytes'
                sys.exit()
        # check if new file exists
        if not os.path.isfile(new_file):
                print new_file + ' does not exists'
                sys.exit()
        # check if old file exists
        if not os.path.isfile(old_file):
                print old_file + ' does not exists'
                sys.exit()
        try:
                # check if files are same or different
                if filecmp.cmp(new_file, old_file):
                        print 'files are identical'
                else:
                        print 'files are different'

                        # try to remove the _backup file
                        try:
                                os.remove(old_file + '_backup')
                        except:
                                print old_file + '_backup does not exists'

                        # try to make a new _backup file
                        try:
                                shutil.copy(old_file, old_file + '_backup')
                        except IOError:
                                try:
                                        os.chmod(where, 777)
                                        shutil.copy(old_file, old_file + '_backup')
                                except:
                                        print 'could not copy ' + old_file + ' to ' + old_file + '_backup'
                                        sys.exit()

                        # move the new file in place of old file
                        try:
                                os.rename(new_file, old_file)
                        except:
                                print 'could not rename ' + new_file + ' to ' + old_file
                                sys.exit()

                        # try to restart the ezproxy service
                        try:
                                os.system("./ezproxy restart")
                        except:
                                print 'failed to restart ezproxy service'
                                sys.exit()
        except:
                print 'could not compare files'
                sys.exit()
        print '<<script end>>'
if __name__ == "__main__":
        main()              

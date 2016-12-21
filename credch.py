##
# File:     credch.py
# config:   gitCredentials.json
# Author:   arwk
# Github:   https://github.com/arwk/gitCredentialChanger
# Created:  09.12.16
# Modified: 19.12.16
##

import os, sys
from subprocess import call, STDOUT
import argparse
import json
import re

#################
# Global config #
#################
scriptPath = os.path.dirname(os.path.realpath(__file__))
configFilename = "gitCredentials.json"
configFilenameDemo = "gitCredentialsDemo.json"

##################
# Setup argparse #
##################
parser = argparse.ArgumentParser(description='Git credential changer')
parser.add_argument('abbreviation', metavar='ABBRV', type=str, nargs='?',
                    help='Abbreviation of user')
parser.add_argument("-s", "--show", action='store_true',
                    help="Show current credentials and quit")
parser.add_argument("-r", "--reset", action='store_true',
                    help="Reset credentials to the default values")
parser.add_argument("-l", "--list", action='store_true',
                    help="List entries in config file")
parser.add_argument("-c", "--check", action='store_true',
                    help="Check if the current credentials equal the default ones")
args = parser.parse_args()


####################
# Define functions #
####################
def checkIfGitRepo():
    """
    returns
      - True, if the current working directory is a git repository
      - False, if the current directory isn't a git repository
    """
    if call(["git", "rev-parse", "--is-inside-work-tree"], stderr=STDOUT, stdout=open(os.devnull, 'w')) != 0:
        # We arent inside an git repo, nothing we can do. Inform user
        return False
    else:
        # Yay, we are inside an git repo
        return True

def getGitRepoPath():
    """
    returns the toplevel path of the current git repository
    """
    path = os.popen("git rev-parse --show-toplevel").read().strip()
    return path

def checkConfigFile(toplevelPath):
    """
    Checks if a configfile is present inside the toplevel directory
    """
    configFile = '{}/{}'.format(toplevelPath, configFilename)
    if os.path.isfile(configFile):
        # Found config File
        return True
    else:
        # Config File not found
        return False

def getCurrentCredentials():
    """
    returns an array containing [currentName, currentMail] retrieved by git
    """
    cmdName = "git config user.name"
    cmdMail = "git config user.email"
    try:
        currentName = os.popen(cmdName).read().strip()
        currentMail = os.popen(cmdMail).read().strip()
        return  [currentName, currentMail]
    except Exception, e:
        print "Error: {}".format(e)

def choice(personsList):
    try:
        # Get name and mail configured in git
        [currentName, currentMail] = getCurrentCredentials()
        for n, person in enumerate(personsList):
            realName = person['name']
            short = person['abbr']
            # Mark the current setting
            if person['gitMail'] == currentMail:
                selected = "->"
            else:
                selected = "  "
            if "note" in person:
                note = "({})".format(person['note'])
            else:
                note = ""
            print "{} {:01d}) ({}) {} {}".format(selected, n+1, short, realName, note)

        idxChoice = int(raw_input('Please enter a number: '))
        return personsList[idxChoice-1]

    except KeyboardInterrupt:
        # Catch Ctrl-C Interrupts
        print "\nStopped by User: Goodbye!"
        sys.exit()

    except Exception, e:
        # Catch everything else
        print "An error occured: {}\n\nGoodbye!".format(e)
        sys.exit()

def setCredentials(person):
    """
    Function that sets git name and mail
    Parameters:
      - person: dict containing keys {'gitName':?, 'gitMail':?}
    """
    nickName = person['gitName']
    mailAddr = person['gitMail']
    print "\nSetting git credentials to:\n  {} <{}>\n".format(nickName, mailAddr)
    cmdName = "git config user.name '{}'".format(nickName)
    cmdMail = "git config user.email '{}'".format(mailAddr)
    print "Executing:\n  {}\n  {}".format(cmdName, cmdMail)
    os.system(cmdName)
    os.system(cmdMail)

#####################
# Checks on startup #
#####################
if not checkIfGitRepo():
    # Exit if the current directory isn't a git repo
    print "This doesn't look like an git repo.\nNothing I can do..\nExiting..."
    sys.exit()

if args.check:
    # Check if the current credentials equal to the default entries of the
    # config file
    # TODO: IMPLEMENTED
    print "To be implemented"
    sys.exit()
    [nCurrent, mCurrent] = getCurrentCredentials()
    [nDefault, mDefault] = getDefaultCredentials()

    if nCurrent == nDefault and mCurrent == mDefault:
        print "Matching"
    else:
        print "False"

path = getGitRepoPath()
print "Toplevel repo path: {}\n".format(path)

#################################
# Print current git cred config #
#################################
[n,m] = getCurrentCredentials()
print "Current Cred:\n  {} <{}>\n".format(n,m)

if args.show:
    #Only show git credential config and exit
    print "Goodbye!"
    sys.exit()

if not checkConfigFile(path):
    # Exit if no configfile is present
    configFilePath = "{}/{}".format(path, configFilename)
    demopath = "{}/{}".format(scriptPath, configFilenameDemo)
    print "There seems to be no config file '{cpath}' :(\nTo create one, you might want to copy the demo file.\n  cp {demopath} {cpath}\nExiting...".format(demopath=demopath, cpath=configFilePath)
    sys.exit()

if args.list:
    # List the entries of configFile
    print "To be implemented...\nGoodbye!"
    sys.exit()

# Check if there are any command line arguments
if args.abbreviation != None:
    shortArgv = args.abbreviation
else:
    shortArgv = ""


idxList = []
shortMatches = []

# Open configfile <cred.json>
# Example entry:
#  [
#    {
#      "name": "Foo",
#      "abbr": "f",
#      "gitName": "Foo Bar",
#      "gitMail": "foo@bar.ch"
#    }
#  ]

with open('{}/{}'.format(path, configFilename)) as data_file:
    try:
        persons = json.load(data_file)
        # Iterate over all entries
        for idx, person in enumerate(persons):
            realName = person['name']
            short = person['abbr']
            idxList.append(person)
            # Try to find matching abbreviations
            if shortArgv != "" and shortArgv in short:
                shortMatches.append(person)
    except ValueError, e:
        print "ERROR: Your Configfile ({}/{}) couldn't be parsed...\nGoodbye!".format(path, configFilename)
        print e
        sys.exit()

if len(shortMatches) == 0:
    print "Nothing matched. Please choose"
    resPers = choice(idxList)
    setCredentials(resPers)
elif len(shortMatches) == 1:
    print "Matched!"
    resPers = shortMatches[0]
    setCredentials(resPers)
else:
    print "Matched too many. Please choose"
    resPers = choice(shortMatches)
    setCredentials(resPers)

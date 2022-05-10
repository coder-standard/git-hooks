# -*- coding: utf-8 -*

import getopt
import os
import sys
import logging
import shutil
from distutils.spawn import find_executable


logging.basicConfig(level=logging.DEBUG)

globalFlag = False
opts, args = getopt.getopt(sys.argv[1:], "-g-v", [ "global", 'version'])
for opt_name, opt_value in opts:
    if opt_name in ("-g", "--global"):
        globalFlag = True
    if opt_name in ("-v", "--version"):
        print("The version is v1.0")
        exit()


programPath = find_executable("git")
if programPath is None:
    logging.critical("no git installed")
    exit(1)

programPath = find_executable("gitleaks")
if programPath is None:
    logging.critical("no gitleaks installed, please install gitleasks first by url "
                     "https://github.com/zricethezav/gitleaks")
    exit(1)


workDir = os.getcwd()
logging.info("cur work dir: %s", workDir)

if globalFlag:
    logging.info("global mode")
else:
    logging.info("local mode")

if not os.path.isdir(os.path.join(workDir, ".git")):
    if not globalFlag:
        logging.warning("not git root, use --global or enter root of git project")

if globalFlag:
    initTemplateDir = os.popen("git config --global init.templateDir").read().strip()
    if len(initTemplateDir) == 0:
        initTemplateDir = os.path.join(os.path.expanduser("~"), ".git-template")
        if not os.path.isdir(initTemplateDir):
            os.makedirs(initTemplateDir)
        if not os.path.isdir(initTemplateDir):
            logging.critical("no file %s", initTemplateDir)
            exit(1)
        os.popen("git config --global init.templateDir " + initTemplateDir)

    initTemplateDir = os.popen("git config --global init.templateDir").read().strip()
    if len(initTemplateDir) == 0:
        logging.critical("valid  init.templateDir")
        exit(1)

    logging.info("init.templateDir is %s", initTemplateDir)
    hooks_root = initTemplateDir
    hooks_dir = os.path.join(initTemplateDir, "hooks")
else:
    hooks_dir = os.path.join(workDir, ".git", "hooks")

if not os.path.isdir(hooks_dir):
    os.makedirs(hooks_dir)

preCommitFile = os.path.join(hooks_dir, "pre-commit")

hasInstalled = False

if not os.path.isfile(preCommitFile):
    with open(preCommitFile, 'a', encoding='utf-8') as f:
        f.write("#!/bin/sh\n")

gitHooksPyFile = "./.git/hooks/git-hooks-precommit.sh"

with open(preCommitFile, 'r', encoding='utf-8') as f:
    line = f.readline()
    if not line:
        with open(preCommitFile, 'a', encoding='utf-8') as f:
            f.write("#!/bin/sh\n")
    else:
        if line.strip() != "#!/bin/sh":
            logging.critical("need /bin/sh flag")
            exit(1)
        while True:
            line = f.readline()
            if not line:
                break
            line = line.strip()
            if line == gitHooksPyFile:
                hasInstalled = True
                break

os.popen("chmod +x " + preCommitFile)

if hasInstalled:
    logging.critical("has installed")
else:
    shutil.copyfile(os.path.join(workDir, "git-hooks-precommit.sh"), os.path.join(hooks_dir, "git-hooks-precommit.sh"))
    os.popen("chmod +x " + os.path.join(hooks_dir, "git-hooks-precommit.sh"))
    shutil.copyfile(os.path.join(workDir, ".gitleaks.toml"), os.path.join(hooks_dir, "gitleaks.toml"))
    with open(preCommitFile, 'a', encoding='utf-8') as f:
        f.write("\n"+gitHooksPyFile+"\n")

logging.info("install hooks success")

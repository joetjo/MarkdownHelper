# Copyright 2021 joetjo https://github.com/joetjo/MarkdownHelper
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

from base.setup import GhSetup

from pathlib import Path

from markdown.markdownfile import MhMarkdownFile
from markdown.report import MhReport

#
# Setup from $home/.markdownHelper
#    ( Sample provided in example.markdownHelper.json )
#
SETUP = GhSetup('markdownHelper')
VAULT = SETUP.getBloc("global")["base_folder"]
IGNORE = SETUP.getBloc("global")["ignore"]
REPORTS = SETUP.getBloc("global")["reports"]
FILES = dict()
SORTED_FILES = dict()
TAGS = dict()

# folder: Path
# shift: String ( String length provide the indentation level )
def processFolder(folder, shift):
    print("{}{}".format(folder, shift))
    entryCount = 0

    # Loop on file in current folder
    for entry in folder.iterdir():
        if entry.is_file() and entry.name.endswith(".md") and entry.name not in IGNORE:
            key = entry.name[0:len(entry.name) - 3]
            entryCount = entryCount + 1
            mdfile = MhMarkdownFile(key, entry)
            FILES[key] = mdfile
            print("{}>{} {}".format(shift, key, mdfile.tags))
            for tag in mdfile.tags:
                TAGS[tag] = tag

    # Loop on sub folder
    for entry in folder.iterdir():
        if not entry.is_file() and entry.name not in IGNORE:
            entryCount = entryCount + processFolder(entry, "{}{}".format(shift, " "))

    return entryCount


def markdown():
    print("   | Markdown vault: {}\n====".format(VAULT))
    count = processFolder(Path(VAULT), "")

    print("\n=================")
    print("> {} md files detected".format(count))
    print("> {} tags detected".format(len(TAGS)))

    for key in sorted(FILES):
        SORTED_FILES[key] = FILES[key]

    try:
        for report in REPORTS:
            print("\n=================\nProcessing report \"{}\"\n=================\n".format(report["title"]))
            MhReport(report, SORTED_FILES, TAGS).generate()
    except Exception as e:
        raise

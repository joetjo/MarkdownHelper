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
from datetime import datetime

# Ugly but simple
LONG_BLANK = "                                                                                                         "

ALLOWED_ATTRIBUTES = ["target",  # 1st level only: target file path
                      "title",  # mandatory on each bloc
                      "tag_condition",  # optional: tag list to filter content ( can be tag prefix )
                      "path_condition",  # optional: name list that should be used in folder path
                      "condition_type",  # if "not" --> inverse the tag_condition or path condition
                      "contents",  # sub blocs / in not defined --> leaf to print
                      "else"]  # optional: bloc to process all entries not selected by filter


class UnknownJSonAttribute(Exception):
    def __init__(self, attName, json,
                 message="Unknown JSon attribute \"{}\" used in report, allowed attributes are: {}, json bloc:\n{}"):
        self.message = message
        super().__init__(self.message.format(attName, ALLOWED_ATTRIBUTES, json))


class MhReportEntry:

    # inputFiles: dict of name, MhMarkdownFiles
    def __init__(self, json, inputFiles, allTags, level="#"):
        self.json = json
        self.level = level
        self.inputFiles = inputFiles
        self.allTags = allTags

        for key in json:
            if key not in ALLOWED_ATTRIBUTES:
                raise UnknownJSonAttribute(key, json)

        # Setup content filter
        try:
            self.tags = self.json["tag_condition"]
        except KeyError:
            self.tags = []

        try:
            self.paths = self.json["pathf_condition"]
        except KeyError:
            self.paths = []

        self.inverseCondition = ""
        try:
            self.inverseCondition = self.json["condition_type"]
            if self.inverseCondition != "not":
                raise UnknownJSonAttribute(key, json, message="Invalid value \"{}\" for attribute \"condition_type\"".format(self.inverseCondition))

        except KeyError:
            self.paths = []

        self.isFiltering = not len(self.tags) == 0 or not len(self.paths) == 0
        self.isVirtual = self.title() == "%TAGNAME%"
        self.isRoot = level == "#"

        # Setup content
        self.elseFiles = dict()
        if not self.isFiltering:
            self.filteredFiles = inputFiles.copy()
        else:
            self.filteredFiles = dict()
            for name, file in self.inputFiles.items():
                if self.matchCondition(file):
                    self.filteredFiles[name] = file
                else:
                    self.elseFiles[name] = file

        if self.inverseCondition == "not":
            tmp = self.filteredFiles
            self.filteredFiles = self.elseFiles
            self.elseFiles = tmp

    # Returns True if file match report condition
    def matchCondition(self, file):
        result = False

        for tag in self.tags:
            if file.hasTagStartingBy(tag):
                result = True
                break

        for path in self.paths:
            if file.pathMatch(path):
                result = True
                break

        return result

    def title(self):
        return self.json["title"]

    @staticmethod
    def mappingTags(tags, allTags):
        result = []
        for token in tags:
            token = "#{}".format(token)
            for tag in allTags:
                if tag.startswith(token):
                    result.append(tag)
        return result

    def generate(self, writer):
        if self.isVirtual:
            print("  | {} VIRTUAL [{}->{}] ({} {})".format(LONG_BLANK[0:len(self.level) * 2],
                                                           len(self.inputFiles), len(self.filteredFiles), self.tags,
                                                           self.paths))
            if len(self.filteredFiles) > 0:
                # virtual content that must be expanded !
                for tag in sorted(self.mappingTags(self.tags, self.allTags)):
                    content = self.json.copy()
                    del content["else"]
                    content["title"] = tag[len(self.tags[0]) + 1:]  # Replace %TAGNAME% title by expended tag detected
                    content["tag_condition"] = [tag[1:]]  # and use the expanded tag to filer
                    if len(content["title"]) > 0:
                        MhReportEntry(content, self.filteredFiles.copy(), self.allTags, self.level).generate(writer)
            # Proceed to else of VIRTUAL block
            try:
                MhReportEntry(self.json["else"], self.elseFiles, self.allTags, self.level).generate(writer)
            except KeyError:
                pass

            return

        print("  | {} {} [{}->{} / {}] ({} {})".format(LONG_BLANK[0:len(self.level) * 2], self.title(),
                                                  len(self.inputFiles), len(self.filteredFiles), len(self.elseFiles), self.tags, self.paths))

        if self.isRoot:
            writer.writelines("#MarkdownHelperReport {}\n".format(datetime.now().strftime("%d/%m/%Y %H:%M:%S")))

        nextLevel =   "{}#".format(self.level)
        if len(self.filteredFiles) > 0:
            writer.writelines("{} {} ({})\n".format(self.level, self.title(), len(self.filteredFiles)))
            try:
                json_contents = self.json["contents"]
                for content in json_contents:
                    MhReportEntry(content, self.filteredFiles, self.allTags, nextLevel).generate(
                        writer)
            except KeyError:
                for name, file in self.filteredFiles.items():
                    writer.writelines("- [[{}]] \n".format(name))

            try:
                MhReportEntry(self.json["else"], self.elseFiles, self.allTags, nextLevel).generate(writer)
            except KeyError:
                pass


class MhReport:

    def __init__(self, json, inputFiles, allTags):
        self.json = json
        self.inputFiles = inputFiles
        self.allTags = allTags

    def target(self):
        return self.json["target"]

    def generate(self):
        rootReport = MhReportEntry(self.json, self.inputFiles, self.allTags)
        print("Generate report \"{}\" to {}".format(rootReport.title(), self.target()))
        with open(self.target(), 'w', encoding='utf-8') as writer:
            rootReport.generate(writer)

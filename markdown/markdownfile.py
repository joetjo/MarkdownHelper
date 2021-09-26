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
import re


class MhMarkdownFile:

    # name : String
    # path : Path from PathLib
    def __init__(self, name, path):
        # String
        self.name = name
        # WindowsPath ( from pathLib )
        self.path = path
        self.tags = []
        self.loadTags()
        self.matchTag = None

    def loadTags(self):
        with open(self.path, 'r', encoding='utf8') as reader:
            for line in reader:
                self.tags.extend(re.findall(r"#[\w|/_-]+", line))

    # expr : re regexp
    def pathMatch(self, path):
        return str(self.path.resolve()).find(path) != -1

    # Search tag like #XXXXX ( with tag = '#XXXXX' )
    def hasExactTag(self, tag):
        result = tag in self.tags
        if result:
            self.matchTag = tag

    # Search tag like #XXXXX....  ( with prefix = '#XXXXX' )
    def hasTagStartingBy(self, prefix):
        token = "#{}".format(prefix)
        for tag in self.tags:
            if tag.startswith(token):
                self.matchTag = tag
                return True
        return False

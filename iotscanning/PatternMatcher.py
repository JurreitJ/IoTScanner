import re

class PatternMatcher():
    """
    Methods to check, if the given pattern matches the expected pattern.
    """
    def is_header(self, field):
        if field == "header":
            return True
        else:
            return False


    def is_regex(self, operator):
        if operator == "regex":
            return True
        else:
            return False

    def is_equals(self, operator):
        if operator == "==":
            return True
        else:
            return False

    def is_title(self, tag_name):
        if tag_name == "title":
            return True
        else:
            return False

    def is_meta(self, tag_name):
        if tag_name == "meta":
            return True
        else:
            return False

    def match_equals(self, string, pattern):
        if string == pattern:
            return True
        else:
            return False

    def match_regex(self, string, pattern):
        if re.match(pattern, string):
            return True
        else:
            return False

    def is_empty_tag(self, tag_name):
        if tag_name == "" and tag_name is None:
            return True
        else:
            return False

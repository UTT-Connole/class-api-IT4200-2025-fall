# no_comments_checker.py
from pylint.checkers import BaseTokenChecker
import tokenize

class NoCommentsChecker(BaseTokenChecker):
    name = "no-comments-checker"
    msgs = {
        "E9999": (
            "Comment found in file",
            "no-comments",
            "Comments are not allowed in this project.",
        ),
    }
    
    def process_tokens(self, tokens):
        for toknum, tokval, (srow, _), _, _ in tokens:
            if toknum == tokenize.COMMENT:
                self.add_message("no-comments", line=srow)

def register(linter):
    """Required method to register the checker."""
    linter.register_checker(NoCommentsChecker(linter))
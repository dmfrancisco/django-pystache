from django.template.base import *

BLOCK_TAG_START = '{{'
BLOCK_TAG_END = '}}'
VARIABLE_TAG_START = '{%'
VARIABLE_TAG_END = '%}'

class Lexer(object):
    def __init__(self, template_string, origin):
        self.template_string = template_string
        self.origin = origin
        self.lineno = 1

    def tokenize(self):
        "Return a list of tokens from a given template_string."
        in_tag = False
        result = []
        for bit in tag_re.split(self.template_string):
            if bit:
                result.append(self.create_token(bit, in_tag))
            in_tag = not in_tag
        return result

    def create_token(self, token_string, in_tag):
        """
        Convert the given token string into a new Token object and return it.
        If in_tag is True, we are processing something that matched a tag,
        otherwise it should be treated as a literal string.
        """
        if in_tag:
            if token_string.startswith(VARIABLE_TAG_START):
                token = Token(TOKEN_VAR, token_string[len(VARIABLE_TAG_START):-len(VARIABLE_TAG_END)].strip())
            elif token_string.startswith(BLOCK_TAG_START):
                token = Token(TOKEN_BLOCK, token_string[len(BLOCK_TAG_START):-len(BLOCK_TAG_END)].strip())
            elif token_string.startswith(COMMENT_TAG_START):
                content = ''
                if token_string.find(TRANSLATOR_COMMENT_MARK):
                    content = token_string[len(COMMENT_TAG_START):-len(COMMENT_TAG_END)].strip()
                token = Token(TOKEN_COMMENT, content)
        else:
            token = Token(TOKEN_TEXT, token_string)
        token.lineno = self.lineno
        self.lineno += token_string.count('\n')
        return token

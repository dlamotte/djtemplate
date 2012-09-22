from django import template

register = template.Library()

# from: https://gist.github.com/629508
"""
jQuery templates use constructs like:

    {% templatetag openvariable %}if condition{% templatetag closevariable %} print something{% templatetag openvariable %}/if{% templatetag closevariable %}

This, of course, completely screws up Django templates,
because Django thinks {% templatetag openvariable %} and {% templatetag closevariable %} mean something.

Wrap {% templatetag openblock %} verbatim {% templatetag closeblock %} and {% templatetag openblock %} endverbatim {% templatetag closeblock %} around those
blocks of jQuery templates and this will try its best
to output the contents with no changes.
"""

class VerbatimNode(template.Node):

    def __init__(self, text):
        self.text = text

    def render(self, context):
        return self.text


@register.tag
def verbatim(parser, token):
    text = []
    while 1:
        token = parser.tokens.pop(0)
        if token.contents == 'endverbatim':
            break
        if token.token_type == template.TOKEN_VAR:
            text.append('{% templatetag openvariable %}')
        elif token.token_type == template.TOKEN_BLOCK:
            text.append('{% templatetag openblock %}')
        text.append(token.contents)
        if token.token_type == template.TOKEN_VAR:
            text.append('{% templatetag closevariable %}')
        elif token.token_type == template.TOKEN_BLOCK:
            text.append('{% templatetag closeblock %}')
    return VerbatimNode(''.join(text))

# end gist

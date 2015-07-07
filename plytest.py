# A grammar for chemical equations like "H2O", "CH3COOH" and "H2SO4"
# Uses David Beazley's PLY parser.
# Implements two functions: count the total number of atoms in the equation and
#   count the number of times each element occurs in the equation.

import ply.lex as lex
import ply.yacc as yacc
import re, logging

class SpecFileLexer(object):

    tokens = (
        "VERSION",
        "NUMBER",
        "DOT",
        "EQUALS",
        "DOUBLEQUOTE"
    )

    t_VERSION = r'VERSION'

    t_EQUALS = r'='

    t_DOUBLEQUOTE = r'"'

    t_DOT = r'.'

    def t_NUMBER(self, t):
        r'\d+'
        t.value = int(t.value)
        return t

    def t_newline(self, t):
        r'\n+'
        t.lexer.lineno += len(t.value)

    t_ignore  = ' \t'

    def t_error(self, t):
        raise TypeError("Unknown text '%s'" % (t.value,))

    def build(self, **kwargs):
        self.lexer = lex.lex(module=self, **kwargs)

    def __iter__(self):
        return self.lexer

    def input(self, data):
        self.lexer.input(data)

    def token(self):
        g = self.lexer.token()
        return g


class SpecFileParser(object):

    def __init__(self,**kwargs):
        """ Create a new parser.
            Some arguments for controlling the debug/optimization
            level of the parser are provided. The defaults are
            tuned for release/performance mode.
            The simple rules for using them are:
            *) When tweaking the lexer/parser, set these to False
            *) When releasing a stable parser, set to True
            lex_optimize:
                Set to False when you're modifying the lexer.
                Otherwise, changes in the lexer won't be used, if
                some lextab.py file exists.
                When releasing with a stable lexer, set to True
                to save the re-generation of the lexer table on
                each run.
            lextab:
                Points to the lex table that's used for optimized
                mode. Only if you're modifying the lexer and want
                some tests to avoid re-generating the table, make
                this point to a local lex table file (that's been
                earlier generated with lex_optimize=True)
            yacc_optimize:
                Set to False when you're modifying the parser.
                Otherwise, changes in the parser won't be used, if
                some parsetab.py file exists.
                When releasing with a stable parser, set to True
                to save the re-generation of the parser table on
                each run.
            yacctab:
                Points to the yacc table that's used for optimized
                mode. Only if you're modifying the parser, make
                this point to a local yacc table file
            yacc_debug:
                Generate a parser.out file that explains how yacc
                built the parsing table from the ammar.
        """
        self.logger = logging.getLogger('parser')
        self.lex = SpecFileLexer()

        self.lex.build(optimize=False)
        self.tokens = self.lex.tokens

        self.parser = yacc.yacc(
            module=self,
            start='version',
            debug=True,
            optimize=False)

    def parse(self, text, debuglevel=0):
        """ Parses a file and returns a pdf.
            text:
                A string containing the C source code
            filename:
                Name of the file being parsed (for meaningful
                error messages)
            debuglevel:
                Debug level to yacc
        """
        return self.parser.parse(text, lexer=self.lex, debug=debuglevel)

    def p_version(self, p):
        """
        version : VERSION versionstring
        """
        p[0] = Test(p[2])

    def p_versionstring(self, p):
        """
        versionstring : NUMBER DOT NUMBER DOT NUMBER
        """
        p[0] = "{0}.{1}.{2}".format(p[1], p[3], p[5])

    def p_error(self, p):
        print "Syntax error at {0}".format(p.value)

class Test(object):
    def __init__(self, version):
        self.version = version
    def __repr__(self):
        return "Version is {0}".format(self.version)

if __name__ == "__main__":
    # Test it out
    data = '''
    VERSION 1.1.1
    '''
    parser = SpecFileParser(lex_optimize=False, yacc_debug=True, yacc_optimize=False)
    print parser.parse(data)

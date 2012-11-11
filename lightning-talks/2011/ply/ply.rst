PLY -- What?
================================================

- Python Lex & Yacc

  - Lex: Lexical analyzer
  - Yacc: Yet Another Compiler Compiler
  - Long-time (since 1970s) tools for building compilers

- Written and maintained by David Beazley

  - 1.0 in 2001, result of teaching compiler course
  - 2.0 in 2006, "major update"
  - 3.0 in 2009, supports Python 3
  - Current version is 3.4

----

PLY -- Why?
------------------------------------------------

- Sometimes projects need "scripting" built-in
- Medical billing "scrub rules"

  - Decide whether a Claim charge is OK or should be rejected
  - Examples

    - `require sup_dr_npi onlyif sup_dr`
    - `require LENGTH(dr_npi) = 10`

- Survey "skip rules"

  - Decide, based on answers so far, whether a question should be shown
  - Examples

    - `item54 = 3`
    - `item23 < 4 and item24 >= 1`

----

Lexing and Parsing Basics
------------------------------------------------

- Lexing

  - Splits input into tokens
  - Tokens have type and value
  - Tokens are recognized by pattern-matching

- Parsing

  - Transforms a sequence of tokens
  - Uses set of parsing rules
  - Rules expressed in BNF (Backus Normal Form)

.. code-block:: none

      expr : expr AND expr
      expr : ITEMID EQUALS NUMBER
           | ITEMID LT NUMBER
           | ITEMID GT NUMBER`

----

Example Lexer, plex.py (Part 1)
------------------------------------------------

.. code-block:: python

    from ply import lex

    class ExampleLexer(object):
        reserved = {
            'and': 'AND',
            'or': 'OR',
        }

        tokens = [
            'EQUALS',
            'LT',
            'LTE',
            'GT',
            'GTE',
            'NUMBER',
            'ITEMID',
        ] + list(reserved.values())

        t_EQUALS = r'='
        t_LT = r'\<'
        t_LTE = r'\<='
        t_GT = r'\>'
        t_GTE = r'\>='

        def t_NUMBER(self, t):
            r'\d+'
            t.value = int(t.value)
            return t

----

Example Lexer, plex.py (Part 2)
------------------------------------------------

.. code-block:: python

    from ply import lex

    class ExampleLexer(object):

        # ...Code from previous slide omitted...

        def t_ignore = ' \t'

        def t_error(self, t):
            raise Exception('Unknown token (%s) at offset %d.' % (t.value, t.lexpos))

        def t_ITEMID(self, t):
            r'[a-zA-Z_][a-zA-Z_0-9]*'
            t.type = self.reserved.get(t.value, 'ITEMID')
            if t.type == 'ITEMID':
                tval = self.item_dict.get(t.value, '')
                if tval == '':
                    self.t_error(t)
                else:
                    t.value = tval
            return t

----

Example Lexer, plex.py (Part 3)
------------------------------------------------

.. code-block:: python

    from ply import lex

    class ExampleLexer(object):

        # ...Code from previous slides omitted...

        def __init__(self, item_dict):
            self.item_dict = item_dict
            self.lexer = lex.lex(module=self)

        def tokenize(self, rule_string):
            self.lexer.input(rule_string)
            while True:
                token = self.lexer.token()
                if token:
                    print 'Token: type=%s, value=%s' % (token.type, token.value)
                else:
                    break
            return True

----

Example Lexer In Action
------------------------------------------------

.. code-block:: python

    >>> from plex import ExampleLexer
    >>> lexer = ExampleLexer({'abc': 123, 'xyz': 987})
    >>> lexer.tokenize('abc = 44')
    Token: type=ITEMID, value=123
    Token: type=EQUALS, value==
    Token: type=NUMBER, value=44
    True
    >>> lexer.tokenize('abc and 86')
    Token: type=ITEMID, value=123
    Token: type=AND, value=and
    Token: type=NUMBER, value=86
    True
    >>> lexer.tokenize('nonsense!')
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
      File "plex.py", line 53, in tokenize
        token = self.lexer.token()
      File "/home/kmtracey/.virtualenvs/present_ply/lib/python2.6/site-packages/ply/lex.py", line 348, in token
        newtok = func(tok)
      File "plex.py", line 41, in t_ITEMID
        self.t_error(t)
      File "plex.py", line 33, in t_error
        raise Exception('Unknown token (%s) at offset %d.' % (t.value, t.lexpos))
      Exception: Unknown token (nonsense) at offset 0.
    >>>

----

Example Parser, pparse.py (Part 1)
------------------------------------------------

.. code-block:: python

    from ply import yacc

    from plex import ExampleLexer

    class ExampleParser(object):

        def __init__(self, response_dict):
            self.tokens = ExampleLexer.tokens
            self.response_dict = response_dict
            self.parser = yacc.yacc(module=self)

        def evaluate(self, rule):
            lexer = ExampleLexer(self.response_dict).lexer
            return self.parser.parse(rule, lexer)

        def p_error(self, p):
            raise SyntaxError('Syntax error in input: %s' % p)

----

Example Parser, pparse.py (Part 2)
------------------------------------------------

.. code-block:: python

    from ply import yacc

    from plex import ExampleLexer

    class ExampleParser(object):

        # ...Code from previous slide omitted...

        def p_expr_and(self, p):
            """
            expr : expr AND expr
            """
            if not p[1]:
                p[0] = p[1]
            else:
                p[0] = p[3]

        def p_expr_or(self, p):
            """
            expr : expr OR expr
            """
            if p[1]:
                p[0] = p[1]
            else:
                p[0] = p[3]

----

Example Parser, pparse.py (Part 3)
------------------------------------------------

.. code-block:: python

    from ply import yacc

    from plex import ExampleLexer

    class ExampleParser(object):

        # ...Code from previous slides omitted...

        def p_expr_terminal(self, p):
            """
            expr : ITEMID EQUALS NUMBER
                 | ITEMID LT NUMBER
                 | ITEMID LTE NUMBER
                 | ITEMID GT NUMBER
                 | ITEMID GTE NUMBER
            """
            if p[2] == '=':
                oper = '=='
            else:
                oper = p[2]
            eval_str = '%s %s %s' % (p[1], oper, p[3])
            p[0] = eval(eval_str)

----

Example Parser In Action: How It Works
------------------------------------------------

.. code-block:: python

    Python 2.6.5 (r265:79063, Apr 16 2010, 13:57:41)
    [GCC 4.4.3] on linux2
    Type "help", "copyright", "credits" or "license" for more information.
    >>> from pparse import ExampleParser
    >>> parser = ExampleParser({'abc': 123, 'xyz': 987})
    Generating LALR tables
    WARNING: 4 shift/reduce conflicts
    >>> p2 = ExampleParser({'abc': 1, 'xyz': 2})
    >>> parser.evaluate('abc = 123')
    True
    >>> parser.evaluate('xyz=777')
    False
    >>> parser.evaluate('abc = 123 and xyz = 987')
    True
    >>> parser.evaluate('abc = 123 and xyz = 9887')
    False
    >>> parser.evaluate('abc = 123 or xyz = 9887')
    True
    >>> parrser.evaluate('abc = 123 and xyz = 44 or abc = 99')
    False
    >>> parser.evaluate('abc = 123 and xyz = 987 or abc = 99')
    True

----

Parser In Action: How it Breaks (Part 1)
------------------------------------------------

- What happens if the lexer doesn't find a valid token?

.. code-block:: python

    >>> parser.evaluate('abc >= 4 and xyzz = 987')
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
      File "pparse.py", line 14, in evaluate
        return self.parser.parse(rule, lexer)
      File "/home/kmtracey/.virtualenvs/present_ply/lib/python2.6/site-packages/ply/yacc.py", line 265, in parse
        return self.parseopt_notrack(input,lexer,debug,tracking,tokenfunc)
      File "/home/kmtracey/.virtualenvs/present_ply/lib/python2.6/site-packages/ply/yacc.py", line 921, in parseopt_notrack
        lookahead = get_token()     # Get the next token
      File "/home/kmtracey/.virtualenvs/present_ply/lib/python2.6/site-packages/ply/lex.py", line 348, in token
        newtok = func(tok)
      File "plex.py", line 41, in t_ITEMID
        self.t_error(t)
      File "plex.py", line 33, in t_error
        raise Exception('Unknown token (%s) at offset %d.' % (t.value, t.lexpos))
    Exception: Unknown token (xyzz) at offset 13.
    >>>

----

Parser In Action: How it Breaks (Part 2)
------------------------------------------------

- What happens if the parser doesn't find a valid parsing rule?

.. code-block:: python

    >>> parser.evaluate('abc = 123 and xyz = abc or abc = 99')
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
      File "pparse.py", line 14, in evaluate
        return self.parser.parse(rule, lexer)
      File "/home/kmtracey/.virtualenvs/present_ply/lib/python2.6/site-packages/ply/yacc.py", line 265, in parse
        return self.parseopt_notrack(input,lexer,debug,tracking,tokenfunc)
      File "/home/kmtracey/.virtualenvs/present_ply/lib/python2.6/site-packages/ply/yacc.py", line 1047, in parseopt_notrack
        tok = self.errorfunc(errtoken)
      File "pparse.py", line 17, in p_error
        raise SyntaxError('Syntax error in input: %s' % p)
    SyntaxError: Syntax error in input: LexToken(ITEMID,123,1,20)


"""Query grammar definition."""
import importlib
import pkgutil

from collections import namedtuple

import pyparsing as pp

from cumin import backends, CuminError


Backend = namedtuple('Backend', ['keyword', 'name', 'cls'])
""":py:func:`collections.namedtuple` that define a Backend object.

Keyword Arguments:
    keyword (str): The backend keyword to be used in the grammar.
    name (str): The backend name.
    cls (BaseQuery): The backend class object.
"""


def get_registered_backends():
    """Get a mapping of all the registered backends with their keyword.

    Returns:
        dict: A dictionary with a ``{keyword: Backend object}`` mapping for each available backend.

    Raises:
        cumin.CuminError: If unable to register a backend because the key is already used by another backend.

    """
    available_backends = {}
    backend_names = [name for _, name, ispkg in pkgutil.iter_modules(backends.__path__) if not ispkg]

    for name in backend_names:
        try:
            backend = importlib.import_module('cumin.backends.{backend}'.format(backend=name))
        except ImportError:
            continue  # Backend not available, are all dependencies installed?

        keyword = backend.GRAMMAR_PREFIX
        if keyword in available_backends:
            raise CuminError("Unable to register backend {name}, keyword '{key}' already registered: {backends}".format(
                name=name, key=keyword, backends=available_backends))

        available_backends[keyword] = Backend(name=name, keyword=keyword, cls=backend.query_class)

    return available_backends


REGISTERED_BACKENDS = get_registered_backends()
""":py:class:`dict`: Hold the dictionary of available backends generated at load time mapped by their keyword."""


def grammar():
    """Define the main multi-query grammar.

    Cumin provides a user-friendly generic query language that allows to combine the results of subqueries for multiple
    backends:

    * Each query part can be composed with the others using boolean operators ``and``, ``or``, ``and not``, ``xor``.
    * Multiple query parts can be grouped together with parentheses ``(``, ``)``.
    * Specific backend query ``I{backend-specific query syntax}``, where ``I`` is an identifier for the specific
      backend.
    * Alias replacement, according to aliases defined in the configuration file ``A:group1``.
    * The identifier ``A`` is reserved for the aliases replacement and cannot be used to identify a backend.
    * A complex query example: ``(D{host1 or host2} and (P{R:Class = Role::MyClass} and not A:group1)) or D{host3}``

    Backus-Naur form (BNF) of the grammar::

              <grammar> ::= <item> | <item> <boolean> <grammar>
                 <item> ::= <backend_query> | <alias> | "(" <grammar> ")"
        <backend_query> ::= <backend> "{" <query> "}"
                <alias> ::= A:<alias_name>
              <boolean> ::= "and not" | "and" | "xor" | "or"

    Given that the pyparsing library defines the grammar in a BNF-like style, for the details of the tokens not
    specified above check directly the source code.

    Returns:
        pyparsing.ParserElement: the grammar parser.

    """
    # Boolean operators
    boolean = (pp.CaselessKeyword('and not').leaveWhitespace() | pp.CaselessKeyword('and') |
               pp.CaselessKeyword('xor') | pp.CaselessKeyword('or'))('bool')

    # Parentheses
    lpar = pp.Literal('(')('open_subgroup')
    rpar = pp.Literal(')')('close_subgroup')

    # Backend query: P{PuppetDB specific query}
    query_start = pp.Combine(pp.oneOf(REGISTERED_BACKENDS.keys(), caseless=True)('backend') + pp.Literal('{'))
    query_end = pp.Literal('}')
    # Allow the backend specific query to use the end_query token as well, as long as it's in a quoted string
    # and fail if there is a query_start token before the first query_end is reached
    query = pp.SkipTo(query_end, ignore=pp.quotedString, failOn=query_start)('query')
    backend_query = pp.Combine(query_start + query + query_end)

    # Alias
    alias = pp.Combine(pp.CaselessKeyword('A') + ':' + pp.Word(pp.alphanums + '-_.+')('alias'))

    # Final grammar, see the docstring for its BNF based on the tokens defined above
    # Group are used to have an easy dictionary access to the parsed results
    full_grammar = pp.Forward()
    item = backend_query | alias | lpar + full_grammar + rpar
    full_grammar << pp.Group(item) + pp.ZeroOrMore(pp.Group(boolean + item))  # pylint: disable=expression-not-assigned

    return full_grammar

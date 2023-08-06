# -*- coding: utf-8 -*-
# :Project:   pg_query -- Serialization logic
# :Created:   mer 02 ago 2017 15:46:11 CEST
# :Author:    Lele Gaifax <lele@metapensiero.it>
# :License:   GNU General Public License version 3 or later
# :Copyright: © 2017 Lele Gaifax
#

from contextlib import contextmanager
from io import StringIO
from re import match

from .error import Error
from .node import Node, Scalar
from .keywords import RESERVED_KEYWORDS
from .parser import parse_plpgsql, parse_sql


NODE_PRINTERS = {}
"Registry of specialized printers, keyed by their `tag`."


class PrinterAlreadyPresentError(Error):
    "Exception raised trying to register another function for a tag already present."


def get_printer_for_node_tag(node_tag):
    "Get specific printer implementation for given `node_tag`."

    try:
        return NODE_PRINTERS[node_tag]
    except KeyError:
        raise NotImplementedError("Printer for node %r is not implemented yet"
                                  % node_tag)


def node_printer(node_tag, override=False):
    """Decorator to register a specific printer implementation for given `node_tag`.

    :param str node_tag: the node tag
    :param bool override: when ``True`` the function will be registered even if already present
    """

    def decorator(impl):
        if not override and node_tag in NODE_PRINTERS:
            raise PrinterAlreadyPresentError("A printer is already registered for tag %r"
                                             % node_tag)
        NODE_PRINTERS[node_tag] = impl
        return impl
    return decorator



class OutputStream(StringIO):
    "A stream that has a concept of a *pending separator* between consecutive writes."

    def __init__(self):
        super().__init__()
        self.pending_separator = False
        self.last_emitted_char = ' '

    def separator(self):
        """Possibly insert a single whitespace character before next output.

        When the last character written is not a space, set the `pending_separator` flag to
        ``True``: the next call to :meth:`write` will prepend a single whitespace to its
        argument if that begins with an alphanumeric character.
        """

        if not self.last_emitted_char.isspace():
            self.pending_separator = True

    def maybe_write_space(self, nextc=None, _special_chars=set("""_*+/-"'=<>$@""")):
        """Emit a space when needed.

        :param nextc: either None or the next character that will be written
        :return: the number of characters written to the stream

        If the last character written was not a space, and `nextc` is either ``None`` or
        a *special character*, then emit a single whitespace.
        """

        if not self.last_emitted_char.isspace():
            if nextc is None or nextc.isalnum() or nextc in _special_chars:
                return self.write(' ')
        return 0

    def write(self, s):
        """Emit string `s`.

        :param str s: the string to emit
        :return: the number of characters written to the stream

        When `s` is not empty and `pending_separator` is ``True`` and the first character of
        `s` is alphanumeric, emit a single whitespace before writing out `s` and then reset
        `pending_separator` to ``False``.
        """

        count = 0
        if s:
            if self.pending_separator:
                if s != ' ':
                    count = self.maybe_write_space(s[0])
                self.pending_separator = False
            count += super().write(s)
            self.last_emitted_char = s[-1]

        return count

    def writes(self, s):
        "Shortcut for ``self.write(s); self.separator()``."

        count = self.write(s)
        self.separator()
        return count

    def swrite(self, s):
        "Shortcut for ``self.maybe_write_space(s[0]); self.write(s);``."

        count = self.maybe_write_space(s[0])
        return count + self.write(s)

    def swrites(self, s):
        "Shortcut for ``self.swrite(s); self.separator()``."

        count = self.swrite(s)
        self.separator()
        return count


class RawStream(OutputStream):
    """Basic SQL parse tree writer.

    :param int expression_level: start the stream with the given expression level depth, 0 by
                                 default
    :param bool separate_statements: ``True`` by default, tells whether multiple
                                     statements shall be separated by an empty line

    This augments :class:`OutputStream` and implements the basic machinery needed to serialize
    the *parse tree* produced by :func:`~.parser.parse_sql()` back to a textual representation,
    without any adornment.
    """

    def __init__(self, expression_level=0, **options):
        super().__init__()
        if 'separate_statements' not in options:
            options['separate_statements'] = True
        self.options = options
        self.expression_level = expression_level
        self.current_column = 0

    def __call__(self, sql, plpgsql=False):
        """Main entry point: execute :meth:`print` on each statement in `sql`.

        :param sql: either the source SQL in textual form, or a :class:`~.node.Node` instance
        :param bool plpgsql: whether `sql` is really a ``plpgsql`` statement
        :returns: a string with the equivalent SQL obtained by serializing the syntax tree
        """

        if isinstance(sql, str):
            sql = Node(parse_plpgsql(sql) if plpgsql else parse_sql(sql))

        first = True
        for statement in sql:
            if first:
                first = False
            else:
                self.write(';')
                self.newline()
                if self.options['separate_statements']:
                    self.newline()
            self.print(statement)
        return self.getvalue()

    def concat_nodes(self, nodes, sep=' ', are_names=False):
        """Concatenate given `nodes`, using `sep` as the separator.

        :param scalars: a sequence of nodes
        :param str sep: the separator between them
        :param bool are_names: whether the nodes are actually *names*, which possibly require
                               to be enclosed between double-quotes
        :returns: a string

        Use a temporary :class:`RawStream` instance to print the list of nodes and return the
        result.
        """

        rawstream = RawStream(expression_level=self.expression_level)
        rawstream.print_list(nodes, sep, are_names=are_names, standalone_items=False)
        return rawstream.getvalue()

    def dedent(self):
        "Do nothing, shall be overridden by the prettifier subclass."

    def indent(self, amount=0, relative=True):
        "Do nothing, shall be overridden by the prettifier subclass."

    def maybe_double_quote_name(self, scalar):
        """Double-quote the given `scalar` if needed.

        :param scalar: a :class:`~.node.Scalar` string instance
        :return: the string value of the scalar, possibly double quoted

        The `scalar` represent a name of a column/table/alias: when any of its characters
        is not a lower case letter, a digit or underscore, it must be double quoted.
        """

        assert isinstance(scalar, Scalar) and isinstance(scalar.value, str)
        s = scalar.value
        if not match(r'[a-z_][a-z0-9_]*$', s) or s in RESERVED_KEYWORDS:
            return '"%s"' % s
        else:
            return s

    def newline(self):
        "Emit a single whitespace, shall be overridden by the prettifier subclass."

        self.separator()

    @contextmanager
    def push_indent(self, amount=0, relative=True):
        "Create a no-op context manager, shall be overridden by the prettifier subclass."

        yield

    def _print_items(self, items, sep, newline, are_names=False):
        first = True
        for item in items:
            if first:
                first = False
            else:
                if not are_names:
                    if newline:
                        self.newline()
                self.write(sep)
                if not are_names:
                    self.write(' ')
            self.print(item, is_name=are_names)

    def _print_scalar(self, node, is_name):
        value = self.maybe_double_quote_name(node) if is_name else str(node.value)
        self.write(value)

    def print(self, node, is_name=False):
        """Lookup the specific printer for the given `node` and execute it."""

        if isinstance(node, Scalar):
            self._print_scalar(node, is_name)
        else:
            printer = get_printer_for_node_tag(node.node_tag)
            if is_name and node.node_tag == 'String':
                printer(node, self, is_name=True)
            else:
                printer(node, self)
            self.separator()

    @contextmanager
    def expression(self):
        self.expression_level += 1
        if self.expression_level > 1:
            self.write('(')
        yield
        if self.expression_level > 1:
            self.write(')')
        self.expression_level -= 1

    def print_list(self, nodes, sep=',', relative_indent=None, standalone_items=None,
                   are_names=False):
        """Execute :meth:`print` on all the `items`, separating them with `sep`.

        :param nodes: a sequence of :class:`~.node.Node` instances
        :param str sep: the separator between them
        :param bool relative_indent: if given, the relative amount of indentation to apply
                                     before the first item, by default computed automatically
                                     from the length of the separator `sep`
        :param bool standalone_items: whether a newline will be emitted before each item
        :param bool are_names: whether the nodes are actually *names*, which possibly require
                               to be enclosed between double-quotes
        """

        if relative_indent is None:
            relative_indent = -(len(sep) + 1)

        if standalone_items is None:
            standalone_items = not all(isinstance(n, Node) and n.node_tag == 'A_Const'
                                       for n in nodes)

        with self.push_indent(relative_indent):
            self._print_items(nodes, sep, standalone_items, are_names=are_names)

    def print_lists(self, lists, sep=',', relative_indent=None, standalone_items=None,
                    are_names=False, sublist_open='(', sublist_close=')', sublist_sep=',',
                    sublist_relative_indent=None):
        """Execute :meth:`print_list` on all the `lists` items.

        :param lists: a sequence of sequences of :class:`~.node.Node` instances
        :param str sep: passed as is to :meth:`print_list`
        :param bool relative_indent: passed as is to :meth:`print_list`
        :param bool standalone_items: passed as is to :meth:`print_list`
        :param bool are_names: passed as is to :meth:`print_list`
        :param sublist_open: the string that will be emitted before each sublist
        :param sublist_close: the string that will be emitted after each sublist
        :param str sublist_sep: the separator between them each sublist
        :param bool sublist_relative_indent: if given, the relative amount of indentation to
                                             apply before the first sublist, by default
                                             computed automatically from the length of the
                                             separator `sublist_sep`
        """

        if sublist_relative_indent is None:
            sublist_relative_indent = -(len(sublist_sep) + 2)

        self.write(sublist_open)
        with self.push_indent(sublist_relative_indent):
            first = True
            for lst in lists:
                if first:
                    first = False
                else:
                    self.newline()
                    self.write(sublist_sep)
                    self.write(' ')
                    self.write(sublist_open)
                self.print_list(lst, sep, relative_indent, standalone_items, are_names)
                self.write(sublist_close)


class IndentedStream(RawStream):
    """Indented SQL parse tree writer.

    :param bool align_expression_operands: whether to vertically align the operands of an
                                           expression
    :param int compact_lists_margin: an integer value that, if given, is used to print
                                     lists on a single line, when they do not exceed
                                     the given margin on the right
    :param \*\*options: other options accepted by :class:`Serializer`

    This augments :class:`RawStream` to emit a prettified representation of a *parse tree*.
    """

    def __init__(self, **options):
        if 'align_expression_operands' not in options:
            options['align_expression_operands'] = True
        if 'compact_lists_margin' not in options:
            options['compact_lists_margin'] = None
        super().__init__(**options)
        self.current_indent = 0
        self.indentation_stack = []

    def dedent(self):
        "Pop the indentation level from the stack and set `current_indent` to that."

        self.current_indent = self.indentation_stack.pop()

    def indent(self, amount=0, relative=True):
        """Push current indentation level to the stack, then set it adding `amount` to the
        `current_column` if `relative` is ``True`` otherwise to `current_indent`.
        """

        self.indentation_stack.append(self.current_indent)
        base_indent = (self.current_column if relative else self.current_indent)
        assert base_indent + amount >= 0
        self.current_indent = base_indent + amount

    @contextmanager
    def push_indent(self, amount=0, relative=True):
        """Create a context manager that calls :meth:`indent` and :meth:`dedent` around a block
        of code.

        This is just an helper to simplify code that adjust the indentation level:

        .. code-block:: python

          with output.push_indent(4):
              # code that emits something with the new indentation
        """

        if self.pending_separator and relative:
            amount += 1
        if self.current_column == 0 and relative:
            amount += self.current_indent
        self.indent(amount, relative)
        yield
        self.dedent()

    def newline(self):
        "Emit a newline."

        self.write('\n')

    def print_list(self, nodes, sep=',', relative_indent=None, standalone_items=None,
                   are_names=False):
        """Execute :meth:`print` on all the `items`, separating them with `sep`.

        :param nodes: a sequence of :class:`~.node.Node` instances
        :param str sep: the separator between them
        :param bool relative_indent: if given, the relative amount of indentation to apply
                                     before the first item, by default computed automatically
                                     from the length of the separator `sep`
        :param bool standalone_items: whether a newline will be emitted before each item
        :param bool are_names: whether the nodes are actually *names*, which possibly require
                               to be enclosed between double-quotes
        """

        if standalone_items is None:
            if self.options['compact_lists_margin']:
                rawlist = self.concat_nodes(nodes, sep, are_names)
                if self.current_column + len(rawlist) < self.options['compact_lists_margin']:
                    self.write(rawlist)
                    return

            standalone_items = not all(
                isinstance(n, Node) and n.node_tag in ('A_Const', 'SetToDefault')
                for n in nodes)

        if (len(nodes) > 1
            and len(sep) > 1
            and relative_indent is None
            and not are_names
            and standalone_items):
            self.write(' '*(len(sep) + 1)) # separator added automatically

        super().print_list(nodes, sep, relative_indent, standalone_items, are_names)

    def write(self, s):
        """Write string `s` to the stream, adjusting the `current_column` accordingly.

        :param str s: the string to emit
        :return: the number of characters written to the stream

        If `s` is a newline character (``\\n``) set `current_column` to 0. Otherwise when
        `current_column` is 0 and `current_indent` is not emit a number of whitespaces *before*
        emitting `s`, to indent it as expected.
        """

        if s and s != '\n' and self.current_column == 0 and self.current_indent > 0:
            self.current_column = super().write(' ' * self.current_indent)

        count = super().write(s)
        if s == '\n':
            self.current_column = 0
        else:
            self.current_column += count

        return count

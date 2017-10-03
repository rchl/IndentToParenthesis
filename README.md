Indent to parenthesis Sublime Text package
==========================================

As I was dissatisfied with Sublime's `indent_to_bracket` option, I've created my own implementation that behaves in a smarter way.

The general idea is to indent arguments in a function call to the opening bracket so that:

```
function Foo(arg1,<enter>
```

aligns caret following way:

```
function Foo(arg1,
             |
```

*Caveat*: Currently this package only works when using spaces for indentation (`translate_tabs_to_spaces` setting is `true`). I don't code with tabs so I'm probably not gonna spend time to make it work with tabs. If you care, please submit a pull request.

Why is it better than built-in functionality?
=============================================

For example, with code like this:

```
function(arg1, arg2) {}
```

when wanting to break the arguments into two lines (because line is too long, for example), one would put the caret after the comma and press enter.

Built-in functionality would break them incorrectly, leaving this result:

```
function(arg1,
 arg2) {}
```

while this package will align it correctly:

```
function(arg1,
         arg2) {}
```

Built-in functionality aligns code properly when placing cursor after the space (that follows the comma), but then it leaves trailing space on the line. This package handles both cases properly.

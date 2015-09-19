Indent to parenthesis Sublime Text plugin
=========================================

As I was dissatisfied with Sublime's indent_to_bracket option, I've created my own implementation that behaves in a smarter way. I don't remember now what makes it smarter but something does ;).

The general idea is to indent arguments in a function call to the opening bracket so that:

```
function Foo(arg1,<enter>
```

aligns caret following way:

```
function Foo(arg1,
             |
```

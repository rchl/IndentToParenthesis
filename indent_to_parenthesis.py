import sublime
import sublime_plugin


class IndentToParenthesisCommand(sublime_plugin.TextCommand):
  def run(self, edit):
    view = self.view
    selections = view.sel()
    for selection in selections:
      line_to_cursor = view.substr(
          sublime.Region(view.line(selection).a, selection.b))
      column = self.find_last_unmatched_paren(line_to_cursor)
      if column:
        view.insert(edit, selection.a, '\n%s' % (' ' * column))
      else:
        # Would be better to run built in 'insert' command as it has some
        # heuristics also, but that would trigger for all selections so can't do.
        view.insert(edit, selection.a, '\n')

  def find_last_unmatched_paren(self, line):
    line_length = len(line)
    closing_paren = 0
    while line_length > 0:
      line_length -= 1
      char = line[line_length]
      if char is ')':
        closing_paren += 1
      elif char is '(':
        if closing_paren > 0:
          closing_paren -= 1
        else:
          # Get index beneath the opening parenthesis.
          return line_length + 1

    return None

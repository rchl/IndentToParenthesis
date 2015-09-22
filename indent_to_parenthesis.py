import sublime
import sublime_plugin


class IndentToParenthesisCommand(sublime_plugin.TextCommand):
  def run(self, edit):
    view = self.view
    selections = view.sel()
    for selection in selections:
      line_upto_cursor = view.substr(
          sublime.Region(view.line(selection).a, selection.b))
      column = self.find_last_unmatched_open_paren(line_upto_cursor)
      whitespace_region = self.expand_to_whitespace(selection.a)
      view.erase(edit, whitespace_region)
      if column:
        view.insert(edit, whitespace_region.a, '\n%s' % (' ' * column))
      else:
        # Would be better to run built in 'insert' command as it does some
        # heuristics, but that would trigger for all selections so can't do.
        view.insert(edit, whitespace_region.a, '\n')

  def find_last_unmatched_open_paren(self, line):
    '''Returns offset of the last unmatched opening parenthesis on the line'''
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

  def expand_to_whitespace(self, point):
    '''Returns region with all spaces matched before and after the point'''
    view = self.view
    line_upto_point = view.substr(sublime.Region(view.line(point).a, point))
    whitespace_to_eat = 0
    last_non_ws_index = len(line_upto_point)
    while last_non_ws_index > 0:
      last_non_ws_index -= 1
      char = line_upto_point[last_non_ws_index]
      if char != ' ':
        break
      whitespace_to_eat += 1

    return view.find(' *', point - whitespace_to_eat)

import sublime
import sublime_plugin


class IndentToParenthesisCommand(sublime_plugin.TextCommand):
  def run(self, edit):
    view = self.view
    for selection in view.sel():
      view.erase(edit, selection)
    for selection in view.sel():
      line_upto_cursor = view.substr(sublime.Region(view.line(selection).begin(), selection.end()))
      param_column = self.find_last_unmatched_open_paren(line_upto_cursor)
      whitespace_region = self.expand_to_whitespace(selection.begin())
      view.erase(edit, whitespace_region)
      if param_column:
        view.insert(edit, whitespace_region.begin(), '\n%s' % (' ' * param_column))
      else:
        view.run_command('insert', {'characters': '\n'})

  def find_last_unmatched_open_paren(self, line):
    '''Returns offset of the last unmatched opening parenthesis on the line'''
    line_length = len(line)
    closing_paren = 0
    while line_length > 0:
      line_length -= 1
      char = line[line_length]
      if char == ')':
        closing_paren += 1
      elif char == '(':
        if closing_paren > 0:
          closing_paren -= 1
        else:
          # Get index beneath the opening parenthesis.
          return line_length + 1

    return None

  def expand_to_whitespace(self, point):
    '''Returns region with all spaces matched before and after the point'''
    view = self.view
    line_upto_point = view.substr(sublime.Region(view.line(point).begin(), point))
    whitespace_to_eat = 0
    last_non_ws_index = len(line_upto_point)
    while last_non_ws_index > 0:
      last_non_ws_index -= 1
      char = line_upto_point[last_non_ws_index]
      if char != ' ':
        break
      whitespace_to_eat += 1

    return view.find(' *', point - whitespace_to_eat)

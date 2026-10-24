import sublime
import sublime_plugin


class IndentToParenthesisCommand(sublime_plugin.TextCommand):
  def run(self, edit):
    view = self.view
    for selection in view.sel():
      view.erase(edit, selection)
    for selection in view.sel():
      line_region_upto_cursor = sublime.Region(view.line(selection).begin(), selection.end())
      param_column = self.find_last_unmatched_open_paren(line_region_upto_cursor)
      whitespace_region = self.expand_to_whitespace(selection.begin())
      view.erase(edit, whitespace_region)
      if param_column is not None:
        view.insert(edit, whitespace_region.begin(), '\n%s' % (' ' * param_column))
      else:
        view.run_command('insert', {'characters': '\n'})

  def find_last_unmatched_open_paren(self, region):
    """Return offset of the last unmatched opening parenthesis in the region.

    Parentheses in strings and comments are ignored, except in the string or
    comment that the end of the region (the cursor) is in.
    """
    view = self.view
    line = view.substr(region)
    ignored_selector = 'string, comment'
    in_cursor_token = view.match_selector(region.end(), ignored_selector)
    line_length = len(line)
    closing_paren = 0
    while line_length > 0:
      line_length -= 1
      char = line[line_length]
      point = region.begin() + line_length
      if not view.match_selector(point, ignored_selector):
        in_cursor_token = False
      elif not in_cursor_token:
        continue
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
    """Return region with all spaces matched before and after the point."""
    view = self.view
    line = view.line(point)
    before = view.substr(sublime.Region(line.begin(), point))
    after = view.substr(sublime.Region(point, line.end()))
    start = line.begin() + len(before.rstrip(' '))
    end = line.end() - len(after.lstrip(' '))
    return sublime.Region(start, end)

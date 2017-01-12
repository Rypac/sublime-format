import sublime


def settings():
    return sublime.load_settings('Format.sublime-settings')


def save_settings():
    return sublime.save_settings('Format.sublime-settings')


def settings_for(formatter):
    return settings().get(formatter) or {}

def set_language(link, lang_flag, lang='en'):
    pos = link.find(lang_flag)
    if pos == -1:
        return link + '?' + lang_flag + '=' + lang
    pos += len(lang_flag) + 1
    assert link[pos - 1] == '='
    return link[:pos] + lang

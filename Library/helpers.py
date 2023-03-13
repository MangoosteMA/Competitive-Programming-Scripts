def set_language(link, lang_flag, lang='en'):
    pos = link.find(lang_flag)
    if pos == -1:
        return link + '?' + lang_flag + '=' + lang
    pos += len(lang_flag) + 1
    assert link[pos - 1] == '='
    return link[:pos] + lang


def determine_system(link):
    if link.find('codeforces') != -1:
        return 'codeforces'
    elif link.find('atcoder') != -1:
        return 'atcoder'
    else:
        return None


def colored(text, red, green, blue):
    return f"\033[38;2;{red};{green};{blue}m{text}\033[0m"


def get_html_code(url, use_selenium=False):
    if not use_selenium:
        import requests
        result = requests.get(url)
        return None if result.status_code != 200 else result.text
    else:
        from selenium import webdriver
        print('Creating driver.')
        driver = webdriver.Chrome()
        print('Requesting data.')
        driver.get(url)
        html_code = driver.page_source
        driver.close()
        print('Got html code!')
        return html_code

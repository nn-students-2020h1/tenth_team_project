import re
import logging


logger = logging.getLogger(__name__)

class UrlParser:
    def __init__(self, string: str = None, strings: list = None):
        assert (string or strings) and (string is None or strings is None)
        self.strings = [string] if string else strings
        self.one_string = True if string else False
        self.url_list = list()

    @classmethod
    def http_add_space(cls, string):
        string = re.sub("http://", " http://", string)
        string = re.sub("https://", " https://", string)
        return string

    @classmethod
    def split_by_space(cls, string):
        return re.findall(r"[\s]*([\S]+)[\s]*", string)

    def dirty_parse(self):
        self.strings = [self.http_add_space(string) for string in self.strings]
        self.strings = [word for string in self.strings for word in self.split_by_space(string)]
        self.parse()
        return self.url_list

    @classmethod
    def get_url_protocol(cls, url: str, default="http"):
        result = re.findall(r"(http[s]?)://", url)
        return result[0] if result else default

    @classmethod
    def http_replace(cls, string):
        return re.sub(r"http[s]?://", "", string)

    @classmethod
    def get_url_domain(cls, url: str):
        if re.findall(r"http[s]?", url):
            result = re.findall(r"http[s]?://([a-zA-Zа-яА-ЯёЁ0-9\-]+[.][a-zA-Zа-яА-ЯёЁ0-9\-.]+)", url)
        else:
            result = re.findall(r"[a-zA-Zа-яА-ЯёЁ0-9\-]+[.][a-zA-Zа-яА-ЯёЁ0-9\-.]+", url)
        return result[0] if result else None
        # dl = r"[a-zA-Zа-яА-ЯёЁ0-9\-]+"  # domain letters
        # ndl = r"[^a-zA-Zа-яА-ЯёЁ0-9\-]*"  # not domain letters
        # return (re.findall(r"[a-zA-Zа-яА-ЯёЁ0-9\-]+[.][a-zA-Zа-яА-ЯёЁ0-9\-.]+", url) + [None])[0]
        # return (re.findall(r"[a-zA-Zа-яА-ЯёЁ0-9\-.{1,}]+", url) + [None])
        # return (re.findall(r"^[.]*"+ndl+r"("+dl+r"\."+dl+r")[\s]*$", url) + [None])[0]
        # return (re.findall(r"^"+ndl+r"("+dl+r"\."+dl+")[\s]*$", url) + [None])[0]
        # return (re.findall(r"^[\s\]*" + f'({dl}.{dl})' + r"[\s]*$", url) + [None])[0]

    @classmethod
    def get_url_page(cls, url: str, domain: str = None):
        domain = cls.get_url_domain(url) if domain is None else domain
        assert domain is not None
        result = re.findall(domain + r"[/]?(\S*)\s*$", url)
        return result[0] if result else ""

    def parse(self):
        for string in self.strings:
            protocol = self.get_url_protocol(string)
            domain = self.get_url_domain(string)
            if domain:
                page = self.get_url_page(domain)
                url = f"{protocol}://{domain}/{page}"
                self.url_list.append(url)
            logger.debug(f"{string} -> {url}")

        self.url_list = list(dict.fromkeys(self.url_list).keys())
        return self.url_list
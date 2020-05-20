import unittest
import re
from url_parser import UrlParser

get_protocol = UrlParser.get_url_protocol
http_replace = UrlParser.http_replace
http_add_space = UrlParser.http_add_space
split_by_space = UrlParser.split_by_space
url_domain = UrlParser.get_url_domain
url_page = UrlParser.get_url_page


class TestAuxiliaryTools(unittest.TestCase):
    # @unittest.skip
    def test_001_regex_http(self):
        self.assertEqual(get_protocol('http://gok-olimp.ru'), "http")
        self.assertEqual(get_protocol('https://gok-olimp.ru'), "https")
        self.assertEqual(get_protocol('gok-olimp.ru'), "http")
        self.assertEqual(get_protocol('hellohttps.com'), "http")

    # @unittest.skip
    def test_002_regex_http_replace(self):
        self.assertEqual(http_replace('http://gok-olimp.ru'), "gok-olimp.ru")
        self.assertEqual(http_replace('https://gok-olimp.ru'), "gok-olimp.ru")
        self.assertEqual(http_replace('gok-olimp.ru'), "gok-olimp.ru")
        self.assertEqual(http_replace('hellohttp.com'), "hellohttp.com")

    # @unittest.skip
    def test_003_regex_http_add_space(self):
        self.assertEqual(http_add_space('http://gok-olimp.ru'), " http://gok-olimp.ru")

    # @unittest.skip
    def test_004_split(self):
        self.assertEqual(split_by_space("gok-olimp.ru"), ["gok-olimp.ru"])
        self.assertEqual(split_by_space("gok-olimp.ru gok-olimp.ru"), ["gok-olimp.ru", "gok-olimp.ru"])
        self.assertEqual(split_by_space("  gok-olimp.ru"), ["gok-olimp.ru"])


class MainFunctional(unittest.TestCase):
    def test_010_domain_basic(self):
        self.assertEqual(url_domain(" gok-olimp.ru "), "gok-olimp.ru")

    def test_011_domain_basic(self):
        self.assertIsNone(url_domain("dbhshfbsdhbfsdh"))

    def test_012_domain_basic(self):
        self.assertIsNone(url_domain("j sdfnhjb sdfb"))

    def test_013_domain_basic(self):
        self.assertEqual(url_domain('site:gok-olimp.ru'), "gok-olimp.ru")

    def test_014_domain_basic(self):
        self.assertIsNone(url_domain("http://gok_olimp.ru"))

    def test_020_domain_http(self):
        self.assertEqual(url_domain('http://gok-olimp.ru'), "gok-olimp.ru")

    def test_030_domain_page(self):
        self.assertEqual(url_domain('http://gok-olimp.ru/test/index.html'), "gok-olimp.ru")

    def test_040_domain_subdomain(self):
        self.assertEqual(url_domain('http://www.gok-olimp.ru'), "www.gok-olimp.ru")

    def test_110_page_basic(self):
        self.assertEqual(url_page('http://www.gok-olimp.ru'), '/')

    def test_111_page_basic(self):
        self.assertEqual(url_page('http://gok-olimp.ru/test/index.html'), "/test/index.html")

    def test_111_with_space_page_basic(self):
        self.assertEqual(url_page('http://gok-olimp.ru/test/index.html  '), "/test/index.html")

    def test_112_page_basic(self):
        self.assertRaises(Exception, url_page, 'http://gok')  # AssertionError,
        # self.assertIsNone()

    def test_120_page_additional_argv(self):
        self.assertEqual(url_page('http://www.gok-olimp.ru', 'www.gok-olimp.ru'), '/')



    # def test_basic(self):
    #     self.assertEqual(url_parser("http://google.com/"), "http://google.com/")
    #
    # def test_http_missing(self):
    #     self.assertEqual(url_parser("google.com/"), "http://google.com/")
    #     self.assertEqual(url_parser("http://google.com/"), "http://google.com/")
    #     self.assertEqual(url_parser("https://google.com/"), "https://google.com/")
    #
    # def test_sub_domain(self):
    #     self.assertEqual(url_parser("http://www.google.com/"), "http://www.google.com/")
    #     self.assertEqual(url_parser("http://www.yahoo.com.ru/"), "http://www.yahoo.com.ru/")
    #
    # def test_url_page(self):
    #     self.assertEqual(url_parser("http://google.com/index.html"), "http://google.com/index.html")
    #     self.assertEqual(url_parser("http://google.com/test/index.html"), "http://google.com/test/index.html")
    #
    # def test_end_slash_missing(self):
    #     self.assertEqual(url_parser("http://google.com"), "http://google.com/")

    # def test_several_urls(self):
    #     urls = UrlCleaner("http://dot.tk https://yandex.ru http://mail.ru/main/index.html")
    #     urls.split_string()
    #     self.assertEqual(
    #         urls.list(),
    #         [""]
    #     )
    #     correct = ["http://google.com/", "http://yandex.ru/"]
    #     strings = [
    #         "http://google.com/ http://yandex.ru/",
    #         "google.com/ yandex.ru/",
    #         "http://google.comhttp://yandex.ru/",
    #         "http://google.comhttp://yandex.ru",
    #         "google.com/yandex.ru/",
    #         "http://google.comhttp://yandex.ru/",
    #         "http://google.comhttp://yandex.ru",
    #     ]
    #     for i in range(len(strings)):
    #         self.assertEqual(result(strings[i]), correct)

    # def test_find_in_trash(self):
    #     with_trash = [
    #         [".http://google.com/"],
    #         ["trashhttp://google.com/"],
    #         ["_http://google.com/"],
    #         [" http://google.com/ "],
    #     ]
    #     for i in range(len(with_trash)):
    #         self.assertEqual(with_trash[i], ["http://google.com/"])
    #

    #
    #
    # def test_incorrect_url(self):
    #     self.assertEqual(url_formatter([""]), [])
    #     self.assertEqual(url_formatter(["http://google/"]), [])
    #     self.assertEqual(url_formatter(["https://google/"]), [])
    #     self.assertEqual(url_formatter(["google/"]), [])
    #
    #
    # def test_multi_url_str(self):
    #     pass
    #
    #
    # def test_incorrect_url1(self):
    #     pass
    #     url_list = [
    #         "https://google.com/",
    #         "b",
    #         "   ",
    #         ""
    #         "hello world",
    #         "http://freenom.com/",
    #         "hello,world!"
    #     ]
    #     # expected = ["https://google.com", "http://yandex.ru", "http://freenom.com"]
    #
    # def test_many_url_in_str(self):
    #     pass

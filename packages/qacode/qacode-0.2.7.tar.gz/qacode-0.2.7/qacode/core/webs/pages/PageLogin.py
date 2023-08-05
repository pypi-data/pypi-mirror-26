# -*- coding: utf-8 -*-
# pylint: disable=too-many-arguments
"""Package qacode.core.webs.pages"""


from qacode.core.webs.pages.PageBase import PageBase
from qacode.core.exceptions.PageException import PageException
from selenium.webdriver.common.by import By


class PageLogin(PageBase):
    """Inherit PageBase class with login and valitation methods"""

    txt_username = None
    txt_password = None
    btn_login = None

    def __init__(self, bot, url, by=By.CSS_SELECTOR, selectors=None,
                 go_url=True):
        super(PageLogin, self).__init__(bot, url, by, selectors, go_url)
        if selectors is None:
            raise PageException(message='Param selectors can\'t be None')
        if len(selectors) != 3:
            raise PageException(
                message='Can\'t instance PageLogin elements '
                'if not have 3 selectors'
            )
        self.txt_username = self.elements[0]
        self.txt_password = self.elements[1]
        self.btn_login = self.elements[2]

    def login(self, username, password, is_login_now=True):
        """Allows to do login on a page loaded throught selenium"""
        error_template = "Can't '{}' '{}' on field '{}' for class PageLogin"
        error_username = error_template.format(
            "send_keys", username, "txt_username")
        error_password = error_template.format(
            "send_keys", username, "txt_username")
        error_btn = error_template.format(
            "click", '', "btn_login")
        try:
            self.txt_username.send_keys(username)
        except Exception as err:
            raise PageException(err=err, message=error_username)
        try:
            self.txt_password.send_keys(password)
        except Exception as err:
            raise PageException(err=err, message=error_password)
        if is_login_now:
            try:
                self.btn_login.click()
            except Exception as err:
                raise PageException(err=err, message=error_btn)

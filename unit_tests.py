#!/usr/bin/python
# -*- coding: utf-8 -*-

import unittest
from faker import Faker
from bs4 import BeautifulSoup
from json import loads

from application.app import create_app
from application.config import (instance_config,
                                datastore_config as ds_config,
                                verbiage_config as v_config)
from application.config.password import password_config as p_config

from flask import session


class HNSTestCase(unittest.TestCase):
    parser = 'html.parser'  # Beautiful Soup HTML Parser
    admin_username = 'rickyadmin'
    admin_username_2 = 'asaadmin'
    admin_password = 'abc123'
    admin_password_2 = 'ames'
    admin_first_name = 'Ricky'
    admin_last_name = 'Whitaker'
    admin_email = 'ricky@hns.com'
    base_username = 'ricky'
    base_password = 'abc123'
    base_first_name = 'Ricky'
    base_last_name = 'Whitaker'
    base_email = 'ricky.whitaker@undeadcodersociety.com'
    base_username_2 = 'asa'
    base_password_2 = 'ames'
    msgs = {'login_required': 'please log in to access this page'}
    myFactory = Faker()

    def find_csrf_token(self, data):
        soup = BeautifulSoup(data, self.parser)
        csrf_token = soup.find(id='csrf_token').attrs['value']
        return csrf_token

    def setUp(self):
        from render_db import init_db

        db_creation = init_db()
        self.app = create_app([instance_config]).test_client()
        self.datastore = self.app.application.extensions['security'].datastore
        assert db_creation == 0

    """##########################################################
    # TEST MAIN BP
    ##########################################################"""

    def test_homepage(self):
        rv = self.app.get('/')
        assert rv._status_code == 200

    def test_staff_page(self):
        rv = self.app.get('/staff/')
        assert rv._status_code == 200

    def test_first_visit_page(self):
        rv = self.app.get('/first-visit/')
        assert rv._status_code == 200

    def test_faq_page(self):
        rv = self.app.get('/faq/')
        assert rv._status_code == 200

    def test_contact(self):
        rv = self.app.get('/contact/')
        assert rv._status_code == 200

    #############################################################
    # SERVICES SUB-ROUTE
    #############################################################

    def test_services_in_office_page(self):
        rv = self.app.get('/services/in-office-services/')
        assert rv._status_code == 200

    def test_services_crossfiber_corrective_muscle_therapy_page(self):
        rv = self.app.get('/services/crossfiber-corrective-muscle-therapy/')
        assert rv._status_code == 200

    def test_services_event_page(self):
        rv = self.app.get('/services/event-services/')
        assert rv._status_code == 200

    def test_services_classes_page(self):
        rv = self.app.get('/services/classes/')
        assert rv._status_code == 200

    def test_services_booking_policies_page(self):
        rv = self.app.get('/services/booking-policies/')
        assert rv._status_code == 200

    #############################################################
    # TEST BOOKING
    #############################################################

    def test_booking(self):
        rv = self.app.get('/book/')
        assert rv._status_code == 200

    #############################################################
    # TEST SHOPPING
    #############################################################

    def test_shopping(self):
        rv = self.app.get('/shop/')
        assert rv._status_code == 200

    def test_shopping_cart(self):
        rv = self.app.get('/shopping-cart/')
        assert rv._status_code == 200

    def test_gift_certificate(self):
        rv = self.app.get('/gift-certificates/')
        assert rv._status_code == 200

    """##########################################################
    # TEST LOGIN BP
    ##########################################################"""

    #############################################################
    # TEST LOGIN
    #############################################################

    def login(self, username, password):
        rv = self.app.get('/login/')
        soup = BeautifulSoup(rv.data, self.parser)
        csrf_token = soup.find(id='csrf_token').attrs['value']
        return self.app.post('/login/', data=dict(username=username,
                                                  password=password,
                                                  csrf_token=csrf_token),
                             follow_redirects=True)

    def login_admin(self, username, password):
        rv = self.app.get('/admin/login/')
        soup = BeautifulSoup(rv.data, self.parser)
        csrf_token = soup.find(id='csrf_token').attrs['value']
        return self.app.post('/admin/login/', data=dict(username=username,
                                                        password=password,
                                                        csrf_token=csrf_token),
                             follow_redirects=True)

    def logout(self):
        return self.app.get('/logout/', follow_redirects=True)

    def confirm_admin_user_login(self, rv):
        soup = BeautifulSoup(rv.data, self.parser)
        self.assertTrue(soup.title.contents[0].lower() == 'heart & sole massage')

    def test_admin_login(self):
        rv = self.login_admin(self.admin_username, self.admin_password)
        self.confirm_admin_user_login(rv)

    def confirm_user_login(self, rv):
        soup = BeautifulSoup(rv.data, self.parser)
        self.assertTrue(self.base_username.lower() in soup)

    def test_user_login(self):
        rv = self.login(self.base_username, self.base_password)
        self.confirm_user_login(rv)

    def test_login_success_session(self):
        """Successfull login should put user_name in session"""
        with self.app as c:
            rv = self.login_admin(self.admin_username, self.admin_password)
            self.assertTrue('user_id' in session)

    def test_logout_success(self):
        """Successfull logout should remove user-name from session"""
        with self.app as c:
            self.login_admin(self.admin_username, self.admin_password)
            rv = self.logout()
            self.assertTrue('user_id' not in session)

    def test_login_failed_bad_password(self):
        """Failed Logins with bad password should display failure message"""
        rv = self.login_admin(self.admin_username, 'badpassword')
        self.assertTrue(b'invalid password' in rv.data.lower())

    def test_login_failed_bad_username(self):
        """Failed Logins with bad username should display failure message"""
        rv = self.login_admin('badusername', 'badpassword')
        self.assertTrue(b'specified user does not exist' in rv.data.lower())

    #############################################################
    # TEST REGISTRATION
    #############################################################
    def register(self, password, confirm_password, first_name, last_name, email):
        rv = self.app.get('/register/')
        csrf_token = self.find_csrf_token(rv.data)

        return self.app.post('/register/', data=dict(password=password,
                                                     confirm_password=confirm_password,
                                                     first_name=first_name,
                                                     last_name=last_name,
                                                     email=email,
                                                     csrf_token=csrf_token),
                             follow_redirects=True)

    def test_user_registration(self):
        self.register(password='SomeNewPassword',
                      confirm_password='SomeNewPassword',
                      first_name='New',
                      last_name='User',
                      email='moo@cow.com')

        if self.app.application.testing:
            user = self.datastore.find_user(email='moo@cow.com')
            self.assertTrue(user is not None)
            self.assertEqual(user.first_name, 'New')
            self.assertEqual(user.last_name, 'User')

    def test_duplicate_user_registration(self):
        rv = self.register(password='SomeNewPassword',
                           confirm_password='SomeNewPassword',
                           first_name='New',
                           last_name='User',
                           email=self.admin_email)

        if self.app.application.testing:
            self.assertTrue('that email has already been registered' in rv.data.lower())

    def test_mismatched_password_registration(self):
        rv = self.register(password='SomeNewPassword',
                           confirm_password='SomeOtherPassword',
                           first_name='New',
                           last_name='User',
                           email='this@that.com')
        self.assertTrue('field must be equal to password' in rv.data.lower())

        # TODO get this all working with email confirmations.... woof; this would also require confirmation

    #############################################################
    # TEST FORGOT PASSWORD
    #############################################################
    def test_forgot_password(self):
        rv = self.app.get('/forgot-password/')
        csrf_token = self.find_csrf_token(rv.data)
        rv = self.app.post('/forgot-password/', data=dict(email=self.admin_email,
                                                          csrf_token=csrf_token),
                           follow_redirects=True)
        self.assertTrue(
            'instructions to reset your password have been sent to {}'.format(self.admin_email) in rv.data.lower())

        # TODO: Can we test the password reset functionality?  Something about sending the email is fucking me up

    #############################################################
    # TEST USER SETTINGS PAGE
    #############################################################
    def test_user_settings(self):
        with self.app as c:
            self.login(self.base_username, self.base_password)
            rv = self.app.get('/user-settings/')
            self.assertTrue(rv._status_code == 200)

    def test_user_settings_name_change(self):
        with self.app as c:
            self.login(self.base_username, self.base_password)
            rv = self.app.get('/user-settings/')
            csrf_token = self.find_csrf_token(rv.data)
            rv = self.app.post('/user-settings-change-name/', data=dict(first_name='Sandy',
                                                                        last_name='Squirrel',
                                                                        csrf_token=csrf_token),
                               follow_redirects=True)
            user = self.datastore.find_user(username=self.base_username)
            self.assertEqual(user.first_name, 'Sandy')
            self.assertEqual(user.last_name, 'Squirrel')

            rv = self.app.get('/user-settings/')
            soup = BeautifulSoup(rv.data, self.parser)
            self.assertEqual(soup.find(id='first_name').attrs['value'], 'Sandy')
            self.assertEqual(soup.find(id='last_name').attrs['value'], 'Squirrel')

    def test_user_settings_name_change_failure(self):
        with self.app as c:
            self.login(self.base_username, self.base_password)
            rv = self.app.get('/user-settings/')
            csrf_token = self.find_csrf_token(rv.data)

            '''
            TEST LENGTH
            '''
            way_too_long_first_name = self.myFactory.sentence(nb_words=ds_config.USER_FIRST_NAME_MAX_LENGTH)
            way_too_long_last_name = self.myFactory.sentence(nb_words=ds_config.USER_LAST_NAME_MAX_LENGTH)
            rv = self.app.post('/user-settings-change-name/', data=dict(
                first_name=way_too_long_first_name,
                last_name='Squirrel',
                csrf_token=csrf_token),
                               follow_redirects=True)
            self.assertTrue(
                'Field cannot be longer than {} characters'.format(ds_config.USER_FIRST_NAME_MAX_LENGTH) in rv.data)
            rv = self.app.post('/user-settings-change-name/', data=dict(
                first_name='This',
                last_name=way_too_long_last_name,
                csrf_token=csrf_token),
                               follow_redirects=True)
            self.assertTrue(
                'Field cannot be longer than {} characters'.format(ds_config.USER_LAST_NAME_MAX_LENGTH) in rv.data)

            '''
            TEST ILLEGAL CHARACTERS
            '''
            invalid_names = ['a b', 'a.b', 'a@b', 'a%b', 'a*b', 'a(b', 'a)b', '12adsf', '<html>']
            for name in invalid_names:
                rv = self.app.post('/user-settings-change-name/', data=dict(first_name=name,
                                                                            last_name='Squirrel',
                                                                            csrf_token=csrf_token),
                                   follow_redirects=True)
                self.assertTrue(rv._status_code == 500)
                self.assertTrue(v_config.ALPHABET_ONLY in rv.data)
                user = self.datastore.find_user(username=self.base_username)
                self.assertEqual(user.first_name, self.admin_first_name)
                self.assertEqual(user.last_name, self.admin_last_name)

                rv = self.app.post('/user-settings-change-name/', data=dict(first_name='Sandy',
                                                                            last_name=name,
                                                                            csrf_token=csrf_token),
                                   follow_redirects=True)
                self.assertTrue(rv._status_code == 500)
                self.assertTrue(v_config.ALPHABET_ONLY in rv.data)
                user = self.datastore.find_user(username=self.base_username)
                self.assertEqual(user.first_name, self.admin_first_name)
                self.assertEqual(user.last_name, self.admin_last_name)

            '''
            TEST NO CHANGE
            '''
            rv = self.app.post('/user-settings-change-name/', data=dict(first_name=self.admin_first_name,
                                                                        last_name=self.admin_last_name,
                                                                        csrf_token=csrf_token),
                               follow_redirects=True)
            self.assertTrue(v_config.NAME_TEXT_NOT_CHANGED in rv.data)

            '''
            TEST CURSING
            '''
            rv = self.app.post('/user-settings-change-name/', data=dict(first_name='fucker',
                                                                        last_name=self.admin_last_name,
                                                                        csrf_token=csrf_token),
                               follow_redirects=True)
            self.assertTrue(v_config.NO_CURSE_WORDS in rv.data)

            '''
            TEST ERROR COMBINATIONS
            '''
            '''
            TEST CURSING AND INVALID CHARACTER
            '''
            rv = self.app.post('/user-settings-change-name/', data=dict(first_name='cunt',
                                                                        last_name='a b',
                                                                        csrf_token=csrf_token),
                               follow_redirects=True)
            self.assertTrue(v_config.NO_CURSE_WORDS in rv.data and v_config.ALPHABET_ONLY in rv.data)
            '''
            TEST NAME TOO LONG AND INVALID CHARACTER
            '''
            rv = self.app.post('/user-settings-change-name/', data=dict(first_name=way_too_long_first_name,
                                                                        last_name='a b',
                                                                        csrf_token=csrf_token),
                               follow_redirects=True)
            self.assertTrue('Field cannot be longer than {} characters'.format(
                ds_config.USER_FIRST_NAME_MAX_LENGTH) in rv.data and v_config.ALPHABET_ONLY in rv.data)

    def update_password(self, new_password, confirm_password, old_password):
        with self.app as c:
            self.login(self.base_username, self.base_password)
            rv = self.app.get('/user-settings/')
            csrf_token = self.find_csrf_token(rv.data)
            rv = self.app.post('/user-settings-change-password/', data=dict(new_password=new_password,
                                                                            confirm_password=confirm_password,
                                                                            old_password=old_password,
                                                                            csrf_token=csrf_token
                                                                            ),
                               follow_redirects=True)
            self.logout()
            return rv

    def test_user_settings_admin_password_change(self):
        '''
        use self.update_password for convenience
        '''
        expected = {"message": [v_config.PASSWORD_UPDATED_SUCCESS_MESSAGE]}
        rv = self.update_password(new_password='rickywhitaker',
                                  confirm_password='rickywhitaker',
                                  old_password=self.admin_password)
        self.assertEqual(loads(rv.data), expected)

    def test_user_settings_password_failures(self):
        '''
        use self.update_password for convenience
        '''
        '''
        TEST PASSWORD LENGTH
        '''
        rv1 = self.update_password(new_password='moocow',
                                   confirm_password='moocow',
                                   old_password=self.admin_password)
        rv2 = self.update_password(new_password='qweradfzxcgaseoijsadoifjalscv',
                                   confirm_password='qweradfzxcgaseoijsadoifjalscv',
                                   old_password=self.admin_password)
        self.assertTrue(p_config.PASSWORD_LENGTH_ERROR in rv1.data)
        self.assertTrue(p_config.PASSWORD_LENGTH_ERROR in rv2.data)

        expected = {'message': [{'confirm_password': [p_config.PASSWORD_NOT_MATCH_ERROR],
                                 'new_password': [p_config.PASSWORD_NOT_MATCH_ERROR]}]}
        rv = self.update_password(new_password='rickywhitaker',
                                  confirm_password='rockywhitaker',
                                  old_password=self.admin_password)
        self.assertEqual(loads(rv.data), expected)

        '''
        TEST INCORRECT PASSWORD
        '''

        rv = self.update_password(new_password='rickywhitaker',
                                  confirm_password='rickywhitaker',
                                  old_password='somethingmadeup')
        self.assertTrue(p_config.INCORRECT_PASSWORD_ERROR in rv.data)

        '''
        TEST PASSWORD ILLEGAL STRING
        '''
        rv = self.update_password(new_password='1qaz2wsx3edc',
                                  confirm_password='1qaz2wsx3edc',
                                  old_password=self.admin_password)
        self.assertTrue(p_config.PASSWORD_WORD_MATCH_ERROR in rv.data)

        '''
        TEST INVALID CHARACTER
        '''
        rv = self.update_password(new_password='this is my password',
                                  confirm_password='this is my password',
                                  old_password=self.admin_password)
        self.assertTrue(p_config.PASSWORD_INVALID_CHARACTER_ERROR in rv.data)

        '''
        TEST PASSWORD PARTIAL ILLEGAL STRING
        '''
        rv = self.update_password(new_password='p@ssw0rd124',
                                  confirm_password='p@ssw0rd124',
                                  old_password=self.admin_password)
        self.assertTrue(p_config.PASSWORD_WORD_INCLUSION_ERROR in rv.data)

    def update_username(self, username):
        with self.app as c:
            self.login(self.base_username, self.base_password)
            rv = self.app.get('/user-settings/')
            csrf_token = self.find_csrf_token(rv.data)
            rv = self.app.post('/user-settings-change-username/', data=dict(username=username,
                                                                            csrf_token=csrf_token),
                               follow_redirects=True)
            self.logout()
            return rv

    def test_user_settings_username_change(self):
        expected = {
            u'field_values': {u'username': u'rwhitaker'},
            u'message': [u'{}'.format(v_config.USERNAME_UPDATED_SUCCESS_MESSAGE)]
        }
        rv = self.update_username(username='rwhitaker')
        self.assertTrue(loads(rv.data) == expected)
        with self.app as c:
            rv = self.login('rwhitaker', self.base_password)
            self.confirm_admin_user_login(rv)

    def test_user_settings_username_change_failures(self):
        '''
        use self.update_username for shortcut
        '''
        '''
        TEST NON UNIQUE NAME CHANGE
        '''
        expected = {u'message': [{u'username': [u'{}'.format(v_config.USERNAME_ALREADY_EXISTS)]}]}
        rv = self.update_username(username=self.admin_username_2)
        self.assertEqual(loads(rv.data), expected)

        '''
        TEST NO CHANGE
        '''
        expected = {u'message': [{u'username': [u'{}'.format(v_config.USERNAME_TEXT_NOT_CHANGED)]}]}
        rv = self.update_username(username=self.base_username)
        self.assertEqual(loads(rv.data), expected)

        '''
        TEST INVALID CHARACTERS
        '''
        expected = {u'message': [{u'username': [u'{}'.format(v_config.ALPHANUMERIC_UNDERSCORE_PERIOD_ONLY)]}]}
        rv = self.update_username(username='@thisismynewusername')
        self.assertEqual(loads(rv.data), expected)

        '''
        TEST INVALID LENGTH
        '''
        expected = {u'message': [
            {u'username': [u'Field cannot be longer than {} characters.'.format(ds_config.USER_USERNAME_MAX_LENGTH)]}]}
        rv = self.update_username(username='ajseroijasdofjasodfjoiasdjviasdfjasodjroiasjdfojasdofjaosijdfojasdf')
        self.assertEqual(loads(rv.data), expected)

        '''
        TEST CURSING
        '''
        expected = {u'message': [{u'username': [u'{}'.format(v_config.NO_CURSE_WORDS)]}]}
        rv = self.update_username(username='PUSSY')
        self.assertEqual(loads(rv.data), expected)

        '''
        TEST MULTIPLE FAILURES
        '''
        expected = {u'message': [{u'username': [u'{}'.format(v_config.ALPHANUMERIC_UNDERSCORE_PERIOD_ONLY),
                                                u'{}'.format(v_config.NO_CURSE_WORDS)]}]}
        rv = self.update_username(username='@cocksutring isfuck')
        self.assertEqual(loads(rv.data), expected)

    def update_email(self, email):
        with self.app as c:
            self.login(self.base_username, self.base_password)
            rv = self.app.get('/user-settings/')
            csrf_token = self.find_csrf_token(rv.data)
            rv = self.app.post('/user-settings-change-email/', data=dict(email=email,
                                                                         csrf_token=csrf_token),
                               follow_redirects=True)
            self.logout()
            return rv

    def test_user_settings_email_change(self):
        expected = {
            u'field_values': {u'email': u'this@that.com'},
            u'message': [u'{}'.format(v_config.EMAIL_UPDATED_SUCCESS_MESSAGE)]
        }
        rv = self.update_email(email='this@that.com')
        self.assertTrue(loads(rv.data) == expected)
        with self.app as c:
            rv = self.login('this@that.com', self.admin_password)
            self.confirm_admin_user_login(rv)

    def test_user_settings_email_failures(self):
        '''
        use self.update_email for funzies
        '''
        '''
        TEST NON EMAIL EMAIL UPDATE
        TEST CURSE WORDS
        '''
        expected = {u'message': [{u'email': [u'Invalid email address.',
                                             u'{}'.format(v_config.NO_CURSE_WORDS)]}]}
        rv = self.update_email(email='hellofuck')
        self.assertEqual(loads(rv.data), expected)
        '''
        TEST INVALID EMAIL ADDERESS
        TEST STRING TOO LONG
        '''
        expected = {u'message': [{u'email': [u'Field cannot be longer than 50 characters.',
                                             u'Invalid email address.']}]}
        rv = self.update_email(
            email='aisetoiasjdfoijasdoifjasodfjoaisdjfoisajd@oaiejroitajsdfijasoirjoasidjfoiasdjfoiasjdf')
        self.assertEqual(loads(rv.data), expected)
        '''
        TEST NO NAME CHANGE
        '''
        expected = {u'message': [{u'email': [u'{}'.format(v_config.MSG_TEXT_NOT_CHANGED)]}]}
        rv = self.update_email(email=self.base_email)
        self.assertEqual(loads(rv.data), expected)
        '''
        TEST INVALID CHARACTERS
        '''
        # TODO: turns out this is gonna be rough, we should send a confirmation email to allow email update
        rv = self.update_email(email='@this @aol.comis my email@aol.com')
        # rv = self.update_email(email=self.myFactory.binary(length=49))
        # print rv.data

    '''
    FAILURE CASES INCLUDE:
    Field Length too long
    Invalid Characters
    Name is not changed
    Curse Words?

    Uniqueness for fields that require that.
    '''

    #############################################################
    # TEST PAGE PERMISSIONS
    #############################################################

    def test_user_settings_permissions(self):
        rv = self.app.get('/user-settings/', follow_redirects=True)
        self.assertTrue(self.msgs['login_required'] in rv.data.lower())

    """##########################################################
    # TEST STOREFRONT BP
    ##########################################################"""

    def test_main_store(self):
        rv = self.app.get('/shop/')
        for product in self.datastore.find_all_products()[1]:
            self.assertTrue(str(product.id) in rv.data)

    def modify_cart(self, url, product_title, quantity, refresh_quantity=False, username=None, password=None):
        if not username:
            username = self.base_username
            password = self.base_password
        success, product = self.datastore.find_product(title=product_title)
        if not success:
            product_id = 'alkdsjfoiaseroiclvkjadsf'
        else:
            product_id = product.id
        with self.app as c:
            self.login(username=username, password=password)
            rv = self.app.get(url)
            csrf_token = self.find_csrf_token(rv.data)
            rv = self.app.post('/modify-shopping-cart/', data=dict(product_id=product_id,
                                                                   quantity=quantity,
                                                                   refresh_quantity=refresh_quantity,
                                                                   csrf_token=csrf_token),
                               follow_redirects=True)
            return rv

    def save_for_later(self, url, product_title, username=None, password=None):
        if not username:
            username = self.base_username
            password = self.base_password
        success, product = self.datastore.find_product(title=product_title)
        if not success:
            product_id = 'asierjocvlsalfj'
        else:
            product_id = product.id
        with self.app as c:
            self.login(username, password)
            rv = self.app.get(url)
            csrf_token = self.find_csrf_token(rv.data)
            rv = self.app.post('/save-for-later/', data=dict(product_id=product_id,
                                                             csrf_token=csrf_token),
                               follow_redirects=True)
            return rv

    def test_add_item_to_new_cart(self):
        url = '/shop/'
        product_title = 'DeBest Lotion'
        expected = v_config.MSG_CART_UPDATED
        rv = self.modify_cart(product_title=product_title, quantity=2, url=url,
                              username=self.base_username_2, password=self.base_password_2)
        self.assertTrue(expected in str(rv.data))

        success, cart = self.datastore.find_cart(user=self.datastore.find_user(username=self.base_username_2))
        item_found = False
        for item in cart.items:
            if item.product.title == product_title:
                item_found = True
                self.assertTrue(item.quantity == 2)
        self.assertTrue(item_found)

    def test_add_existing_item_to_cart(self):
        url = '/shop/'
        product_title = 'DeBest Lotion'
        expected = v_config.MSG_CART_UPDATED
        rv = self.modify_cart(product_title=product_title, quantity=1, url=url)
        print rv.data
        self.assertTrue(expected in str(rv.data))

        success, cart = self.datastore.find_cart(user=self.datastore.find_user(username=self.base_username))
        item_found = False
        for item in cart.items:
            if item.product.title == product_title:
                item_found = True
                self.assertTrue(item.quantity == 7)
        self.assertTrue(item_found)

    def test_add_new_item_to_cart(self):
        url = '/shop/'
        product_title = 'Rick and Morty Candle Collection'
        expected = v_config.MSG_CART_UPDATED
        rv = self.modify_cart(product_title=product_title, quantity=1, url=url)
        self.assertTrue(expected in str(rv.data))

        success, cart = self.datastore.find_cart(user=self.datastore.find_user(username=self.base_username))
        item_found = False
        for item in cart.items:
            if item.product.title == product_title:
                item_found = True
                self.assertTrue(item.quantity == 1)
        self.assertTrue(item_found)

    def test_add_multiple_items_to_cart(self):
        url = '/shop/'
        product_titles = ['DeBest Lotion', 'DeBest Aroma', 'Lotion of the Gods', 'Rick and Morty Candle Collection']
        expected = v_config.MSG_CART_UPDATED
        for product_title in product_titles:
            rv = self.modify_cart(product_title=product_title, quantity=1, url=url,
                                  username=self.base_username, password=self.base_password)
            self.assertTrue(expected in str(rv.data))
            self.logout()

        success, cart = self.datastore.find_cart(user=self.datastore.find_user(username=self.base_username))
        added_products = []
        for item in cart.items:
            added_products.append(item.product.title)

        self.assertEqual(product_titles, added_products)

    def test_add_too_many_quantities_of_nonexistent_item_to_cart(self):
        url = '/shop/'
        product_title = 'Rick and Morty Candle Collection'
        expected = v_config.MSG_QUANTITY_STOCK_ERROR
        rv = self.modify_cart(product_title=product_title, quantity=1000, url=url)
        self.assertTrue(expected in str(rv.data))
        success, cart = self.datastore.find_cart(user=self.datastore.find_user(username=self.base_username))
        item_found = False
        for item in cart.items:
            if item.product.title == product_title:
                item_found = True
        self.assertFalse(item_found)

    def test_add_too_many_quantities_of_existing_item_to_cart(self):
        url = '/shop/'
        product_title = 'DeBest Lotion'
        expected = v_config.MSG_QUANTITY_STOCK_ERROR
        success, cart = self.datastore.find_cart(user=self.datastore.find_user(username=self.base_username))
        original_quantity = -1
        for item in cart.items:
            if item.product.title == product_title:
                original_quantity = item.quantity
        rv = self.modify_cart(product_title=product_title, quantity=100, url=url)
        self.assertTrue(expected in str(rv.data))
        success, cart = self.datastore.find_cart(user=self.datastore.find_user(username=self.base_username))
        for item in cart.items:
            if item.product.title == product_title:
                self.assertEqual(item.quantity, original_quantity)

    def test_add_to_cart_bad_product_id(self):
        url = '/shop/'
        product_title = 'ESOITjSOIJVOIDRoiass'
        quantity = 1
        expected = v_config.MSG_INVALID_PRODUCT_ID
        rv = self.modify_cart(url=url, product_title=product_title, quantity=quantity)
        self.assertTrue(expected in str(rv.data))

    def test_remove_from_cart(self):
        url = '/shop/'
        product_title = 'DeBest Lotion'
        expected = v_config.MSG_CART_UPDATED
        rv = self.modify_cart(product_title=product_title, quantity=0, url=url)
        print rv.data
        self.assertTrue(expected in str(rv.data))
        success, cart = self.datastore.find_cart(user=self.datastore.find_user(username=self.base_username))
        item_found = False
        for item in cart.items:
            if item.product.title == product_title:
                item_found = True
        self.assertFalse(item_found)

    def test_remove_from_cart_no_item(self):
        url = '/shop/'
        product_title = 'Rick and Morty Candle Collection'
        expected = "Unable to find cart item"
        rv = self.modify_cart(product_title=product_title, quantity=0, url=url)
        self.assertTrue(expected in str(rv.data))
        success, cart = self.datastore.find_cart(user=self.datastore.find_user(username=self.base_username))
        item_found = False
        for item in cart.items:
            if item.product.title == product_title:
                item_found = True
        self.assertFalse(item_found)

    def test_remove_from_cart_bad_product_id(self):
        url = '/shop/'
        product_title = 'ESOITjSOIJVOIDRoiass'
        expected = v_config.MSG_INVALID_PRODUCT_ID
        rv = self.modify_cart(quantity=0, url=url, product_title=product_title)
        self.assertTrue(expected in str(rv.data))

    def test_add_back_to_cart(self):
        url = '/shop/'
        product_title = 'Lotion of the Gods'
        quantity = 1
        expected = v_config.MSG_CART_UPDATED
        rv = self.modify_cart(product_title=product_title, quantity=quantity, url=url, refresh_quantity=True)
        self.assertTrue(expected in str(rv.data))
        success, cart = self.datastore.find_cart(user=self.datastore.find_user(username=self.base_username))
        item_found = False
        item_quantity = -1
        for item in cart.items:
            if item.product.title == product_title:
                item_found = True
                item_quantity = item.quantity
        self.assertTrue(item_found and item_quantity == quantity)

    def test_save_for_later(self):
        url = '/shop/'
        product_title = 'DeBest Lotion'
        expected = v_config.MSG_ITEM_SAVED_FOR_LATER
        rv = self.save_for_later(url, product_title)
        self.assertTrue(expected in str(rv.data))
        success, cart = self.datastore.find_cart(user=self.datastore.find_user(username=self.base_username))
        item_saved = False
        for item in cart.saved_for_later:
            if item.product.title == product_title:
                item_saved = True
        self.assertTrue(item_saved)

    """##########################################################
    # TEST BOOKING BP
    ##########################################################"""

    def get_calendar(self, url, session_duration, employee_id, service_id):
        rv = self.app.get(url)
        csrf_token = self.find_csrf_token(rv.data)
        rv = self.app.post('/get-calendar/', data=dict(session_duration=session_duration,
                                                       employee_id=employee_id,
                                                       service_id=service_id,
                                                       csrf_token=csrf_token),
                           follow_redirects=True)
        return rv

    def add_appt(self, url, start_date, start_time, session_length, employee_id, customer_id, service_id,
                 username=None, password=None, ):
        if not username:
            username = self.base_username
            password = self.base_password
        with self.app as c:
            self.login(username=username, password=password)
            rv = self.app.get(url)
            csrf_token = self.find_csrf_token(rv.data)
            rv = self.app.post('/add-appointment/', data=dict(start_date=start_date,
                                                              start_time=start_time,
                                                              session_length=session_length,
                                                              employee_id=employee_id,
                                                              customer_id=customer_id,
                                                              service_id=service_id,
                                                              csrf_token=csrf_token),
                               follow_redirects=True)
            return rv

    def test_main_booking(self):
        rv = self.app.get('/book/')
        for shift in self.datastore.find_all_shifts()[1]:
            self.assertTrue(str(shift.id) in rv.data)
            # TODO: print out what we're getting back here

    def test_get_calendar(self):
        service_id = self.datastore.find_service(name='Customized Massage')[1].id
        rv = self.get_calendar('/book/', session_duration=90, service_id=service_id, employee_id=None)
        print rv.data

    def test_add_appt(self):
        from datetime import datetime as DT
        rv = self.add_appt(url='/book/',
                           start_date=str(DT.date(DT.now())),
                           start_time='15:00',
                           session_length=30,
                           employee_id=self.datastore.find_user(username=self.admin_username).id,
                           customer_id=self.datastore.find_user(username=self.base_username).id,
                           service_id=self.datastore.find_service(title='Customized')[1].id)
        print rv.data

    # def modify_cart(self, url, product_title, quantity, refresh_quantity=False, username=None, password=None):
    #     if not username:
    #         username = self.admin_username
    #         password = self.admin_password
    #     success, product = self.datastore.find_product(title=product_title)
    #     if not success:
    #         product_id = 'alkdsjfoiaseroiclvkjadsf'
    #     else:
    #         product_id = product.id
    #     with self.app as c:
    #         self.login(username=username, password=password)
    #         rv = self.app.get(url)
    #         csrf_token = self.find_csrf_token(rv.data)
    #         rv = self.app.post('/modify-shopping-cart/', data=dict(product_id=product_id,
    #                                                                quantity=quantity,
    #                                                                refresh_quantity=refresh_quantity,
    #                                                                csrf_token=csrf_token),
    #                            follow_redirects=True)
    #         return rv



    """##########################################################
        # TEST ADMIN BP
        ##########################################################"""

    def modify_user(self, user_id, reset_password=False, username=None, first_name=None, last_name=None, email=None,
                    active=None, admin_user=None, admin_password=None):
        if not admin_user:
            admin_user = self.admin_username
        if not admin_password:
            admin_password = self.admin_password
        data_dict = {'user_id': user_id}
        if reset_password:
            data_dict.update({'reset_password': reset_password})
        if username:
            data_dict.update({'username': username})
        if first_name:
            data_dict.update({'first_name': first_name})
        if last_name:
            data_dict.update({'last_name': last_name})
        if email:
            data_dict.update({'email': email})
        if active:
            data_dict.update({'active': active})
        with self.app as c:
            self.login_admin(username=admin_user, password=admin_password)
            rv = self.app.get('/admin/users/')
            csrf_token = self.find_csrf_token(rv.data)
            data_dict.update({'csrf_token': csrf_token})
            rv = self.app.post('/admin/modify-user/', data=data_dict, follow_redirects=True)
            return rv

    def modify_admin_user(self, user_id, reset_password=False, username=None, first_name=None, last_name=None,
                          email=None, active=None, roles=None, admin_user=None, admin_password=None):
        if not admin_user:
            admin_user = self.admin_username
        if not admin_password:
            admin_password = self.admin_password
        data_dict = {'user_id': user_id}
        if reset_password:
            data_dict.update({'reset_password': reset_password})
        if username:
            data_dict.update({'username': username})
        if first_name:
            data_dict.update({'first_name': first_name})
        if last_name:
            data_dict.update({'last_name': last_name})
        if email:
            data_dict.update({'email': email})
        if active:
            data_dict.update({'active': active})
        if roles:
            role_objs = []
            for role in roles:
                role_objs.append(self.datastore.find_role(role))
            data_dict.update({'roles': roles})
        with self.app as c:
            self.login_admin(username=admin_user, password=admin_password)
            rv = self.app.get('/admin/employees/')
            csrf_token = self.find_csrf_token(rv.data)
            data_dict.update({'csrf_token': csrf_token})
            rv = self.app.post('/admin/modify-admin-user/', data=data_dict, follow_redirects=True)
            return rv

    def test_admin_modify_base_user(self):
        username = 'mookybro'
        first_name = 'Mooky'
        last_name = 'Bro'
        email = 'mooky@bro.com'
        user = self.datastore.find_user(username=self.base_username)
        if user.active:
            active = False
        else:
            active = True
        user_id = user.id
        rv = self.modify_user(user_id=user_id, username=username,
                              first_name=first_name, last_name=last_name,
                              email=email, active=active)
        user = self.datastore.find_user(id=user_id)
        self.assertEqual(user.username, username)
        self.assertEqual(user.first_name, first_name)
        self.assertEqual(user.last_name, last_name)
        self.assertEqual(user.email, email)
        self.assertEqual(user.active, active)

    def test_admin_modify_base_user_failures(self):
        expected = ['Field cannot be longer than 20 characters.', 'No curse words please.']
        username = 'oiasjvlkjasdiuaoiesrasdfaserdvadf'
        first_name = 'fuck'
        last_name = 'Bro'
        email = 'mooky@bro.com'
        user = self.datastore.find_user(username=self.base_username)
        if user.active:
            active = False
        else:
            active = True
        user_id = user.id
        rv = self.modify_user(user_id=user_id, username=username,
                              first_name=first_name, last_name=last_name,
                              email=email, active=active)
        for message in expected:
            self.assertTrue(message in rv.data)

    def test_admin_modify_admin_user(self):
        username = 'mookybro'
        first_name = 'Mooky'
        last_name = 'Bro'
        email = 'mooky@bro.com'
        roles = ['employee', 'superuser']
        user = self.datastore.find_user(username=self.admin_username_2)
        if user.active:
            active = False
        else:
            active = True
        user_id = user.id
        rv = self.modify_admin_user(user_id=user_id, username=username,
                                    first_name=first_name, last_name=last_name,
                                    email=email, active=active, roles=roles)
        user = self.datastore.find_user(id=user_id)
        self.assertEqual(user.username, username)
        self.assertEqual(user.first_name, first_name)
        self.assertEqual(user.last_name, last_name)
        self.assertEqual(user.email, email)
        self.assertEqual(user.active, active)
        print user.roles
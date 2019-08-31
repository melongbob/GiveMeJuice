# -*- coding: utf-8 -*-

from __future__ import (absolute_import, division, print_function, unicode_literals)

from bothub_client.bot import BaseBot
from bothub_client.messages import Message
from bothub_client.decorators import command


class Bot(BaseBot):
    def handle_message(self, event, context):
        content = event.get('content')

        if not content:
            if event['new_joined']:
                self.send_chatroom_welcome_message(event)
            return

        if content == '/start':
            self.send_welcome_message(event)
        elif content == 'see menu':
            self.send_menu(event)
        # be aware of tailing space
        elif content.startswith('/show '):
            print(content)
            _, name = content.split()
            self.send_show(name, event)
        # be aware of tailing space
        elif content.startswith('/order_confirm '):
            _, name = content.split()
            self.send_order_confirm(name, event)
        elif content.startswith('/order '):
            _, name = content.split()
            self.send_order(name, event)
        elif content.startswith('/done '):
            self.send_drink_done(content, event)
        elif content == '/feedback':
            self.send_feedback_request()
        # in case of natural language
        else:
            data = self.get_user_data()
            wait_feedback = data.get('wait_feedback')
            if wait_feedback:
                self.send_feedback(content, event)
                return
            recognized = self.recognize(event)
            if recognized:
                return
            self.send_error_message(event)

    def send_welcome_message(self, event):
        message = Message(event).set_text('Hi, I\'m GiveMeJuice.\n'\
                                          'How about some juice?')\
                                .add_quick_reply('see menu')
        self.send_message(message)

    def send_menu(self, event):
        menu = self.get_project_data()['menu']
        names = [name for name in menu.keys()]
        message = Message(event).set_text('What kind of juice would you like?')

        for name in names:
            message.add_postback_button(name, '/show {}'.format(name))

        self.send_message(message)

    def send_show(self, name, event):
        print(name)
        menu = self.get_project_data()['menu']
        selected_menu = menu[name]
        print(selected_menu)
        text = '{name} is made by {description}\n and the price is ${price}.'.format(name=name, **selected_menu)
        message = Message(event).set_text(text)\
                                .add_quick_reply('Order {}'.format(name), '/order {}'.format(name))\
                                .add_quick_reply('see menu')
        self.send_message(message)

    def send_order_confirm(self, name, event):
        message = Message(event).set_text('Do you want to order {}?'.format(name))\
                                .add_quick_reply('Yes', '/order {}'.format(name))\
                                .add_quick_reply('Cancel', 'see menu')
        self.send_message(message)

    def send_order(self, name, event, quantity=1):
        self.send_message('{}of {} is ordered. I\'ll let you know when it\'s ready.'.format(quantity, name))

        chat_id = self.get_project_data().get('chat_id')
        order_message = Message(event).set_text('Order received! {} {}'.format(quantity, name))\
                                      .add_quick_reply('Completed', '/done {} {}'.format(event['sender']['id'], name))

        self.send_message(order_message, chat_id=chat_id)

    def send_drink_done(self, content, event):
        _, sender_id, menu_name = content.split()
        self.send_message('{} is ready. Please take your drinks.'.format(menu_name), chat_id=sender_id)
        message = Message(event).set_text('Let us know how we did.')\
                                .add_quick_reply('Evaluate', '/feedback')
        self.send_message(message, chat_id=sender_id)
        self.send_message('Customer was notified to pick up drinks.')

    def send_feedback_request(self):
        self.send_message('Did you enjoy the juice? Tell us about your experience.')
        data = self.get_user_data()
        data['wait_feedback'] = True
        self.set_user_data(data)

    def send_feedback(self, content, event):
        chat_id = self.get_project_data().get('chat_id')
        self.send_message('Customer comments:\n{}'.format(content), chat_id=chat_id)

        message = Message(event).set_text('Thank you for your comments!')\
                                .add_quick_reply('see menu')
        self.send_message(message)
        data = self.get_user_data()
        data['wait_feedback'] = False
        self.set_user_data(data)

    def recognize(self, event, context):
        response = self.nlu('apiai').ask(event=event)
        action = response.action

        message = Message(event)

        if action.intent == 'input.unknown':
            return False

        if not action.completed:
            message.set_text(response.next_message)
            self.send_message(message)
            return True

        if action.intent == 'show-menu':
            self.send_menu(event, context, [])
            return True

        if action.intent == 'order-drink':
            params = action.parameters
            self.send_order(event, context, (params['menu'], params['quantity']))
            return True

        message.set_text(response.next_message)
        self.send_message(message)
        return True

    def send_error_message(self, event):
        message = Message(event).set_text('I didn\'t quite catch that.\n'\
                                          'How about some juice?')\
                                .add_quick_reply('see menu')
        self.send_message(message)

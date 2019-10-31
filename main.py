import requests
from requests import Response
from http.cookiejar import CookieJar
import json
import sys
import argparse
import threading
import settings

class asdf:
    _cookies = None

    def __init__(self, dry_run):
        '''
        dry_run: if true, then requests will not fire, but only print to consol
        '''
        self.dry_run = dry_run

    def mailboxes_json(self):
        res = self.get_mailboxes()
        return {
            x['mailbox']: x['destinations']
            for x in json.loads(res.content)['result']['mailboxes']
        } 

    @property
    def cookies(self) -> CookieJar:
        '''
        Lazy load cookies
        '''
        if self._cookies is None:
            self._cookies = self.login().cookies
        return self._cookies

    def login(self) -> Response:
        '''
        Does a login request to domain.com and gets cookies
        '''
        cookies = {
            'country': 'USA',
            'Currency': 'USD',
            'Currency_Symbol': '%24',
            'eigi-geolocated-country-code': 'ca',
            'host': 'U2FsdGVkX18IPWXXkr907F200cPF9dRx9AoXYSGnJgVWGC%2F15tTUdRetWRJ9P%2Fa1eDRma2jMJpRKbJ7V%2Bh7Yby1bum0Wj8GwzBdjk%2F6Hk8k%3D',
            'session_id': '76eac6e582b3c00f6f1c82170725bbd9e',
            'customerpixel': '%7B%22visits%22%3A1%2C%22current_visit%22%3A%222019-10-26%2004%3A05%3A57%22%2C%22last_visit%22%3A%222019-10-26%2004%3A05%3A57%22%2C%22first_visit%22%3A%222019-10-26%2004%3A05%3A57%22%2C%22login%22%3A0%7D',
            'optimizelyEndUserId': 'oeu1572062757523r0.21813671432849602',
            '_gcl_au': '1.1.452615655.1572062758',
            'optimizely_exp': '15887130518',
            'optimizely_var': '15883160624',
            '_ga': 'GA1.2.1642355111.1572062758',
            '_gid': 'GA1.2.1803832372.1572062758',
            '_gat_UA-69116836-5': '1',
            '_hjid': 'b3b50194-5f92-4faa-8b5f-8f43ca9d42dc',
            'SESSION_ID': 'a885249f82b5372961c0ec980454aef4',
            '_hjIncludedInSample': '1',
        }

        headers = {
            'Connection': 'keep-alive',
            'Cache-Control': 'max-age=0',
            'Origin': 'https://www1.domain.com',
            'Upgrade-Insecure-Requests': '1',
            'DNT': '1',
            'Content-Type': 'application/x-www-form-urlencoded',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-User': '?1',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
            'Sec-Fetch-Site': 'same-origin',
            'Referer': 'https://www1.domain.com/secure/login.html',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en-US,en;q=0.9',
        }

        data = {
        '__token_timestamp__': '1572062759',
        '__token_val__': '4418e6a80554713f9427d4a18fc72094',
        'credential_0': settings.username,
        'credential_1': settings.password,
        'destination': 'http://www1.domain.com/controlpanel'
        }
        print("Logging in...")
        return requests.post('https://www1.domain.com/secureLogin', headers=headers, cookies=cookies, data=data)

    def get_mailboxes(self) -> Response:
        '''
        Get a list of mailboxes

        The structure of the result is wack.. 
        '''
        headers = {
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'DNT': '1',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en-US,en;q=0.9',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36',
            'Accept': 'application/json, text/plain, */*',
            'Referer': 'https://www1.domain.com/controlpanel/foundation/amacss.org/summary',
            'Connection': 'keep-alive',
        }
        print("Fetching all mailboxes...")
        return requests.get('https://www1.domain.com/api/2.0/enterprise_email/dom.hackvalleyorg1/mailboxes', headers=headers, cookies=self.cookies)

    def add_mailbox(self, mailbox: str, destination: str) -> Response:
        '''
        Add a mailbox
        The destination is manditory for some reason :/
        '''
        headers = {
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'Origin': 'https://www1.domain.com',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en-US,en;q=0.9',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36',
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Referer': 'https://www1.domain.com/controlpanel/foundation/amacss.org/summary',
            'Connection': 'keep-alive',
            'Content-Length': '0',
            'DNT': '1',
        }

        params = (
            ('mailbox', mailbox),
            ('type', 'forward'),
            ('destination', destination),
        )

        print(f"Adding mailbox {mailbox}")
        print(f"Adding forwarding rule {mailbox} -> {destination}")
        if self.dry_run:
            return
        return requests.post('https://www1.domain.com/api/2.0/enterprise_email/dom.hackvalleyorg1/mailbox', headers=headers, params=params, cookies=self.cookies)

        #NB. Original query string below. It seems impossible to parse and
        #reproduce query strings 100% accurately so the one below is given
        #in case the reproduced version is not "correct".
        # response = requests.post('https://www1.domain.com/api/2.0/enterprise_email/dom.hackvalleyorg1/mailbox?mailbox=testemail@amacss.org&type=forward&destination=liu.jordan.com@gmail.com', headers=headers, cookies=cookies)

    def add_mailbox_destination(self, mailbox: str, destination: str) -> Response:
        '''
        Add a new forwarding rule to a mailbox
        '''
        headers = {
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'Origin': 'https://www1.domain.com',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en-US,en;q=0.9',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36',
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Referer': 'https://www1.domain.com/controlpanel/foundation/amacss.org/summary',
            'Connection': 'keep-alive',
            'Content-Length': '0',
            'DNT': '1',
        }

        params = (
            ('email', mailbox),
            ('destination', destination),
        )
        print(f"Adding forwarding rule {mailbox} -> {destination}")
        if self.dry_run:
            return
        return requests.post('https://www1.domain.com/api/2.0/enterprise_email/dom.hackvalleyorg1/destination', headers=headers, params=params, cookies=self.cookies)

        #NB. Original query string below. It seems impossible to parse and
        #reproduce query strings 100% accurately so the one below is given
        #in case the reproduced version is not "correct".
        # response = requests.post('https://www1.domain.com/api/2.0/enterprise_email/dom.hackvalleyorg1/destination?email=testemail@amacss.org&destination=jordan.liu@mail.utoronto.ca', headers=headers, cookies=cookies)

    def delete_mailbox_destination(self, mailbox: str, destination: str) -> Response:
        '''
        Deletes a forwarding rule for a given mailbox
        '''
        headers = {
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'Origin': 'https://www1.domain.com',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en-US,en;q=0.9',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36',
            'Accept': 'application/json, text/plain, */*',
            'Referer': 'https://www1.domain.com/controlpanel/foundation/amacss.org/summary',
            'Connection': 'keep-alive',
            'DNT': '1',
        }

        params = (
            ('email', mailbox),
            ('destination', destination),
        )
        print(f"Deleting forwarding rule {mailbox} -> {destination}")
        if self.dry_run:
            return
        return requests.delete('https://www1.domain.com/api/2.0/enterprise_email/dom.hackvalleyorg1/destination', headers=headers, params=params, cookies=self.cookies)

        #NB. Original query string below. It seems impossible to parse and
        #reproduce query strings 100% accurately so the one below is given
        #in case the reproduced version is not "correct".
        # response = requests.delete('https://www1.domain.com/api/2.0/enterprise_email/dom.hackvalleyorg1/destination?email=testemail@amacss.org&destination=liu.jordan.com@gmail.com', headers=headers, cookies=cookies)

    def delete_mailbox(self, mailbox: str) -> Response:
        '''
        Deletes given mailbox
        '''
        headers = {
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'Origin': 'https://www1.domain.com',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en-US,en;q=0.9',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36',
            'Accept': 'application/json, text/plain, */*',
            'Referer': 'https://www1.domain.com/controlpanel/foundation/amacss.org/email',
            'Connection': 'keep-alive',
            'DNT': '1',
        }

        params = (
            ('email', mailbox),
        )
        print(f"Deleting mailbox {mailbox}")
        if self.dry_run:
            return
        return requests.delete('https://www1.domain.com/api/2.0/enterprise_email/dom.hackvalleyorg1/mailbox', headers=headers, params=params, cookies=self.cookies)

        #NB. Original query string below. It seems impossible to parse and
        #reproduce query strings 100% accurately so the one below is given
        #in case the reproduced version is not "correct".
        # response = requests.delete('https://www1.domain.com/api/2.0/enterprise_email/dom.hackvalleyorg1/mailbox?email=testemail@amacss.org', headers=headers, cookies=cookies)

    def update_mailboxes(self, new: dict) -> None:
        '''
        Update mailboxes and their forwarding rules conccurently
        One thread per mailbox add/edit(rules)/delete
        One thread per forwarding rule add/delete

        The api only allows single entry updates so thats why this is multiple threaded requests instead of a single request

        Arguments:
            new: dict like
                {
                    "some_email@mail.com": [
                        "something@forward.com",
                        "something@forward2.com"
                    ]
                }
        '''
        # collect all threads
        threads = []

        # function to add/delete a forwarding rule to run in new thread
        def update_destinations(m, cur_dest: list, new_dest: list):
            to_add = list(filter(lambda x: x not in cur_dest, new_dest))
            to_delete = list(filter(lambda x: x not in new_dest, cur_dest))

            for d in to_add:
                self.add_mailbox_destination(m, d)
            for d in to_delete:
                self.delete_mailbox_destination(m, d)

        # figure out what needs to be done and what is left unchanged
        cur_mailboxes = self.mailboxes_json()
        m_to_add = list(filter(lambda x: x not in cur_mailboxes.keys(), new.keys()))
        m_to_update = list(filter(lambda x: x in cur_mailboxes.keys(), new.keys()))
        m_to_delete = list(filter(lambda x: x not in new.keys(), cur_mailboxes.keys()))

        # do the thing
        for m in m_to_add:
            def temp(m):
                self.add_mailbox(m, new[m][0])
                update_destinations(m, new[m][0:1], new[m])
            thread = threading.Thread(target=temp, args=(m,))
            thread.start()
            threads.append(thread)
        for m in m_to_update:
            thread = threading.Thread(target=update_destinations, args=(m, cur_mailboxes[m], new[m]))
            thread.start()
            threads.append(thread)
        for m in m_to_delete:
            thread = threading.Thread(target=self.delete_mailbox, args=(m,))
            thread.start()
            threads.append(thread)

        # wait for threads to finish
        for t in threads:
            t.join()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('filename')
    parser.add_argument('--dry-run', '-d', help='Dry run', action='store_true')
    args = parser.parse_args()

    a = asdf(args.dry_run)
    filename = sys.argv[1]
    with open(filename, 'r') as f:
        data = json.load(f)
        a.update_mailboxes(data)
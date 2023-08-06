import time
import re


__all__ = ['Cache']


class Cache:

    def __init__(self, preston, base_url):
        """Cache class

        The cache is desgined to respect the caching rules of CREST as to
        not request a page more often than it is updated by the server.

        Args:
            preston (preston.Preston): the containing Preston instance
            base_url (str): the root url of CREST

        Returns:
            None
        """
        self.data = {}
        self._preston = preston
        self.logger = preston.logger
        self.fetch = preston.__call__
        self.base_url = base_url

    def _proper_url(self, url):
        """Converts URLs.

        Covert a potentially simple string ('alliances') to the full url of
        the CREST endpoint ('https://CREST.tech.ccp.is/latest/alliances/').

        Args:
            url (str) - url or url fragment to modify

        Returns:
            value (str) of the proper url
        """
        if self.base_url not in url:
            url = self.base_url + url
        url = re.sub(r'(?<!https:)//', '/', url)
        if not url.endswith('/'):
            url = url + '/'
        return url

    def _get_expiration(self, headers):
        """Gets the expiration time of the data from the response headers.

        Args:
            headers (dict) - dictionary of headers from CREST

        Returns:
            value (int) of seconds from now the data expires
        """
        if headers.get('Cache-Control') in ('no-cache', 'no-store'):
            return 0
        match = re.search(r'max-age=([0-9]+)', headers.get('Cache-Control', ''))
        if match:
            return int(match.group(1))
        return 0

    def set(self, response):
        """Adds a response to the cache.

        Args:
            response (requests.Response) - response from CREST

        Returns:
            None
        """
        self.data[response.url] = Page(response.json(), self._get_expiration(response.headers))
        self.logger.info('Added cache for url {}, expires in {} seconds'.format(response.url, self.data[response.url].expires_in))

    def _check_expiration(self, url, data):
        """Checks the expiration time for data for a url.

        If the data has expired, it is deleted from the cache.

        Args:
            url (str) - url to check
            data (preston.cache.Page) - page of data for that url

        Returns:
            value (any) of either the passed data or None if it expired
        """
        if data.expires_after < time.time():
            self.logger.warning('Cached page at url {} expired. Now: {}, expired after: {}'.format(
                url, time.time(), data.expires_after))
            del self.data[url]
            data = None
        return data

    def get(self, url, ignore_expires=False):
        """Get data from the cache by the url.

        If the data has expired, the callback function is called to get the data again.

        Args:
            url (str) - url to get data for
            ignore_expires (bool [False]) - whether to ignore the expiration date
                in returning data to the caller

        Returns:
            value (any) of either the passed data or None if it expired
        """
        url = self._proper_url(url)
        data = self.data.get(url)
        if not data:
            return self.fetch()
        if ignore_expires:
            self._check_expiration(url, data)
        return data.data if data else None

    def check(self, url):
        """Check if data for a url has expired.

        Data is not fetched again if it has expired.

        Args:
            url (str) - url to check expiration on

        Returns:
            value (bool) that's True if the data has expired
        """
        url = self._proper_url(url)
        data = self.data.get(url)
        if data:
            data = self._check_expiration(url, data)
        return bool(data)

    def __len__(self):
        """Returns the number of items in the stored data.

        More of a debugging tool, since getting the number of dictionary keys
        isn't a good indicator of how much data is actually here.

        Args:
            None

        Returns:
            value (int) of the number of keys in the data
        """
        return len(self.data.keys())


class Page:

    def __init__(self, data, expires_in):
        """Page class

        A wrapper around a page from CREST that also includes the expiration time
        in seconds and the time after which the wrapped data expires.

        Args:
            data (any) - page data from CREST
            expires_in (float) - number of seconds from now that the data expires

        Returns:
            None
        """
        self.data = data
        self.expires_in = expires_in
        self.expires_after = time.time() + expires_in



class Job(object):
    def __init__(self, site, url, **details):
        self._site = site
        self._url = url
        self.__dict__.update(details)

    def __repr__(self):
        return "<Job title='{}', uid='{}', site='{}'>"\
            .format(self.title, self.uid, self._site.__class__.__name__)

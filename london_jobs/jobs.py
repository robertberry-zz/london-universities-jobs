

class Job(object):
    def __init__(self, **details):
        self.__dict__.update(details)

    def __repr__(self):
        return "<Job title={}, uid={}>".format(self.title, self.uid)

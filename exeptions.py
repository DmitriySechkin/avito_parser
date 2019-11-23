class Error(Exception):
    """
    Base Error. All other Errors thrown by DNF should inherit from this.
    :api
    """
    def __init__(self, value=None):
        super(Error, self).__init__()
        self.value = value

    def __str__(self):
        return "%s" %(self.value,)

    def __unicode__(self):
        return '%s' % self.value


class NoSectionException(Error):
    def __init__(self, section, file):
        value = "Section {0} not found in file {1}".format(section, file)
        super(NoSectionException, self).__init__(value)


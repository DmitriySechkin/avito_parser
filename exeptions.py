class Error(Exception):
    """
    Base Error, all other Errors thrown by Parser should inherit from this
    """

    def __init__(self, value=None):
        super(Error, self).__init__()
        self.value = value

    def __str__(self):
        return "%s" % (self.value,)

    def __unicode__(self):
        return '%s' % self.value


class NoSectionException(Error):
    """
    The exception is thrown when there is no requested section in the config file
    """

    def __init__(self, section, file):
        err_text = "Section {0} not found in file {1}!".format(section, file)
        super(NoSectionException, self).__init__(err_text)


class NoFileException(Error):
    """
    The exception is thrown when the requested file does not exist
    """

    def __init__(self, file):
        err_text = "No file {} found in work directory!".format(file)
        super(NoFileException, self).__init__(err_text)


class NoSettingFindInSection(Error):
    """
    The exception is thrown when the requested setting file does not exist in the file
    """

    def __init__(self, section, name_param):
        err_text = "No setting {0} found in section {1}!".format(name_param, section)
        super(NoSettingFindInSection, self).__init__(err_text)


class SettingValueIsEmpty(Error):
    """
    The exception is thrown when the requested setting value is empty
    """

    def __init__(self, name_setting):
        err_text = "Value of setting {0} is empty!".format(name_setting)
        super(SettingValueIsEmpty, self).__init__(err_text)


class ZeroPageNumber(Error):
    """
    The exception is thrown when the passed page number equal to zero
    """

    def __init__(self):
        err_text = "The page number cannot be zero!".format()
        super(ZeroPageNumber, self).__init__(err_text)


class ErrorSummParameter(Error):
    """
    The exception is thrown when the minimum summ parameter passed in query url is greater than
    the maximum parameter
    """

    def __init__(self, min_summ, max_summ):
        err_text = "the minimum amount = {0} is greater than the maximum! = {1}".format(min_summ, max_summ)
        super(ErrorSummParameter, self).__init__(err_text)


class FailedGetRequest(Error):
    """
    The exception is thrown when the response code is not success
    """

    def __init__(self, code):
        err_text = "Failed get request! Response code is {}".format(code)
        super(FailedGetRequest, self).__init__(err_text)


class FailedGettingNumberPages(Error):
    """
    The exception is thrown when failed the getting of number last page
    """

    def __init__(self):
        err_text = "Failed get number of pages in html!"
        super(FailedGettingNumberPages, self).__init__(err_text)


class FailedAdsDataGet(Error):
    """
    The exception is thrown when failed the getting of ads data on the page
    """

    def __init__(self, number_page):
        err_text = "Failed ads data get on page {}!".format(number_page)
        super(FailedAdsDataGet, self).__init__(err_text)



class FailedItemsGetting(Error):
    """
    The exception is thrown when failed the getting of ads data on the page
    """

    def __init__(self):
        err_text = "Not found items tag in page data!".format()
        super(FailedItemsGetting, self).__init__(err_text)

import dateutil.parser
import six
from scipy import sort, array, searchsorted

from quantdsl.priceprocess.base import datetime_from_date


class ForwardCurve(object):
    def __init__(self, name, data):
        assert isinstance(name, six.string_types)
        assert isinstance(data, (list, tuple))
        self.name = name
        self.data = data
        self.by_date = dict(
            [(datetime_from_date(dateutil.parser.parse(d)), v) for (d, v) in self.data]
        )
        self.sorted = sort(array(list(self.by_date.keys())))

    def get_price(self, date):
        try:
            price = self.by_date[date]
        except:
            # Search for earlier date.
            index = searchsorted(self.sorted, date) - 1
            if index < 0:
                raise KeyError("Delivery date {} not found in '{}' forward curve.".format(date, self.name))
            price = self.by_date[self.sorted[index]]
        return price
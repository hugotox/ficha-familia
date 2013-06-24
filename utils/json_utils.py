from django.http import HttpResponse
import json
import datetime
import decimal
from django.db import models


class JSONEncoderX(json.JSONEncoder):
    """
    JSONEncoder subclass that knows how to encode date/time and decimal types.
    """

    def default(self, o):
        # See "Date Time String Format" in the ECMA-262 specification.
        if isinstance(o, datetime.datetime) or isinstance(o, datetime.time):
            r = o.isoformat()
            if o.microsecond:
                r = r[:23] + r[26:]
            if r.endswith('+00:00'):
                r = r[:-6] + 'Z'
            return r
        elif isinstance(o, datetime.date):
            return o.isoformat()
        elif isinstance(o, decimal.Decimal):
            return str(o)
        elif isinstance(o, models.Model):
            return str(o)  # this will call the __unicode__ method inside the model
        else:
            return super(JSONEncoderX, self).default(o)


def json_response(data):
    return HttpResponse(json.dumps(data, cls=JSONEncoderX), content_type='application/json')
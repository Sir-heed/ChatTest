from datetime import datetime
from django.conf import settings

# This class returns the string needed to generate the key
class generateKey:
    @staticmethod
    def returnValue(phone):
        return f'{phone}{datetime.date(datetime.now())}{settings.SECRET_KEY}'
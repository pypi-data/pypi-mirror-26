from __future__ import unicode_literals
from __future__ import division
from __future__ import absolute_import
from __future__ import print_function

from future import standard_library
standard_library.install_aliases()

__version__ = '4.5.0'

from notifications_python_client.errors import REQUEST_ERROR_STATUS_CODE, REQUEST_ERROR_MESSAGE

from notifications_python_client.notifications import NotificationsAPIClient

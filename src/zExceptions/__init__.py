##############################################################################
#
# Copyright (c) 2002 Zope Foundation and Contributors.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE
#
##############################################################################
"""General exceptions that wish they were standard exceptions

These exceptions are so general purpose that they don't belong in Zope
application-specific packages.
"""

import warnings

from zope.interface import implements
from zope.interface.common.interfaces import IException
from zope.publisher.interfaces import INotFound
from zope.security.interfaces import IForbidden
from zExceptions.unauthorized import Unauthorized


# __builtins__ was renamed to builtins in Python 3
try:
    import __builtin__ as builtins
except ImportError:
    import builtins


# Python 3 no longer has old-style classes
CLASS_TYPES = [type]
try:
    from types import ClassType
except ImportError:
    pass
else:
    CLASS_TYPES.append(ClassType)
CLASS_TYPES = tuple(CLASS_TYPES)


class BadRequest(Exception):
    implements(IException)


class InternalError(Exception):
    implements(IException)


class NotFound(Exception):
    implements(INotFound)


class Forbidden(Exception):
    implements(IForbidden)


class MethodNotAllowed(Exception):
    pass


class Redirect(Exception):
    pass


def convertExceptionType(name):
    import zExceptions
    etype = None
    if name in builtins.__dict__:
        etype = getattr(builtins, name)
    elif hasattr(zExceptions, name):
        etype = getattr(zExceptions, name)
    if (etype is not None and
        isinstance(etype, CLASS_TYPES) and
        issubclass(etype, Exception)):
        return etype


def upgradeException(t, v):
    # If a string exception is found, convert it to an equivalent
    # exception defined either in builtins or zExceptions. If none of
    # that works, then convert it to an InternalError and keep the
    # original exception name as part of the exception value.
    if isinstance(t, basestring):
        warnings.warn('String exceptions are deprecated starting '
                    'with Python 2.5 and will be removed in a '
                    'future release', DeprecationWarning, stacklevel=2)

        etype = convertExceptionType(t)
        if etype is not None:
            t = etype
        else:
            v = t, v
            t = InternalError
    return t, v

# -*- coding: utf-8 -*-
###############################################################################
#   Copyright 2006 to the present, Orbitz Worldwide, LLC.
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
###############################################################################
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import sys
import time

from twisted.internet import defer
from twisted.python.failure import Failure


def raises(exc):
    '''a python take on a java classic. lets you state what exception
       your function will raise. the actuall exception is stored on the
       raised exception object at the property exc.inner_exception.
       #1 simply tells us if caught exception is of same type as what we have
          stated we will raise from our decorated function. if so just throw
          that exception. no need to re-wrap.
    '''

    def decorator(func):
        def newfunc(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception:
                failure = Failure()
                caught_exc = failure.value
                err_msg = failure.getErrorMessage()
                if failure.check(exc):
                    # pylint: disable=raising-bad-type
                    raise caught_exc  # 1
                    # pylint: enable=raising-bad-type
                exc_inst = exc(err_msg)
                exc_inst.inner_exception = caught_exc
                raise exc_inst

        return newfunc

    return decorator


def safe(defaults):
    """On failure emit defaults as the result of the call"""

    def decorator(func):
        """Stop exception propagation (except KeyboardInterrupt & SystemExit)
           but print tracebacks, works on methods that return a deferred.
        """

        def newfunc(*args, **kwargs):
            debugKwargs = {
                'defaults': defaults,  # default to return on failure
                'trap': True,  # trap all errors
                'fd': None,  # don't display caller or result
                'debug': False  # disable extranious debugging
            }
            caller = _InspectorGadget(func, **debugKwargs)
            return caller(*args, **kwargs)

        return newfunc

    return decorator


def debugCall(func, **debugKwargs):
    """Free debugging hooks for Everybody!!!
       this decorator works with deferrable and blocking methods.
       @param func (a callable object)
       @optionals
         @param fd (file like object supporting write attr)
         @param trap (trap selective exceptions or None or All (if True))
            see twisted.python.failure.Failure.trap
         @param verbose (turn on verbose stack traces)
            see twisted.python.failure.Failure.printDetailedTraceback
         @param defaults (object) object to return on trap success
       @return (object)
    """

    def newfunc(*args, **kwargs):
        debugKwargs['debug'] = True
        if 'fd' not in debugKwargs:
            debugKwargs['fd'] = sys.stderr
        if 'defaults' not in debugKwargs:
            debugKwargs['defaults'] = None
        if 'trap' not in debugKwargs:
            debugKwargs['trap'] = None
        caller = _InspectorGadget(func, **debugKwargs)
        return caller(*args, **kwargs)

    return newfunc


def retry(delay=0.25, maximum=10, trap=None, debug=False, fd=None, defaults=None, verbose=False):
    """retry this call a maximum number of tries with a delay in between
       attempts. if this call never succeeds the last failure will be
       emitted.  Handles standard methods and deferrable methods.
       Note: if the function is not deferrable and you are running
          inside of a twisted reactor, your reactor will be blocked.
       @param delay (float) delay between retries
       @param maximum (int) maximum retry attempts
       @param debug (bool) display messages
       @param fd (file like object supporting write attr)
       @param trap (trap selective exceptions or None or All (if True))
            see twisted.python.failure.Failure.trap
       @param verbose (turn on verbose stack traces)
            see twisted.python.failure.Failure.printDetailedTraceback
       @param defaults (object) object to return on trap success
    """

    def decorator(func):
        @defer.deferredGenerator
        def _deferred(deferredResult, caller):
            """only callable by ``newfunc``"""
            from twisted.internet import reactor
            result = None
            attempt = 0
            while attempt <= maximum:
                try:
                    wfd = defer.waitForDeferred(deferredResult)
                    yield wfd
                    result = wfd.getResult()
                    break  # didn't throw exception then we have the result
                except SystemExit:
                    result = Failure()
                    break
                except KeyboardInterrupt:
                    result = Failure()
                    break
                except Exception:
                    attempt += 1
                    if attempt > maximum:
                        result = Failure()
                        break  # failure captured
                    d = defer.Deferred()
                    # pylint: disable=no-member
                    reactor.callLater(delay, d.callback, None)
                    # pylint: enable=no-member
                    wfd = defer.waitForDeferred(d)
                    yield wfd
                    wfd.getResult()
                    # fortunatly the caller has been set up in advance
                    caller.write('>>> Retry attempt %d' % attempt)
                    deferredResult = caller(*caller.args, **caller.kwargs)
            yield result

        def newfunc(*args, **kwargs):
            result = None
            attempt = 0
            # setup the caller object
            iKwargs = {
                'debug': debug,
                'fd': fd,
                'verbose': verbose,
                'defaults': defaults,
                'trap': trap
            }
            caller = _InspectorGadget(func, **iKwargs)
            while attempt <= maximum:
                try:  # initial caller setup
                    result = caller(*args, **kwargs)
                    if isinstance(result, defer.Deferred):
                        return _deferred(result, caller)
                    break  # reset data
                except SystemExit:
                    result = Failure()
                    break
                except KeyboardInterrupt:
                    result = Failure()
                    break
                except Exception:
                    attempt += 1
                    if attempt > maximum:
                        result = Failure()
                        break
                    time.sleep(delay)
                    caller.write('>>> Retry attempt %d' % attempt)
            if isinstance(result, Failure):
                result.raiseException()
            return result

        return newfunc

    return decorator


def typesafety(*typs, **kwtyps):
    """LBYL - look before you leap decorator"""

    def decorator(func):
        def enforcer(*args, **kwargs):
            util = _typeSafeUtil()
            args = util.extractSelf(args, func)
            util.compareTypes(args, typs)
            util.compareTypes(kwargs, kwtyps)
            args = util.addSelf(args)
            return func(*args, **kwargs)

        return enforcer

    return decorator


class _typeSafeUtil(object):
    def __init__(self):
        self.selfArg = None
        self.passType = None

    def extractSelf(self, args, func):
        try:  # need to check if "self is first arg, if so check args - 1
            self.selfArg = dir(args[0]).index(func.__name__)
            if self.selfArg > None:
                return args[1:]  # shorten args for rest of func
        except Exception:
            return args

    def addSelf(self, args):
        if self.selfArg > None:
            args = list(args)
            args.insert(0, self.selfArg)
            return tuple(args)
        return args

    def compareTypes(self, args, refTypes):
        if len(args) != len(refTypes):
            raise InvalidArgsLengthException
        args = self.dictToList(args)
        refTypes = self.dictToList(refTypes)

        for a, b in zip(args, refTypes):
            try:
                if isinstance(b, self.passType):
                    continue
                elif isinstance(a, type(b)):
                    continue
                elif isinstance(b, type):
                    if isinstance(a, b):
                        continue
                elif isinstance(a, b):
                    continue
                raise TypeError
            except Exception:
                raise TypeError

    def dictToList(self, tryDict):
        if not isinstance(tryDict, dict):
            return tryDict
        tmp = []
        for k in tryDict.keys():
            tmp.append(tryDict[k])
        return tmp


class _InspectorGadget(object):
    """Helper class used by various decorator methods to aid in method
       debugging.  Works with standard methods and deferred methods.
    """

    def __init__(self, func, trap=None, debug=False, fd=None, verbose=False, defaults=None):
        """constructor method
           #required
           @param func (callable object)
           #optional
           @param trap (bool|None|Exception|list(Exception,...))
           @param debug (bool) - whether or not to display caller and result
           @param fd (file like object supporting ``write`` method)
           @param verbose (bool) - make stack traces more verbose
           @param defaults (object) - on failures that are trapped return this
           @return (instance)
        """
        # well i am just being nice
        if debug and not fd:
            fd = sys.stderr
        self.function = func
        self.trap = trap
        self.args = ()
        self.kwargs = {}
        self.debug = debug
        self.fd = fd
        self.verbose = verbose
        self.defaults = defaults

    def write(self, data):
        """write data to some file like object only writes happen if debug was
           specified during instantiation.
        """
        if hasattr(self.fd, 'write') and hasattr(self.fd.write, '__call__') \
                and self.debug:  # only write on debug true
            try:
                self.fd.write(str(data) + '\n')
            except Exception:
                failure = Failure()
                if self.verbose:
                    failure.printDetailedTraceback(sys.stderr)
                else:
                    failure.printTraceback(sys.stderr)

    def display_result(self, result):
        """display the result in debug mode, always display tracebacks
           on failure. this is callback safe.
           @param result (object)
           @return (param -> result)
        """
        if isinstance(result, Failure):
            if hasattr(result.value, '__class__'):
                eName = result.value.__class__.__name__
            else:  # guess in event failure doesn't make sense
                try:  # preload and reset later
                    eName = sys.exc_info()[0].__name__
                except AttributeError:
                    eName = 'Unknown'  # fail
                except Exception:
                    failure = Failure()
                    self.write('Something bad has happened')
                    fd = self.fd
                    if not fd:
                        self.fd = sys.stderr
                    if self.verbose:
                        failure.printDetailedTraceback(self.fd)
                    else:
                        failure.printTraceback(self.fd)
                    # restore the previous fd object
                    self.fd = fd
                    return result
            self.write(">>> %s call raised %s" % (self.function.func_name, eName))
            # make sure the fd is valid for tracebacks
            fd = self.fd
            if not fd:
                self.fd = sys.stderr
            if self.verbose:
                result.printDetailedTraceback(self.fd)
            else:
                result.printTraceback(self.fd)
            # restore the previous fd object
            self.fd = fd
            self.write(">>>")
        else:
            self.write(">>> Returning %s -> %s" % (self.function.func_name, str(result)))
        return result

    def display_caller(self):
        """display the calling arguments"""
        argsString = ','.join(map(str, self.args))
        if self.kwargs:
            argsString += (',' + ','.join(["%s=%s" % pair for pair in self.kwargs.items()]))
        self.write(">>> Calling %s(%s)" % (self.function.func_name, argsString))

    def __call__(self, *args, **kwargs):
        """invoke the method with user defined args"""
        try:
            self.args = args
            self.kwargs = kwargs
            # no need to iterate through the args
            if self.debug:
                self.display_caller()
            result = self.function(*args, **kwargs)
            if isinstance(result, defer.Deferred):
                result.addErrback(self.handleFailure)
                result.addCallback(self.display_result)
                return result
            return self.display_result(result)
        except Exception:
            result = self.handleFailure(Failure())
            if isinstance(result, Failure):
                result.raiseException()
            return self.display_result(result)  # must have fully trapped

    def handleFailure(self, failure):
        """handle failures, by either trapping or passing them through
           @param failure (instance twisted.python.failure.Failure)
           @return (failure| self.defaults)
        """
        try:
            failure.raiseException()
        except KeyboardInterrupt:
            self.write(">>> Refusing to handle KeyboardInterrupt")
            return Failure()
        except SystemExit:
            self.write(">>> Refusing to handle SystemExit")
            return Failure()
        except Exception:
            failure = self.display_result(Failure())
            if isinstance(self.trap, bool) and self.trap:
                self.write(">>> Trapped all failures")
                return self.defaults  # return the defaults on trap
            elif self.trap:  # trap selective failures
                try:
                    x = failure.trap(self.trap)
                    self.write(">>> Trapped specific failure %s" % str(x))
                    return self.defaults
                except Exception:
                    self.write(">>> Unable to trap error")
            return failure  # behave like a good twisted errback


class InvalidArgsLengthException(Exception):
    pass


_EXPORTS = [
    'safe',
    'debugCall',
    'retry',
    'typesafety',
    'InvalidArgsLengthException',
]

# export our methods
__all__ = _EXPORTS

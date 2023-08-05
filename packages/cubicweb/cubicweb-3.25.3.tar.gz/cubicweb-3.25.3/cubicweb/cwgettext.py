# copyright 2003-2010 LOGILAB S.A. (Paris, FRANCE), all rights reserved.
# contact http://www.logilab.fr/ -- mailto:contact@logilab.fr
#
# This file is part of CubicWeb.
#
# CubicWeb is free software: you can redistribute it and/or modify it under the
# terms of the GNU Lesser General Public License as published by the Free
# Software Foundation, either version 2.1 of the License, or (at your option)
# any later version.
#
# CubicWeb is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more
# details.
#
# You should have received a copy of the GNU Lesser General Public License along
# with CubicWeb.  If not, see <http://www.gnu.org/licenses/>.

import gettext

from six import PY3


class cwGNUTranslations(gettext.GNUTranslations):
    # The encoding of a msgctxt and a msgid in a .mo file is
    # msgctxt + "\x04" + msgid (gettext version >= 0.15)
    CONTEXT_ENCODING = "%s\x04%s"

    def pgettext(self, context, message):
        ctxt_msg_id = self.CONTEXT_ENCODING % (context, message)
        missing = object()
        tmsg = self._catalog.get(ctxt_msg_id, missing)
        if tmsg is missing:
            if self._fallback:
                return self._fallback.pgettext(context, message)
            return message
        # Encode the Unicode tmsg back to an 8-bit string, if possible
        if self._output_charset:
            return tmsg.encode(self._output_charset)
        elif self._charset:
            return tmsg.encode(self._charset)
        return tmsg

    def lpgettext(self, context, message):
        ctxt_msg_id = self.CONTEXT_ENCODING % (context, message)
        missing = object()
        tmsg = self._catalog.get(ctxt_msg_id, missing)
        if tmsg is missing:
            if self._fallback:
                return self._fallback.lpgettext(context, message)
            return message
        if self._output_charset:
            return tmsg.encode(self._output_charset)
        return tmsg.encode(locale.getpreferredencoding())

    def npgettext(self, context, msgid1, msgid2, n):
        ctxt_msg_id = self.CONTEXT_ENCODING % (context, msgid1)
        try:
            tmsg = self._catalog[(ctxt_msg_id, self.plural(n))]
            if self._output_charset:
                return tmsg.encode(self._output_charset)
            elif self._charset:
                return tmsg.encode(self._charset)
            return tmsg
        except KeyError:
            if self._fallback:
                return self._fallback.npgettext(context, msgid1, msgid2, n)
            if n == 1:
                return msgid1
            else:
                return msgid2        

    def lnpgettext(self, context, msgid1, msgid2, n):
        ctxt_msg_id = self.CONTEXT_ENCODING % (context, msgid1)
        try:
            tmsg = self._catalog[(ctxt_msg_id, self.plural(n))]
            if self._output_charset:
                return tmsg.encode(self._output_charset)
            return tmsg.encode(locale.getpreferredencoding())
        except KeyError:
            if self._fallback:
                return self._fallback.lnpgettext(context, msgid1, msgid2, n)
            if n == 1:
                return msgid1
            else:
                return msgid2

    if PY3:
        ugettext = gettext.GNUTranslations.gettext

    def upgettext(self, context, message):
        ctxt_message_id = self.CONTEXT_ENCODING % (context, message)
        missing = object()
        tmsg = self._catalog.get(ctxt_message_id, missing)
        if tmsg is missing:
            # XXX logilab patch for compat w/ catalog generated by cw < 3.5
            return self.ugettext(message)
            if self._fallback:
                return self._fallback.upgettext(context, message)
            return unicode(message)
        return tmsg

    def unpgettext(self, context, msgid1, msgid2, n):
        ctxt_message_id = self.CONTEXT_ENCODING % (context, msgid1)
        try:
            tmsg = self._catalog[(ctxt_message_id, self.plural(n))]
        except KeyError:
            if self._fallback:
                return self._fallback.unpgettext(context, msgid1, msgid2, n)
            if n == 1:
                tmsg = unicode(msgid1)
            else:
                tmsg = unicode(msgid2)
        return tmsg


def translation(domain, localedir=None, languages=None,
                class_=None, fallback=False, codeset=None):
    if class_ is None:
        class_ = cwGNUTranslations
    return gettext.translation(domain, localedir=localedir,
                               languages=languages, class_=class_,
                               fallback=fallback, codeset=codeset)

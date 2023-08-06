# -*- coding: utf-8 -*-

from __future__ import absolute_import

from media_converter.streams.instream import Instream
from media_converter.streams.instream import VideoInstream
from media_converter.streams.instream import AudioInstream
from media_converter.streams.instream import SubtitleInstream


class Outstream(object):
    def __init__(self, instream):
        self._instreams = [instream]
        self._filters = []

    @property
    def instreams(self):
        return self._instreams

    @property
    def filters(self):
        return self._filters


class VideoOutstream(Outstream):
    def __init__(self, instream):
        Outstream.__init__(self, instream if isinstance(instream, Instream) else VideoInstream.factory(instream))

        self._filters = []

    def scale(self, width=None, height=None):
        if width is None:
            width = -2
        if height is None:
            height = -2

        self._filters.append((None, 'scale={}:{}'.format(width, height)))
        return self

    def deinterlace(self):
        self._filters.append((None, 'yadif'))
        return self

    def deinterlace_slow(self):
        self._filters.append((None, 'yadif=3'))
        self._filters.append((None, 'mcdeint=2:1:10'))
        return self

    def overlay(self, instream, x=0, y=0):
        instream = instream if isinstance(instream, Instream) else VideoInstream.factory(instream)
        self._instreams.append(instream)

        self._filters.append((instream, 'overlay={}:{}'.format(x, y)))
        return self

    def crop(self, area):
        self._filters.append((None, 'crop={}'.format(area)))
        return self


class AudioOutstream(Outstream):
    def __init__(self, instream):
        Outstream.__init__(self, instream if isinstance(instream, Instream) else AudioInstream.factory(instream))

        self._filters = []


class SubtitleOutstream(Outstream):
    def __init__(self, instream):
        Outstream.__init__(self, instream if isinstance(instream, Instream) else SubtitleInstream.factory(instream))

        self._filters = []

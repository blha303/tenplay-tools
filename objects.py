#
#   Network Ten CatchUp TV Video API Library
#
#   Copyright (c) 2013 Adam Malcontenti-Wilson
# 
#   Permission is hereby granted, free of charge, to any person obtaining a copy
#   of this software and associated documentation files (the "Software"), to deal
#   in the Software without restriction, including without limitation the rights
#   to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#   copies of the Software, and to permit persons to whom the Software is
#   furnished to do so, subject to the following conditions:
# 
#   The above copyright notice and this permission notice shall be included in
#   all copies or substantial portions of the Software.
# 
#   THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#   IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#   FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#   AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#   LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#   OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
#   THE SOFTWARE.
#

from brightcove.core import APIObject, Field, DateTimeField, ListField, EnumField
from brightcove.objects import ItemCollection, enum

ChannelNameEnum = enum('ten', 'eleven', 'one')
PlaylistTypeEnum = enum('full_episodes', 'web_extras', 'news', 'season', 'week', 'category', 'special', 'preview')
MediaDeliveryEnum = enum('default', 'http', 'http_ios')

class EnumNumField(Field):
    def __init__(self, enum_cls, help=None):
        self.help = help
        self.enum_cls = enum_cls

    def to_python(self, value):
        for i, field in enumerate(self.enum_cls._fields):
            if i == value:
                return field
        raise Exception('Invalid Enum: %s' % value)

    def from_python(self, value):
        return self.enum_cls._fields[value]

class Playlist(APIObject):
  _fields = ['name', 'type', 'season', 'week', 'query']
  type = EnumField(PlaylistTypeEnum)

  def __repr__(self):
    return '<Playlist name=\'{0}\'>'.format(self.name)

class Show(APIObject):
  _fields = ['showName', 'channelName', 'videoLink', 'mobileLink', 'logo', 'fanart', 'playlists', 'tvdbSeriesId']
  channelName = EnumField(ChannelNameEnum)
  playlists = ListField(Playlist)

  def __repr__(self):
    return '<Show name=\'{0}\'>'.format(self.showName)

class AMFRendition(APIObject):
  _fields = ['defaultURL', 'audioOnly', 'mediaDeliveryType', 'encodingRate',
               'frameHeight', 'frameWidth', 'size', 
               'videoCodec', 'videoContainer']
  mediaDeliveryType = EnumNumField(MediaDeliveryEnum)

  def __repr__(self):
    return '<Rendition bitrate=\'{0}\' type=\'{1}\' frameSize=\'{2}x{3}\'>'.format(self.encodingRate, self.mediaDeliveryType, self.frameWidth, self.frameHeight)

class ShowItemCollection(ItemCollection):
  _item_class = Show
  items = ListField(Show)

class PlaylistItemCollection(ItemCollection):
  _item_class = Playlist
  items = ListField(Playlist)

class MediaRenditionItemCollection(ItemCollection):
  _item_class = AMFRendition
  items = ListField(AMFRendition)

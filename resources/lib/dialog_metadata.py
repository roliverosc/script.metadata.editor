#!/usr/bin/python
# coding: utf-8

########################

from resources.lib.helper import *
from resources.lib.json_map import *
from resources.lib.utils import *

########################

class EditDialog(object):
    def __init__(self,params):
        self.params = params
        self.dbid = params.get('dbid')
        self.dbtype = params.get('type')

        if self.dbtype in ['movie', 'tvshow', 'season', 'episode', 'musicvideo']:
            library = 'Video'
            self.nfo_support = True
        else:
            library = 'Audio'
            self.nfo_support = False

        self.method_details = '%sLibrary.Get%sDetails' % (library, self.dbtype)
        self.param = '%sid' % self.dbtype
        self.key_details = '%sdetails' % self.dbtype
        self.properties = eval('%s_properties' % self.dbtype)

        winprop('SelectDialogPreselect', clear=True)

        self.init()

    def init(self):
        self.details = self.get_details()

        self.modeselect = []
        self.keylist = []
        self.presetlist = []
        self.typelist = []
        self.xmllist = []

        self.generate_list()
        self.field_dialog()

    def field_dialog(self):
        preselect = winprop('SelectDialogPreselect')
        if not preselect:
            preselect = -1

        self.editdialog = DIALOG.select(xbmc.getLocalizedString(14241), self.modeselect, preselect=int(preselect), useDetails=True)

        if self.editdialog == -1:
            winprop('SelectDialogPreselect', clear=True)
            return

        winprop('SelectDialogPreselect', str(self.editdialog))

        write_db(value_type=self.typelist[self.editdialog],
                 dbid=self.dbid,
                 dbtype=self.dbtype,
                 string=self.keylist[self.editdialog],
                 preset=self.presetlist[self.editdialog],
                 xml=self.xmllist[self.editdialog],
                 details=self.details,
                 file=self.details.get('file'),
                 update_nfo=self.nfo_support
                 )

        self.init()

    def get_details(self):
        json_query = json_call(self.method_details,
                               properties=self.properties,
                               params={self.param: int(self.dbid)}
                               )
        try:
            result = json_query['result'][self.key_details]
            return result

        except KeyError:
            return

    def generate_list(self):
        details = self.details

        if self.dbtype == 'movie':
            '''
            x [ Optional.String title ]
            [ Optional.Integer playcount ]
            [ Optional.Integer runtime ] Runtime in seconds
            x [ mixed director ]
            x [ mixed studio ]
            x [ Optional.Integer year ] linked with premiered. Overridden by premiered parameter
            x [ Optional.String plot ]
            x [ mixed genre ]
            x [ Optional.Number rating ]
            x [ Optional.String mpaa ]
            x [ Optional.String imdbnumber ]
            x [ Optional.String votes ]
            [ Optional.String lastplayed ]
            x [ Optional.String originaltitle ]
            x [ Optional.String trailer ]
            x [ Optional.String tagline ]
            x [ Optional.String plotoutline ]
            x [ mixed writer ]
            x [ mixed country ]
            x [ Optional.Integer top250 ]
            x [ Optional.String sorttitle ]
            [ Optional.String set ]
            [ mixed showlink ]
            [ Optional.String thumbnail ]
            [ Optional.String fanart ]
            x [ mixed tag ]
            [ mixed art ]
            [ mixed resume ]
            x [ Optional.Integer userrating ]
            [ Video.Ratings.Set ratings ]
            [ Optional.String dateadded ]
            x [ Optional.String premiered ] linked with year. Overriedes year
            x [ mixed uniqueid ]
            '''
            self._create_list(xbmc.getLocalizedString(369), 'title', value=details.get('title'), type='string')
            self._create_list(xbmc.getLocalizedString(20376), 'originaltitle', value=details.get('originaltitle'), type='string')
            self._create_list(xbmc.getLocalizedString(171), 'sorttitle', value=details.get('sorttitle'), type='string')
            self._create_list(xbmc.getLocalizedString(345) + ' / ' + xbmc.getLocalizedString(172), 'premiered', value=details.get('premiered'), type='date')
            self._create_list(xbmc.getLocalizedString(515), 'genre', value=get_joined_items(details.get('genre')), type='array')
            self._create_list(xbmc.getLocalizedString(563), 'rating', value=str(get_rounded_value(details.get('rating'))), type='float')
            self._create_list(xbmc.getLocalizedString(205), 'votes', value=str(details.get('votes')), type='integer')
            self._create_list(ADDON.getLocalizedString(32001), 'userrating', value=str(details.get('userrating')), type='integer')
            self._create_list(xbmc.getLocalizedString(20074), 'mpaa', value=details.get('mpaa'), type='string')
            self._create_list(xbmc.getLocalizedString(202), 'tagline', value=details.get('tagline'), type='string')
            self._create_list(xbmc.getLocalizedString(207), 'plot', value=details.get('plot'), type='string')
            self._create_list(xbmc.getLocalizedString(203), 'plotoutline', value=details.get('plotoutline'), type='string', xml='outline')
            self._create_list(xbmc.getLocalizedString(20339), 'director', value=get_joined_items(details.get('director')), type='array')
            self._create_list(xbmc.getLocalizedString(20417), 'writer', value=get_joined_items(details.get('writer')), type='array')
            self._create_list(xbmc.getLocalizedString(20457), 'set', value=details.get('set'), type='string')
            self._create_list(xbmc.getLocalizedString(21875), 'country', value=get_joined_items(details.get('country')), type='array')
            self._create_list(xbmc.getLocalizedString(572), 'studio', value=get_joined_items(details.get('studio')), type='array')
            self._create_list(xbmc.getLocalizedString(20459), 'tag', value=get_joined_items(details.get('tag')), type='array')
            self._create_list(xbmc.getLocalizedString(20410), 'trailer', value=details.get('trailer'), type='string')
            self._create_list(xbmc.getLocalizedString(13409), 'top250', value=str(details.get('top250')), type='integer')
            self._create_list('IMDb ID', 'uniqueid', value=get_key_item(details.get('uniqueid'),'imdb'), type='uniqueid_imdb')
            self._create_list('TMDb ID', 'uniqueid', value=get_key_item(details.get('uniqueid'),'tmdb'), type='uniqueid_tmdb')
            self._create_list(xbmc.getLocalizedString(570), 'dateadded', value=details.get('dateadded'), type='string')

        elif self.dbtype == 'tvshow':
            '''
            x [ Optional.String title ]
            x [ Optional.Integer playcount ]
            x [ mixed studio ]
            x [ Optional.String plot ]
            x [ mixed genre ]
            x [ Optional.Number rating ]
            x [ Optional.String mpaa ]
            x [ Optional.String imdbnumber ]
            x [ Optional.String premiered ]
            x [ Optional.String votes ]
            [ Optional.String lastplayed ]
            x [ Optional.String originaltitle ]
            x [ Optional.String sorttitle ]
            [ Optional.String episodeguide ]
            [ Optional.String thumbnail ]
            [ Optional.String fanart ]
            x [ mixed tag ]
            [ mixed art ]
            x [ Optional.Integer userrating ]
            [ Video.Ratings.Set ratings ]
            x [ Optional.String dateadded ]
            [ Optional.Integer runtime ] Runtime in seconds
            [ Optional.String status ]
            x [ mixed uniqueid ]
            '''
            self._create_list(xbmc.getLocalizedString(369), 'title', value=details.get('title'), type='string')
            self._create_list(xbmc.getLocalizedString(20376),'originaltitle', value=details.get('originaltitle'), type='string')
            self._create_list(xbmc.getLocalizedString(171), 'sorttitle', value=details.get('sorttitle'), type='string')
            self._create_list(xbmc.getLocalizedString(345) + ' / ' + xbmc.getLocalizedString(172), 'premiered', value=details.get('premiered'), type='date')
            self._create_list(xbmc.getLocalizedString(515), 'genre', value=get_joined_items(details.get('genre')), type='array')
            self._create_list(xbmc.getLocalizedString(563), 'rating', value=str(get_rounded_value(details.get('rating'))), type='float')
            self._create_list(xbmc.getLocalizedString(205), 'votes', value=str(details.get('votes')), type='integer')
            self._create_list(ADDON.getLocalizedString(32001), 'userrating', value=str(details.get('userrating')), type='integer')
            self._create_list(xbmc.getLocalizedString(20074), 'mpaa', value=details.get('mpaa'), type='string')
            self._create_list(xbmc.getLocalizedString(207), 'plot', value=details.get('plot'), type='string')
            self._create_list(xbmc.getLocalizedString(572), 'studio', value=get_joined_items(details.get('studio')), type='array')
            self._create_list(xbmc.getLocalizedString(20459), 'tag', value=get_joined_items(details.get('tag')), type='array')
            #self._create_list(xbmc.getLocalizedString(126), 'status', value=details.get('status'), type='string') not available in GetDetails
            self._create_list('IMDb ID', 'uniqueid', value=get_key_item(details.get('uniqueid'),'imdb'), type='uniqueid_imdb')
            self._create_list('TMDb ID', 'uniqueid', value=get_key_item(details.get('uniqueid'),'tmdb'), type='uniqueid_tmdb')
            self._create_list('TVDb ID', 'uniqueid', value=get_key_item(details.get('uniqueid'),'tvdb'), type='uniqueid_tvdb')
            self._create_list(xbmc.getLocalizedString(570), 'dateadded', value=details.get('dateadded'), type='string')

        elif self.dbtype == 'episode':
            '''
            x [ Optional.String title ]
            x [ Optional.Integer playcount ]
            [ Optional.Integer runtime ] Runtime in seconds
            x [ mixed director ]
            x [ Optional.String plot ]
            x [ Optional.Number rating ]
            x [ Optional.String votes ]
            [ Optional.String lastplayed ]
            x [ mixed writer ]
            x [ Optional.String firstaired ]
            [ Optional.String productioncode ]
            x [ Optional.Integer season ]
            x [ Optional.Integer episode ]
            x [ Optional.String originaltitle ]
            [ Optional.String thumbnail ]
            [ Optional.String fanart ]
            [ mixed art ]
            [ mixed resume ]
            x [ Optional.Integer userrating ]
            [ Video.Ratings.Set ratings ]
            x [ Optional.String dateadded ]
            x [ mixed uniqueid ]
            '''
            self._create_list(xbmc.getLocalizedString(369), 'title', value=details.get('title'), type='string')
            self._create_list(xbmc.getLocalizedString(20376), 'originaltitle', value=details.get('originaltitle'), type='string')
            self._create_list(xbmc.getLocalizedString(20359), 'episode', value=str(details.get('episode')), type='integer')
            self._create_list(xbmc.getLocalizedString(20373), 'season', value=str(details.get('season')), type='integer')
            self._create_list(xbmc.getLocalizedString(20416), 'firstaired', value=details.get('firstaired'), type='date')
            self._create_list(xbmc.getLocalizedString(563), 'rating', value=str(get_rounded_value(details.get('rating'))), type='float')
            self._create_list(xbmc.getLocalizedString(205), 'votes', value=str(details.get('votes')), type='integer')
            self._create_list(ADDON.getLocalizedString(32001), 'userrating', value=str(details.get('userrating')), type='integer')
            self._create_list(xbmc.getLocalizedString(207), 'plot', value=details.get('plot'), type='string')
            self._create_list(xbmc.getLocalizedString(20339), 'director', value=get_joined_items(details.get('director')), type='array')
            self._create_list(xbmc.getLocalizedString(20417), 'writer', value=get_joined_items(details.get('writer')), type='array')
            self._create_list('IMDb ID', 'uniqueid', value=get_key_item(details.get('uniqueid'),'imdb'), type='uniqueid_imdb')
            self._create_list('TMDb ID', 'uniqueid', value=get_key_item(details.get('uniqueid'),'tmdb'), type='uniqueid_tmdb')
            self._create_list('TVDb ID', 'uniqueid', value=get_key_item(details.get('uniqueid'),'tvdb'), type='uniqueid_tvdb')
            self._create_list(xbmc.getLocalizedString(570), 'dateadded', value=details.get('dateadded'), type='string')

        elif self.dbtype == 'artist':
            '''
            x [ Optional.String artist ]
            x [ mixed instrument ]
            x [ mixed style ]
            x [ mixed mood ]
            x [ Optional.String born ]
            x [ Optional.String formed ]
            x [ Optional.String description ]
            x [ mixed genre ]
            x [ Optional.String died ]
            x [ Optional.String disbanded ]
            x [ mixed yearsactive ]
            '''
            self._create_list(xbmc.getLocalizedString(21899), 'artist', value=details.get('artist'), type='string')
            self._create_list(xbmc.getLocalizedString(515), 'genre', value=get_joined_items(details.get('genre')), type='array')
            self._create_list(xbmc.getLocalizedString(21892), 'instrument', value=get_joined_items(details.get('instrument')), type='array')
            self._create_list(xbmc.getLocalizedString(736), 'style', value=get_joined_items(details.get('style')), type='array')
            self._create_list(xbmc.getLocalizedString(175), 'mood', value=get_joined_items(details.get('mood')), type='array')
            self._create_list(xbmc.getLocalizedString(21893), 'born', value=details.get('born'), type='string')
            self._create_list(xbmc.getLocalizedString(21897), 'died', value=details.get('died'), type='string')
            self._create_list(xbmc.getLocalizedString(21894), 'formed', value=details.get('formed'), type='string')
            self._create_list(xbmc.getLocalizedString(21896), 'disbanded', value=details.get('disbanded'), type='string')
            self._create_list(xbmc.getLocalizedString(21821), 'description', value=details.get('description'), type='string')
            self._create_list(xbmc.getLocalizedString(21898), 'yearsactive', value=get_joined_items(details.get('yearsactive')), type='array')

        elif self.dbtype == 'album':
            '''
            x [ Optional.String title ]
            x [ mixed artist ]
            x [ Optional.String description ]
            x [ mixed genre ]
            x [ mixed theme ]
            x [ mixed mood ]
            x [ mixed style ]
            x [ Optional.String type ]
            [ Optional.String albumlabel ]
            x [ Optional.Number rating ]
            x [ Optional.Integer year ]
            x [ Optional.Integer userrating ]
            x [ Optional.Integer votes ]
            '''
            self._create_list(xbmc.getLocalizedString(21899), 'title', value=details.get('title'), type='string')
            self._create_list(xbmc.getLocalizedString(467), 'type', value=details.get('type'), type='string')
            #self._create_list(xbmc.getLocalizedString(21899), 'albumlabel', value=details.get('albumlabel'), type='string')
            self._create_list(xbmc.getLocalizedString(345), 'year', value=str(details.get('year')), type='integer')
            self._create_list(xbmc.getLocalizedString(133), 'artist', value=get_joined_items(details.get('artist')), type='array')
            self._create_list(xbmc.getLocalizedString(21821), 'description', value=details.get('description'), type='string')
            self._create_list(xbmc.getLocalizedString(515), 'genre', value=get_joined_items(details.get('genre')), type='array')
            self._create_list(xbmc.getLocalizedString(15111), 'theme', value=get_joined_items(details.get('theme')), type='array')
            self._create_list(xbmc.getLocalizedString(175), 'mood', value=get_joined_items(details.get('mood')), type='array')
            self._create_list(xbmc.getLocalizedString(736), 'style', value=get_joined_items(details.get('style')), type='array')
            self._create_list(xbmc.getLocalizedString(563), 'rating', value=str(get_rounded_value(details.get('rating'))), type='float')
            self._create_list(xbmc.getLocalizedString(205), 'votes', value=str(details.get('votes')), type='integer')
            self._create_list(ADDON.getLocalizedString(32001), 'userrating', value=str(details.get('userrating')), type='integer')

        elif self.dbtype == 'song':
            '''
            x [ Optional.String title ]
            x [ mixed artist ]
            x [ mixed albumartist ]
            x [ mixed genre ]
            x [ Optional.Integer year ]
            x [ Optional.Number rating ]
            x [ Optional.String album ]
            x [ Optional.Integer track ]
            x [ Optional.Integer disc ]
            [ Optional.Integer duration ]
            x [ Optional.String comment ]
            x [ Optional.String musicbrainztrackid ]
            x [ Optional.String musicbrainzartistid ] -> wrong. is array.
            x [ Optional.String musicbrainzalbumid ]
            x [ Optional.String musicbrainzalbumartistid ] -> wrong. is array.
            [ Optional.Integer playcount ]
            [ Optional.String lastplayed ]
            x[ Optional.Integer userrating ]
            [ Optional.Integer votes ]
            '''
            self._create_list(xbmc.getLocalizedString(21899), 'title', value=details.get('title'), type='string')
            self._create_list(xbmc.getLocalizedString(558), 'album', value=details.get('album'), type='string')
            self._create_list(xbmc.getLocalizedString(554), 'track', value=str(details.get('track')), type='integer')
            self._create_list(xbmc.getLocalizedString(427), 'disc', value=str(details.get('disc')), type='integer')
            self._create_list(xbmc.getLocalizedString(133), 'artist', value=get_joined_items(details.get('artist')), type='array')
            self._create_list(xbmc.getLocalizedString(566), 'albumartist', value=get_joined_items(details.get('albumartist')), type='array')
            self._create_list(xbmc.getLocalizedString(515), 'genre', value=get_joined_items(details.get('genre')), type='array')
            self._create_list(xbmc.getLocalizedString(345), 'year', value=str(details.get('year')), type='integer')
            self._create_list(xbmc.getLocalizedString(569), 'comment', value=details.get('comment'), type='string')
            self._create_list(xbmc.getLocalizedString(563), 'rating', value=str(get_rounded_value(details.get('rating'))), type='float')
            self._create_list(xbmc.getLocalizedString(205), 'votes', value=str(details.get('votes')), type='integer')
            self._create_list(ADDON.getLocalizedString(32001), 'userrating', value=str(details.get('userrating')), type='integer')
            self._create_list('MusicBrainz Track-ID', 'musicbrainztrackid', value=details.get('musicbrainztrackid'), type='string')
            self._create_list('MusicBrainz Artist-ID', 'musicbrainzartistid', value=get_joined_items(details.get('musicbrainzartistid')), type='array')
            self._create_list('MusicBrainz Album-ID', 'musicbrainzalbumid', value=details.get('musicbrainzalbumid'), type='string')
            self._create_list('MusicBrainz Album-Artist-ID', 'musicbrainzalbumartistid', value=get_joined_items(details.get('musicbrainzalbumartistid')), type='array')

        elif self.dbtype == 'musicvideo':
            '''
            x [ Optional.String title ]
            [ Optional.Integer playcount ]
            [ Optional.Integer runtime ] Runtime in seconds
            x [ mixed director ]
            x [ mixed studio ]
            x [ Optional.Integer year ] linked with premiered. Overridden by premiered parameter
            x [ Optional.String plot ]
            x [ Optional.String album ]
            x [ mixed artist ]
            x [ mixed genre ]
            x [ Optional.Integer track ]
            [ Optional.String lastplayed ]
            [ Optional.String thumbnail ]
            [ Optional.String fanart ]
            x [ mixed tag ]
            [ mixed art ]
            [ mixed resume ]
            x [ Optional.Number rating ]
            x [ Optional.Integer userrating ]
            x [ Optional.String dateadded ]
            x [ Optional.String premiered ] linked with year. Overriedes year
            '''
            self._create_list(xbmc.getLocalizedString(369), 'title', value=details.get('title'), type='string')
            self._create_list(xbmc.getLocalizedString(558), 'album', value=details.get('album'), type='string')
            self._create_list(xbmc.getLocalizedString(345) + ' / ' + xbmc.getLocalizedString(172), 'premiered', value=details.get('premiered'), type='date')
            self._create_list(xbmc.getLocalizedString(515), 'genre', value=get_joined_items(details.get('genre')), type='array')
            self._create_list(xbmc.getLocalizedString(207), 'plot', value=details.get('plot'), type='string')
            self._create_list(xbmc.getLocalizedString(557), 'artist', value=get_joined_items(details.get('artist')), type='array')
            self._create_list(xbmc.getLocalizedString(20339), 'director', value=get_joined_items(details.get('director')), type='array')
            self._create_list(xbmc.getLocalizedString(572), 'studio', value=get_joined_items(details.get('studio')), type='array')
            self._create_list(xbmc.getLocalizedString(20459), 'tag', value=get_joined_items(details.get('tag')), type='array')
            self._create_list(xbmc.getLocalizedString(563), 'rating', value=str(get_rounded_value(details.get('rating'))), type='float')
            self._create_list(xbmc.getLocalizedString(554), 'track', value=str(details.get('track')), type='integer')
            self._create_list(ADDON.getLocalizedString(32001), 'userrating', value=details.get('userrating'), type='integer')
            self._create_list(xbmc.getLocalizedString(570), 'dateadded', value=details.get('dateadded'), type='string')


    def _create_list(self,label,key,type,value,xml=None):
        value = 'n/a' if not value else value
        xml = key if not xml else xml
        icon = type if not type.startswith('uniqueid') else 'string'

        li_item = xbmcgui.ListItem(label=label, label2=value)
        li_item.setArt({'icon': 'special://home/addons/script.metadata.editor/resources/media/%s.png' % icon})

        self.modeselect.append(li_item)
        self.keylist.append(key)
        self.typelist.append(type)
        self.xmllist.append(xml)

        if value:
            self.presetlist.append(value)
        else:
            self.presetlist.append('')
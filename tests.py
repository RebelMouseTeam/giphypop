from unittest import TestCase

from mock import Mock, patch

from giphypop import (AttrDict,
                      Giphy,
                      GiphyApiException,
                      GiphyImage,
                      search,
                      search_list,
                      translate,
                      gif,
                      screensaver)


# TEST DATA
FAKE_DATA = {
    "bitly_fullscreen_url": "http://gph.is/XH7Sri",
    "bitly_gif_url": "http://gph.is/XH7V6j",
    "bitly_tiled_url": "http://gph.is/XH7Srk",
    "id": "3avUsGhmckIYE",
    "images": {
        "fixed_height": {
            "height": "200",
            "url": "http://media.giphy.com/media/3avUsGhmckIYE/200.gif",
            "width": "289"
        },
        "fixed_height_downsampled": {
            "height": "200",
            "url": "http://media.giphy.com/media/3avUsGhmckIYE/200_d.gif",
            "width": "289"
        },
        "fixed_height_still": {
            "height": "200",
            "url": "http://media.giphy.com/media/3avUsGhmckIYE/200_s.gif",
            "width": "289"
        },
        "fixed_width": {
            "height": "138",
            "url": "http://media.giphy.com/media/3avUsGhmckIYE/200w.gif",
            "width": "200"
        },
        "fixed_width_downsampled": {
            "height": "138",
            "url": "http://media.giphy.com/media/3avUsGhmckIYE/200w_d.gif",
            "width": "200"
        },
        "fixed_width_still": {
            "height": "138",
            "url": "http://media.giphy.com/media/3avUsGhmckIYE/200w_s.gif",
            "width": "200"
        },
        "original": {
            "height": "346",
            "url": "http://media.giphy.com/media/3avUsGhmckIYE/giphy.gif",
            "width": "500",
            "frames": "100",
            "size": "123",
        }
    },
    "type": "gif",
    "url": "http://giphy.com/gifs/3avUsGhmckIYE"
}

FAKE_DATA_RECENT = [{u'bitly_gif_url': u'http://gph.is/1ixq1i1',
  u'bitly_url': u'http://gph.is/1ixq1i1',
  u'embed_url': u'http://giphy.com/embed/9cwKs74Hfwkvu',
  u'id': u'9cwKs74Hfwkvu',
  u'images': {u'fixed_height': {u'height': u'200',
                                u'url': u'http://media0.giphy.com/media/9cwKs74Hfwkvu/200.gif',
                                u'width': u'388'},
              u'fixed_height_downsampled': {u'height': u'200',
                                            u'url': u'http://media0.giphy.com/media/9cwKs74Hfwkvu/200_d.gif',
                                            u'width': u'388'},
              u'fixed_height_still': {u'height': u'200',
                                      u'url': u'http://media0.giphy.com/media/9cwKs74Hfwkvu/200_s.gif',
                                      u'width': u'388'},
              u'fixed_width': {u'height': u'103',
                               u'url': u'http://media0.giphy.com/media/9cwKs74Hfwkvu/200w.gif',
                               u'width': u'200'},
              u'fixed_width_downsampled': {u'height': u'103',
                                           u'url': u'http://media0.giphy.com/media/9cwKs74Hfwkvu/200w_d.gif',
                                           u'width': u'200'},
              u'fixed_width_still': {u'height': u'103',
                                     u'url': u'http://media0.giphy.com/media/9cwKs74Hfwkvu/200w_s.gif',
                                     u'width': u'200'},
              u'original': {u'frames': u'7',
                            u'height': u'258',
                            u'size': u'488020',
                            u'url': u'http://media0.giphy.com/media/9cwKs74Hfwkvu/giphy.gif',
                            u'width': u'500'}},
  u'type': u'gif',
  u'url': u'http://giphy.com/gifs/9cwKs74Hfwkvu'},
 {u'bitly_gif_url': u'http://gph.is/N9B4o6',
  u'bitly_url': u'http://gph.is/N9B4o6',
  u'embed_url': u'http://giphy.com/embed/QIWpM84uTbhmg',
  u'id': u'QIWpM84uTbhmg',
  u'images': {u'fixed_height': {u'height': u'200',
                                u'url': u'http://media1.giphy.com/media/QIWpM84uTbhmg/200.gif',
                                u'width': u'258'},
              u'fixed_height_downsampled': {u'height': u'200',
                                            u'url': u'http://media1.giphy.com/media/QIWpM84uTbhmg/200_d.gif',
                                            u'width': u'258'},
              u'fixed_height_still': {u'height': u'200',
                                      u'url': u'http://media1.giphy.com/media/QIWpM84uTbhmg/200_s.gif',
                                      u'width': u'258'},
              u'fixed_width': {u'height': u'155',
                               u'url': u'http://media1.giphy.com/media/QIWpM84uTbhmg/200w.gif',
                               u'width': u'200'},
              u'fixed_width_downsampled': {u'height': u'155',
                                           u'url': u'http://media1.giphy.com/media/QIWpM84uTbhmg/200w_d.gif',
                                           u'width': u'200'},
              u'fixed_width_still': {u'height': u'155',
                                     u'url': u'http://media1.giphy.com/media/QIWpM84uTbhmg/200w_s.gif',
                                     u'width': u'200'},
              u'original': {u'frames': u'25',
                            u'height': u'194',
                            u'size': u'1105075',
                            u'url': u'http://media1.giphy.com/media/QIWpM84uTbhmg/giphy.gif',
                            u'width': u'250'}},
  u'type': u'gif',
  u'url': u'http://giphy.com/gifs/QIWpM84uTbhmg'},
 {u'bitly_gif_url': u'http://gph.is/LBYtge',
  u'bitly_url': u'http://gph.is/LBYtge',
  u'embed_url': u'http://giphy.com/embed/mxt1DW6JbjTSo',
  u'id': u'mxt1DW6JbjTSo',
  u'images': {u'fixed_height': {u'height': u'200',
                                u'url': u'http://media2.giphy.com/media/mxt1DW6JbjTSo/200.gif',
                                u'width': u'200'},
              u'fixed_height_downsampled': {u'height': u'200',
                                            u'url': u'http://media2.giphy.com/media/mxt1DW6JbjTSo/200_d.gif',
                                            u'width': u'200'},
              u'fixed_height_still': {u'height': u'200',
                                      u'url': u'http://media2.giphy.com/media/mxt1DW6JbjTSo/200_s.gif',
                                      u'width': u'200'},
              u'fixed_width': {u'height': u'200',
                               u'url': u'http://media2.giphy.com/media/mxt1DW6JbjTSo/200w.gif',
                               u'width': u'200'},
              u'fixed_width_downsampled': {u'height': u'200',
                                           u'url': u'http://media2.giphy.com/media/mxt1DW6JbjTSo/200w_d.gif',
                                           u'width': u'200'},
              u'fixed_width_still': {u'height': u'200',
                                     u'url': u'http://media2.giphy.com/media/mxt1DW6JbjTSo/200w_s.gif',
                                     u'width': u'200'},
              u'original': {u'frames': u'4',
                            u'height': u'500',
                            u'size': u'88666',
                            u'url': u'http://media2.giphy.com/media/mxt1DW6JbjTSo/giphy.gif',
                            u'width': u'500'}},
  u'type': u'gif',
  u'url': u'http://giphy.com/gifs/mxt1DW6JbjTSo'}]

FAKE_DATA_RELEVANT = [{u'bitly_gif_url': u'http://gph.is/XIp6Vb',
  u'bitly_url': u'http://gph.is/XIp6Vb',
  u'embed_url': u'http://giphy.com/embed/CHc9dLQVQOAXm',
  u'id': u'CHc9dLQVQOAXm',
  u'images': {u'fixed_height': {u'height': u'200',
                                u'url': u'http://media2.giphy.com/media/CHc9dLQVQOAXm/200.gif',
                                u'width': u'340'},
              u'fixed_height_downsampled': {u'height': u'200',
                                            u'url': u'http://media2.giphy.com/media/CHc9dLQVQOAXm/200_d.gif',
                                            u'width': u'340'},
              u'fixed_height_still': {u'height': u'200',
                                      u'url': u'http://media2.giphy.com/media/CHc9dLQVQOAXm/200_s.gif',
                                      u'width': u'340'},
              u'fixed_width': {u'height': u'118',
                               u'url': u'http://media2.giphy.com/media/CHc9dLQVQOAXm/200w.gif',
                               u'width': u'200'},
              u'fixed_width_downsampled': {u'height': u'118',
                                           u'url': u'http://media1.giphy.com/media/CHc9dLQVQOAXm/200w_d.gif',
                                           u'width': u'200'},
              u'fixed_width_still': {u'height': u'118',
                                     u'url': u'http://media2.giphy.com/media/CHc9dLQVQOAXm/200w_s.gif',
                                     u'width': u'200'},
              u'original': {u'frames': u'46',
                            u'height': u'206',
                            u'size': u'1021747',
                            u'url': u'http://media0.giphy.com/media/CHc9dLQVQOAXm/giphy.gif',
                            u'width': u'350'}},
  u'type': u'gif',
  u'url': u'http://giphy.com/gifs/CHc9dLQVQOAXm'},
 {u'bitly_gif_url': u'http://gph.is/XL4dZt',
  u'bitly_url': u'http://gph.is/XL4dZt',
  u'embed_url': u'http://giphy.com/embed/QBtzAnMFO5i9O',
  u'id': u'QBtzAnMFO5i9O',
  u'images': {u'fixed_height': {u'height': u'200',
                                u'url': u'http://media0.giphy.com/media/QBtzAnMFO5i9O/200.gif',
                                u'width': u'306'},
              u'fixed_height_downsampled': {u'height': u'200',
                                            u'url': u'http://media2.giphy.com/media/QBtzAnMFO5i9O/200_d.gif',
                                            u'width': u'306'},
              u'fixed_height_still': {u'height': u'200',
                                      u'url': u'http://media1.giphy.com/media/QBtzAnMFO5i9O/200_s.gif',
                                      u'width': u'306'},
              u'fixed_width': {u'height': u'131',
                               u'url': u'http://media2.giphy.com/media/QBtzAnMFO5i9O/200w.gif',
                               u'width': u'200'},
              u'fixed_width_downsampled': {u'height': u'131',
                                           u'url': u'http://media3.giphy.com/media/QBtzAnMFO5i9O/200w_d.gif',
                                           u'width': u'200'},
              u'fixed_width_still': {u'height': u'131',
                                     u'url': u'http://media0.giphy.com/media/QBtzAnMFO5i9O/200w_s.gif',
                                     u'width': u'200'},
              u'original': {u'frames': u'28',
                            u'height': u'160',
                            u'size': u'729141',
                            u'url': u'http://media3.giphy.com/media/QBtzAnMFO5i9O/giphy.gif',
                            u'width': u'245'}},
  u'type': u'gif',
  u'url': u'http://giphy.com/gifs/QBtzAnMFO5i9O'},
 {u'bitly_gif_url': u'http://gph.is/1jjxRxn',
  u'bitly_url': u'http://gph.is/1jjxRxn',
  u'embed_url': u'http://giphy.com/embed/ODy29v7YAJrck',
  u'id': u'ODy29v7YAJrck',
  u'images': {u'fixed_height': {u'height': u'200',
                                u'url': u'http://media2.giphy.com/media/ODy29v7YAJrck/200.gif',
                                u'width': u'356'},
              u'fixed_height_downsampled': {u'height': u'200',
                                            u'url': u'http://media2.giphy.com/media/ODy29v7YAJrck/200_d.gif',
                                            u'width': u'356'},
              u'fixed_height_still': {u'height': u'200',
                                      u'url': u'http://media2.giphy.com/media/ODy29v7YAJrck/200_s.gif',
                                      u'width': u'356'},
              u'fixed_width': {u'height': u'112',
                               u'url': u'http://media2.giphy.com/media/ODy29v7YAJrck/200w.gif',
                               u'width': u'200'},
              u'fixed_width_downsampled': {u'height': u'112',
                                           u'url': u'http://media2.giphy.com/media/ODy29v7YAJrck/200w_d.gif',
                                           u'width': u'200'},
              u'fixed_width_still': {u'height': u'112',
                                     u'url': u'http://media2.giphy.com/media/ODy29v7YAJrck/200w_s.gif',
                                     u'width': u'200'},
              u'original': {u'frames': u'16',
                            u'height': u'281',
                            u'size': u'512364',
                            u'url': u'http://media2.giphy.com/media/ODy29v7YAJrck/giphy.gif',
                            u'width': u'500'}},
  u'type': u'gif',
  u'url': u'http://giphy.com/gifs/ODy29v7YAJrck'}]

class AttrDictTestCase(TestCase):

    def test_get_attribute_raises(self):
        foo = AttrDict()
        self.assertRaises(AttributeError, lambda: foo.bar)

    def test_get_attribte(self):
        foo = AttrDict(bar='baz')
        assert foo.bar == 'baz'

    def test_get_attribute_proxies_key(self):
        foo = AttrDict(bar='baz')
        foo['bar'] = 'baz'
        assert foo.bar == 'baz'

    def test_set_attribute(self):
        foo = AttrDict()
        foo.bar = 'baz'
        assert foo.bar == 'baz'

    def test_set_attribute_proxies_key(self):
        foo = AttrDict()
        foo.bar = 'baz'
        assert foo['bar'] == 'baz'

    def test_hasattr(self):
        foo = AttrDict(bar='baz')
        assert hasattr(foo, 'bar')
        assert not hasattr(foo, 'baz')

    def test_with_property(self):
        class Foo(AttrDict):
            @property
            def foo(self):
                return 'bar'

        foo = Foo()
        assert foo.foo == 'bar'


class GiphyImageCase(TestCase):

    def test_normalize(self):
        result = GiphyImage()
        norm = result._normalized({
            'width': '200',
            'height': 300,
            'something': 'foo',
            'frames': '100',
            'size': '1234567890'
        })

        assert isinstance(norm['width'], int)
        assert isinstance(norm['height'], int)
        assert isinstance(norm['frames'], int)
        assert isinstance(norm['size'], int)
        assert isinstance(norm['something'], str)

    def test_make_images_creates_attribute(self):
        # Expect that make_images will create an attribute with key name
        result = GiphyImage()
        img = {'original': FAKE_DATA['images']['original']}

        assert not hasattr(result, 'original')
        result._make_images(img)
        assert hasattr(result, 'original')

    def test_make_images_doesnt_subattr(self):
        # If there is a single underscore, don't subattr
        result = GiphyImage()
        img = {'fixed_width': FAKE_DATA['images']['fixed_width']}

        assert not hasattr(result, 'fixed')
        assert not hasattr(result, 'fixed_width')
        result._make_images(img)
        assert not hasattr(result, 'fixed')
        assert hasattr(result, 'fixed_width')

    def test_make_images_creates_subattr(self):
        result = GiphyImage()
        img = {'fixed_width': FAKE_DATA['images']['fixed_width'],
               'fixed_width_still': FAKE_DATA['images']['fixed_width_still']}

        assert not hasattr(result, 'fixed_width')
        result._make_images(img)
        assert hasattr(result, 'fixed_width')
        assert hasattr(result.fixed_width, 'still')

    def test_original_properties(self):
        result = GiphyImage()
        img = {'original': FAKE_DATA['images']['original']}
        props = {
            'media_url': 'url',
            'frames': 'frames',
            'width': 'width',
            'height': 'height',
            'filesize': 'size'
        }

        for prop in props:
            self.assertRaises(AttributeError, lambda: getattr(result, prop))

        result._make_images(img)

        for prop, attr in props.items():
            assert getattr(result, prop) == getattr(result.original, attr)


class GiphyTestCase(TestCase):

    def runTest(self):
        pass

    def setUp(self):
        self.g = Giphy()

    def test_endpoint(self):
        assert self.g._endpoint('search') == 'http://api.giphy.com/v1/gifs/search'

    def test_check_or_raise_raises(self):
        self.assertRaises(GiphyApiException, self.g._check_or_raise, {'status': 400})

    def test_check_or_raise_no_status(self):
        self.assertRaises(GiphyApiException, self.g._check_or_raise, {})

    def test_check_or_raise(self):
        assert self.g._check_or_raise({'status': 200}) is None

    @patch('giphypop.requests')
    def test_fetch_error_raises(self, requests):
        # api returns error messages sorta like...
        err = {'meta': {'error_type': 'ERROR', 'code': 400, 'error_message': ''}}
        requests.get.return_value = requests
        requests.json.return_value = err

        self.assertRaises(GiphyApiException, self.g._fetch, 'foo')

    @patch('giphypop.requests')
    def test_fetch(self, requests):
        data = {'data': FAKE_DATA, 'meta': {'status': 200}}
        requests.get.return_value = requests
        requests.json = data

        assert self.g._fetch('foo') == data

    @patch('giphypop.requests')
    def test_fetch_sort_recent(self, requests):
        data = {'data': FAKE_DATA_RECENT, 'meta': {'status': 200}}
        requests.get.return_value = requests
        requests.json = data

        assert self.g._fetch('foo', recent=True) == data

    @patch('giphypop.requests')
    def test_fetch_data_sort_relevant(self, requests):
        data = {'data': FAKE_DATA_RELEVANT, 'meta': {'status': 200}}
        requests.get.return_value = requests
        requests.json = data

        assert self.g._fetch('foo') == data

    def fake_search_fetch(self, num_results, pages=3):
        self.g._fetch = Mock()
        self.g._fetch.return_value = {
            'data': [FAKE_DATA for x in range(num_results)],
            'pagination': {
                'total_count': pages,
                'count': 25,
                'offset': 0
            },
            'meta': {'status': 200}
        }

    def fake_search_fetch_recent(self):
        self.g._fetch = Mock()
        self.g._fetch.return_value = {
            'data': FAKE_DATA_RECENT,
            'pagination': {
                'total_count': 3,
                'count': len(FAKE_DATA_RECENT),
                'offset': 0
            },
            'meta': {'status': 200}
        }

    def fake_search_fetch_relevant(self):
        self.g._fetch = Mock()
        self.g._fetch.return_value = {
            'data': FAKE_DATA_RELEVANT,
            'pagination': {
                'total_count': 3,
                'count': len(FAKE_DATA_RELEVANT),
                'offset': 0
            },
            'meta': {'status': 200}
        }

    def fake_fetch(self, result=FAKE_DATA):
        self.g._fetch = Mock()
        self.g._fetch.return_value = {
            'data': result or None,
            'meta': {'status': 200}
        }

    def test_search_no_results(self):
        self.fake_search_fetch(0, pages=1)
        results = [x for x in self.g.search('foo')]
        assert len(results) == 0

    def test_search_respects_hard_limit(self):
        self.fake_search_fetch(25)
        results = [x for x in self.g.search('foo', limit=10)]
        assert len(results) == 10

    def test_search_handles_pages(self):
        self.fake_search_fetch(25)
        results = [x for x in self.g.search('foo', limit=50)]
        assert len(results) == 50

    def test_search_no_limit_returns_all(self):
        self.fake_search_fetch(25)
        results = [x for x in self.g.search('foo', limit=None)]
        assert len(results) == 75

    def test_search_list_returns_list(self):
        self.fake_search_fetch(25)
        results = self.g.search_list('foo', limit=10)
        assert isinstance(results, list)
        assert len(results) == 10

    def test_search_with_phrase_hyphenates(self):
        self.fake_search_fetch(0, pages=1)
        self.g.search(phrase='foo bar baz')
        assert self.g._fetch.called_with(q='foo-bar-baz')

    def test_search_with_recent_parameter(self):
        self.fake_search_fetch_recent()
        results = self.g._fetch(phrase='foo', sort_recent=True)
        assert results.get('data') == FAKE_DATA_RECENT

    def test_search_with_relevant_parameter(self):
        self.fake_search_fetch_relevant()
        results = self.g._fetch(phrase='foo', sort_recent=False)
        assert results.get('data') == FAKE_DATA_RELEVANT

    def test_translate_with_phrase_hyphenates(self):
        self.fake_fetch()
        self.g.translate(phrase='foo bar baz')
        assert self.g._fetch.called_with(s='foo-bar-baz')

    def test_translate(self):
        self.fake_fetch()
        assert isinstance(self.g.translate('foo'), GiphyImage)
        assert self.g._fetch.called_with('translate')

    def test_gif(self):
        self.fake_fetch()
        assert isinstance(self.g.gif('foo'), GiphyImage)
        assert self.g._fetch.called_with('foo')

    def test_screensaver(self):
        self.fake_fetch()
        assert isinstance(self.g.screensaver(), GiphyImage)

    def test_screensaver_passes_tag(self):
        self.fake_fetch()
        self.g.screensaver('foo')
        assert self.g._fetch.called_with(tag='foo')

    def test_random_gif(self):
        self.fake_fetch()
        assert isinstance(self.g.random_gif(), GiphyImage)

    def test_translate_returns_none(self):
        self.fake_fetch(result=None)
        assert self.g.translate('foo') is None

    def test_gif_returns_none(self):
        self.fake_fetch(result=None)
        assert self.g.gif('foo') is None

    def test_screensaver_returns_none(self):
        self.fake_fetch(result=None)
        assert self.g.screensaver('foo') is None

    def test_translate_raises_strict(self):
        self.fake_fetch(result=None)
        self.assertRaises(GiphyApiException, self.g.translate, 'foo', strict=True)

    def test_gif_returns_raises_strict(self):
        self.fake_fetch(result=None)
        self.assertRaises(GiphyApiException, self.g.gif, 'foo', strict=True)

    def test_screensaver_raises_strict(self):
        self.fake_fetch(result=None)
        self.assertRaises(GiphyApiException, self.g.screensaver, 'foo', strict=True)

    def test_strict_for_all(self):
        self.g = Giphy(strict=True)
        self.fake_fetch(result=None)

        self.assertRaises(GiphyApiException, self.g.translate, 'foo', strict=False)
        self.assertRaises(GiphyApiException, self.g.gif, 'foo', strict=False)
        self.assertRaises(GiphyApiException, self.g.screensaver, 'foo', strict=False)


class AliasTestCase(TestCase):

    @patch('giphypop.Giphy')
    def test_search_alias(self, giphy):
        giphy.return_value = giphy
        search(term='foo', limit=10, api_key='bar', strict=False)

        giphy.assert_called_with(api_key='bar', strict=False)
        giphy.search.assert_called_with(term='foo', phrase=None, limit=10)

    @patch('giphypop.Giphy')
    def test_search_list_alias(self, giphy):
        giphy.return_value = giphy
        search_list(term='foo', limit=10, api_key='bar', strict=False)

        giphy.assert_called_with(api_key='bar', strict=False)
        giphy.search_list.assert_called_with(term='foo', phrase=None, limit=10)

    @patch('giphypop.Giphy')
    def test_translate_alias(self, giphy):
        giphy.return_value = giphy
        translate(term='foo', api_key='bar', strict=False)

        giphy.assert_called_with(api_key='bar', strict=False)
        giphy.translate.assert_called_with(term='foo', phrase=None)

    @patch('giphypop.Giphy')
    def test_gif_alias(self, giphy):
        giphy.return_value = giphy
        gif('foo', api_key='bar', strict=False)

        giphy.assert_called_with(api_key='bar', strict=False)
        giphy.gif.assert_called_with('foo')

    @patch('giphypop.Giphy')
    def test_screensaver_alias(self, giphy):
        giphy.return_value = giphy
        screensaver(tag='foo', api_key='bar', strict=False)

        giphy.assert_called_with(api_key='bar', strict=False)
        giphy.screensaver.assert_called_with(tag='foo')

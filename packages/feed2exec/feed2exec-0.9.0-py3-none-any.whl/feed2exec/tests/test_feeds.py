#!/usr/bin/python3
# coding: utf-8

# Copyright (C) 2016 Antoine Beaupré <anarcat@debian.org>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from __future__ import division, absolute_import
from __future__ import print_function

from feed2exec.feeds import (FeedStorage, ConfFeedStorage,
                             FeedCacheStorage, parse)
import feed2exec.plugins.echo
import feed2exec.utils as utils
from feed2exec.tests.fixtures import (test_db, conf_path, betamax)  # noqa
import pytest

test_data = {'url': 'file:///dev/null',
             'name': 'test',
             'output': None,
             'args': None}
test_data2 = {'url': 'http://example.com/',
              'name': 'test2',
              'output': None,
              'args': None}
test_nasa = {'url': 'file://%s' % utils.find_test_file('breaking_news.xml'),
             'name': 'nasa-breaking-news',
             'filter': 'feed2exec.plugins.droptitle',
             'filter_args': 'Trump',
             'output': 'feed2exec.plugins.echo',
             'args': 'test_nasa'}
test_sample = {'url': 'file://%s' % utils.find_test_file('sample.xml'),
               'name': 'sample',
               'output': 'feed2exec.plugins.echo',
               'args': '1 2 3 4'}
test_udd = {'url': 'file://%s' % utils.find_test_file('udd.xml'),
            'name': 'udd',
            'output': 'feed2exec.plugins.echo',
            'args': 'test_udd'}
test_restic = {'url': 'file://%s' % utils.find_test_file('restic.xml'),
               'name': 'restic',
               'filter': 'feed2exec.plugins.emptysummary'}
test_dates = {'url': 'file://' + utils.find_test_file('weird-dates.xml'),
              'name': 'date test'}
test_params = {'url': 'file://%s' % utils.find_test_file('sample.xml'),
               'name': 'params',
               'folder': 'test-folder',
               'filter': 'feed2exec.plugins.echo',
               'filter_args': 'test',
               'output': 'feed2exec.plugins.echo',
               'args': '1 2 3 4'}


def test_add(test_db, conf_path):  # noqa
    st = FeedStorage()
    assert test_data['name'] not in st, 'this is supposed to be empty'
    st.add(**test_data)
    assert test_data['name'] in st, 'contains works'
    with pytest.raises(AttributeError):
        st.add(**test_data)
    for r in st:
        assert r['name'] == test_data['name'], 'iterator works'
    st.remove(test_data['name'])
    assert test_data['name'] not in st, 'remove works'


def test_settings(test_db, conf_path, betamax):  # noqa
    st = FeedStorage()
    assert len(list(st)) == 0
    st.add(**test_params)
    assert len(list(st)) == 1
    st.set(test_params['name'], 'catchup', 'True')
    st.remove_option(test_params['name'], 'filter')
    st.fetch()
    assert not feed2exec.plugins.echo.output.called

    st.set(test_params['name'], 'filter', test_params['filter'])
    st.fetch()
    assert feed2exec.plugins.echo.output.called
    feed2exec.plugins.echo.output.called = False

    st.set(test_params['name'], 'pause', 'True')
    st.fetch()
    assert not feed2exec.plugins.echo.output.called

    st.remove(test_params['name'])


def test_pattern(test_db, conf_path):  # noqa
    st = FeedStorage()
    st.add(**test_data)
    assert test_data['name'] in st, 'previous test should have ran'
    st.add(**test_data2)
    assert test_data2['name'] in st, 'second add works'
    feeds = list(FeedStorage(pattern='test2'))
    assert len(feeds) == 1, 'find only one item'
    feeds = list(FeedStorage(pattern='test'))
    assert len(feeds) == 2, 'find two items'


def test_cache(test_db):  # noqa
    st = FeedCacheStorage(feed=test_data['name'])
    assert 'guid' not in st
    st.add('guid')
    assert 'guid' in st
    tmp = FeedCacheStorage()
    assert 'guid' in tmp
    st.add('another')
    for item in tmp:
        assert item
        if item['guid'] == 'another':
            break
    else:  # sanity check
        assert False, 'failed to iterate through storage'  # pragma: nocover
    for item in FeedCacheStorage(feed=test_data['name'], guid='guid'):
        assert 'another' not in item['guid']
    st.remove('guid')
    assert 'guid' not in st


def test_fetch(test_db, conf_path, betamax):  # noqa
    st = FeedStorage()
    st.add(**test_sample)

    st.fetch()
    cache = FeedCacheStorage(feed=test_sample['name'])
    assert '7bd204c6-1655-4c27-aeee-53f933c5395f' in cache
    assert feed2exec.plugins.echo.output.called

    st.add(**test_nasa)
    feed2exec.plugins.echo.output.called = False
    assert not feed2exec.plugins.echo.output.called
    st.fetch()
    assert feed2exec.plugins.echo.output.called == ('test_nasa', )
    feed2exec.plugins.echo.output.called = False
    assert not feed2exec.plugins.echo.output.called
    st.add(**test_udd)
    st.fetch()
    assert feed2exec.plugins.echo.output.called == ('test_udd', )


def test_fetch_parallel(test_db, conf_path, capfd, betamax):  # noqa
    st = FeedStorage()
    st.fetch(parallel=True, force=True)
    # can't use feed2exec.feeds.plugins.echo.output.called as it is
    # set in a separate process.
    out, err = capfd.readouterr()
    assert 'arguments received' in out
    st.fetch(parallel=2, force=True)
    out, err = capfd.readouterr()
    assert 'arguments received' in out


def test_normalize(test_db, conf_path, betamax):  # noqa
    '''black box testing for :func:feeds.normalize_item()'''
    data = parse(betamax.get(test_udd['url']).content, test_udd)
    for item in data.entries:
        assert item.get('id')
    data = parse(betamax.get(test_restic['url']).content, test_restic)
    for item in data.entries:
        assert item.get('link').startswith('file://')
        assert 'restic.atom' not in item.get('link')
        # also test the "github filter"
        assert item.get('summary')
        assert item.get('link') in item.get('summary')
    data = parse(betamax.get(test_dates['url']).content, test_dates)
    for item in data['entries']:
        assert item.get('updated_parsed')


def test_config(conf_path):  # noqa
    conf_path.remove()
    conf = ConfFeedStorage()
    conf.add(**test_sample)
    assert conf_path.check()
    assert conf_path.read() == '''[sample]
url = %s
output = feed2exec.plugins.echo
args = 1 2 3 4

''' % test_sample['url']
    assert 'sample' in conf
    for feed in conf:
        assert type(feed) is dict
    conf.remove('sample')
    assert conf_path.read() == ''

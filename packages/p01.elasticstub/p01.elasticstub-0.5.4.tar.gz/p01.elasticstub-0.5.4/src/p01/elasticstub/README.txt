======
README
======

setup
-----

This test is using an elasticsearch server. The test setUp method used for this
test is calling our startElasticSearchServer method which is starting an
elasticsearch server. The first time this test get called a new elasticsearch
server will get downloaded. The test setup looks like::

  def test_suite():
      return unittest.TestSuite((
          doctest.DocFileSuite('README.txt',
              setUp=testing.doctestSetUp, tearDown=testing.doctestTearDown,
              optionflags=doctest.NORMALIZE_WHITESPACE|doctest.ELLIPSIS,
              encoding='utf-8'),
          ))

If you like to set some custom settings, you can use the confSource which must
point to a config folder with elasticsearch.yml or elasticsearch.json and
logging.yml and optional mapping definitions. Your custom doctest setUp and
tearDown method could look like::

  def mySetUp(test):
      # use default elasticsearch with our server and conf source dir
      here = os.path.dirname(__file__)
      serverDir = os.path.join(here, 'server')
      confSource = os.path.join(here, 'config')
      p01.elasticstub.testing.startElasticSearchServer(serverDir=serverDir,
          confSource=confSource)

  def myTearDown(test):
      p01.elasticstub.testing.stopElasticSearchServer()
      # do some custom teardown stuff here


testing
-------

Let's setup a python httplib connection:

  >>> import httplib
  >>> conn = httplib.HTTPConnection('localhost', 45200)

and test the cluster state:

  >>> conn.request('GET', '_cluster/state')
  >>> response = conn.getresponse()
  >>> response.status
  200

  >>> import json
  >>> from pprint import pprint
  >>> body = response.read()
  >>> pprint(json.loads(body))
  {u'blocks': {},
   u'cluster_name': u'p01_elasticstub_testing',
   u'master_node': u'...',
   u'metadata': {u'cluster_uuid': u'...',
                 u'index-graveyard': {u'...': []},
                 u'indices': {},
                 u'templates': {}},
   u'nodes': {u'...': {u'attributes': {},
                                          u'ephemeral_id': u'...',
                                          u'name': u'...',
                                          u'transport_address': u'...'}},
   u'routing_nodes': {u'nodes': {u'...': []},
                      u'unassigned': []},
   u'routing_table': {u'indices': {}},
   u'state_uuid': u'...',
   u'version': 2}


As you can see our mapping is empty:

  >>> conn.request('GET', '/testing/test/_mapping')
  >>> response = conn.getresponse()
  >>> body = response.read()
  >>> pprint(json.loads(body))
  {u'error': {u'index': u'testing',
              u'index_uuid': u'_na_',
              u'reason': u'no such index',
              u'resource.id': u'testing',
              u'resource.type': u'index_or_alias',
              u'root_cause': [{u'index': u'testing',
                               u'index_uuid': u'_na_',
                               u'reason': u'no such index',
                               u'resource.id': u'testing',
                               u'resource.type': u'index_or_alias',
                               u'type': u'index_not_found_exception'}],
              u'type': u'index_not_found_exception'},
   u'status': 404}


Let's index a simple item:

  >>> body = json.dumps({u'title': u'Title'})
  >>> conn.request('POST', '/testing/test/1', body)
  >>> response = conn.getresponse()
  >>> body = response.read()
  >>> pprint(json.loads(body))
  {u'_id': u'1',
   u'_index': u'testing',
   u'_shards': {u'failed': 0, u'successful': 1, u'total': 2},
   u'_type': u'test',
   u'_version': 1,
   u'created': True,
   u'result': u'created'}

refresh:

  >>> conn.request('GET', '/testing/test/_refresh')
  >>> response = conn.getresponse()
  >>> body = response.read()
  >>> pprint(json.loads(body))
  {u'_id': u'_refresh',
   u'_index': u'testing',
   u'_type': u'test',
   u'found': False}

Let's set a mapping:

  >>> body = json.dumps({'test': {'properties': {'title': {'type': 'string'}}}})
  >>> conn.request('POST', '/testing/test/_mapping', body)
  >>> response = conn.getresponse()
  >>> body = response.read()
  >>> pprint(json.loads(body))
  {u'acknowledged': True}

and test our mapping again:

  >>> conn.request('GET', '/testing/test/_mapping')
  >>> response = conn.getresponse()
  >>> body = response.read()
  >>> pprint(json.loads(body))
  {u'testing': {u'mappings': {u'test': {u'properties': {u'title': {u'fields': {u'keyword': {u'ignore_above': 256,
                                                                                            u'type': u'keyword'}},
                                                                   u'type': u'text'}}}}}}

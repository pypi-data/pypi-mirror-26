MediaCloud Python API Client
============================

This is the source code of the python client for the [MediaCloud API v2](https://github.com/berkmancenter/mediacloud/blob/master/doc/api_2_0_spec/api_2_0_spec.md).

Usage
-----

First [sign up for an API key](https://core.mediacloud.org/login/register).  Then
```
pip install mediacloud
```

Examples
--------

To get the first 2000 the stories associated with a query and dump the output to json:
```python
import mediacloud, json, datetime
mc = mediacloud.api.MediaCloud('MY_API_KEY')

fetch_size = 1000
stories = []
last_processed_stories_id = 0
while len(stories) < 2000:
    fetched_stories = mc.storyList('( obama AND policy ) OR ( whitehouse AND policy)', 
                                   solr_filter=[ mc.publish_date_query( datetime.date(2013,1,1), datetime.date(2015,1,1)), 
                                                                         'tags_id_media:1'],
                                    last_processed_stories_id=last_processed_stories_id, rows= fetch_size)
    stories.extend( fetched_stories)
    if len( fetched_stories) < fetch_size:
        break
    
    last_processed_stories_id = stories[-1]['processed_stories_id']
    
print json.dumps(stories)
```

Find out how many sentences in the US mainstream media that mentioned "Zimbabwe" and "president" in 2013:
```python
import mediacloud, datetime
mc = mediacloud.api.MediaCloud('MY_API_KEY')
res = mc.sentenceCount('( zimbabwe AND president)', solr_filter=[mc.publish_date_query( datetime.date( 2013, 1, 1), datetime.date( 2014, 1, 1) ), 'tags_id_media:1' ])
print res['count'] # prints the number of sentences found
```

Alternatively, this query could be specified as follows
```python
import mediacloud
mc = mediacloud.api.MediaCloud('MY_API_KEY')
results = mc.sentenceCount('( zimbabwe AND president)', '+publish_date:[2013-01-01T00:00:00Z TO 2014-01-01T00:00:00Z} AND +tags_id_media:1')
print results['count']
```

Find the most commonly used words in sentences from the US mainstream media that mentioned "Zimbabwe" and "president" in 2013:
```python
import mediacloud, datetime
mc = mediacloud.api.MediaCloud('MY_API_KEY')
words = mc.wordCount('( zimbabwe AND president)',  solr_filter=[mc.publish_date_query( datetime.date( 2013, 1, 1), datetime.date( 2014, 1, 1) ), 'tags_id_media:1' ] )
print words[0]  #prints the most common word
```

To find out all the details about one particular story by id:
```python
import mediacloud
mc = mediacloud.api.MediaCloud('MY_API_KEY')
story = mc.story(169440976)
print story['url']  # prints the url the story came from
```

To save the first 100 stories from one day to a database:
```python
import mediacloud, datetime
mc = mediacloud.api.MediaCloud('MY_API_KEY')
db = mediacloud.storage.MongoStoryDatabase('one_day')
stories = mc.storyList(mc.publish_date_query( datetime.date (2014, 01, 01), datetime.date(2014,01,02) ), last_processed_stories_id=0,rows=100)
[db.addStory(s) for s in stories]
print db.storyCount()
```

Take a look at the `apitest.py` and `storagetest.py` for more detailed examples.

Development
-----------

If you are interested in adding code to this module, first clone [the GitHub repository](https://github.com/c4fcm/MediaCloud-API-Client).

## Testing

First run all the tests.  Copy `mc-client.config.template` to `mc-client.config` and edit it.
Then run `python tests.py`. Notice you get a `mediacloud-api.log` that tells you about each query it runs.

## Distribution

1. Run `python test.py` to make sure all the test pass
2. Update the version number in `mediacloud/__init__.py`
3. Make a brief note in the version history section in the README file about the changes
4. Run `python setup.py sdist` to test out a version locally
5. Then run `python setup.py sdist upload -r pypitest` to release a test version to PyPI's test server
6. Run `pip install -i https://testpypi.python.org/pypi mediacloud` somewhere and then use it with Python to make sure the test release works.
7. When you're ready to push to pypi run `python setup.py sdist upload -r pypi`
8. Run `pip install mediacloud` somewhere and then try it to make sure it worked.

Version History
---------------

* __v2.43.1__: make JSON posts py3 compatible
* __v2.43.0__: topicList limit option, story-update endpoint, remove story coreNLP support, remove sentence-level tagging
* __v2.42.0__: add is_logogram option to topic creation and updating
* __v2.41.0__: updates to topic stories and media sorting, and ngram_size param to word count endpoints
* __v2.40.1__: auth api fixes 
* __v2.40.0__: add support for listing topics by name, or by if they are public or not
* __v2.39.2__: work on feed-related calls
* __v2.39.1__: fix topicMediaList to accept q as a param
* __v2.39.0__: new user reg endpoints, handle unicode in GET queries better
* __v2.38.2__: don't default wordcount to English
* __v2.38.1__: fix bug in mediaSuggestionsMark for approving media suggestions
* __v2.38.0__: add topic media map support
* __v2.37.0__: media source feed scraping, topic create/update, snapshot generate, mediaUpdate change
* __v2.36.2__: fixed defaults on updateTag
* __v2.36.1__: fixed system stats endpoint
* __v2.36.0__: added mediaSuggest workflow endpoints
* __v2.35.6__: mediaCreate fixes, storyList feed support
* __v2.35.5__: create media fixes
* __v2.35.4__: create collection fixes
* __v2.35.3__: fixes to clear_others support in tag* calls
* __v2.35.2__: fixes to updateMedia
* __v2.35.1__: fixes to createTagSet
* __v2.35.0__: tons of new source-related endpoints
* __v2.34.0__: new permissons endpoints
* __v2.33.1__: move topic endpoints to standard client so users can run them
* __v2.33.0__: lots of new api endpoints for topic management
* __v2.32.0__: fix links in topicStoryList and topicMediaList
* __v2.31.0__: migrate dumpsList and timesliceList to snapshotList and timespanList
* __v2.30.0__: migrate controversyList and controversy to topicList and topic 
* __v2.29.1__: fixes to topicWordCount method return value
* __v2.29.0__: add topicSentenceCount, and paging for topicMediaList & topicStoriesList endpoints
* __v2.28.0__: add storyWordMatrix, support long queries via POST automatically
* __v2.27.0__: first topic endpoints
* __v2.26.1__: chunk sentence tag calls to avoid URI length limit in PUT requests
* __v2.26.0__: add storyCount endpoint, cleanup some failing test cases
* __v2.25.0__: add mediaHealth endpoint, support `ap_stories_id` flag in storiesList, fix `controversy_dump_time_slices` endpoint, remove mediaSet and Dashboard endpoints
* __v2.24.1__: fixes tab/spaces bug
* __v2.24.0__: adds new params to the `mediaList` query (searching by controversy, solr query, tags_id, etc)
* __v2.23.0__: adds solr date generation helpers
* __v2.22.2__: fixes the PyPI readme
* __v2.22.1__: moves `sentenceList` to the admin client, preps for PyPI release
* __v2.22.0__: adds the option to enable `all_fields` at the API client level (ie. for all requests) 

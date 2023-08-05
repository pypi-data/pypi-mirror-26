import requests
import re
import time

# Imports
try:
    from .markdown import guildwars2_html2markdown
    from .formats import guildwars2_format
except ImportError:
    import libpolarbytebot.transcriber.markdown.guildwars2_html2markdown as guildwars2_html2markdown
    import libpolarbytebot.transcriber.formats.guildwars2_format as guildwars2_format

__all__ = ['guildwars2_forum_parse', 'guildwars2_findall_forum_urls', 'guildwars2_findall_forum_urls_mentions']


__forum_url_regex = 'http.*?://..-forum\.guildwars2\.com/discussion/[^ \])\s]*'

class ForumUrl:
    def __init__(self, url):
        self.url = str(url).strip()

    @property
    def is_comment(self):
        return re.match('http.*?://..-forum\.guildwars2\.com/discussion/comment/\d*(/#Comment_\d*|/|)',
                        self.url) is not None

    @property
    def is_thread(self):
        return re.match('http.*?://..-forum\.guildwars2\.com/discussion/\d*?/.*', self.url) is not None

    @property
    def is_thread_latest(self):
        return re.match('http.*?://..-forum\.guildwars2\.com/discussion/\d*?/.*?#latest', self.url) is not None

    @property
    def comment_id(self):
        result = None
        try:
            result = re.match('http.*?://..-forum\.guildwars2\.com/discussion/comment/(?P<id>\d*)(/#Comment_\d*|/|)',
                              self.url).group('id')
        except AttributeError:
            pass
        return result

    @property
    def json_url(self):
        return self.url.rsplit('#', maxsplit=1)[0] + '.json'


def guildwars2_findall_forum_urls(content):
    forum_findings = re.findall(__forum_url_regex, content)
    forum_findings = set(forum_findings)
    return forum_findings

def guildwars2_findall_forum_urls_mentions(content, mention_regex):
    forum_mention_findings = []
    temp_forum_mention_findings = re.findall(mention_regex + __forum_url_regex, content)

    for temp_mention in temp_forum_mention_findings:
        forum_mention_findings.extend(guildwars2_findall_forum_urls(temp_mention))

    forum_mention_findings = set(forum_mention_findings)
    return forum_mention_findings

def guildwars2_forum_parse(url):
    """
    Fetch and transform a forums post into a markdown formatted string, usable in the polarbytebot post text body. 
    No signatures included.
    :param url: the url of the discussion or comment to transcribe.
    :return: formatted text which can be used in the textbody.
    """
    def comment(cm, post):
        post.author = cm['InsertName']
        post.timestamp = cm['DateInserted']
        if 'ArenaNet' in cm['Roles'].values():
            post._is_offical = True
        post.text = cm['Body']

    furl = ForumUrl(url)
    json_response = requests.get(furl.json_url).json()
    post = guildwars2_format.GuildWars2Format(type='forum', url=furl.url)
    if furl.is_comment:
        # filter out the comment which maches the id in the anchor tag (#Comment_XXXXXXX)
        ref_comment = list(filter(lambda item: str(item['CommentID']) == furl.comment_id, json_response['Comments']))[0]
        comment(ref_comment, post)
    elif furl.is_thread_latest and list(json_response['Comments']) != []:
        # take the last comment
        ref_comment = list(json_response['Comments'])[-1]
        comment(ref_comment, post)
    elif furl.is_thread:
        ref_discussion = json_response['Discussion']
        post.author = ref_discussion['InsertName']
        post.timestamp = ref_discussion['DateInserted']
        if 'ArenaNet' in ref_discussion['Roles'].values():
            post._is_offical = True
        post.text = ref_discussion['Body']
    return post.result



def requests_get(url):
    counter = 0
    while True:
        try:
            req = requests.get(url)
            time.sleep(0.5)
        except:
            pass
        else:
            return req
        finally:
            counter += 1
            if counter > 100:
                return


if __name__ == '__main__':
    #t1 = '+/u/polarbytebot https://en-forum.guildwars2.com/discussion/2704/spellbreaker-specialization-updates-for-the-path-of-fire-launch#latest \n\n' \
     #    '+/u/polarbytebot https://en-forum.guildwars2.com/discussion/2704/spellbreakfwef-updates-for-the-path-of-fire-launch\n\n'
    #print(guildwars2_findall_forum_urls_mentions(t1, '\+/u/polarbytebot {1,3}'))
    print(guildwars2_forum_parse('https://en-forum.guildwars2.com/discussion/10634/game-update-notes-october-17-2017#latest'))



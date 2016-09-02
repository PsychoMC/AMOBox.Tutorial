# -*- coding: utf-8 -*-

'''
    Specto Add-on
    Copyright (C) 2015 lambda

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''

import re,urlparse,datetime,os,base64,urllib
import zipfile, StringIO

from resources.lib.libraries import cleantitle
from resources.lib import resolvers
from resources.lib.libraries import client
from resources.lib.libraries import control
try:
    from sqlite3 import dbapi2 as database
except:
    from pysqlite2 import dbapi2 as database


class source:
    def __init__(self):
        self.base_link = 'http://cyro.se'
        self.search_link = '/forum/search.php?do=process'
        self.forum_link = '/forum/forum.php'
        self.forum_prefix = '/forum'
        self.data_link = 'aHR0cHM6Ly9yYXcuZ2l0aHVidXNlcmNvbnRlbnQuY29tL21ya25vdy9kYXRhYmFzZS9tYXN0ZXIvZGF5dHNlMS56aXA='
        self.headers = {}

    def get_movie(self,imdb, title, year):

        try:
            url = '%s (%s)' % (title, year)
            url = client.replaceHTMLCodes(url)
            url = url.encode('utf-8')
            return url
        except Exception as e:
            control.log("------ %s | %s " ('DAYT',e))
            return None



    def get_show(self, imdb, tvdb, tvshowtitle, year):
        return


    def dayt_tvcache(self):
        #try:
        #    url = urlparse.urljoin(self.base_link, self.forum_link)
        #    result =  client.source(url)
        #    result = re.compile('<span class="sectiontitle"><a href="([^"]+)">([^<]+)</a></span> <span class="rightrss">').findall(result)
        #    result = [(re.compile('(.+?)(?:&amp)').findall(i[0]), re.sub('&#\d*;', '', i[1])) for i in result]
        #    result = [( i[0][0], cleantitle.get(i[1])) for i in result if len(i[0]) > 0]

        #    return result
        #except:
        #    return
        return


    def get_episode(self, url, imdb, tvdb, title, premiered, season, episode):
        return


    def get_sources(self, url, hosthdDict, hostDict, locDict):
        try:
            sources = []
            if url == None: return sources
            content = re.compile('(.+?)\sS\d*E\d*$').findall(url)
            #control.log('#Dayt content %s' % content)

            if len(content) == 0:
                title, year = re.compile('(.+?) \((\d{4})\)').findall(url)[0]
                mytitle = cleantitle.movie(title)

                data = os.path.join(control.dataPath, 'daytse1.db')
                download = True
                try:download = abs(datetime.datetime.fromtimestamp(os.path.getmtime(data)) - (datetime.datetime.now())) > datetime.timedelta(days=2)
                except:pass
                if download == True:
                    #control.log('#Dayt DDDOOOWNLOAD ')
                    #result = client.request(base64.b64decode(self.data_link))
                    #with open(data, "wb") as code:
                    #    code.write(result)
                    result = client.request(base64.b64decode(self.data_link))
                    print(len(result))
                    #control.log(">>>>>>>>>>>>>>> ONEC Downloading")
                    zip = zipfile.ZipFile(StringIO.StringIO(result))
                    zip.extractall(control.dataPath)
                    zip.close()

                dbcon = database.connect(data)
                dbcur = dbcon.cursor()
                control.log("#Dayt DDDOOOWNLOAD SELECT * FROM movies WHERE title like '%"+cleantitle.movie(title)+"%'")
                dbcur.execute("SELECT * FROM movies WHERE title like '%"+cleantitle.movie(title)+"%'")
                result = dbcur.fetchone()
                #myurl = urlparse.urljoin(self.base_link, '/movies/' + urllib.quote_plus(result[1]))
                myurl = urlparse.urljoin(self.base_link, '/movies/' + result[1])

                myhead = {'Referer': self.base_link}
                result10 = client.request(myurl, headers=myhead)
                result10 = client.parseDOM(result10, 'div', attrs={'id': '5throw'})[0]
                result10 = client.parseDOM(result10, 'a', attrs={'rel': 'nofollow'}, ret='href')
                mquality = 'HD'
                if '1080'in result[2]: mquality = '1080p'
                for i in result10:
                    if 'mail.ru' in i:
                        myresolve = resolvers.request(i)
                        sources.append({'source': 'MAIL.RU', 'quality': mquality, 'provider': 'Dayt', 'url': myresolve})
                    if 'yadi.sk' in i:
                        myresolve = resolvers.request(i)
                        sources.append({'source': 'YADISK', 'quality': mquality, 'provider': 'Dayt', 'url': myresolve})

                result = client.parseDOM(result, 'iframe', ret='src')
                result = [i for i in result if 'pasep' in i][0]
                result = client.request(result)
                result = client.parseDOM(result, 'iframe', ret='src')[0]
                result = client.request(result)
                result = client.parseDOM(result, 'iframe', ret='src')[0]
                links = resolvers.request(result)
                for i in links: sources.append({'source': 'gvideo', 'quality': i[1], 'provider': 'Dayt', 'url': i[0]})
                return sources
        except Exception as e:
            control.log("------ %s | %s "('DAYT', e))
            return sources


    def resolve(self, url):
        try:
            return url
        except:
            return



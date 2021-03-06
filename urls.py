from django.conf.urls.defaults import *
from django.conf import settings
from news.feeds import RssNewsFeed, AtomNewsFeed
from news.models import Entry
from phonedb.feeds import RssPhonesFeed, AtomPhonesFeed
from phonedb.models import Phone, Vendor
from django.contrib.sitemaps import GenericSitemap, Sitemap
from downloads.models import Release
import os
import datetime

news_dict = {
    'queryset': Entry.objects.all(),
    'date_field': 'pub_date',
}

phones_dict = {
    'queryset': Phone.objects.all().exclude(state = 'deleted'),
    'date_field': 'created',
}

vendors_dict = {
    'queryset': Vendor.objects.all(),
}

releases_dict = {
    'queryset': Release.objects.all(),
    'date_field': 'date',
}

class PagesSitemap(Sitemap):
    changefreq = 'weekly'
    def items(self):
        return [
            ('/', '%s/index.html' % settings.HTML_ROOT, 1),
            ('/gammu/', '%s/gammu.html' % settings.HTML_ROOT, 1),
            ('/libgammu/', '%s/libgammu.html' % settings.HTML_ROOT, 1),
            ('/wammu/', '%s/wammu.html' % settings.HTML_ROOT, 1),
            ('/smsd/', '%s/smsd.html' % settings.HTML_ROOT, 1),
            ('/python-gammu/', '%s/python-gammu.html' % settings.HTML_ROOT, 1),

            ('/authors/', '%s/authors.html' % settings.HTML_ROOT, 0.9),
            ('/license/', '%s/libgammu.html' % settings.HTML_ROOT, 0.9),
            ('/search/', '%s/search.html' % settings.HTML_ROOT, 0.3),
            ('/donate/', '%s/donate.html' % settings.HTML_ROOT, 0.3),

            ('/s60/', '%s/s60.html' % settings.HTML_ROOT, 0.3),

            ('/support/', '%s/support/index.html' % settings.HTML_ROOT, 0.9),
            ('/support/bugs/', '%s/support/bugs.html' % settings.HTML_ROOT, 0.9),
            ('/support/lists/', '%s/support/lists.html' % settings.HTML_ROOT, 0.9),
            ('/support/online/', '%s/support/online.html' % settings.HTML_ROOT, 0.9),
            ('/support/buy/', '%s/support/buy.html' % settings.HTML_ROOT, 0.9),

            ('/contribute/', '%s/contribute/index.html' % settings.HTML_ROOT, 0.9),
            ('/contribute/code/', '%s/contribute/code.html' % settings.HTML_ROOT, 0.9),
            ('/contribute/translate/', '%s/contribute/translate.html' % settings.HTML_ROOT, 0.9),
            ('/contribute/publicity/', '%s/contribute/publicity.html' % settings.HTML_ROOT, 0.9),
            ('/contribute/wanted/', '%s/contribute/wanted.html' % settings.HTML_ROOT, 0.9),

            ('/docs/', '%s/docs/index.html' % settings.HTML_ROOT, 0.9),

            ('/screenshots/', None, 0.8),
            ('/downloads/gammu/', None, 0.7),
            ('/downloads/gammu/source/', None, 0.7),
            ('/downloads/gammu/win32/', None, 0.7),
            ('/downloads/wammu/', None, 0.7),
            ('/downloads/wammu/source/', None, 0.7),
            ('/links/', None, 0.4),
            ]
    def location(self, item):
        return item[0]

    def lastmod(self, item):
        if item[1] is None:
            return None
        (mode, ino, dev, nlink, uid, gid, size, atime, mtime, ctime) = os.stat(item[1])
        return datetime.datetime.fromtimestamp(mtime)

    def priority(self, item):
        return item[2]

sitemaps = {
    'news': GenericSitemap(news_dict, priority=0.8, changefreq='monthly'),
    'phones': GenericSitemap(phones_dict, priority=0.8, changefreq='monthly'),
    'releases': GenericSitemap(releases_dict, priority=0.9, changefreq='monthly'),
    'vendors': GenericSitemap(vendors_dict, priority=0.2, changefreq='monthly'),
    'pages': PagesSitemap(),
}

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^wammu/', include('wammu.foo.urls')),
    (r'^$', 'wammu.views.index'),
    (r'^gammu/$', 'wammu.views.gammu'),
    (r'^smsd/$', 'wammu.views.smsd'),
    (r'^wammu/$', 'wammu.views.wammu'),
    (r'^libgammu/$', 'wammu.views.libgammu'),
    (r'^python-gammu/$', 'wammu.views.pygammu'),

    (r'^authors/$', 'wammu.views.static', {'page': 'authors.html'}),
    (r'^license/$', 'wammu.views.static', {'page': 'license.html'}),
    (r'^search/$', 'wammu.views.static', {'page': 'search.html'}),

    (r'^support/$', 'wammu.views.support'),
    (r'^support/bugs/$', 'wammu.views.static', {'page': 'support/bugs.html'}),
    (r'^support/lists/$', 'wammu.views.static', {'page': 'support/lists.html'}),
    (r'^support/online/$', 'wammu.views.static', {'page': 'support/online.html'}),
    (r'^support/buy/$', 'wammu.views.static', {'page': 'support/buy.html'}),

    (r'^contribute/$', 'wammu.views.static', {'page': 'contribute/index.html'}),
    (r'^contribute/code/$', 'wammu.views.static', {'page': 'contribute/code.html'}),
    (r'^contribute/translate/$', 'wammu.views.static', {'page': 'contribute/translate.html'}),
    (r'^contribute/publicity/$', 'wammu.views.static', {'page': 'contribute/publicity.html'}),
    (r'^contribute/wanted/$', 'wammu.views.static', {'page': 'contribute/wanted.html'}),

    (r'^docs/$', 'wammu.views.static', {'page': 'docs/index.html'}),

    (r'^s60/$', 'wammu.views.static', {'page': 's60.html'}),

    (r'^tools/$', 'wammu.views.static', {'page': 'tools/index.html'}),
    (r'^tools/pdu-encode/$', 'tools.views.pduencode'),
    (r'^tools/pdu-decode/$', 'tools.views.pdudecode'),
    (r'^tools/countries/$', 'tools.views.countries'),
    (r'^tools/networks/$', 'tools.views.networks'),

    # RSS feeds
    (r'^news/rss/$', RssNewsFeed()),
    (r'^news/atom/$', AtomNewsFeed()),

    # News
    (r'^news/$', 'news.views.index'),
    (r'^news/(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<day>\d{1,2})/(?P<slug>[^/]*)/$',
        'news.views.entry'),
    (r'^news/(?P<slug>.*)/$', 'news.views.category'),

    (r'^download/$', 'downloads.views.download'),
    (r'^download/(?P<program>[^/]*)/$', 'downloads.views.program'),
    (r'^download/(?P<program>[^/]*)/(?P<version>[0-9.]*)/$', 'downloads.views.release'),
    (r'^download/(?P<program>[^/]*)/(?P<platform>[^/]*)/$', 'downloads.views.list'),

    # RSS feeds
    (r'^phones/rss/$', RssPhonesFeed()),
    (r'^phones/atom/$', AtomPhonesFeed()),


    (r'^phones/csv/$', 'phonedb.views.phones_csv'),

    # Phone database
    (r'^phones/$', 'phonedb.views.index'),
    (r'^phones/history.png$', 'phonedb.views.phones_chart'),
    (r'^phones/new/$', 'phonedb.views.create'),
    (r'^phones/search/$', 'phonedb.views.search'),
    (r'^phones/review/$', 'phonedb.views.review'),
    (r'^phones/model.php/$', 'phonedb.views.phone_redirect'),
    (r'^phones/search/(?P<featurename>[^/]*)/$', 'phonedb.views.search'),
    (r'^phones/(?P<vendorname>[^/]*)/$', 'phonedb.views.vendor'),
    (r'^phones/(?P<vendorname>[^/]*)/(?P<id>[0-9]*)/$', 'phonedb.views.phone'),
    (r'^phones/(?P<vendorname>[^/]*)/(?P<id>[0-9]*)/delete/$', 'phonedb.views.delete'),
    (r'^phones/(?P<vendorname>[^/]*)/(?P<id>[0-9]*)/approve/$', 'phonedb.views.approve'),
    (r'^phones/(?P<vendorname>[^/]*)/new/$', 'phonedb.views.create'),

    # API for Wammu
    (r'^api/phones/new/$', 'phonedb.views.create_wammu'),

    # DOAP/PAD syndication
    (r'^api/doap/(?P<program>[^/.]*).xml$', 'downloads.views.doap'),
    (r'^api/pad/(?P<program>[^/.]*).xml$', 'downloads.views.pad'),
    (r'^api/pad/padmap.txt$', 'downloads.views.padmap'),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs'
    # to INSTALLED_APPS to enable admin documentation:
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),

    # Media files
    (r'^media/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': './media'}),


    # Donations
    (r'^donate/$', 'donate.views.donate'),
    (r'^donate/thanks/$', 'donate.views.thanks'),

    # Screenshots
    (r'^screenshots/$', 'screenshots.views.index'),
    (r'^screenshots/(?P<slug>.*)/$', 'screenshots.views.category'),

    # Links
    (r'^links/$', 'links.views.index'),

    # Compatibility
    (r'^install/$', 'django.views.generic.simple.redirect_to', {'url': '/download/'}),
    (r'^improve/$', 'django.views.generic.simple.redirect_to', {'url': '/contribute/'}),
    (r'^wammu.xml$', 'django.views.generic.simple.redirect_to', {'url': '/api/pad/wammu.xml'}),
    (r'^wammu.doap$', 'django.views.generic.simple.redirect_to', {'url': '/api/doap/wammu.xml'}),
    (r'^phones/features/(?P<featurename>[^/]*)/$', 'django.views.generic.simple.redirect_to', {'url': '/phones/search/%(featurename)s/'}),

    # Sitemap
    (r'^sitemap.xml$', 'django.contrib.sitemaps.views.index', {'sitemaps': sitemaps}),
    (r'^sitemap-(?P<section>.+)\.xml$', 'django.contrib.sitemaps.views.sitemap', {'sitemaps': sitemaps}),

    # Robots
    (r'^robots.txt$', 'wammu.views.robots'),

    # Redirects for crazy bots who investiage full urls
    (r'^api/$', 'django.views.generic.simple.redirect_to', {'url': '/download/'}),
    (r'^api/doap/$', 'django.views.generic.simple.redirect_to', {'url': '/download/'}),
    (r'^api/pad/$', 'django.views.generic.simple.redirect_to', {'url': '/download/'}),

    # Broken links
    (r'^(?P<link>.*)/\)\.$', 'django.views.generic.simple.redirect_to', {'url': '/%(link)s'}),
    (r'^(?P<link>.*)/\)$', 'django.views.generic.simple.redirect_to', {'url': '/%(link)s'}),
    (r'^(?P<link>.*)/index\.php$', 'django.views.generic.simple.redirect_to', {'url': '/%(link)s'}),
    (r'^(?P<link>phones/(?P<vendorname>[^/]*)/(?P<id>[0-9]*)/),.*', 'django.views.generic.simple.redirect_to', {'url': '/%(link)s'}),
    (r'^snapshot/$', 'django.views.generic.simple.redirect_to', {'url': '/download/'}),
    (r'^manual/$', 'django.views.generic.simple.redirect_to', {'url': '/docs/manual/'}),
    (r'^docs/faq/$', 'django.views.generic.simple.redirect_to', {'url': '/docs/manual/faq/'}),
    (r'^docs/roadmap/$', 'django.views.generic.simple.redirect_to', {'url': '/docs/manual/project/roadmap.html'}),
    (r'^docs/devel/$', 'django.views.generic.simple.redirect_to', {'url': '/docs/'}),
    (r'^docs/man/.*$', 'django.views.generic.simple.redirect_to', {'url': '/docs/'}),
    (r'^wiki/$', 'django.views.generic.simple.redirect_to', {'url': '/'}),
    (r'^en/$', 'django.views.generic.simple.redirect_to', {'url': 'http://wammu.eu/'}),
    (r'^cs/$', 'django.views.generic.simple.redirect_to', {'url': 'http://cs.wammu.eu/'}),
    (r'^cz/$', 'django.views.generic.simple.redirect_to', {'url': 'http://cs.wammu.eu/'}),
    (r'^es/$', 'django.views.generic.simple.redirect_to', {'url': 'http://es.wammu.eu/'}),
)

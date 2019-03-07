import logging
import socket
from collections import Counter

import tldextract

from soleadify_ml.models.website_meta import WebsiteMeta
from soleadify_ml.utils.SocketUtils import connect
import scrapy
from scrapy.http import Request, HtmlResponse
from scrapy.linkextractors import LinkExtractor
from django.conf import settings
from crawler.items import WebsitePageItem
from crawler.pipelines.website_page_pipeline_v2 import WebsitePagePipelineV2
from soleadify_ml.models.website import Website
from soleadify_ml.models.website_contact import WebsiteContact
from soleadify_ml.utils.SpiderUtils import get_possible_email

logger = logging.getLogger('soleadify_ml')


class WebsiteSpider(scrapy.Spider):
    name = 'WebsiteSpider'
    allowed_domains = []
    start_urls = []
    pages = []
    pipeline = [WebsitePagePipelineV2]
    contacts = {}
    secondary_contacts = {}
    website = None
    soc_spacy = None
    url = None
    emails = []
    cached_links = {}
    cached_docs = {}
    ignored_links = ['tel:', 'mailto:']
    max_page = 500
    organizations = []

    def __init__(self, website_id, force=False, **kw):
        self.website = Website.objects.get(pk=website_id)
        super(WebsiteSpider, self).__init__(**kw)

        self.soc_spacy = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.soc_spacy.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        connect(self.soc_spacy, '', settings.SPACY_PORT)

        if self.website and (self.website.contact_state == 'pending' or force):
            self.url = self.website.link
            self.link_extractor = LinkExtractor()

            self.website.contact_state = 'working'
            self.website.save(update_fields=['contact_state'])
        elif self.website and self.website.contact_state != 'pending':
            logger.debug('already processed: ' + self.website.link)
        else:
            logger.debug("couldn't find website: ")

    def start_requests(self):
        if self.url:
            logger.debug('start website: ' + self.url)
            return [Request(self.url, callback=self.parse, dont_filter=True)]
        else:
            return []

    def parse(self, response):
        if len(self.allowed_domains) == 0:
            self.allowed_domains.append(self.website.domain)
            domain = tldextract.extract(str(response.request.url)).registered_domain
            if domain not in self.allowed_domains:
                self.allowed_domains.append(domain)
        page = self._get_item(response)
        r = [page]
        r.extend(self._extract_requests(response))

        return r

    def is_linked_allowed(self, link):
        if len(self.allowed_domains) > 0:
            domain = tldextract.extract(link).registered_domain
            if domain in self.allowed_domains:
                return True
        return False

    def _get_item(self, response):
        try:
            item = WebsitePageItem({'response': response})
            return item
        except AttributeError as exc:
            logger.error('error website: ' + self.website.link + '-' + str(exc))
            pass

    def _extract_requests(self, response):
        r = []
        parsed_links = []
        priority_pages = {'team': 8, 'staff': 8, 'people': 8, 'meet': 7, 'member': 6, 'detail': 5, 'directory': 4,
                          'contact': 3, 'about': 2, 'find': 1}
        if isinstance(response, HtmlResponse):
            def sort_links(current_link):
                url = current_link.url.lower()
                url_text = current_link.text
                for key, value in priority_pages.items():
                    if key in url or key in url_text:
                        return value
                return 0

            links = self.link_extractor.extract_links(response)
            links = sorted(links, key=sort_links, reverse=True)
            for link in links:
                if self.max_page >= 0 and not self.is_ignored(link.url) and link.url not in self.cached_links:
                    parsed_links.append(link)
                    self.cached_links[link.url] = True
                    self.max_page -= 1

            r.extend(Request(x.url, callback=self.parse) for x in parsed_links)
        return r

    def close(self, spider):
        most_common_org = Counter(self.organizations).most_common(3)
        for key, contact in self.contacts.items():
            for email in self.emails:
                if 'EMAIL' in contact:
                    break
                possible_email = get_possible_email(contact['PERSON'], email)
                if possible_email:
                    contact['EMAIL'] = [possible_email['email']]

            WebsiteContact.save_contact(self.website, contact)

        for key, contact in self.secondary_contacts.items():
            if key in self.contacts:
                continue
            WebsiteContact.save_contact(self.website, contact, 0)

        db_organizations = []
        for org in most_common_org:
            website_meta = WebsiteMeta(website_id=self.website.id, meta_key='ORGANIZATION', meta_value=org[0],
                                       count=org[1])
            db_organizations.append(website_meta)
        WebsiteMeta.objects.bulk_create(db_organizations, ignore_conflicts=True)

        if self.url:
            self.website.contact_state = 'finished'
            self.website.save(update_fields=['contact_state'])

            logger.debug('end website: ' + self.website.link)

    def is_ignored(self, url):
        link_domain = tldextract.extract(str(url)).registered_domain
        if len(self.allowed_domains) == 0:
            return False
        for domain in self.allowed_domains:
            if domain in link_domain or link_domain in domain:
                for ignored in self.ignored_links:
                    if ignored in url:
                        return True
                return False

        return True

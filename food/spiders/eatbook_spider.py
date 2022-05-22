import scrapy
import datetime as dt
import re
from ..items import FoodItem
import logging
from scrapy.utils.log import configure_logging

class EatbookSpider(scrapy.Spider):
    configure_logging(install_root_handler=False)
    current_time = dt.datetime.now().strftime("%Y%m%d_%H%M%S")
    logging.basicConfig(
        filename=f'log_{current_time}.txt',
        format='%(levelname)s: %(message)s',
        level=logging.ERROR
    )

    name = 'eatbook'
    page_number = 2
    start_urls =[
        "https://eatbook.sg/category/food-reviews/"
    ]

    # Trackers
    page = 0
    object = 0

    def parse(self, response):
        self.page += 1
        print(f'Search page No. {self.page}')
        
        article_link = response.css('article h2 a').xpath("@href").extract()
        # parse each article
        for url in article_link:    
            yield response.follow(url=url, callback=self.parse_review, meta={'url': url})
        
        # next_page = response.css('div.older a::attr(href)').get()
        next_page = 'https://eatbook.sg/category/food-reviews/page/'+ str(self.page_number) + '/'
        if self.page_number <=5: # TO CHANGE WHEN DEPLOYING
            self.page_number += 1
            yield response.follow(next_page, callback=self.parse)

    def parse_review(self, response):
        article_link = response.meta['url']
        self.object += 1
        print(f'Review No. {self.object}')

        items = FoodItem()

        article_id = response.xpath('//article/@id').extract_first().replace('post-','').split(' ')[0]
        article_tag = response.css('article span.cat a::text').extract()
        article_date = response.css('article span.date::text').extract_first()
        # remove st,nd,rd,th from date and convert to SQL dateformat
        article_date = re.sub(r'(\d)(st|nd|rd|th)', r'\1', article_date)
        article_date = dt.datetime.strptime(article_date, '%d %B %Y')
        article_date = article_date.strftime("%Y-%m-%d")
        article_title = response.css('article h1::text').extract_first()

        items['article_id'] = article_id
        items['article_date'] = article_date
        items['article_title'] = article_title
        items['article_link'] = article_link
        items['article_tag'] = ', '.join([re.sub(r' Reviews', '', t) for t in article_tag])
        items['review_score'] = float(response.css('span.review-total-box::text').extract_first().split('/')[0])
        items['scraped_date'] = dt.datetime.now().date().strftime("%Y-%m-%d")
        items['venue_name'] = article_title.split(' Review: ')[0].strip('\n ')
        
        review_text = response.css('div.review-desc').xpath('//text()[preceding::*[contains(text(),"Summary")] and following::div[@class="googlemaps left"]]').getall()
        review_text = [text.replace('\n','') for text in review_text]
        review_text = [text for text in review_text if (len(text)>0) and (text != ' ')]

        idx_pros = [i for i, text in enumerate(review_text) if 'Pros' in text][0]
        idx_cons = [i for i, text in enumerate(review_text) if 'Cons' in text][0]
        idx_recommended = [i for i, text in enumerate(review_text) if 'recommended' in text.lower()][0]
        idx_opening = [i for i, text in enumerate(review_text) if re.search(r'hours?:?', text.lower())][0]
        # idx_opening = [i for i, text in enumerate(review_text) if 'hours:' in text.lower()][0]
        idx_address = [i for i, text in enumerate(review_text) if 'Address' in text][0]

        items['review_pros'] = ', '.join([text.strip('-– ') for text in review_text[idx_pros+1:idx_cons] if len(text)>2])
        items['review_cons'] = ', '.join([text.strip('-– ') for text in review_text[idx_cons+1:idx_recommended] if len(text)>2])
        items['recommended_dish'] = review_text[idx_recommended+1:idx_opening][0].strip(' :-–')
        try:
            items['opening_hours'] = review_text[idx_opening+1:idx_address][0].strip(' :')
        except:
            items['opening_hours'] = response.xpath('//*[contains(text(),"Opening hour")]').get().split("Opening hours: ")[-1].split("<")[0].strip(' :')
        items['address'] = ''.join(review_text[idx_address+1:]).strip(' :')
        items['source'] = 'eatbook'
        items['article_writer'] = response.css('div.author-content a::text').extract_first()

        yield items


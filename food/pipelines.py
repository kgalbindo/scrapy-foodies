# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from sqlalchemy.orm import sessionmaker
from food.models import FoodReview, db_connect, create_table

class FoodPipeline(object):
    def __init__(self):
        """
        Initializes database connection and sessionmaker.
        Creates deals table.
        """
        engine = db_connect()
        create_table(engine)
        self.Session = sessionmaker(bind=engine)

    def process_item(self, item, spider):
        """Save in the database.
        This method is called for every item pipeline component.
        """
        session = self.Session()

        # check if item with this title exists in DB
        item_exists = session.query(FoodReview).filter_by(venue_name=item['venue_name']).first()
        
        # if item exists in DB - we just update other columns
        if item_exists:
            item_exists.article_id = item['article_id']
            item_exists.article_date = item['article_date']
            item_exists.article_link = item['article_link']
            item_exists.article_tag = item['article_tag']
            item_exists.scraped_date = item['scraped_date']

            item_exists.review_score = item['review_score']
            item_exists.review_pros = item['review_pros']
            item_exists.review_cons = item['review_cons']
            item_exists.recommended_dish = item['recommended_dish']
            item_exists.opening_hours = item['opening_hours']

            item_exists.address = item['address']
            item_exists.source = item['source']
            item_exists.article_writer = item['article_writer']
            print('Item {} updated.'.format(item['venue_name']))

        # if not - we insert new item to DB
        else:     
            review = FoodReview()

            review.article_id = item['article_id']
            review.article_date = item['article_date']
            review.article_title = item['article_title']
            review.article_link = item['article_link']
            review.article_tag = item['article_tag']

            review.scraped_date = item['scraped_date']
            review.review_score = item['review_score']
            review.review_pros = item['review_pros']
            review.review_cons = item['review_cons']
            review.recommended_dish = item['recommended_dish']
            
            review.venue_name = item['venue_name']
            review.opening_hours = item['opening_hours']
            review.address = item['address']
            review.source = item['source']
            review.article_writer = item['article_writer']
            
            session.add(review)
            print('New item {} added to DB.'.format(item['venue_name']))        

        try:
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()
        
        return item


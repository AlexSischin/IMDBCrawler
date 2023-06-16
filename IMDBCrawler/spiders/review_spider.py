from scrapy import Spider
from scrapy.http import TextResponse


class ReviewSpider(Spider):
    name = 'reviews'
    start_urls = [
        'https://www.imdb.com/list/ls000634294/?sort=moviemeter,asc&st_dt=&mode=detail&ref_=ttls_vm_dtl&page=1',
    ]

    def parse(self, response: TextResponse, **kwargs):
        movie_refs = response.css('.lister-item-header a::attr(href)').getall()
        review_refs = [f'{r}reviews' for r in movie_refs]
        yield from response.follow_all(review_refs, self.parse_reviews)

        yield from response.follow_all(response.css('a.next-page'), self.parse)

    def parse_reviews(self, response: TextResponse, **kwargs):
        review_boxes = response.css('.review-container')
        for review_box in review_boxes:
            title = review_box.css('a::text').get()
            text = review_box.css('.show-more__control::text').get()
            rating = review_box.css('.rating-other-user-rating span::text').get()

            if title is not None:
                title = title.strip()

            if text is not None:
                text = text.strip()

            if rating is not None:
                rating = rating.strip()

            yield {
                'title': title,
                'text': text,
                'rating': rating,
            }

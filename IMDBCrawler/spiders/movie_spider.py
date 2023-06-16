from scrapy import Spider
from scrapy.http import TextResponse


class MovieSpider(Spider):
    name = 'movies'
    start_urls = [
        'https://www.imdb.com/list/ls000634294/?sort=moviemeter,asc&st_dt=&mode=detail&ref_=ttls_vm_dtl&page=1'
    ]

    def parse(self, response: TextResponse, **kwargs):
        yield from self.parse_movies(response)
        yield from response.follow_all(response.css('a.next-page'), self.parse)

    @staticmethod
    def parse_movies(response: TextResponse):
        movie_boxes = response.css('.mode-detail')
        for movie_box in movie_boxes:
            title = movie_box.css('.lister-item-header a::text').get()
            year = movie_box.css('span.lister-item-year::text').get()
            runtime = movie_box.css('span.runtime::text').get()
            genres = movie_box.css('span.genre::text').get()
            rating = movie_box.css('.ipl-rating-star__rating::text').get()
            votes = movie_box.css('span[name="nv"]::text').get()

            if title is not None:
                title = title.strip()

            if year is not None:
                year = year.strip()

            if runtime is not None:
                runtime = runtime.strip()

            if genres is not None:
                genres = [g.strip() for g in genres.strip().split(r'[,;]')]

            if rating is not None:
                rating = float(rating.strip())

            yield {
                'title': title,
                'year': year,
                'runtime': runtime,
                'genres': genres,
                'rating': rating,
                'votes': votes,
            }

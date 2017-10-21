import scrapy
import re
#to do: course_specialisation 
#       instructors_list

class PrometheusSpider(scrapy.Spider):
    name = 'prometheus'
    custom_settings = {
        'ITEM_PIPELINES': {
            'tutorial.pipelines.TutorialPipeline': 400
        }
    }
    start_urls = ['https://prometheus.org.ua/courses/']

    def parse(self, response):
        for href in response.xpath('//h3[contains(@class, "gdlr-item-title gdlr-skin-title gdlr-skin-border")]/a[contains(@href, "courses")]/@href').extract():
            yield scrapy.Request(response.urljoin(href),
                                callback=self.parse_course)


    def parse_course(self, response):
        instructors_list = {}
        # print(response.xpath('//article[contains(@class, "teacher")]/h3/text()'))
        # print(response.xpath('//article[contains(@class, "teacher")]/p').extract())
        for instructor, info in zip(response.xpath('//article[contains(@class, "teacher")]/h3/text()').extract(), response.xpath('//article[contains(@class, "teacher")]/p').extract()):
            instructors_list[instructor] = info.replace('<p>', '').replace('</p>', '')
        weeks_duration = response.xpath('(//h2[contains(text(), "Тривалість") or contains(text(), "ТРИВАЛІСТЬ КУРСУ") or contains(text(), "Довжина курсу")]/following-sibling::p)[1]/text()').extract()
        course_provider = (response.url).split('/')[4]
        if 'course-v1' in course_provider:
            course_provider = None
        try:
            duration_filter = (re.findall('\d+', weeks_duration[0]))[0]

            # duration_filter = int(weeks_duration[0][0])
        except:
            duration_filter = None
        # instructor_name = response.xpath('//article[contains(@class, "teacher")]/h3/text()').extract()
        # instructors_desc = response.xpath('//article[contains(@class, "teacher")]/p/text()').extract()
        yield {
            'name': response.xpath('//div[contains(@class, "heading-group")]/h1/text()').extract()[0].strip(),
            'source': 'prometheus',
            'category': None,
            'provider': course_provider,
            'language': 'Українська',
            'duration': None if not weeks_duration else weeks_duration[0],
            'duration_filter': duration_filter,
            'instructors_list': instructors_list,
            'start_date': response.xpath('//span[contains(@class, "important-dates-item-text start-date")]/text()').extract()[0],
            'description': response.xpath('//section[contains(@class, "about")]/p/text()').extract()[0],
            'link': response.url,
            'video': None,
            # 'price': None,
            'img': 'https://edx.prometheus.org.ua' + response.xpath('//div[contains(@class, "hero")]/img/@src').extract()[0]
                    # }
        }
import scrapy

#to do: course_specialisation 
#       instructors_list

class AuthorSpider(scrapy.Spider):
    name = 'quotes'

    start_urls = ['https://www.coursera.org/browse/']

    def parse(self, response):
        for href in response.xpath('//a[contains(@class, "rc-DomainNavItem")]/@href').extract():
            yield scrapy.Request(response.urljoin(href),
                                callback=self.parse_category)

    def parse_category(self, response):
        print ("URL: ", response.url)
        subacategory_hrefs = response.xpath('//div[contains(@class, "bt3-text-center")]/a/@href').extract()
        if not subacategory_hrefs:
            # h = response.xpath('//a[contains(@class, "rc-OfferingCard")]/@href').extract()
            # yield scrapy.Request(response.urljoin(h[0]),
            #                     callback=self.parse_course)
            course_hrefs = response.xpath('//a[contains(@class, "rc-OfferingCard")]/@href').extract()
            for href in course_hrefs:
                yield scrapy.Request(response.urljoin(href),
                                callback=self.parse_course)
        for href in subacategory_hrefs:
            yield scrapy.Request(response.urljoin(href),
                                callback=self.parse_subcategory)

    def parse_subcategory(self, response):
        print ("URL SUB: ", response.url)
        course_hrefs = response.xpath('//a[contains(@class, "rc-OfferingCard")]/@href').extract()
        for href in course_hrefs:
            yield scrapy.Request(response.urljoin(href),
                                callback=self.parse_course)


    def parse_course(self, response):
        yield {
            'course_name': response.xpath('//h2[contains(@class, "headline-4-text course-title")]/text()').extract(),
            'course_source': 'coursera',
            'course_provider': response.xpath('//div[contains(@class, "creator-names")]/span/text()').extract()[1],
            'language': response.xpath('//div[contains(@class, "rc-Language")]/text()').extract(),
            'weeks_duration': len(response.xpath('//div[contains(@class, "week")]').extract()),
            'instructors_list': response.xpath('//span[contains(@class, "body-1-text")]/a/text()').extract(),
                                # response.xpath('//span[contains(@class, "body-1-text")]/text()').extract()[0]
            'start_date': response.xpath('//div[contains(@class, "startdate rc-StartDateString caption-text")]/span/text()').extract(),
            'course_description': response.xpath('//p[contains(@class, "course-description")]/text()').extract()
        # }
        }
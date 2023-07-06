import scrapy
from scrapy_splash import SplashRequest

class CoinSpider(scrapy.Spider):
    name = "coin"
    allowed_domains = ["web.archive.org"]
    
    script = '''
        function main(splash, args)
            url = args.url
            assert(splash:go(url))
            --assert(splash:wait(1))
 	        splash:set_viewport_full()
            return splash:html() 
        end   
    '''
    def start_requests(self):
        yield SplashRequest(url="https://web.archive.org/web/20200116052415/https://www.livecoin.net/en/", callback=self.parse,endpoint="execute", args={
            'lua_source':self.script
        })

    def parse(self, response):
        for currency in response.xpath("//div[@class='ReactVirtualized__Table__row tableRow___3EtiS ']"):
            yield {
                'currency Pair':currency.xpath(".//div[1]/div/text()").get(),
                'volume':currency.xpath(".//div[2]/span/text()").get()
            }
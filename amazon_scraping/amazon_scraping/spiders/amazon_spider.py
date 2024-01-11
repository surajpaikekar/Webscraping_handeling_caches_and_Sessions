import scrapy
from scrapy_splash import SplashRequest 
import base64

lua_script = """
function main(splash, args)
    splash:init_cookies(splash.args.cookies)

    assert(splash:go(args.url))
    assert(splash:wait(1))

    splash:set_viewport_full()

    local email_input = splash:select('input[name=email]')   
    email_input:send_text("8888284452")
    assert(splash:wait(1))

    local email_submit = splash:select('input[class="a-button-input"]')
    email_submit:click()
    assert(splash:wait(3))

    local password_input = splash:select('input[name=password]')   
    password_input:send_text("Suraj@123")
    assert(splash:wait(1))

    local password_submit = splash:select('input[id=signInSubmit]')
    password_submit:click()
    assert(splash:wait(3))

    return {
        html=splash:html(),
        url = splash:url(),
        png = splash:png(),
        cookies = splash:get_cookies(),
        }
    end
"""


class AmazonSpiderSpider(scrapy.Spider):
    name = "amazon"

    def start_requests(self):
        signin_url = 'https://www.amazon.in/ap/signin?openid.pape.max_auth_age=0&openid.return_to=https%3A%2F%2Fwww.amazon.in%2F%3Fref_%3Dnav_signin&openid.identity=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.assoc_handle=inflex&openid.mode=checkid_setup&openid.claimed_id=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.ns=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0'
        yield SplashRequest(
            url=signin_url, 
            callback=self.start_scrapping,
            endpoint='execute', 
            args={
                'width': 1000,
                'lua_source': lua_script,
                'ua': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36"
                },
            )
    
    def start_scrapping(self,response):
        imgdata = base64.b64decode(response.data['png'])
        filename = 'after_login.png'
        with open(filename, 'wb') as f:
            f.write(imgdata)

        cookies_dict = {cookie['name']: cookie['value'] for cookie in response.data['cookies']}
        url_list = ['https://www.amazon.in/']
        for url in url_list:
            yield scrapy.Request(url=url, cookies=cookies_dict, callback=self.parse)

    def parse(self, response):
        # save the full page html
        with open('response.html', 'wb') as f:
            f.write(response.body)

        # scraping all the links on the page
        page_urls = response.css('a')
        for page_url in page_urls:
            if(page_url.css('a::text').get() is not None):
                try:
                    yield {
                        'url_text' : page_url.css('a::text').get(),
                        'url' : page_url.css('a').attrib['href']
                    }
                except:
                    print("An error occurred when scraping a link")


    





# import scrapy
# from ..items import AmazonScrapingItem
# import requests
# from scrapy.http import FormRequest
# from scrapy_splash import SplashRequest

# class AmazonSpiderSpider(scrapy.Spider):
#     page_number = 2
#     name = "amazon"
#     start_urls = [
#         "https://www.amazon.com/ap/signin?openid.pape.max_auth_age=0&openid.return_to=https%3A%2F%2Fwww.amazon.com%2F%3Fref_%3Dnav_signin&openid.identity=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.assoc_handle=usflex&openid.mode=checkid_setup&openid.claimed_id=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.ns=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0"
#                   ]

#     def parse(self, response):
#             yield FormRequest.from_response(
#             response,
#             formdata={
#                 'username': 'surajpaikekar',
#                 # 'password': 'suraj123'
#             },
#             callback=self.after_login
#         )

#     def after_login(self, response):
#         if response.status_code == 200:
#             self.log('Login successful!')
#             yield scrapy.Request(url='https://www.amazon.com/s?k=books&i=stripbooks-intl-ship&ref=nb_sb_noss_1', callback=self.parse_data)
#         else:
#             self.log('Login failed!')

#     def parse_data(self, response):
#         items = AmazonScrapingItem()
#         title = response.css('.a-size-medium.a-color-base.a-text-normal::text').extract() 
#         author = response.css('.a-color-secondary .a-size-base.s-link-style').css('::text').extract()
#         # price = response.css('.a-price span span').css('::text').extract()
#         # imageLink= response.css('.s-image::attr(src)').extract()
        
#         items['product_title'] = title
#         items['product_author'] = author
#         # items['product_price'] = price
#         # items['product_imageLink'] = imageLink

#         yield items

#         next_page = 'https://www.amazon.com/s?k=books&i=stripbooks-intl-ship&'+str(AmazonSpiderSpider.page_number)+'&ref=sr_pg_2'
#         if AmazonSpiderSpider.page_number <= 100:
#             AmazonSpiderSpider.page_number += 1
#             yield response.follow(next_page, callback=self.parse)








# class AmazonSpiderSpider(scrapy.Spider):
#     page_number = 2
#     name = "amazon"
#     start_urls = [
#         "https://www.amazon.com/s?k=books&i=stripbooks-intl-ship&ref=nb_sb_noss_1"
#                   ]
# #     def start_requests(self):
# #         self.session = requests.Session()
    
#           # sending a GET request to the login page
# #         return [scrapy.Request(url='https://www.amazon.com/ap/signin?openid.pape.max_auth_age=0&openid.return_to=https%3A%2F%2Fwww.amazon.com%2F%3Fref_%3Dnav_signin&openid.identity=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.assoc_handle=usflex&openid.mode=checkid_setup&openid.claimed_id=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.ns=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0', callback=self.login)]

# #     def login(self, response):
# #         login_url = 'https://www.amazon.com/ap/signin?openid.pape.max_auth_age=0&openid.return_to=https%3A%2F%2Fwww.amazon.com%2F%3Fref_%3Dnav_signin&openid.identity=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.assoc_handle=usflex&openid.mode=checkid_setup&openid.claimed_id=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.ns=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0
# #         username = 'surajpaikekar'
# #         password = 'suraj123'

# #         login_data = {
# #             'username': username,
# #             'password': password
# #         }

# #       
# #         response = self.session.post(login_url, data=login_data)    # Posting the login data to the login URL using the session

# #         if response.status_code == 200:   
# #             self.log('Login successful!')
# #             # Once logged in, we can proceed to scrape data by making requests with the session
# #             yield scrapy.Request(url='https://www.amazon.com/s?k=books&i=stripbooks-intl-ship&ref=nb_sb_noss_1', callback=self.parse)

#     def parse(self, response):
#         items = AmazonScrapingItem()
#         title = response.css('.a-size-medium.a-color-base.a-text-normal::text').extract() 
#         author = response.css('.a-color-secondary .a-size-base.s-link-style').css('::text').extract()
#         # price = response.css('.a-price span span').css('::text').extract()
#         # imageLink= response.css('.s-image::attr(src)').extract()
        
#         items['product_title'] = title
#         items['product_author'] = author
#         # items['product_price'] = price
#         # items['product_imageLink'] = imageLink

#         yield items

#         next_page = 'https://www.amazon.com/s?k=books&i=stripbooks-intl-ship&'+str(AmazonSpiderSpider.page_number)+'&ref=sr_pg_2'
#         if AmazonSpiderSpider.page_number <= 100:
#             AmazonSpiderSpider.page_number += 1
#             yield response.follow(next_page, callback=self.parse)








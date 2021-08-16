import scrapy
from scrapy.crawler import CrawlerProcess

class GtrPeopleSpider(scrapy.Spider):
    
    name = 'gtr_people'

    custom_settings = {
        'FEED_URI': 'gtr_people.csv',
        'ITEM_PIPELINES': {
            'gtr.pipelines.GtrPeoplePipeline': 300,
            }
        }

    allowed_domains = ['gtr.ukri.org']
    start_urls = ['https://gtr.ukri.org/search/person?term=*&selectedFacets=&fields=acp.d,is.t,prod.t,pol.oid,acp.oid,rtp.t,pol.in,prod.i,per.pro.abs,acp.i,col.org,acp.t,is.d,is.oid,cpro.rtpc,prod.d,stp.oid,rtp.i,rdm.oid,rtp.d,col.dept,ff.d,ff.c,col.pc,pub.t,kf.d,dis.t,col.oid,pro.t,per.sn,org.orcidId,per.on,ff.dept,rdm.t,org.n,dis.d,prod.oid,so.cn,dis.i,pro.a,pub.orcidId,pol.gt,rdm.i,rdm.d,so.oid,per.fnsn,per.org.n,per.pro.t,pro.orcidId,pub.a,col.d,per.orcidId,col.c,ip.i,pro.gr,pol.i,so.t,per.fn,col.i,ip.t,ff.oid,stp.i,so.i,cpro.rcpgm,cpro.hlt,col.pic,so.d,ff.t,ip.d,dis.oid,ip.oid,stp.d,rtp.oid,ff.org,kf.oid,stp.t&type=&fetchSize=25&selectedSortableField=score&selectedSortOrder=DESC&page=1']

    def parse(self, response):

        links = response.xpath('//a[contains(@href,"person")]/@href')
        next_page = response.xpath('//a[@class="btn-mini btn-css3 btn-responsive btn-css3-default next"]/@href')

        for ind, link in enumerate(links):
            if ind == 0:
                continue
            url = response.urljoin(link.extract())
            req = scrapy.Request(url, callback=self.parse_person)
            #time.sleep(0.1)
            yield req

        try:
            goto_next_page = response.urljoin(next_page[0].extract())
            yield scrapy.Request(goto_next_page, callback=self.parse)
        except:
            print("# Finished scrapping data...")
            
    def parse_person(self, response):
        data = {}
        
        # url = response.request.url

        try:
            name = response.xpath('//h1[@class="gtr-per-name"]/text()').extract()[0].strip()
        except:
            name = ""
            
        name_tmp = name.split(" ")
        first_name = name_tmp[0]
        last_name = name_tmp[1:]

        try:
            organisation = response.xpath('//div[@class="gtr-per-org"]/text()').extract()[1].strip()
        except:
            organisation = ""
            
        data["Name"] = name
        data["First Name"] = first_name
        data["Last Name"] = " ".join(last_name)
        data["Organisation"] = organisation
                
        yield data
                        
if __name__ == "__main__":
    
    process = CrawlerProcess()
    process.crawl(GtrPeopleSpider)
    process.start()
import scrapy
from scrapy.crawler import CrawlerProcess
#import time

class GtRProjectPeopleSpider(scrapy.Spider):
    
    # Scrape projects from Gateway to Research
    
    name = 'gtr'

    custom_settings = {
        'FEED_URI': 'gtr_project_people.csv',
        'ITEM_PIPELINES': {
            'gtr.pipelines.GtrProjectPeoplePipeline': 300,
            }
        }
    
    allowed_domains = ['gtr.ukri.org']
    start_urls = ['https://gtr.ukri.org/search/project?term=*&selectedFacets=&fields=acp.d,is.t,prod.t,pol.oid,acp.oid,rtp.t,pol.in,prod.i,per.pro.abs,acp.i,col.org,acp.t,is.d,is.oid,cpro.rtpc,prod.d,stp.oid,rtp.i,rdm.oid,rtp.d,col.dept,ff.d,ff.c,col.pc,pub.t,kf.d,dis.t,col.oid,pro.t,per.sn,org.orcidId,per.on,ff.dept,rdm.t,org.n,dis.d,prod.oid,so.cn,dis.i,pro.a,pub.orcidId,pol.gt,rdm.i,rdm.d,so.oid,per.fnsn,per.org.n,per.pro.t,pro.orcidId,pub.a,col.d,per.orcidId,col.c,ip.i,pro.gr,pol.i,so.t,per.fn,col.i,ip.t,ff.oid,stp.i,so.i,cpro.rcpgm,cpro.hlt,col.pic,so.d,ff.t,ip.d,dis.oid,ip.oid,stp.d,rtp.oid,ff.org,kf.oid,stp.t&type=%3E&fetchSize=25&selectedSortableField=score&selectedSortOrder=DESC&page=1']

    def parse(self, response):
        links = response.xpath('//a[contains(@href,"project")]/@href')#response.xpath('//a[@href[contains(text(), "project")]]')
        next_page = response.xpath('//a[@class="btn-mini btn-css3 btn-responsive btn-css3-default next"]/@href')

        for ind, link in enumerate(links):
            if ind == 0:
                continue
            url = response.urljoin(link.extract())
            req = scrapy.Request(url, callback=self.parse_projects)
            #time.sleep(0.1)
            yield req
        
        try:
            goto_next_page = response.urljoin(next_page[0].extract())
            yield scrapy.Request(goto_next_page, callback=self.parse)
        except:
            print("# Finished scrapping data...")

    def parse_projects(self, response):
     
        data = {}
        
        # url = response.request.url

        try:
            project_reference = response.xpath('//div[@class="aside-category"]/text()').extract()[4].strip()
        except:
            project_reference = ""

        try:
            title = response.xpath('//h1[@id="gtr-project-title"]/text()').extract()[0]
        except:
            title = ""

        people = response.xpath('//a[contains(@href, "/person/")]/text()').extract()

        for i in range(len(people)):
            person = people[i].replace(",","").strip()

            try:
                per_role = person.split("(")[1][:-1]
            except:
                per_role = ""
                
            try:
                person = people[i].replace(",","").strip().split("(")[0]
            except:
                pass


            data["Project Reference"] = project_reference
            data["Title"] = title
            
            org_url = response.xpath('//a[contains(@href, "/organisation/")]/@href')[0].extract()
            lead_org_id = org_url.split("/")[2]

            data["Lead Organisation ID"] = lead_org_id
            data["Lead Organisation URL"] = "https://gtr.ukri.org"+org_url

            data["People"] = person
            data["Person Role"] = per_role
            
            yield data 
        
if __name__ == "__main__":
    
    process = CrawlerProcess()
    process.crawl(GtRProjectOrganisationsSpider)
    process.start()
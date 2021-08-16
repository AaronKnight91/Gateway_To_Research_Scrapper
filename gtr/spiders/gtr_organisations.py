import scrapy
from scrapy.crawler import CrawlerProcess

class GtrOrganisationsSpider(scrapy.Spider):

    name = 'gtr_organisations'

    custom_settings = {
        'FEED_URI': 'gtr_organisations.csv',
        'ITEM_PIPELINES': {
            'gtr.pipelines.GtrOrganisationsPipeline': 300,
            }
        }

    allowed_domains = ['gtr.ukri.org']
    start_urls = ['https://gtr.ukri.org/search/organisation?term=*&selectedFacets=&fields=acp.d,is.t,prod.t,pol.oid,acp.oid,rtp.t,pol.in,prod.i,per.pro.abs,acp.i,col.org,acp.t,is.d,is.oid,cpro.rtpc,prod.d,stp.oid,rtp.i,rdm.oid,rtp.d,col.dept,ff.d,ff.c,col.pc,pub.t,kf.d,dis.t,col.oid,pro.t,per.sn,org.orcidId,per.on,ff.dept,rdm.t,org.n,dis.d,prod.oid,so.cn,dis.i,pro.a,pub.orcidId,pol.gt,rdm.i,rdm.d,so.oid,per.fnsn,per.org.n,per.pro.t,pro.orcidId,pub.a,col.d,per.orcidId,col.c,ip.i,pro.gr,pol.i,so.t,per.fn,col.i,ip.t,ff.oid,stp.i,so.i,cpro.rcpgm,cpro.hlt,col.pic,so.d,ff.t,ip.d,dis.oid,ip.oid,stp.d,rtp.oid,ff.org,kf.oid,stp.t&type=&fetchSize=25&selectedSortableField=score&selectedSortOrder=DESC&page=1']

    def parse(self, response):

        links = response.xpath('//a[contains(@href,"organisation")]/@href')
        next_page = response.xpath('//a[@class="btn-mini btn-css3 btn-responsive btn-css3-default next"]/@href')

        for ind, link in enumerate(links):
            if ind == 0:
                continue
            url = response.urljoin(link.extract())
            req = scrapy.Request(url, callback=self.parse_organisations)
            #time.sleep(0.1)
            yield req

        try:
            goto_next_page = response.urljoin(next_page[0].extract())
            yield scrapy.Request(goto_next_page, callback=self.parse)
        except:
            print("# Finished scrapping data...")

    def parse_organisations(self, response):
        data = {}
        
        url = response.request.url

        try:
            organisation_name = response.xpath('//h1[@class="gtr-org-name"]/text()').extract()[0].strip()
        except:
            organisation_name = ""

        try:
            organisation_address = response.xpath('//p[@class="gtr-org-addr"]/text()').extract()[0].strip()
        except:
            organisation_address = ""
            
        try:
            address = organisation_address.split("(")
            region = address[-1][:-1]
            if not region:
                region = ""
            country = ""
            address = address[0]                
            if region == "Outside UK":
                country = address.split(",")[-1]

        except:
            address = ""
            region = ""
            country = ""
            
        try:
            postcode = ""
            add = organisation_address.split(", ")
            
            for i in range(len(add)):
                tmp = add[i].strip()
                
                try:
                    tmp = tmp.split("(")[0].strip()
  
                    num_numeric = sum(i.isdigit() for i in tmp)
                    num_alpha = sum(i.isalpha() for i in tmp)
                    num_space = sum(i.isspace() for i in tmp)

                    if (len(tmp) <= 9) and (num_space == 1) and (num_alpha >= 3):
                        if num_numeric >= 2 and num_numeric <= 4:
                            postcode = tmp
                
                except:
                    num_numeric = sum(i.isdigit() for i in tmp)
                    num_alpha = sum(i.isalpha() for i in tmp)
                    num_space = sum(i.isspace() for i in tmp)

                    if (len(tmp) <= 9) and (num_space == 1) and (num_alpha >= 3):
                        if num_numeric >= 2 and num_numeric <= 4:
                            postcode = tmp

        except:
            postcode = ""
            
        org_id = url.split("/organisation/")[1]

        data["Organisation ID"] = org_id
        data["Organisation URL"] = url

        data["Organisation Name"] = organisation_name
        data["Address"] = address
        data["Region"] = region
        data["Postcode"] = postcode
        data["Country"] = country        
        data["Type"] = ""
        
        yield data
                        
if __name__ == "__main__":
    
    process = CrawlerProcess()
    process.crawl(GtrOrganisationsSpider)
    process.start()
import scrapy
from scrapy.crawler import CrawlerProcess
#import time

class GtRProjectsSpider(scrapy.Spider):
    
    # Scrape projects from Gateway to Research
    
    name = 'gtr'

    custom_settings = {
        'FEED_URI': 'gtr_projects.csv',
        'ITEM_PIPELINES': {
            'gtr.pipelines.GtrProjectsPipeline': 300,
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
        
        url = response.request.url
        
        try:
            project_reference = response.xpath('//div[@class="aside-category"]/text()').extract()[4].strip()
        except:
            project_reference = ""

        try:
            project_category = response.xpath('//div[@class="aside-category"]/text()').extract()[3].strip()
        except:
            project_category = ""

        try:
            title = response.xpath('//h1[@id="gtr-project-title"]/text()').extract()[0]
        except:
            title = ""

        try:
            lead_org = response.xpath('//a/text()').extract()[6].strip()
        except:
            lead_org = ""

        try:
            department = response.xpath('//div[@id="gtr-proj-dept"]/text()').extract()[0].split(":")[1]
        except:
            department = ""

        abstract = ""
        tech_sum = ""
        planned_impact = ""
        try:
            for ind, ab in enumerate(response.xpath('//div[@id="abstract"]/text()').extract()):
                if ind == 0:
                    continue
                abstract += response.xpath('//div[@id="abstract"]/text()').extract()[ind].strip() + " "
        except:
            abstract = ""
        
        other_sum = response.xpath('//h3[@class="project-h3"]/text()').extract()
        for i in range(len(other_sum)):
            if other_sum[i] == "Technical Summary":
                for ind, ts in enumerate(response.xpath('//div[@id="technicalSummary"]/text()').extract()):
                    tech_sum += response.xpath('//div[@id="technicalSummary"]/text()').extract()[ind].strip() + " "
            if other_sum[i] == "Planned Impact":
                for ind, ts in enumerate(response.xpath('//div[@id="plannedImpactText"]/text()').extract()):
                    planned_impact += response.xpath('//div[@id="plannedImpactText"]/text()').extract()[ind].strip() + " "
            
        try:
            funder = response.xpath('//div[@id="result-collapse"]/text()').extract()[4].strip()
        except:
            funder = ""
            
        try:
            project_status = response.xpath('//div[@class="aside-category"]/text()').extract()[1].strip()
        except:
            project_status = ""
                        
        try:
            fund_period_start = response.xpath('//div[@id="result-collapse"]/text()').extract()[3].strip()[:6]
            fund_period_end = response.xpath('//div[@id="result-collapse"]/text()').extract()[3].strip()[-6:]
        except:
            fund_period_start = ""
            fund_period_end = ""

        fund_title = response.xpath('//h3[@class="fund-title"]/text()').extract()
        if len(fund_title) > 0:
            if fund_title[0] == "Funded Value:":
                try:
                    fund = response.xpath('//span[@id="totalFund"]/strong/text()').extract()[0].strip("£").replace(",","")
                    expenditure = ""
                except:
                    fund = ""
                    expenditure = ""
            else:
                try:
                    expenditure = response.xpath('//span[@id="totalFund"]/strong/text()').extract()[0].strip("£").replace(",","")
                    fund = ""
                except:
                    expenditure = ""
                    fund = ""
        else:
            fund = ""
            expenditure = ""

        try:
            person = response.xpath('//a[contains(@href,"person")]/text()').extract()[0].split()
            if len(person) == 2:
                principle_investigator_first = person[0]
                principle_investigator_last = person[1]
                principle_investigator_other = ""
            elif len(person) >= 3:
                if person[2][0] == "(":
                    principle_investigator_first = person[0]
                    principle_investigator_last = person[1]
                    principle_investigator_other = ""
                else:
                    principle_investigator_first = person[0]
                    principle_investigator_other = person[1]
                    principle_investigator_last = person[2]
            elif len(person) == 1:
                principle_investigator_first = person[0]
                principle_investigator_other = ""
                principle_investigator_last = ""
        except:
            principle_investigator_first = ""
            principle_investigator_other = ""
            principle_investigator_last = ""

        student = response.xpath('//div[@id="result-collapse"]/h3/text()').extract()
        person = response.xpath('//a[contains(@href, "/person/")]/text()').extract()

        student_first_name = ""
        student_last_name = ""
        student_other_name = ""
        if student[0] == "Student:":
            student = student[0].split()
            if len(student) == 2:
                student_first_name = student[0]
                student_last_name = student[1]
            if len(student) == 3:
                student_first_name = student[0]
                student_last_name = student[2]
                student_other_name = student[1]

        data["GtR Project URL"] = url                   
        data["Project Reference"] = project_reference
        data["Project Category"] = project_category
        data["Title"] = title
        data["Lead Organisation"] = lead_org
        data["Department"] = department
        data["Abstract"] = abstract     
        data["Technical Summary"] = tech_sum        
        data["Planned Impact"] = planned_impact
        data["Funder"] = funder
        data["Project Status"] = project_status
        data["Funded Period Start"] = fund_period_start
        data["Funded Period End"] = fund_period_end
        data["Total Fund"] = fund
        data["Expenditure"] = expenditure
        data["Principle Investigator First Name"] = principle_investigator_first
        data["Principle Investigator Last Name"] = principle_investigator_last
        data["Principle Investigator Other Name"] = principle_investigator_other
        data["Student First Name"] = student_first_name
        data["Student Last Name"] = student_last_name
        data["Student Other Name"] = student_other_name

        org_url = response.xpath('//a[contains(@href, "/organisation/")]/@href')[0].extract()
        lead_org_id = org_url.split("/")[2]

        data["Lead Organisation ID"] = lead_org_id
        data["Lead Organisation URL"] = "https://gtr.ukri.org"+org_url

        yield scrapy.Request("https://gtr.ukri.org"+org_url, meta={"data":data}, callback=self.parse_lead_organisation, dont_filter=True)

    def parse_lead_organisation(self, response):
        
        data = response.request.meta["data"]
        
        try:
            address = response.xpath('//p[@id="org.addr.id"]/text()').extract()[0].replace(",","").split()
        except:
            address = response.xpath('//p[@id="org.addr.id"]/text()').extract()#.replace("(","").replace(")","")

        region = []
        post_code = ""
        
        region_start = 0
        region_end = 0
        try:
            if len(address) > 1:
                for ind, add in enumerate(address):
                    if add[0] == "(":
                        region_start = ind
                    if add[-1] == ")":
                        region_end = ind
    
                if region_start == region_end:
                    region = address[region_start].replace("(","").replace(")","")
                else:
                    tmp_region = []
                    for i in range(region_start, region_end+1):
                        tmp_region.append(address[i])
                    region = " ".join(tmp_region).replace("(","").replace(")","")
        
                if address[region_start-2] == "United" and address[region_start-1] == "Kingdom":
                    post_code = address[region_start-4] + " " + address[region_start-3]
                else:
                    post_code = address[region_start-2] + " " + address[region_start-1]
        except:
            region = ""
            post_code = ""

        if not region:
            region = ""

        data["Post Code"] = post_code
        data["Region"] = region

        global org_dict
        org_dict = {data["Lead Organisation"]: [post_code, region]}
        
        yield data 
        
if __name__ == "__main__":
    
    process = CrawlerProcess()
    process.crawl(GtRProjectsSpider)
    process.start()
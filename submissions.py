from client import EdgarClient
from datetime import datetime
from constants import ARCHIVE_DATA_ENDPOINT, SUBMISSIONS_API_ENDPOINT
from itertools import chain
from parserdoc import ParserDoc
from bs4 import BeautifulSoup

today = datetime.today()
today_f = today.strftime("%Y-%m-%d")










class Submissions():


    def __init__(self, user: str):
        
        self.client = EdgarClient(user=user)
        
        
        
    @staticmethod
    def merge_submission_dicts(to_merge):
        """Merge dictionaries with same keys."""
        merged = {}
        for k in to_merge[0].keys():
            merged[k] = list(chain.from_iterable(d[k] for d in to_merge))
        return merged



    def get_all_raw_submissions_(self, cik, start_date: str = None):

        z_cik = str(cik).zfill(10)

        endpoint = f"{SUBMISSIONS_API_ENDPOINT}/CIK{z_cik}.json"
        subms = self.client.get_resp(endpoint)
        
        filings = subms['filings']
        pages = filings['files']

        if pages:
            to_merge = [filings['recent']]
            for sub in pages:
                filename = sub['name']
                filingto = sub['filingTo']
                if self.f_date(start_date) < self.f_date(filingto):
                    api_endpoint = f"{SUBMISSIONS_API_ENDPOINT}/{filename}"
                    r =  self.client.get_resp(api_endpoint)
                    to_merge.append(r)
                else:
                    break

            filings['recent'] = self.merge_submission_dicts(to_merge)
            filings['files']  = []

        return subms

        



    def get_filings_from_subms_(self, cik, start_date):
        data = self.get_all_raw_submissions_(cik, start_date)
        filings = data['filings']['recent']
        name = data['name']
        
        return name, filings


    


    def get_all_filings_(self, cik, start_date):

        z_cik = str(cik).zfill(10)

        c_name, filings = self.get_filings_from_subms_(cik, start_date)

        num_filings = len(filings['accessionNumber'])

        master_filings_list = []
        for i in range(num_filings):
            
            fil_dict = {}
            accession_number = filings['accessionNumber'][i].strip()
            accession_name = accession_number.replace('-', '').strip()
            primary_document_name = filings['primaryDocument'][i].strip()

            fil_dict['companyName'] = c_name
            fil_dict['accessionNumber'] = accession_number
            fil_dict['formType'] = filings['form'][i].strip()
            fil_dict['filingDate'] = filings['filingDate'][i].strip()
            fil_dict['reportDate'] = filings['reportDate'][i].strip()
            fil_dict['primaryDocLink'] = f"{ARCHIVE_DATA_ENDPOINT}/{z_cik}/{accession_name}/{primary_document_name}"
            
            master_filings_list.append(fil_dict)
        
        return master_filings_list




    @staticmethod
    def f_date(date_str: str):
        return int(date_str.strip().replace('-', ''))




    def get_filings(self, ciks, form_type=None, start_date:str='2000-01-01', end_date:str=today_f) -> dict:
        start_date_f = self.f_date(start_date)
        end_date_f = self.f_date(end_date)


        filings_list = []

        if type(ciks) == int:
            cik_list = [ciks]
        else:
            cik_list = ciks

        
        for cik in cik_list:
            all_filings = self.get_all_filings_(cik, start_date)


            for i in all_filings:
                filing_date_f = self.f_date(i['filingDate'])

                if form_type != None:
                    if type(form_type) == list:
                        for k in form_type:
                            if i['formType'].upper() == k.upper() and filing_date_f >= start_date_f and filing_date_f <= end_date_f:
                                filings_list.append(i)
                    elif type(form_type) == str:
                        if i['formType'].upper() == form_type.upper() and filing_date_f >= start_date_f and filing_date_f <= end_date_f:
                            filings_list.append(i)
                else:
                    if filing_date_f >= start_date_f and filing_date_f <= end_date_f:
                        filings_list.append(i)

            

        return filings_list





    def get_doc_from_url_(self, url):
        # resp = self.client.get_resp(url)
        # soup = BeautifulSoup(resp, 'lxml')
        # doc = soup.extract()
        
        return BeautifulSoup(self.client.get_resp(url), 'lxml').extract()




    def parse_10k(self, filings_list_dict):
    
        parsed_10k_list = []
        for i in filings_list_dict:
            #url = i['primaryDocLink']
            doc_parser = ParserDoc(self.get_doc_from_url_(url=i['primaryDocLink']))
            parsed_doc_l = doc_parser.get_10k_parsed_text_()
            parsed_doc_d = {key: value for d in parsed_doc_l for key, value in d.items()}
            m_dict = i | parsed_doc_d
            parsed_10k_list.append(m_dict)
                
        return parsed_10k_list

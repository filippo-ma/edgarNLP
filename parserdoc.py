from bs4 import BeautifulSoup
import re

from patterns import standardize_item_name, ITEM_PATTERNS, ITEM_CODES_CLEAN, SINGLE_ITEM_PATTERN, ITEM_NAMES



class ParserDoc():


    def __init__(self, soup_doc):
        self.doc = soup_doc
       
    
    def get_10form_item_tags_(self):

        item_tags_ = []
        company_item_codes = []
        doc_tags = self.doc.find_all(name=['span', 'p'], text=True)
        
        for index, tag in enumerate(doc_tags):
            tag_text = standardize_item_name(tag.text.replace("\xa0", ' ').replace("\t", ' '))
            matched1 = re.match(ITEM_PATTERNS, tag_text)
            matched2 = re.match(SINGLE_ITEM_PATTERN, tag_text)

            if matched1:
                if tag.contents[0].name != 'span' and tag.parent.name != 'td' and tag.parent.parent.name != 'td' and tag.parent.parent.parent.name != 'td':
                    tag_split = tag_text.split(' ')
                    
                    if len(tag_split) > 1:
                        item_code = f"{tag_split[0].strip()}_{tag_split[1].strip()}".replace('.','').upper()
                    else:
                        item_code = tag_text.replace('.', '').upper().strip()
                    
                    company_item_codes.append(item_code)
                    item_tags_.append(tag)

            # tags case (e.g <span>Item. 1</span><span>Business</span>)
            elif matched2:
                if tag.contents[0].name != 'span' and tag.parent.name != 'td' and tag.parent.parent.name != 'td' and tag.parent.parent.parent.name != 'td':
                    tag_split = tag_text.split(' ')

                    next_tag = doc_tags[index+1]
                    next_tag_text = standardize_item_name(next_tag.text.replace("\xa0", " ").replace("\t", ' '))
                    next_tag_matched = re.match(r"|".join(ITEM_NAMES), next_tag_text)

                    if next_tag_matched:
                    
                        if len(tag_split) > 1:
                            item_code = f"{tag_split[0].strip()}_{tag_split[1].strip()}".replace('.','').upper()
                        else:
                            item_code = tag_text.replace('.', '').upper().strip()
                    
                        company_item_codes.append(item_code)
                        item_tags_.append(tag)

            
        item_tags = [str(i) for i in item_tags_]

        
        return item_tags, company_item_codes


    

    def get_10k_company_index_(self):

        item_index_ = []

        tags, company_item_codes = self.get_10form_item_tags_()

        if len(tags) > 0:

            regex_delimiter_pattern = '|'.join(map(re.escape, tags))
            splitted_doc = re.split(regex_delimiter_pattern, str(self.doc))

            for index, item in enumerate(company_item_codes):

                item_dict = {}
                
                item_str = splitted_doc[1:][index]
                item_soup = BeautifulSoup(item_str, 'html.parser')

                item_dict['itemCode'] = item
                item_dict['itemPageRaw'] = item_soup

                item_index_.append(item_dict)

        item_index = [item for item in item_index_ if item['itemCode'] in ITEM_CODES_CLEAN]

        for i in item_index:
            i['rawText'] = ''.join(i['itemPageRaw'].get_text(' ', strip=True))

        
        return item_index




    def get_10k_parsed_text_(self):
            
        company_index = self.get_10k_company_index_()
        standardized_item_index = []
        for code in ITEM_CODES_CLEAN:
            item_dict = {}
            for item in company_index:
                if code == item['itemCode']:
                    item_dict[code] = item['rawText']
                    break
                else:
                    item_dict[code] = 'not found'
                
            standardized_item_index.append(item_dict)

   
        return standardized_item_index
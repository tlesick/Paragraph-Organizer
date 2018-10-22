# -*- coding: utf-8 -*-
import re
# All parameters take in a list  v 
class Paragraph_Organizer(object):
    def getIterLength(self, iterator):
        temp = list(iterator)
        result = len(temp)
        iterator = iter(temp)
        return result


    def space_removal(self, array_paragraph):
        new_para = []
        non_white = re.compile("\S+")
        white_space_text = re.compile("\s{2,}")

        for value in array_paragraph:
            if len(value) == 1 and False == bool(non_white.match(value)):
                continue
            temp = ''
            # remove the symbols
            if '\r\n' in value or '\n' in value or '\r' in value:
                temp = value.replace('\r\n', '')
                temp.replace('\r', '')
                temp.replace('\n', '')
                value = temp
            a_match = white_space_text.search(value)
            if a_match:
                # print(value)
                beg_removal, end_removal = a_match.span()[0], a_match.span()[1]
                # All Spaces
                if beg_removal == 0 and len(value) == end_removal:
                    continue
                # Spaces in beginning
                if beg_removal == 0 and len(value) != end_removal:
                    value = value[end_removal:]
                    # Spaces then Words then spaces
                    end_space_match = white_space_text.search(value)
                    if end_space_match:
                        beg_rm_2 = end_space_match.span()[0]
                        end_rm_2 = end_space_match.span()[1]
                        if beg_rm_2 != 0 and  len(value) == end_rm_2:
                            value = value[:beg_rm_2]
                # Words then excess space
                if beg_removal != 0 and  len(value) == end_removal:
                    value = value[:beg_removal]
                
            new_para.append(value)
        return new_para

    def paragraph_organizer(self, entire_para, para_only, links_only, exclude):
        reformatted = []
        entire_encoded = []
        para_encoded = []
        links_encoded = []
        exclude_encoded = []
        white_space = re.compile("\s+")
        count = 0
        
        
        # Encode the Paragraphs
        while((len(entire_para)-1)>= count):
            entire_encoded.append(entire_para[count].encode('utf-8').decode('unicode_escape').encode('ascii', 'ignore').decode('utf-8'))
            try:
                if para_only[count].find('\u2592'):
                    para_only[count].replace('\u2592', '')
                if "\r" or "\n" in para_only[count]:
                    try:
                        para_only[count].replace("\r", '')
                        para_only[count].replace("\n", '')
                    except:
                        pass
                para_encoded.append(para_only[count].encode('utf-8').decode('unicode_escape').encode('ascii', 'ignore').decode('utf-8'))
            except:
                pass
            try:
                links_encoded.append(links_only[count].encode('utf-8').decode('unicode_escape').encode('ascii', 'ignore').decode('utf-8'))
            except:
                pass
            try:
                exclude_encoded.append(exclude[count].encode('utf-8').decode('unicode_escape').encode('ascii', 'ignore').decode('utf-8'))
            except:
                pass
            count += 1
    
        # Go through Entire text of article
        for entire_key, entire_value in enumerate(entire_encoded):
            if white_space.match(entire_value):
                continue
            inner_break = False
            for excluded_key, excluded_value in enumerate(exclude):
                if str(excluded_value) == str(entire_value) or bool(str(entire_value).find(str(excluded_value))):
                    inner_break = True
                    break
            if inner_break:
                continue
            for para_key, para_value in enumerate(para_encoded):
                if str(para_value) == str(entire_value) or bool(str(entire_value).find(str(para_value))):
                    
                    reformatted.append(para_value)
                    entire_encoded.pop(entire_key)
                    para_encoded.pop(para_key)
                    break
                elif str(para_value) != str(entire_para) or False == bool(str(entire_value).find(str(para_value))):
                    for link_key, link_value in enumerate(links_encoded):
                        if str(link_value) == str(entire_value) or bool(str(entire_value).find(str(link_value))):
                            reformatted.append(link_value)
                            entire_encoded.pop(entire_key)
                            links_encoded.pop(link_key)
                            inner_break = True
                            break
                elif inner_break == True:
                    break

        reformatted = Paragraph_Organizer.space_removal(self, array_paragraph=reformatted)
        
        return reformatted
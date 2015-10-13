#!/usr/bin/python3

# -*- coding: utf-8 -*-
#
# read_text_file.py
#
#  Copyright 2015 Stefan Schaub
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  

import json,collections
import re,sys
import geonames
import certificates as ce

def get_key_value_pair(fileobject):
    print ("test")

def removing_whitspaces(dict):
    for k, v in dict.items():
        dict[k] = v.lstrip()

def to_json(fileobject, text_file_name='testJsonOutput'):

    with open(text_file_name, 'w') as outfile:
        for i in fileobject:
 
            json.dump(i, outfile,indent=2,ensure_ascii=False)

def get_data_sets(string):
    data_set_array = re.split(r'\.-\s',string)
    return data_set_array

def check_for_date(__substring,birth_date):
    __date_regex = '[0-9]+\.[0-9]+\.[0-9][0-9]+'
    __place_of_date=re.search(__date_regex,__substring) 
    if __place_of_date is not None:
        __date = __substring[__place_of_date.start():__place_of_date.end()]
        birth_date.append(__date)
        __rest_of_substring = __substring[:__place_of_date.start()]+__substring[__place_of_date.end():]
        return __rest_of_substring 
    return __substring

def get_academic_title(value,dict):
    __regex_4_academic_title='(stud\.)+|(Dr\.)+|(dr\.)+|(Stud\.)+'
    __aca_title_begin = re.search(__regex_4_academic_title,value)
    if __aca_title_begin is not None:
        __aca_title_end = value.find(',')
        if __aca_title_end == -1: 
            __aca_title_end_2 = value.lower().find('aus')

        if __aca_title_end != -1:
            __substring = value[__aca_title_begin.start(): __aca_title_end]
            dict['academic_title'] = __substring
            return value[(__aca_title_end)+1 :]
        elif __aca_title_end_2 != -1:
            __substring = value[__aca_title_begin.start(): __aca_title_end_2]
            
            dict['academic_title'] = __substring
            rest_of_substring=value[:__aca_title_begin.start()]+value[__aca_title_end_2:]
            return rest_of_substring 
        print("No delimiter found for get_academic_title in: ", value)
    else:
        pass
    return value 
                
    

def get_birth_place_and_academic_title(value,dict):
    loc=None
    __FROM_LEIPZIG=0
    __look_for_suffix=False
    __counter=0
    __substring_additional_info=''
    if value.find('--') == -1:
        return -2
    try:
        __substring=re.split(':',value,1)
        __substring=re.split('--',__substring[1],1)
        __substring=__substring[0]
        __birth_date_tmp=[]
        __birth_date=None
        __substring=check_for_date(__substring,__birth_date_tmp)
        if len(__birth_date_tmp) != 0: 
            __birth_date=__birth_date_tmp[0]

        __substring=get_academic_title(__substring,dict)
        
        __regex_4_add_information=r'(,)+|(\Wb.\W)+|(\Wb\W)+|(Bez.)+|(bez.)+|(\Wa.d.\W)+'
        __birthplace_delimiter = re.search(__regex_4_add_information,__substring)


        if __birthplace_delimiter is not None:
           
            __substring_additional_info=__substring[__birthplace_delimiter.start():] 
            __substring=__substring[:__birthplace_delimiter.start()]
            __look_for_suffix=True
        __cut_prefix_string=r'(\Wgeb.\W)+|(\Waus\W)+|(\Win\W)|(\WAus\W)+'

        __substring= re.sub(__cut_prefix_string,'',__substring)
        __substring=__substring.strip()
        
        list_leipzig_suburb=open('liste_leipziger_vororte_clean','r')
        for item in list_leipzig_suburb:
            if item.strip().lower() == __substring.lower():
                __look_for_suffix=True
                __substring_additional_info=__substring
                __substring='Leipzig'
                __FROM_LEIPZIG=1         
        if not __FROM_LEIPZIG:
            print('get location "' + __substring + '"...')

            loc = geonames.Location.getLocation(__substring)

            if __birth_date is not None:

                if(loc is None):
                    dict['birthplace'] = {"name": __substring,"birth_date": __birth_date}
                else:
                    dict['birthplace'] = {"source": __substring, "geonameId": loc.getGeonameId(),  "name": loc.getName(), "latitude": loc.getLat(), "longitude": loc.getLng(), "url": loc.getUrl(), "birth_date": __birth_date}
            else:
                if(loc is None):
                    dict['birthplace'] = {"name": __substring}
                else:
                    dict['birthplace'] = {"source": __substring, "geonameId": loc.getGeonameId(),  "name": loc.getName(), "latitude": loc.getLat(), "longitude": loc.getLng(), "url": loc.getUrl()}
        if __look_for_suffix==True:
            __substring_additional_info=re.sub(__regex_4_add_information,'',__substring_additional_info)
            __substring_additional_info=__substring_additional_info.strip()
            if __birth_date is not None:
                if(loc is None):
                    dict['birthplace'] = {"name": __substring,"birth_date": __birth_date ,"additional_information_of_birthplace": __substring_additional_info}
                else:
                    dict['birthplace'] = {"source": __substring, "geonameId": loc.getGeonameId(),  "name": loc.getName(), "latitude": loc.getLat(), "longitude": loc.getLng(), "url": loc.getUrl(), "birth_date": __birth_date,"additional_information_of_birthplace": __substring_additional_info}
            else:
                if(loc is None):
                    dict['birthplace'] = {"name": __substring,"additional_information_of_birthplace": __substring_additional_info}
                else:
                    dict['birthplace'] = {"source": __substring, "geonameId": loc.getGeonameId(),  "name": loc.getName(), "latitude": loc.getLat(), "longitude": loc.getLng(), "url": loc.getUrl(),"additional_information_of_birthplace": __substring_additional_info}

            return 2
        
    except IndexError:
        return -1
    return 1

def get_surname(value_list,dict):
    __substring=re.split(',',value_list)
    try:
        dict['surname'] = __substring[0]
    except IndexError:
        print("No surname was found! ", file=sys.stderr)
        

def get_prename(value_list,dict):
    value_list=value_list.strip()
    dict['prename'] = value_list

def get_certificate(value,dict,jump_to_certificate ):
    __look_4_zeugnis = value.find('--')
    
    if __look_4_zeugnis != -1: 
        certificate = value[__look_4_zeugnis+2:].strip() 
    elif jump_to_certificate:
        __look_4_zeugnis = value.find(':')
        certificate = value[__look_4_zeugnis+1:].strip() 
    else:
        pass

    jsonCertifications = []
    for cert in ce.Certificate.getCertificates(certificate):
        loc = cert.getLocation()

        #jsonCert = {'source': cert.getSource().strip(), 'name': cert.getName()}
        jsonCert = {'name': cert.getName()}
        if cert.getType() is not None:
            jsonCert['type'] = cert.getType()
        if cert.getYear() is not None:
            jsonCert['year'] = cert.getYear()
        if(loc is not None):
            jsonCert['location'] = {"geonameId": loc.getGeonameId(),  "name": loc.getName(), "latitude": loc.getLat(), "longitude": loc.getLng(), "url": loc.getUrl()}
        
        jsonCertifications.append(jsonCert)

    dict['certificate'] = jsonCertifications

def getting_name(value_list,dict):
    """ get everything before the colon """
    __substring = re.split(':',value_list, 1)

    try:
        __substring = __substring[0]
        get_surname(__substring,dict)
        __substring=re.sub('.*,','',__substring,1)
        get_prename(__substring,dict)
    except IndexError:
        print("No surmane and/or prename section found before \':\' ! ", file=sys.stderr)

def academic_title(value_string,dict):
    __substring=re.split(':',value_string,1)
    __substring=__substring[:1]
    __substring=re.split('--',__substring[1],1)

def check_for_begin(line):
    mat = re.search('[A-Za-z]*\s?,\s?[A-Za-z]*\s?[A-Za-z]*\s?[A-Za-z]*:',line)
    print (line)
    if mat:
        begin = mat.start()
        return line[begin:]

    else:
        return -1

def fill_dict(textfile_object):
    jump_to_certificate = 0
    list_of_dicts = []
    data_set_array=get_data_sets(textfile_object)

    for listitem in data_set_array:
        dict = collections.OrderedDict()
        org_listitem = listitem
        getting_name(listitem,dict)
        jump_to_certificate = get_birth_place_and_academic_title(listitem,dict)
        get_certificate(listitem,dict,jump_to_certificate) 
        list_of_dicts.append(dict)
        dict['object_under_onvestigation'] = listitem 
        del dict

    return list_of_dicts



if __name__ == '__main__':
    dictionary_list = []
    __file_to_read='personendaten2.txt'
    __file_name=re.sub('\.txt','',__file_to_read)
    file_object = open(__file_to_read, 'r')
    for line in file_object:
        line = check_for_begin (line)
        if line == -1:
            continue
        dictionary_list.append(fill_dict(line))
    to_json(dictionary_list,__file_name+'.json')

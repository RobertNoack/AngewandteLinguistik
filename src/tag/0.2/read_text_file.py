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

    #print ("in JASON:",fileobject)
    #text_file = open('text_file_name', 'w')
    #json.dump(fileobject, text_file, True)
    #for i in fileobject:
        #print ("+++",i)
    #json.dumps(fileobject, text_file, True)
    #print ("+++++",json.dumps(fileobject))


    with open(text_file_name, 'w') as outfile:
        for i in fileobject:
#            json.dump(i['surname'],outfile,indent=2,ensure_ascii=False)   
#            json.dump(i['prename'],outfile,indent=2,ensure_ascii=False)   
#            json.dump(i['birthplace'],outfile,indent=2,ensure_ascii=False)   
#            json.dump(i['additional_information_of_birthplace'],outfile,indent=2,ensure_ascii=False)   
#            json.dump(i['certificate'],outfile,indent=2,ensure_ascii=False)   
#            json.dump(i['object_under_onvestigation'],outfile,indent=2,ensure_ascii=False)   

 
            json.dump(i, outfile,indent=2,ensure_ascii=False)

def get_data_sets(string):
    data_set_array = re.split(r'\.-\s',string)
    return data_set_array

def check_for_date(__substring,__substring_additional_info ):
    __date_regex = '[0-9]+\.[0-9]+\.[0-9][0-9]+'
    __look_for_suffix=False
    __place_of_date=re.search(__date_regex,__substring) 
    if __place_of_date is not None:
        __substring_additional_info = __substring_additional_info + __substring[__place_of_date.start():__place_of_date.end()]
        #print ("üüüüüüüüüüüü ",__substring_additional_info)
        __look_for_suffix=True
        __substring=__substring[:__place_of_date.start()] + __substring [__place_of_date.end():]
        #__substring=re.sub(__date_regex,'',__substring)
        #print ("----------------",__substring)
    return ([__substring,__substring_additional_info, __look_for_suffix ])

def get_academic_title(value,dict):
    __regex_4_academic_title='(stud\.)+|(Dr\.)+|(dr\.)+|(Stud\.)+'
    __aca_title_begin = re.search(__regex_4_academic_title,value)
    if __aca_title_begin is not None:
        __aca_title_end = value.find(',')
        if __aca_title_end == -1: 
            __aca_title_end_2 = value.find('aus')
            if __aca_title_end_2 == -1:
                __aca_title_end_2 = value.find('Aus')
        if __aca_title_end != -1:
            __substring = value[__aca_title_begin.start(): __aca_title_end]
            dict['academic_title'] = __substring
            return value[(__aca_title_end)+1 :]
        elif __aca_title_end_2 != -1:
            __substring = value[__aca_title_begin.start(): __aca_title_end]
            dict['academic_title'] = __substring
            return value[(__aca_title_end):]
        print("No delimiter found for get_academic_title in: ", value)
    else:
        dict['adcademic title'] = None
    return value 
                
    

def get_birth_place_and_academic_title(value,dict):
    __FROM_LEIPZIG=0
    __look_for_suffix=False
    __counter=0
    __substring_additional_info=''
    ## if no -- was found, there are no birthplace informations
    if value.find('--') == -1:
        #print ("\n",value)
        #print ("jumping to certificate",dict['surname']," ",dict['prename'])
        dict['additional_information_of_birthplace'] = None 
        dict['birthplace'] = None
        return -2
    try:
        __substring=re.split(':',value,1)
        __substring=re.split('--',__substring[1],1)
        __substring=__substring[0]
       
        __substring=get_academic_title(__substring,dict)
        #print ("rest 4 Birthplace: ",__substring)
        
        __regex_4_add_information=r'(,)+|(\Wb.\W)+|(\Wb\W)+|(Bez.)+|(bez.)+'
        __birthplace_delimiter = re.search(__regex_4_add_information,__substring)
        #print (__birthplace_delimiter )


        if __birthplace_delimiter is not None:
           
            #print("präfix found! ")
            __substring_additional_info=__substring[__birthplace_delimiter.start():] 
            __substring=__substring[:__birthplace_delimiter.start()]
            #print("__birthplace_delimiter.start(): ", __birthplace_delimiter.start() )
            __look_for_suffix=True
        else:
            list=check_for_date(__substring,__substring_additional_info )
            __substring = list[0]
            __substring_additional_info= list[1]  
            __look_for_suffix = list[2]
            
           #print ("----+++++--------",__substring_additional_info) 
        #__substring = value[(__colon_place+1):]
        __cut_prefix_string=r'(geb.)+|(aus)+|(in)'

        __substring= re.sub(__cut_prefix_string,'',__substring)
        __substring=__substring.strip()
        #print ("---------", __substring,"--------",__substring_additional_info )
        
        list_leipzig_suburb=open('liste_leipziger_vororte_clean','r')
        for item in list_leipzig_suburb:
            if item.strip().lower() == __substring.lower():
                dict['birthplace'] = {"name": "Leipzig"}
                __look_for_suffix=True
                __substring_additional_info=__substring
                __FROM_LEIPZIG=1         
        if not __FROM_LEIPZIG:
               print('get location "' + __substring + '"...')
               loc = geonames.Location.getLocation(__substring)
                  
               if(loc is None):
                  dict['birthplace'] = {"name": __substring}
               else:
                  dict['birthplace'] = {"source": __substring, "geonameId": loc.getGeonameId(),  "name": loc.getName(), "latitude": loc.getLat(), "longitude": loc.getLng(), "url": loc.getUrl()}

        if __look_for_suffix==True:
            ##new substring    
             
            #__possible_suffix_string=r'(Bez.)+|(bez.)+|(b.)+|(b)+'             
            #__possible_suffix=re.findall(__possible_suffix_string,__substring_additional_info)
            __substring_additional_info=re.sub(__regex_4_add_information,'',__substring_additional_info)
            
            #print () 
            
            #print ("__possible_suffix: ", __possible_suffix)
            #if __possible_suffix:
            # __substring_additional_info=__substring_additional_info[1:]
            __substring_additional_info=__substring_additional_info.strip()
           
            dict['additional_information_of_birthplace'] = __substring_additional_info
            
            return 2
        else:
            dict['additional_information_of_birthplace'] = None 
       
        #value_list.pop(__counter-1)
        
    except IndexError:
        #print("Did not found informations about birthplace \':\' ! ", file=sys.stderr)
        dict['birthplace'] = None
        dict['additional_information_of_birthplace'] = None
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
    #__counter = 0
    #print (jump_to_certificate)
    __look_4_zeugnis = value.find('--')
    #print("certificates:",value)
    
    if __look_4_zeugnis != -1: 
        #print ("############found certificate!############")
        #print (value[__look_4_zeugnis+2:].strip() )
        certificate = value[__look_4_zeugnis+2:].strip() 
        #value='asd'
        #value_list.pop(__counter)
    #__counter+=1
    elif jump_to_certificate:
        #print ("HALLO")
        __look_4_zeugnis = value.find(':')
        certificate = value[__look_4_zeugnis+1:].strip() 
    else:
        certificate = None

    jsonCertifications = []
    for cert in ce.Certificate.getCertificates(certificate):
        #print("source: " + cert.getSource())
        #print("year: " + str(cert.getYear()))
        loc = cert.getLocation()
        #if(loc is not None):
            #print("location: " + loc.getName())

        jsonCert = {'source': cert.getSource(), 'name': cert.getName()}
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
        #__substring = __substring[:len(__substring)-1]
        #print ("name-substring: ",__substring)
        get_surname(__substring,dict)
        __substring=re.sub('.*,','',__substring,1)
        get_prename(__substring,dict)
        #print ("Name: ",dict)  
    except IndexError:
        print("No surmane and/or prename section found before \':\' ! ", file=sys.stderr)

def academic_title(value_string,dict):
    __substring=re.split(':',value_string,1)
    __substring=__substring[:1]
    __substring=re.split('--',__substring[1],1)
    #print ("academic title: ",__substring)

def fill_dict(textfile_object):
    jump_to_certificate = 0
    list_of_dicts = []
    #print ("\n------------ begin of array---------------\n")
    data_set_array=get_data_sets(textfile_object)
    #print (data_set_array,"\n------------ end of array---------------\n")

    for listitem in data_set_array:
        
        dict = collections.OrderedDict()
        #print ("\nObject under investigation:", listitem)
        org_listitem = listitem
        getting_name(listitem,dict)
        #get_academic_title(listitem,dict)
        jump_to_certificate = get_birth_place_and_academic_title(listitem,dict)
        get_certificate(listitem,dict,jump_to_certificate) 
        list_of_dicts.append(dict)
        dict['object_under_onvestigation'] = listitem 
        #print ("list of dicts: ",listitem)
        #print ("prename \t surname \t birthplace \t add.birth.info \t certificate" )
        #for listitem in list_of_dicts:
        #    print (listitem['prename'],"\t", listitem['surname'],"\t", listitem['birthplace'],"\t", listitem['additional_information_of_birthplace'], \
        #    "\t",listitem['certificate']) 
        
        #for listitem in list_of_dicts:
        #    print ("original list: ", listitem)
        if org_listitem != listitem:
            print("!!!! CHANGED LISTITEM!!! ",listitem , file=sys.stderr)
            sys.exit 
        del dict
        #print ("left_arguments: : ",listitem)
        #print ("\n\n\n\n")       

    #removing_whitspaces(dict)
    return list_of_dicts

#def main():
 #   return 0


if __name__ == '__main__':
  #  main()
    dictionary_list = []
    file_object = open('personendaten.txt', 'r')
    for line in file_object:
        #print(line, '')
        dictionary_list.append(fill_dict(line))
        #if input("end?") == 'y':
        #    break
    to_json(dictionary_list)
    #print (dictionary_list) 

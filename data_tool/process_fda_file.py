import os.path
import json
import pandas as pd
import pubchempy as pcp
import subprocess
import time
import re
import sys
import csv
import numpy as np
import ast

MetaMap_path = "/Users/wu-chensu/Downloads/public_mm_lite/"
source_file="FDA_0113.csv"
fda_dis_output="fda_disease.json"
fda_drug_output="fda_drug.json"

def create_fda_disease_json_file(): ###create json file for FDA Orphan disease Plug-in
  with open(fda_dis_output, 'a') as outfile:
   doc=[]
   file_name="new_df2.xlsx"
   if os.path.exists(file_name):
     df=pd.read_excel(file_name,engine='openpyxl')
     df['parsed_content'] = df['parsed_content'].apply(lambda x: ast.literal_eval(x))

     if (not df['Marketing Approval Date'].isnull().values.any()):
        df['Marketing Approval Date']=df['Marketing Approval Date'].str.strip()

     if (not df['Exclusivity End Date'].isnull().values.any()):
        df['Exclusivity End Date']=df['Exclusivity End Date'].str.strip()

     dat=df.to_dict('records')

     results={}
     for rec in dat:
         drec={}
         cids=[]
         inchikeys=[]
         drec['pubchem_sid']= [x.strip() for x in rec['pubchem_sid'][1:-1].replace("'","").split(',')]
         cid_list=rec['pubchem_cid_inchikey']
         if (not pd.isna(cid_list)):
             cid_list=cid_list[1:-1].replace("'","").replace("[","").replace("]","").split(",")
             if(len(cid_list)==2):
                drec['pubchem_cid']=cid_list[0].strip()
                drec['inchikey']=cid_list[1].strip()
             else:
                for i,k in zip(cid_list[0::2], cid_list[1::2]):
                   pubchem_cid=i.strip()
                   inchikey=k.strip()
                   cids.append(pubchem_cid)
                   inchikeys.append(inchikey)

                drec['pubchem_cid']=cids
                drec['inchikey']=inchikeys


         if (len(rec['parsed_content'])==1):
             for item in rec['parsed_content']:
                parsed_text=item[0].strip()
                umls_id=item[1].strip()
         else:
                parsed_text=rec['parsed_content'][0].strip()
                umls_id=rec['parsed_content'][1].strip()

         _id="UMLS:"+umls_id
         orphan_designation=rec['Orphan Designation']
         orphan_dict = {'original_text':orphan_designation, 'umls':umls_id,'parsed_text':parsed_text}

         if (pd.isna(rec['Sponsor Country'])):
             drec['sponsor']=rec['Sponsor Company']
         else:
             drec['sponsor']=rec['Sponsor Company']+" ("+rec['Sponsor Country']+")"

         drec['approval_status']=rec['FDA Orphan Approval Status']
         drec['generic_name']=rec['Generic Name']
         drec['designated_status']=rec['Orphan Designation Status']
         drec['designated_date']=rec['Date Designated']
         drec['marketing_approval_date']=rec['Marketing Approval Date']
         drec['exclusivity_end_date']=rec['Exclusivity End Date']
         drec['orphan_designation']= orphan_dict
         drug_rec = drec.copy()
         for key, val in drec.items():
             if (isinstance(val, float)):
               if (pd.isna(val)):
                del drug_rec[key]

         results.setdefault(_id,[]).append(drug_rec)


     for _id,docs in results.items():
        doc.append({"_id": _id, "fda_orphan_drug" : docs})
     json.dump(doc, outfile, indent=4) ###for checking
     print("=====")
     file_exists = os.path.exists(fda_dis_output)
     if (file_exists):
        print("FDA disease file is ready!")
     else:
        print("FDA disease file is not ready!")

def create_fda_drug_json_file(): ###create json file for FDA Orphan drug Plug-in
  with open(fda_drug_output, 'a') as outfile:
   doc=[]
   file_name="new_df2.xlsx"
   if os.path.exists(file_name):
     df=pd.read_excel(file_name,engine='openpyxl')
     df['parsed_content'] = df['parsed_content'].apply(lambda x: ast.literal_eval(x))
     if (not df['Marketing Approval Date'].isnull().values.any()):
        df['Marketing Approval Date']=df['Marketing Approval Date'].str.strip()

     if (not df['Exclusivity End Date'].isnull().values.any()):
        df['Exclusivity End Date']=df['Exclusivity End Date'].str.strip()
    
     dat=df.to_dict('records')
     results={}
     for rec in dat:
         drec={}
         id_list=[]
         drec['pubchem_sid']= [x.strip() for x in rec['pubchem_sid'][1:-1].replace("'","").split(',')]
         cid_list=rec['pubchem_cid_inchikey']
         if (not pd.isna(cid_list)):
             cid_list=cid_list[1:-1].replace("'","").replace("[","").replace("]","").split(",")
             for i,k in zip(cid_list[0::2], cid_list[1::2]):
                 pubchem_cid=i.strip()
                 inchikey=k.strip()
                 id_list.append(inchikey+"_"+pubchem_cid)
         else:
                 id_list=drec['pubchem_sid']

         for _id in id_list:
            if ("_" in _id):
               drec['inchikey']=_id.split("_")[0]
               drec['pubchem_cid']=_id.split("_")[1]
               _id=drec['inchikey']

            orphan_designation=rec['Orphan Designation']

            if (len(rec['parsed_content'])==1):
               for item in rec['parsed_content']:
                parsed_text=item[0].strip()
                umls_id=item[1].strip()
            else:
                parsed_text=rec['parsed_content'][0].strip()
                umls_id=rec['parsed_content'][1].strip()


            orphan_dict = {'original_text':orphan_designation, 'umls':umls_id,'parsed_text':parsed_text}
            if (pd.isna(rec['Sponsor Country'])):
             drec['sponsor']=rec['Sponsor Company']
            else:
             drec['sponsor']=rec['Sponsor Company']+" ("+rec['Sponsor Country']+")"

            drec['approval_status']=rec['FDA Orphan Approval Status']
            drec['generic_name']=rec['Generic Name']
            drec['designated_status']=rec['Orphan Designation Status']
            drec['designated_date']=rec['Date Designated']
            drec['marketing_approval_date']=rec['Marketing Approval Date']
            drec['exclusivity_end_date']=rec['Exclusivity End Date']
            drec['orphan_designation']= orphan_dict
            drug_rec = drec.copy()
            for key, val in drec.items():
                if (isinstance(val, float)):
                  if (pd.isna(val)):
                   del drug_rec[key]
            results.setdefault(_id,[]).append(drug_rec)

     for _id,docs in results.items():
        doc.append({"_id": _id, "fda_orphan_drug" : docs})
     json.dump(doc, outfile, indent=4) ###for checking
     print("=====")
     file_exists = os.path.exists(fda_drug_output)
     if (file_exists):
        print("FDA drug file is ready!")
     else:
        print("FDA drug file is not ready!")


def match_target_type(type_text): ###looking for specified target UMLS types. For example: Disease or Syndrome, Neoplastic Process, Injury or Poisoning ...
    with open("./supp_files/target_type.txt", 'r') as f:
        lines=f.readlines()
        for line in lines:
              
                if (line.strip()==type_text.strip()):
                    return True
        return False

def get_type_meaning(type_text): ###get UMLS mappings
    long_type=[]
    with open("./supp_files/SemanticTypes_2018AB.txt", 'r') as f:
        lines=f.readlines()
        for line in lines:
          type_sum=line.split("|")
          type_name=type_sum[0].strip()
          type_meaning=type_sum[2].strip()

          ### two or more elements
          items=type_text.split(",")
          ### single element
          if (len(items)>1):
            for item in items:
                if (item.strip()==type_name):
                    long_type.append(type_meaning)

          else:
            if (type_text==type_name):
             return [type_meaning]
        
        return long_type


def process_mmifiles(file_path): ### process mmi file (result) from MetaMap
    id_content={}
    max_score=0
    with open(file_path, 'r') as f:
        lines=f.readlines()
        content_list=[]
        for line in lines:
          
           line_content=line.split("|")
           source_file=line_content[0]
           source_id=source_file.split(".")[0]

           txt_sum=re.findall('"([^"]*)"', line_content[6])
           txt=txt_sum[0]
           ori_txt=line_content[6]
           type=get_type_meaning(line_content[5][1:-1])
           if (type==None):
              type=line_content[5]
           score=float(line_content[2])
           assigned_txt=line_content[3]
           umls_id=line_content[4]
           for type_item in type:
                 if (match_target_type(type_item)): ###only match certain types
                    tmp=[assigned_txt,umls_id]
                    if (assigned_txt==txt): #exact match
                       id_content[source_id]=tmp   
                       return id_content ### if match then skip
                    else:
                       if (score>max_score):
                        max_score=score
                        content_list.append(tmp)
                        id_content[source_id]=content_list
        print("-------------------")
    print("content:",id_content)
    return (id_content)  

def update_xlsfile(new_df,id_content): ###update xlsx file
    file_name = 'new_df.xlsx' 
    df = pd.read_excel(file_name, index_col=0)
    for index,row in df.iterrows():
      for i in id_content :
        id_value=id_content[i]
        r_id=row['record_id']
        if (int(r_id)==int(i)):
            row['parsed_content']=id_value
            new_df = new_df.append(row, ignore_index=False)
            return new_df
    return new_df

def process_txtfiles(): ###parse text files from pervious steps using MetaMap
    new_df = pd.DataFrame()
    cwd = os.getcwd()
    cmd="mv "+cwd+"/*.txt "+MetaMap_path
    print(cmd)
    os.system(cmd)
    # Folder Path
    
    # Change the directory
    os.chdir(MetaMap_path)
    # Read text File
   
    # iterate through all file
    for file in os.listdir():
       # Check whether file is in text format or not
       if file.endswith(".txt"):
        file_loc=MetaMap_path+file
        cmd=MetaMap_path+"metamaplite.sh --overwrite --indexdir=data/ivf/2020AB/USABase "+file_loc
        print (cmd)
        os.system(cmd)
        # call read text file function
        cmd="mv "+MetaMap_path+"*.mmi "+cwd
        os.system(cmd)

    os.chdir(cwd)
    for file in os.listdir():
        if file.endswith(".mmi"):
           id_content=process_mmifiles(file)
           print(id_content)
           new_df=update_xlsfile(new_df,id_content)
        
    new_df.to_excel("new_df2.xlsx", index=False,header=True)


def search_pubchem_id(generic): ###search pubchem info
           sub_results = pcp.get_substances(generic, 'name')
           comp_results=pcp.get_compounds(generic, 'name')
           sub=None
           comp=None
           sub_ids=[]
           comp_ids=[]
           if (sub_results):
               for s_id in sub_results:
                print("sid:",s_id,str(s_id)[10:-1])
                sub_ids.append(str(s_id)[10:-1])

           if (comp_results):
               print(comp_results)
               for c_id in comp_results:
                  print("cid:",c_id,str(c_id)[9:-1])
                  comp_ids.append([str(c_id)[9:-1],c_id.inchikey])
           if (len(comp_ids)==0):
            return None,sub_ids
           else:
            return comp_ids,sub_ids


def write_file(file_name,file_content): ###produce text files for MetaMap
    file1 = open(file_name,"w")
    # \n is placed to indicate EOL (End of Line)
    file1.write(file_content)
    file1.close() #to change file access modes 


def append_df_to_excel(df, excel_path): ###append found record to new xlsx
    if (not os.path.exists(excel_path)): ### if not exists, create a new one
       writer = pd.ExcelWriter(excel_path, engine='xlsxwriter')
       writer.save()
   
    df_excel = pd.read_excel(excel_path)
    result = pd.concat([df_excel, df], ignore_index=True)
    result.to_excel(excel_path, index=False)


def parse_fda_file():
    df=pd.read_csv(source_file)
    generic_list=[]
    orphan_list=[]

    try:
        record_id=int(sys.argv[1]) ###input id to restart query process for long wait or other issues
        print("Start checking record id:"+str(record_id)+" in FDA file!")
    except IndexError:
        print("Start checking from first record in FDA file!")
        record_id=1 ###start from first record

    current=0
    for index,row in df.iterrows():
       current+=1
       print("Current:",current)
       if (current>=record_id):
         generic=row['Generic Name']
         orphan_designation=row['Orphan Designation']
         if (not (pd.isna(generic)) and (not (pd.isna(orphan_designation)))):
            print("Try to find id in PubChem:",generic) #generic
            comp_id,sub_id=search_pubchem_id(generic)

            if (comp_id or sub_id):
                   new_df = pd.DataFrame()
                   print("Found!")
                   row['pubchem_cid_inchikey']=comp_id
                   row['pubchem_sid']=sub_id
                   print(row['pubchem_cid_inchikey'],row['pubchem_sid'])
                   row['record_id']=record_id
                   new_df = new_df.append(row, ignore_index=False)
                   file_name=str(record_id)+".txt"
                   write_file(file_name,orphan_designation)
                   append_df_to_excel(new_df, "new_df.xlsx")
            record_id+=1
            time.sleep(15) #sleep for 15 seconds
            print("----------")

if __name__ == '__main__':
   for file in os.listdir():
       # Remove old files first
       if file.endswith(".mmi"):
          os.remove(file)
   parse_fda_file()
   process_txtfiles()
   create_fda_drug_json_file()
   create_fda_disease_json_file()

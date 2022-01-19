Update (01/19/2022):
   Data has been updated to 01/13/2022. The user can verify *.json files in data_tool folder before moving to main folder.

Update(01/12/2022):

1. Manually download Orphan drug data from U.S. FDA site (<a href='https://www.accessdata.fda.gov/scripts/opdlisting/oopd/'>Data Source</a>)
2. Resave the file into .csv format with a meaning name (e.g., FDA_011322.csv)
3. Mnaually download MetamapLite NIH site (<a href="https://lhncbc.nlm.nih.gov/ii/tools/MetaMap/run-locally/MetaMapLite.html">Text Parsing Tool</a>)
4. Change 'MetaMap_path' and 'source_file' in the main program (process_fda_file.py) based on the file location 
5. Run the program (with or without record row id) to produce output files (new_df2.xlsx, fda_disease.json and fda_drug.json)
6. Manually review the final output file (new_df2.xlsx) to adjust any wrong parsing content and reprodce json files if necessary
7. Rename *.json into data.json based on different plugin and move it to upper folder


===old project report
# <a href='https://github.com/r76941156/fda_orphan_drug/blob/main/FDA_orphan_drug_demo.pdf'>Project Report</a>

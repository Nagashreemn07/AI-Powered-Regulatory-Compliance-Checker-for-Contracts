import agreement_comparision

import data_extration
import json


# ********   Phase 2    ******** #
# if __name__ == "__main__":
    
    
#     unseen_file = "templates/Controller-to-Controller-Agreement-1.pdf"
    
#     # step 1: identify the type of agreement
#     agreement_type = agreement_comparision.document_type(unseen_file)
#     print("Document Type: ", agreement_type)
    
#     if agreement_type == "Data Processing Agreement":
        
        
#         # Step 2: Extract clause data from agreement 
#         unseen_data = data_extration.Clause_extraction(unseen_file)
        
#         # Step 2 with summarization:
#         # unseen_data = data_extration.Clause_extraction_with_summarization(unseen_file)
        
#         # Step 3: Fetch stored template data
#         with open("dpa.json", "r", encoding="utf-8") as f:
#             template_data = json.load(f)
        
#         # Step 4: Compare the unseen data with template data
#         result = agreement_comparision.compare_agreements(unseen_data, template_data)
    
#     elif agreement_type == "Controller-to-Controller Agreement":
        
        
#         with open(r"json_files/c2c.json", "r", encoding="utf-8") as f:
#             template_data = json.load(f)
#         # Step 2: Extract clause data from agreement 
#         unseen_data = data_extration.Clause_extraction(unseen_file)
        
#         # Step 2 with summarization:
#         # unseen_data = data_extration.Clause_extraction_with_summarization(unseen_file)
        
#         # Step 3: Fetch stored template data
        
        
#         # Step 4: Compare the unseen data with template data
#         result = agreement_comparision.compare_agreements(unseen_data, template_data)

import streamlit as st 
import schedule
import threading
import time
import scraping

def run_scheduler():
    
    # call call_scrape_funtion function every night at 12 am 
    schedule.every().day.at("00:00").do(scraping.call_scrape_funtion)
    
    
    # these are for testing purpose 
    # for testing part we will call scheduler in every 10 seconds 
    # schedule.every(10).seconds.do(scraping.call_scrape_funtion)
    
    # schedule.every(1).minutes.do(scraping.call_scrape_funtion)
    
    while True:
        schedule.run_pending()
        time.sleep(1)     #check every 5 seconds 

# start scheduler in background thread so streamlit does not block 
threading.Thread(target=run_scheduler, daemon=True).start() 

if __name__ == "__main__":
    
    AGREEMENT_JSON_MAP={
        "Data Processing Agreement":"json_files/dpa.json",
        "Joint Controller Agreement": "json_files/jca.json",
        "Controller-to-Controller Agreement":"json_files/c2c.json",
        "Processor-to-Subprocessor Agreement":"json_files/subprocessor.json",
        "Standard Contractual Clauses": "json_files/scc.json"
    }
    
    st.title("Contract Compliance Checker")
    
    # file upload 
    uploaded_file = st.file_uploader("Upload an agreement (PDF Only)", type=["pdf"] )
    
    if uploaded_file is not None:
        with open("temp_uploded.pdf", "wb") as f:
            f.write(uploaded_file.read())
            
            st.info("Processing your file....")
            
            # step 1: identify the type of agreement
            agreement_type = agreement_comparision.document_type("temp_uploded.pdf")
            
            st.write("**Detected Document Type:** ", agreement_type)
            
            if agreement_type in AGREEMENT_JSON_MAP:
                
                # step 2 : extract clause from unseen file 
                unseen_data = data_extration.Clause_extraction("temp_uploded.pdf")
                
                st.write("**Clause Extraction Completed**")
                
                # step 3: Load respective templete json 
                template_file = AGREEMENT_JSON_MAP[agreement_type]
                
                print("template_file------------", template_file)
                
                with open(template_file, "r", encoding="utf-8") as f:
                    template_data = json.load(f)
                    
                    
                # step 4: Compare agreements
                result = agreement_comparision.compare_agreements(unseen_data, template_data)
                
                # show result
                st.subheader("Comparison Result")
                st.write(result)
            else:
                st.error(f"This document is not under GDPR Complience")
 

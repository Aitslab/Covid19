## Lund-Annotated-CORD-19 silver standard.
Due to licensing limitations we are not allowed to share the full Lund-Annotated-CORD-19 corpus openly. Instead, we release only the subset of abstracts which had permissive licences and you can follow these instructions to recreate the full corpus from the original CORD-19 dataset using EasyNER:

1.	Download the final CORD-19 .tar.gz file CORD-19 released 2022-06-02, which contains the metadata.csv file that is needed for abstract extraction, from the [CORD-19 websote](https://github.com/allenai/cord19?tab=readme-ov-file#download)
    
2.	Install [EasyNER](https://github.com/Aitslab/EasyNER.git). Instructions for installing and using EasyNER can be found [here](https://github.com/Aitslab/EasyNER/blob/main/tutorials/Tutorial-pipeline.md).

3. In the EasyNER script subfolder replace the original ner_spacy.py script with the [modified ner_spacy.py script](../Supplemental_file5/ner_spacy.py). This updated NER module replaces hyphens in the abstracts with blanks to match the dictionaries.

4. Run the EasyNER CORD loader and Sentence splitter modules to extract the abstracts from the metadata.csv file and split them into sentences. 

5. For each dictionary (SARS-CoV2 virus, COVID-19 disease, variants, mutations), run the updated EasyNER module (see step 3). The first run can be done together with the CORD loader and Sentence splitter. For the subsequent runs CORD loader and Sentence splitter are no longer needed as the files from the first run can be reused. Each NER run produces a folder of `.json` files with annotations for a single entity type (i.e. the matches from the dictionary)

6. OPTIONAL STEP: If statistics are desired, follow each NER run with a run of the EasyNER analysis module, which produces tables and graphs with entity counts. To aggregate counts for terms that only differ in letter casing (e.g. COVID19 and Covid19), follow this by running the free-standing [aggregation script](../Supplemental_file5/analysis_cord_19.py).

7. To combine the `.json` files from the individual dictionary NER runs, which have a single entity class (e.g. Disease) into files with all classes run the EasyNER Merger module. To merge the produced multi-class files into a single file with the full Lund-Annotated-CORD-19 silver standard corpus, run the free-standing [json concatenation script](https://github.com/Aitslab/Covid19/blob/main/data/Supplemental_file5/concatenate_json.py). 


Note: To produce the subset of the corpus we released, we filtered the original `metadata.csv` file to include only papers with permissive Creative Commons licenses [filtered_abstracts](filtered_output.csv). We then used this list to remove any non-sharable abstracts from the full Lund-Annotated-CORD-19 silver standard corpus `.json` file with a [filtering script](../Supplemental_file5/Filter_merged_cord19.py). Alternatively, the filtering can be performed directly on the `.json` files from a single dictionay NER run with the [batch filtering script](../Supplemental_file5/Filter_batch_cord19.py) prior to file merging (see step 7).


Here is how to fill in the EasyNER config file for the first run of Cord loader, sentence splitter, NER and analysis module:

```python
config.json
{
  "CPU_LIMIT": 4,
  "TIMEKEEP":true,

  "ignore": {
    "cord_loader": false,
    "downloader": true,
    "text_loader":true,
    "pubmed_bulk_loader":true,
    "splitter": false,
    "ner": false,
    "analysis": false,
    "merger": true, 
    "metrics":true,
    "nel":true,
    "result_inspection":true
  },
  
  "cord_loader": {
    "input_path": "data/metadata.csv",
    "output_path": "results/dataloader/text.json",
    "subset":false,
    "subset_file": ""
  },
  "splitter": {
    "input_path": "results/dataloader/text.json",
    "output_folder": "results/splitter/",
    "output_file_prefix": "sentences",
	  "pubmed_bulk": false,
	  "file_limit":[0,100],
    "tokenizer": "spacy",
    "model_name": "en_core_web_sm",
    "batch_size": 1000
  },
  "ner": {
    "input_path": "results/splitter/",
    "output_path": "results/ner/covid-19/",  ## change to output folder for respective dictionary for next runs
    "output_file_prefix": "ner_spacy-",
    "model_type": "spacy_phrasematcher",
    "model_folder": "",
    "model_name": "en_core_web_sm",
    "vocab_path": "data/Supplemental_file1.txt",   ## change to respective dictionary for next runs
    "store_tokens":"no",
    "labels": "",
    "clear_old_results": true,
    "article_limit": [-1,90000],
    "entity_type": "Virus",  ## change to respective entity class for next run
    "multiprocessing": true,
    "file_batch_size": 15,
    "sentence_batch_size": 1000
  },
  "analysis": {
    "input_path": "results/ner/covid-19", ## this matches the NER module output_path; change for each run to match
    "output_path": "results/analysis/",
    "entity_type":"Virus", ## this needs to match the entity_type from the NER module; change for each run to match
    "plot_top_n":50
  },
  ...



Here is how to fill in the EasyNER config file for the merger run:

  "merger": {
    "paths": ["results/ner/Covid-19/", "results/ner/SarsCov2/","results/ner/Variant/","results/ner/Mutation/"],
    "entities": ["Disease", "Virus" ,"Variant", "Mutation"], 
    "output_path": "results/merged/DVVM/",
    "output_prefix": "merged-"
  },
  ...

```



## Lund-Annotated-CORD-19 silver standard.
Due to licensing limitations we are not allowed to share the full Lund-Annotated-CORD-19 corpus openly. Instead you can follow these instructions to create it:

1.	Download the CORD-19 metadata.csv file released on June 2022 from its original source: https://github.com/allenai/cord19?tab=readme-ov-file#download 
    To be able to run [EasyNER](https://github.com/Aitslab/EasyNER.git) dictionary-based tagger on Cord-19, we have first downloaded last version of cord-19 corpus released 2022-06-02 - [Final release of CORD-19](https://ai2-semanticscholar-cord-19.s3-us-west-2.amazonaws.com/historical_releases.html)
    
2.	Run the CORD loader and Sentence splitter module of EasyNER to extract the abstracts from the metadata.csv file and split the sentences. Instructions for installing and using the free EasyNER tool can be found here: https://github.com/Aitslab/EasyNER/blob/main/tutorials/Tutorial-pipeline.md.

The .tar.gz file with the size of 18.7 GB, were extracted and metadata.csv file were loaded and splitted by [EasyNER](https://github.com/Aitslab/EasyNER.git) cord_loader, and splitter module with the following
    configuration:

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
    "merger": false,
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
    "output_path": "results/ner/covid-19/",  ## This is repeated for each dictionary as Sars_cov2, SarsCov2_variant, and SarsCov2_mutation
    "output_file_prefix": "ner_spacy-",
    "model_type": "spacy_phrasematcher",
    "model_folder": "",
    "model_name": "en_core_web_sm",
    "vocab_path": "dictionaries/Lowercase_hyphen_duplicate_removed/covid-19_synonyms_v3.txt",   ## repeated for all dictionaries (Supp_file1-4)
    "store_tokens":"no",
    "labels": "",
    "clear_old_results": true,
    "article_limit": [-1,90000],
    "entity_type": "covid-19",  ## This repeated for all dictionaries
    "multiprocessing": true,
    "file_batch_size": 15,
    "sentence_batch_size": 1000
  },
  "analysis": {
    "input_path": "results/ner/covid-19",
    "output_path": "results/analysis/",
    "entity_type":"covid-19",
    "plot_top_n":50
  },
  "merger": {
    "paths": ["results/ner/Covid-19/", "results/ner/SarsCov2/","results/ner/Variant/","results/ner/Mutation/"],
    "entities": ["Disease", "Virus","Variant","Mutation"],
    "output_path": "results/merged/DVVM/",
    "output_prefix": "merged-"
  },
  ...

```
3. Different steps have been applied to four dictionaries, as described in [Dictionary_update](data/Supplemental_file5/update_dictionaries.ipynb) within the Jupyter notebooks.	

  We have removed all hyphens from words in all dictionaries and make them all lower case. 

  We have removed all terms of less than 3 characters from the variants dictionary ([readme](data/Supplemental_file5/update_dictionaries.ipynb)).
  
  This has already been completed, and the updated dictionaries are available in [Supplemental_files(1–4).txt](data/).

4.	Run the EasyNER NER module once with each dictionary (virus, disease, variants, mutations).
    
  using ner_spacy.py (This script has also been modified to remove hyphens from the text [modified_ner_spacy](../Supplemental_file5/ner_spacy.py), and analysis.py from  [EasyNER, version 2 (v2.0.0)](https://github.com/Aitslab/EasyNER/tree/main/scripts/)  and saving tagged text into smaller .json batches.

5. run [post_processing](../Supplemental_file5/analysis_cord_19.py) to make the entities case-insensitive and to plot the cumulative frequency of identical words regardless of their letter casing.
  We have first plotted the most 50 frequect terms for all dictionaries, then using the following
  [post_processing](src/analysis_cord_19.py) script in order to make all terms lower case. 


```python
## This script merges identical entities while ignoring capitalization and sums their frequencies, storing and plotting the results in lowercase form.
import os
import json
from glob import glob
from tqdm import tqdm
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def plot_frequency_barchart(df, entity, n):
    '''
    plot a frequency barchart with the top n entities, names or ids
    '''
    
    if n<=50:
        fig = plt.figure(figsize=(10,10))
        ax = sns.barplot(y=df['entities'].head(n),x="total_count", data=df[:n])
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['bottom'].set_visible(False)
        ax.get_xaxis().set_visible(False)

        ax.bar_label(ax.containers[0])
        ax.set_title(f'Top {n} for {entity} model', size=20, pad=12)
        return fig, ax
    
    elif n<=100:
        fig = plt.figure(figsize=(20,20))
        ax = sns.barplot(y=df.index[:n],x="total_count", data=df[:n])
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['bottom'].set_visible(False)
        ax.get_xaxis().set_visible(False)

        ax.bar_label(ax.containers[0])
        ax.set_title(f'Top {n} for {entity} model', size=30, pad=15)
        return fig, ax
    
    else:
        print("Plotting more that 100 entities can result in distorted graph")
        fig = plt.figure(figsize=(2*int(n/10),2*int(n/10)))
        ax = sns.barplot(y=df.index[:n],x="total_count", data=df[:n])
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['bottom'].set_visible(False)
        ax.get_xaxis().set_visible(False)

        ax.bar_label(ax.containers[0])
        ax.set_title(f'Top {n} for {entity} model', size=4*int(n/10), pad=15)
        return fig, ax

def merge_lower_form_of_entities(df):
    df = df.reset_index(drop=True)  # Reset index
    df['entities'] = df['entities'].str.lower()  # Convert column 'A' to lowercase
    df['total_count'] = df.groupby('entities')['total_count'].transform('sum')  # Sum values in 'B' for same 'A'
    df = df.drop_duplicates(subset='entities', keep='first')  # Keep only first occurrence of each 'A'
    return df




if __name__ == "__main__":
    n = 50
    entity = 'Sars_cov2'  ## This has been repeated for all dictionaries
    path_  =  "../results/analysis/analysis_{}/".format(entity)

    df_id     = pd.read_csv(path_+"result_entities_{}.tsv".format(entity),sep='\t')
    df_new    = df_id[['Unnamed: 0','total_count']]
    df_new    = df_new.rename(columns={'Unnamed: 0': 'entities'})
    df_merged = merge_lower_form_of_entities(df_new)
    sorted_df_merged = df_merged.sort_values(by=['total_count'], ascending=[False])

    fig,ax = plot_frequency_barchart(sorted_df_merged,entity , n)
    ax.set_yticklabels(sorted_df_merged['entities'].head(n))
            
   
    os.makedirs(path_, exist_ok=True)
    plt.savefig(path_+"{}_top_{}_lowercase.eps".format(entity,n), bbox_inches="tight", aspect="auto", format="eps")
    plt.savefig(path_+"{}_top_{}_lowercase.png".format(entity,n), bbox_inches="tight", aspect="auto", format="png")
    sorted_df_merged.to_csv(path_+"result_ids_two_col_{}.tsv".format(entity), sep="\t")



```

5.	Run the EasyNER Merger module to merge the files from the individual runs
  
This process merges all tags from all batches. Initially, we used the [merger](../Supplemental_file5/merger.py) function to combine all `.json` files into a single file, creating the original Lund-Annotated-CORD-19 silver standard. However, to enable sharing of a partial corpus, we first filtered the original `metadata.csv` file to include only papers with a Creative Commons (CC) license [filtered_abstracts](filtered_output.csv). 

We then used this list to remove any non-sharable papers from the merged `.json` file, saving the result as a partial Lund-Annotated-CORD-19 silver standard [filter merged file](../Supplemental_file5/Filter_merged_cord19.py).

Alternatively, this filtering could be performed directly on each batch before merging them [filter batches](../Supplemental_file5/Filter_batch_cord19.py).





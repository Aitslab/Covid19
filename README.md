[![License: CC BY-NC 4.0](https://img.shields.io/badge/License-CC%20BY--NC%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by-nc/4.0/)

# Repo for "English dictionaries, gold and silver standard corpora for biomedical natural language processing related to SARS-CoV-2 and COVID-19". 

This repo accomanies the paper and contains 
- COVID-19-related dictionaries that can be used with the [EasyNER](https://github.com/Aitslab/EasyNER.git) pipeline or other tools for dictionary-based Named Entity Recognition.
- Code to expand the dictionaries
- Partial Lund Annotated-CORD-19 silver standard corpus and code and instructions to recreate the entire corpus
- Lund COVID-19 gold standard corpus with NER annotation

The four dictionaries contain the following terms:
1. SARS-CoV-2 synonyms (sars-cov-2_synonyms.txt)  (virus terms)
2. COVID-19 synonyms  (covid-19_synonym.txt)      (disease terms)
3. SARS-CoV-2 variant terms (variants.txt)        (variant terms)
4. SARS-CoV-2 common mutations                    (mutation terms)
   
Please cite this article if you use any of the materials:

```bibtex
@article{rashed2020english,
  title={English dictionaries, gold and silver standard corpora for biomedical natural language processing related to SARS-CoV-2 and COVID-19},
  author={Kazemi Rashed, Salma and Ahmed, Rafsan and Frid, Johan and Aits, Sonja},
  journal={arXiv preprint arXiv:2003.09865 [q-bio.OT]},
  year={2020}
}
```

and please cite the EasyNER paper if you use it with the tools presented here

```bibtex
@article{ahmed2023easyner,
  title={EasyNER: A Customizable Easy-to-Use Pipeline for Deep Learning- and Dictionary-based Named Entity Recognition from Medical Text},
  author={Rafsan Ahmed and Petter Berntsson and Alexander Skafte and Salma Kazemi Rashed and Marcus Klang and Adam Barvesten and Ola Olde and William Lindholm and Antton Lamarca Arrizabalaga and Pierre Nugues and Sonja Aits},
  year={2023},
  eprint={2304.07805},
  archivePrefix={arXiv},
  primaryClass={q-bio.QM}
}
```




For this version of manuscript (v3), we have updated (sars-cov-2_synonyms.txt) and saved as supplemental_file1.txt, 
covid-19_synonym.txt and have it as supplemental_file2.txt and variants.txt as supplemental_file3.txt and added sarscov2_mutations.txt as  supplemental_file4.txt .


Previous versions of this manuscript, files and all references are summarized in:
[(previous_versions)](https://github.com/Aitslab/corona)


For this version, for being able to run dictionary-based tagger first it is good to create an environment ([EasyNER, version 2 (v2.0.0)](https://github.com/Aitslab/EasyNER/tree/main/scripts/)).

Set up an conda environment
```console
conda env create -f environment.yml
```

After installation activate the environment:
```console
conda activate easyner_env
```


## Dictionaries
We have updated dictionaries through [updated_code](https://github.com/Aitslab/Covid19/blob/main/data/Supplemental_file5/).



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
    "input_path": "results/splitter_765/",
    "output_path": "results/ner/covid19/",
    "output_file_prefix": "ner_spacy-",
    "model_type": "spacy_phrasematcher",
    "model_folder": "",
    "model_name": "en_core_web_sm",
    "vocab_path": "dictionaries/Lowercase_hyphen_duplicate_removed/covid-19_synonyms_v3.txt",
    "store_tokens":"no",
    "labels": "",
    "clear_old_results": true,
    "article_limit": [-1,90000],
    "entity_type": "covid19",
    "multiprocessing": true,
    "file_batch_size": 15,
    "sentence_batch_size": 1000
  },
  "analysis": {
    "input_path": "results/ner/covid19",
    "output_path": "results/analysis/",
    "entity_type":"covid19",
    "plot_top_n":50
  },
  "merger": {
    "paths": ["results/ner/Covid19/", "results/ner/SarsCov2/","results/ner/Variant/","results/ner/Mutation/"],
    "entities": ["Disease", "Virus","Variant","Mutation"],
    "output_path": "results/merged/DVVM/",
    "output_prefix": "merged-"
  },
  ...

```
3. Different steps have been applied to four dictionaries, as described in [Dictionary_update](data/Supplemental_file5/update_dictionaries.ipynb) within the Jupyter notebooks.	

  We have removed all hyphens from words in all dictionaries and make them all lower case. 

  We have removed all terms of less than 3 characters from the variants dictionary ([readme](data/Supplemental_file5/update_dictionaries.ipynb)).
  
  This has already been completed, and the updated dictionaries are available in [Supplemental_files(1,2,4, and 11).txt](data/).

4.	Run the EasyNER NER module once with each dictionary (virus, disease, variants, mutations).
    
  using ner_spacy.py (This script has also been modified to remove hyphens from the text [modified_ner_spacy](src/ner_spacy.py)), and analysis.py from  [EasyNER, version 2 (v2.0.0)](https://github.com/Aitslab/EasyNER/tree/main/scripts/)  and saving tagged text into smaller .json batches.

5. run [post_processing](src/analysis_cord_19.py) to make the entities case-insensitive and to plot the cumulative frequency of identical words regardless of their letter casing.
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
    entity = 'Sars_cov2'
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




## License

- 🧠 **Dictionaries and data**: [CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/). See `LICENSE-DATA`.
- 🛠️ **Code**: [Apache License 2.0](https://www.apache.org/licenses/LICENSE-2.0). See `LICENSE`.

Please credit the original [CORD-19](https://github.com/allenai/cord19) dataset by the Allen Institute for AI if you use it to create our silver standard corpus.


The scripts from [EasyNER](https://github.com/Aitslab/EasyNER/tree/main/scripts/) with some small changes used for this manuscript are saved in script directory of this repo.
The supplementary files as well as previous versions of dictionaries are saved in [data](https://github.com/Aitslab/Covid19/tree/main/data) and [dictionaries](https://github.com/Aitslab/Covid19/tree/main/dictionaries) directories.

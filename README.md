This folder contains COVID-19-related dictionaries Collected from various sources and enhanced with added prefixes and suffixes. That can be used with the [EasyNER](https://github.com/Aitslab/EasyNER.git) pipeline.
Please cite this article if you use dictionaries.


```bibtex
@article{rashed2020english,
  title={English dictionaries, gold and silver standard corpora for biomedical natural language processing related to SARS-CoV-2 and COVID-19},
  author={Kazemi Rashed, Salma and Ahmed, Rafsan and Frid, Johan and Aits, Sonja},
  journal={arXiv preprint arXiv:2003.09865 [q-bio.OT]},
  year={2020}
}
```

and Please cite this Easyner paper if you use pipeline for dictionary-based NER.

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

The dictionaries contain the following terms:
1. SARS-CoV-2 synonyms (sars-cov-2_synonyms.txt)  (virus terms)
2. COVID-19 synonyms  (covid-19_synonym.txt)      (disease terms)
3. SARS-CoV-2 variant terms (variants.txt)        (variant terms)


For this version of manuscript (v3), we have updated (sars-cov-2_synonyms.txt) and saved as supplemental_file1_v3.txt, 
covid-19_synonym.txt and have it as supplemental_file2_v3.txt and variants.txt as supplemental_file3_v3.txt.


Previous versions of this manuscript, files and all references are summarized in:
[(previous_versions)](https://github.com/Aitslab/corona)


For this version, for being able to run dictionary-based tagger first it is good to create an environment.

Set up an conda environment
```console
conda env create -f environment.yml
```

After installation activate the environment:
```console
conda activate easyner_env
```


## Dictionaries
We have updated dictionaries through [updated_code](https://github.com/Aitslab/Covid19/blob/main/data/Supplemental_file8_v3.ipynb).



## Cord-19
To be able to run [EasyNER](https://github.com/Aitslab/EasyNER.git) dictionary-based tagger on Cord-19, we have first downloaded last version of cord-19 corpus released 2022-06-02 - [Final release of CORD-19](https://ai2-semanticscholar-cord-19.s3-us-west-2.amazonaws.com/historical_releases.html)

The .tar.gz file with the size of 18.7 GB, were extracted and metadata.csv file were used by [EasyNER](https://github.com/Aitslab/EasyNER.git) pipeline with the following setting.


```python
config.json

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
    "result_inspection":false
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
    "tokenizer": "nltk",
    "model_name": "en_core_web_sm",
    "batch_size": 100
  },
  "ner": {
    "input_path": "results/splitter/",
    "output_path": "results/ner/",
    "output_file_prefix": "ner_spacy",
    "model_type": "spacy_phrasematcher",
    "model_folder": "",
    "model_name": "en_core_web_sm",
    "vocab_path": "dictionaries/dictionaries/covid-19_synonyms_v3.txt",   # we have run it for all dictionaries
    "store_tokens":"no",
    "labels": "",
    "clear_old_results": true,
    "article_limit": [-1,90000],
    "entity_type": "disease",  #virus #variant
    "multiprocessing":true
  },
  "analysis": {
    "input_path": "results/ner/",
    "output_path": "results/analysis/",
    "entity_type":"disease", #virus #variant
    "plot_top_n":50
  },

```
using cord_loader.py, splitter.py, ner_spacy.py, and analysis.py from  [EasyNER](https://github.com/Aitslab/EasyNER/tree/main/scripts/) for saving the abstracts of articles in a text.json file,
split the text into shorter sentences and saving into smaller .json batches and run dictionary_based tagger all over all batches using ner_spacy.py.

We have first plotted the most 50 frequect terms for all dictionaries, then using the following

analysis_cord_19.py script in order to make all terms lower case. 


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
    entity = 'variant'
    path_ =  "../results/analysis/analysis_{}/".format(entity)

    df_id     = pd.read_csv(path_+"result_entities_{}.tsv".format(entity),sep='\t')
    df_new    = df_id[['Unnamed: 0','total_count']]
    df_new    = df_new.rename(columns={'Unnamed: 0': 'entities'})
    df_merged = merge_lower_form_of_entities(df_new)


    fig,ax = plot_frequency_barchart(df_merged,entity , n)
    ax.set_yticklabels(df_merged['entities'].head(n))
            
   
    os.makedirs(path_, exist_ok=True)
    plt.savefig(path_+"{}_top_{}_ids.png".format(entity,n), bbox_inches="tight", aspect="auto", format="png")
    df_merged.to_csv(path_+"result_ids_two_col_{}.tsv".format(entity), sep="\t")


```

The scripts from [EasyNER](https://github.com/Aitslab/EasyNER/tree/main/scripts/) with some small changes used for this manuscript are saved in script directory of this repo.
The supplementary files as well as previous versions of dictionaries are saved in [data](https://github.com/Aitslab/Covid19/tree/main/data) and [dictionaries](https://github.com/Aitslab/Covid19/tree/main/dictionaries) directories.
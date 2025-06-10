[![License: CC BY-NC 4.0](https://img.shields.io/badge/License-CC%20BY--NC%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by-nc/4.0/)

# Repo for "English dictionaries, gold and silver standard corpora for biomedical natural language processing related to SARS-CoV-2 and COVID-19". 

This repo accomanies the paper and contains 
- COVID-19-related dictionaries that can be used with the [EasyNER](https://github.com/Aitslab/EasyNER.git) pipeline or other tools for dictionary-based Named Entity Recognition.
- Code to update the dictionaries
- Partial Lund-Annotated-CORD-19 silver standard corpus and code and instructions to recreate the entire corpus
- Statistics (entitiy counts) for the Lund-Annotated-CORD-19 corpus
- Lund COVID-19 gold standard corpus with NER annotation in several formats
- Code to convert BioC xml to json format (used for th gold standard corpus)

There are five dictionaries in total:
1. [SARS-CoV-2 synonyms (virus terms), version 3](https://github.com/Aitslab/Covid19/blob/main/data/Supplemental_file1.txt)
2. [COVID-19 synonyms (disease terms), version 3](https://github.com/Aitslab/Covid19/blob/main/data/Supplemental_file2.txt)
3. [SARS-CoV-2 variant terms, version 2, including terms consisting of 1 and 2 characters](https://github.com/Aitslab/Covid19/blob/main/data/Supplemental_file3.txt)
4. [SARS-CoV2 variant terms, version 2, excluding terms consistting of 1 and 2 characters](https://github.com/Aitslab/Covid19/blob/main/data/Supplemental_file4.txt)
5. [SARS-CoV-2 common mutations, version 1](https://github.com/Aitslab/Covid19/blob/main/data/Supplemental_file11.txt)
   

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



## Update notice
For this version of manuscript (v3), we have updated sars-cov-2_synonyms.txt (now named supplemental_file1.txt), 
covid-19_synonym.txt (now named supplemental_file2.txt) and variants.txt (with and without 1-2 character entities now named supplemental_file3.txt and supplemental_file11.txt, respectively) and added a dictionary of mutations (supplemental_file4.txt).

Previous version of the dictionaries can be found in the [data/old_dictionaries folder](https://github.com/Aitslab/Covid19/blob/main/data/old_dictionaries).

Previous versions of the manuscript and all associated files can be found in:
[(previous_versions)](https://github.com/Aitslab/corona)


# Usage instructions
The dictionaries can be run with [EasyNER, version 2 (v2.0.0)](https://github.com/Aitslab/EasyNER/).

For this, follow the instructions in the EasyNER repo and start with a fresh conda environment
```console
conda env create -f environment.yml
```

After installation activate the environment:
```console
conda activate easyner_env
```


## Dictionaries
Scripts used to produce the updated dictionaries can be found [here](https://github.com/Aitslab/Covid19/blob/main/data/Supplemental_file5/). They can be used to expand the dicationaries.



## Lund-Annotated-CORD-19 silver standard.
Due to licensing limitations we are not allowed to share the full [Lund-Annotated-CORD-19 corpus](github.com/Aitslab/Covid19/tree/main/data/Supplemental_file6) openly. Instead, we release only the part which had permissive licences and instructions to produce the full corpus from the freely accessible original CORD-19 dataset.






## License

- 🧠 **Dictionaries and data**: [CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/). See `LICENSE-DATA`.
- 🛠️ **Code**: [Apache License 2.0](https://www.apache.org/licenses/LICENSE-2.0). See `LICENSE`.

Please credit the original [CORD-19](https://github.com/allenai/cord19) dataset by the Allen Institute for AI if you use it to create our silver standard corpus.


The scripts from [EasyNER](https://github.com/Aitslab/EasyNER/tree/main/scripts/) with some small changes used for this manuscript are saved in script directory of this repo.
The supplementary files as well as previous versions of dictionaries are saved in [data](https://github.com/Aitslab/Covid19/tree/main/data) and [dictionaries](https://github.com/Aitslab/Covid19/tree/main/dictionaries) directories.

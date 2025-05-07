This folder contains COVID-19-related dictionaries Collected from various sources and enhanced with added prefixes and suffixes. That can be used with the Easyner pipeline.
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
4. SARS-CoV-2 mutations (Sarscov2_mutation.txt)   (Mutation terms)



For this version of manuscript we have covid-19 synonyms with 89901 terms [covid-19](covid-19_synonyms_v3.txt), sars-cov-2 virus synonyms with 807 entries [sars-cov-2 virus](sars-cov-2_synonyms_v3.txt), new variant dictionary with 2633758 entries [variant](variants_v2.txt) and the most popular mutation terms with 113 entries [mutation](sarscov2_mutations_v1.txt).

For creating a silver annotated Cord-19 we have removed single-character entries, entries with two-characters that were common with English identifiers (AS, BY, BE, AN, AT, and HE), and  the part of dictionary that was not found in the Cord-19 corpus [(modified variant dictionary)](variants_v3.txt).  For a more accurate analysis, we have removed all single- and double-character entries as well as those were not tagged in Cord-19 [(modified variant dictionary)](variants_v4.txt).

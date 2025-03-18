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



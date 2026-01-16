import pandas as pd

from pathlib import Path
from sys import argv

from src.blast import get_correspondence_by_blast
from src.seqs import seq_stats





def main():
    #Get proteins with X
    #Get mRNA with Ns
    #Get Detenga results if able
    datasets = {"A": {"transcript": Path(argv[1]),
                      "protein": Path(argv[2])},
                "B": {"transcript": Path(argv[3]),
                      "protein": Path(argv[4])}}
    for key, values in datasets.items():
        for kind, fpath in values.items():
            stats = seq_stats(fpath, kind=kind)
            datasets[key][kind] = stats
    
    for key, values in datasets.items():
        for kind, dataset in values.items():
            print(kind, key)
            print(dataset)
   
    correspondece = get_correspondence_by_blast(Path(argv[5]))
    merged_df = pd.merge(datasets["B"]["transcript"], datasets["B"]["protein"], on="SeqID")
    merged_df = pd.merge(merged_df, correspondece, on="SeqID")
    merged_df = merged_df.drop(columns=["Masked Nucl (%)"])
    refseq_trans_df = datasets["A"]["transcript"]
    refseq_prot_df = datasets["A"]["protein"]
    refseq_trans_df = refseq_trans_df.drop(columns=["Stop Chars transcript (%)"])
    refseq_prot_df = refseq_prot_df.drop(columns=["Stop Chars protein (%)"])
    merged_df = merged_df.rename(columns={"SeqID": "Ensembl_ID", "Match_ID": "RefSeq_ID",
                                          "SeqLength_transcript": "SeqLength_transcript_Ensembl",
                                         "SeqLength_protein": " SeqLength_protein_Ensembl"})
    refseq_prot_df = refseq_prot_df.rename(columns={"SeqID": "RefSeq_ID", "SeqLength_protein": "SeqLength_protein_RefSeq"})
    refseq_trans_df = refseq_trans_df.rename(columns={"SeqID": "RefSeq_ID", "SeqLength_transcript": "SeqLength_transcript_RefSeq"})
    print(merged_df)
    print(refseq_prot_df)
    print(refseq_trans_df)
    merged_df = pd.merge(merged_df, refseq_trans_df, on="RefSeq_ID")
    merged_df = pd.merge(merged_df, refseq_prot_df, on="RefSeq_ID")
    print(merged_df)
    merged_df.to_csv("Results.tsv", sep="\t", index=False)




    

if __name__ == "__main__":
    main()


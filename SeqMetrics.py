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
    print(merged_df)
    print(correspondece[correspondece['IsQueryFragmented'] == "True"])

    

if __name__ == "__main__":
    main()


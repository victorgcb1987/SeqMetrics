import pandas as pd

from Bio import SeqIO

def seq_stats(fpath, kind="transcript"):
    data_columns = {"SeqID": [], "SeqLength": [], "Stop Chars (%)": []}
    if kind == "transcript":
        data_columns.update({"Masked Nucl (%)": []})
    stop_symbol = "N" if kind == "transcript" else "X"
    
    with open(fpath) as fhand:
        records = SeqIO.parse(fhand, "fasta")
        for record in records:
            record_id = record.id.replace("rna_", "").replace("transcript:", "")
            seqLegth = len(record.seq)
            masked = sum(1 for char in record.seq if char.islower())
            masked_percentage = float(masked/ seqLegth) * 100
            stop_chars = sum(1 for char in record.seq if char == stop_symbol) * 100
            stop_percentage = float(stop_chars/seqLegth)
            data_columns["SeqID"].append(record_id)
            data_columns["SeqLength"].append(seqLegth)
            data_columns["Stop Chars (%)"].append(stop_percentage)
            if kind == "transcript":
                data_columns["Masked Nucl (%)"].append(masked_percentage)
    return pd.DataFrame.from_dict(data_columns)
    


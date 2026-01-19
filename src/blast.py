import pandas as pd


def get_correspondence_by_blast(fpath):
    data_columns = {"SeqID": [], "Match_ID":[], "Length Ratio (%)":[]}
    with open(fpath) as fhand:
        for line in fhand:
            if line:
                line = line.split()
                seqid = line[0].replace("rna-", "").replace("transcript:", "").replace("transcript-", "")
                dbid = line[1].replace("rna-", "").replace("transcript:", "").replace("transcript-", "")
                length_ratio = float(int(line[-1]) / int(line[-2])) * 100
                identity = float(line[2])
                evalue = float(line[10])
                if evalue <= 1e-10 and identity >= 95 and length_ratio >= 50:
                    if seqid not in data_columns["SeqID"]:
                        data_columns["SeqID"].append(seqid)
                        data_columns["Match_ID"].append(dbid)
                        data_columns["Length Ratio (%)"].append(length_ratio)
    return pd.DataFrame.from_dict(data_columns)
                


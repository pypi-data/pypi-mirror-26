import sqlite3 as lite
import sys
import os
import threading
import gbk_parser
import ucsc_parser
import conf
records = gbk_parser.get_records()

# creates aliases in specie database file.
# must have a kgAlias.txt file in the specie database folder.
# Input:
# specie: string of the specie (must be one from conf.py)
def create_better_aliases_db(specie):
    with open('db/{}/kgAlias.txt'.format(specie),'r') as f:
        aliases_lines = f.readlines()

    values_keys = [tuple(line.replace('\n','').split('\\t')) for line in aliases_lines]
    try:
        zipped = [(key,value) for value,key in values_keys]
    except:
        values_keys = [tuple(line.replace('\n','').split('\t')) for line in aliases_lines]
        zipped = [(key,value) for value,key in values_keys]
    # write pairs to db
    with lite.connect(conf.databases[specie]) as con:
        cursor = con.cursor()
        cursor.executescript("drop table if exists aliases;")
        cursor.execute("CREATE TABLE aliases (name TEXT, transcript_id TEXT)")
        cursor.executemany('INSERT INTO aliases VALUES(?,?)',zipped)

#
def create_transcript_data_db(specie):
    print ("Creating transcript database for {}...".format(specie))
    with lite.connect(conf.databases[specie]) as con:
        names = ucsc_parser.parse_knownGene(ucsc_parser.knownGene_path.format(specie))
        cur = con.cursor()
        cur.executescript("drop table if exists transcripts;")
        cur.execute("CREATE TABLE transcripts(name TEXT,\
                    chrom TEXT,\
                    strand TEXT,\
                    tx_start TEXT,\
                    tx_end TEXT,\
                    cds_start TEXT,\
                    cds_end TEXT,\
                    exon_count TEXT,\
                    exon_starts TEXT,\
                    exon_ends TEXT,\
                    protein_id TEXT,\
                    align_id TEXT)")

        for name in names:
            values = tuple(names[name].values())
            cur.execute("INSERT INTO transcripts VALUES(?,?,?,?,?,?,?,?,?,?,?,?)",values)

def create_comb_db(specie):
    with lite.connect(conf.databases[specie]) as con:
        print("Creating database for {}...".format(specie))
        cur = con.cursor()
        cur.execute("drop table if exists genebank;")
        cur.execute("CREATE TABLE genebank(Id INT, symbol TEXT, db_xref TEXT, coded_by TEXT, chromosome TEXT,strain TEXT, cds TEXT, sites TEXT, regions TEXT)")
        for index,record in enumerate(records[specie]):
            sites=[]
            regions=[]
            cds = []
            location = ""
            name =""
            db_xref=""
            coded_by =""
            chromosome =""
            strain = ""
            for feature in record.features:
                if feature.type == 'source':
                    if 'strain' in feature.qualifiers:
                        strain = feature.qualifiers['strain'][0]
                    if 'chromosome' in feature.qualifiers:
                        chromosome = feature.qualifiers['chromosome'][0]
                if feature.type == 'CDS':
                    cds.append(str(feature))
                    if 'gene' in feature.qualifiers:
                        name = feature.qualifiers['gene'][0]
                    if 'coded_by' in feature.qualifiers:
                        coded_by = feature.qualifiers['coded_by'][0]
                    if 'db_xref' in feature.qualifiers:
                        db_xref = feature.qualifiers['db_xref'][0]
                    location = str(feature.location)
                if feature.type == 'Site':
                    sites.append(feature.qualifiers['site_type'][0]+str(feature.location))
                if feature.type == 'Region':
                    regions.append(feature.qualifiers['region_name'][0]+str(feature.location))
            sites_comb = ','.join(sites)
            region_comb = ','.join(regions)
            cds_comb = ','.join(cds)
            if sites_comb == '' and region_comb == '':
                continue
            cur.execute("INSERT INTO genebank VALUES(?, ?, ?, ?, ?, ?,  ?, ?,?)",(index,name,db_xref,coded_by,chromosome,strain,cds_comb,sites_comb,region_comb))
            index+=1

if __name__ == "__main__":
    for specie in conf.species:
        create_comb_db(specie)
        create_better_aliases_db(specie)
        create_transcript_data_db(specie)

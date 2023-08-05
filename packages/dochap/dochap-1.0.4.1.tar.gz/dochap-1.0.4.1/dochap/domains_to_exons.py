import os
import json
import time
import dill
import sqlite3 as lite
import progressbar
from pathos.multiprocessing import ProcessingPool, ThreadingPool
from functools import partial
import conf

domains_db = 'db/domains.db'
alias_db = 'db/aliases.db'
comb_db = 'db/comb.db'
transcripts_db = 'db/transcript_data.db'
num_threads = 1
bar = 0
# run on all transcripts in transcripts.db
# for each one find matching alias in alias.db
# use alias to find sites and regions data in comb.db
# get all domains of a transcript
#TODO DOESNT WORK
def get_domains(transcript_id, specie):
    # use better aliases - obselete
    #alias_db = 'db/better_aliases.db'
    with lite.connect(conf.databases[specie]) as con:
        cursor = con.cursor()
        cursor.execute("SELECT name from aliases WHERE transcript_id = ?",(transcript_id,))
        #cursor.execute("SELECT aliases from genes WHERE transcript_id = ?",(transcript_id,))
        data = cursor.fetchall()
        if data:
            # create a list of the aliases
            aliases = list(set([tup[0] for tup in data]))
            #aliases = data[0].split(';')
        else:
            return None
    with lite.connect(conf.databases[specie]) as con:
        for alias in aliases:
            cursor = con.cursor()
            cursor.execute("SELECT sites,regions from genebank WHERE symbol = ?",(alias,))
            results = cursor.fetchall()
            domain_list = []
            #print('result for {} alias {} is:\n{}'.format(transcript_id,alias,results))
            if results:
                # if counter is 0, domain type is site, if counter is 1, domain type is region
                domain_types = ['site','region']
                for counter,domains in enumerate(results[0]):
                    splitted = domains.split(',')
                    #print ('splitted: ',splitted)
                    for result in splitted:
                        if '[' not in result or ']' not in result:
                            #print('bad result for {} alias {} result:\n'.format(transcript_id,alias,result))
                            continue
                        modified = result.replace(',',':')
                        part_one = '['.join(modified.split('[')[:-1])
                        part_two = modified.split('[')[-1].replace(']',':').split(':')
                        domain = {}
                        # check that line is not empty
                        #print ('modified: ',modified)
                        if not modified[0]:
                            #print('bad modified for {} alias {} modified:\n'.format(transcript_id,alias,modified))
                            continue
                        domain['type'] = domain_types[counter]
                        domain['name'] = part_one
                        if len(part_two) < 2:
                            print ('fucked up on part_two')
                            print ('result:', result)
                            print ('part_one: ',part_one)
                            print ('part_two: ',part_two)
                            print ('modified: ',modified)

                        domain['start'] = part_two[0]
                        domain['end'] = part_two[1]
                        domain['index'] = len(domain_list)
                        #print ('domain: ', domain)
                        if not str.isdigit(domain['start']) or not str.isdigit(domain['end']):
                            #print('bad strings in domain for {} alias {} domain:\n'.format(transcript_id,alias,domain))
                            continue
                        domain_list.append(domain)
                #print('found for {} alias {} doms list:\n{}'.format(transcript_id,alias,domain_list))
                return domain_list
            else:
                pass
                #print('found no sites or regions for {} alias {}'.format(transcript_id,alias))

def get_exons_by_transcript_id(transcript_id,specie):
    with lite.connect(conf.databases[specie]) as con:
        con.row_factory = lite.Row
        cursor = con.cursor()
        cursor.execute("SELECT * FROM transcripts WHERE name = ?",(transcript_id,))
        # currently use the first result only (there shouldnt be more then one)
        result = cursor.fetchone()
    exons = get_exons(result)
    return exons

def get_exons(result):
    if not result:
        #print('nothing in result')
        return
    exons =[]
    starts = result['exon_starts'].split(',')
    ends = result['exon_ends'].split(',')
    first_exon_start = int(starts[0])
    last_end = 0
    for i in range(int(result['exon_count'])):
        exon = {}
        exon['index'] = i
        exon['start'] = int(starts[i])
        exon['end'] = int(ends[i])
        exon['length'] = abs(exon['end'] - exon['start'])
        # the exon relative position
        exon['relative_start'] = last_end + 1
        exon['relative_end'] = last_end + 1 + exon['length']
        #exon['relative_start'] = abs(exon['start'] - first_exon_start) + 1
        #exon['relative_end'] = exon['relative_start'] + exon['length']
        last_end = exon['relative_end']
        exon['transcript_id'] = result['name']
        exons.append(exon)
    return exons


def assignDomainsToExons(transcript_id, domains, specie):
    # get data about the transcript
    with lite.connect(conf.databases[specie]) as con:
        con.row_factory = lite.Row
        cursor = con.cursor()
        cursor.execute("SELECT * FROM transcripts WHERE name = ?",(transcript_id,))
        # currently use the first result only (there shouldnt be more then one)
        result = cursor.fetchone()
    exons = get_exons(result)
    #print("exons",exons)
    #print("domains",domains)
    # TODO relative should be counted without spaces between exons
    # next statement might not be accurate
    # i dont know from what each domain relative location is relative to
    relative_start = 1
    relative_stop = 0
    last_exon = None
    for exon in exons:
        # domains indexes will be used as strings
        # states will be start,end,contains,contained
        exon['domains_states'] = {}
        relative_stop = relative_start + exon['length']
        domains_in_exon = []
        if domains == None:
            return
        for domain in domains:
            if (not str.isdigit(domain['start'])):
                print ("FAILED ON {} domain is: {}".format(transcript_id,domain))
                sys.exit(2)
            dom_start = int(domain['start']) * 3 - 2
            dom_stop = int(domain['end']) * 3

            # create ranges of numbers that represents the domain and exon ranges
            if dom_start < dom_stop:
                dom_range = range(dom_start,dom_stop+1)
            else:
                dom_range = range(dom_stop,dom_start+1)

            exon_range = set(range(relative_start,relative_stop+1))
            intersection = exon_range.intersection(dom_range)

            dom_start_in_exon = False
            dom_end_in_exon = False

            if not intersection:
                # empty, no overlap
                continue

            if dom_start in intersection:
                # exon start location in domain
                # domain is atleast partialy on exon
                dom_start_in_exon = True

            if dom_stop in intersection:
                # exon end location in domain
                # domain is atleast partialy on exon
                dom_end_in_exon = True

            dom_index = str(domain['index'])
            if dom_end_in_exon and dom_start_in_exon:
                # domain fully in exon
                exon['domains_states'][dom_index] = 'contained'
                domains_in_exon.append(domain)
                continue
            if dom_start_in_exon:
                exon['domains_states'][dom_index] = 'start'
                domains_in_exon.append(domain)
                continue
            if dom_end_in_exon:
                exon['domains_states'][dom_index] = 'end'
                domains_in_exon.append(domain)
                continue
            # there is an intersection but dom_start and dom_end not in it
            # that means that the domain contains the exon
            exon['domains_states'][dom_index] = 'contains'
            domains_in_exon.append(domain)
            continue

            #dom_start_in = relative_start <= dom_start and dom_start <= relative_stop
            #dom_end_in = relative_start <= dom_stop and dom_stop <= relative_stop

            #if dom_start_in or dom_end_in:
            #    domains_in_exon.append(domain)
        nums = [domain['index'] for domain in domains_in_exon]
        exon['domains'] = domains_in_exon
        relative_start_mod = 0
        if last_exon:
            relative_start_mod = abs(exon['start'] - last_exon['end'])
        relative_start = relative_stop + 1 + relative_start_mod
        last_exon = exon
    return exons

def get_bar():
    return bar

def assign_and_get(specie,name):
    #print ('assign and get specie {} name {}'.format(specie,name))
    global bar
    bar = bar+1
    if name:
        return assignDomainsToExons(name,get_domains(name,specie),specie)
    return None

def write_to_db(data,specie):
    # write all domains in exons to db
    # data is build [(id,index,[domains_nums]),...]
    #print('writing to db/domains.db...')
    with lite.connect(conf.databases[specie]) as con:
        cursor = con.cursor()
        cursor.executescript("drop table if exists domains;")
        cursor.execute("CREATE TABLE domains(transcript_id TEXT, exon_index INT,domains_states TEXT, domains_list TEXT)")
        cursor.executemany("INSERT INTO domains VALUES(?,?,?,?)",data)



def main(specie):
    #print(get_domains('uc007aeu.1'))
    #print(get_domains('uc012gqd.1'))
    #print(get_domains('uc007afi.2'))
    print("loading {} data...".format(specie))
    with lite.connect(conf.databases[specie]) as con:
        cursor = con.cursor()
        # TODO might be a problem here
        cursor.execute("SELECT DISTINCT transcript_id from aliases")
        result = cursor.fetchall()
    names = [value[0] for value in result]
    print("creating transcript database for {}".format(specie))
    # give this thing a progress bar
    global bar
    bar = progressbar.AnimatedProgressBar(end=len(names),width=10)
    pool = ThreadingPool(num_threads)
    assign_and_get_with_specie = partial(assign_and_get, specie)
    result = pool.amap(assign_and_get_with_specie,names)
    while True:
        if result.ready():
            break
        bar.show_progress()
        time.sleep(1)
    data = list(result.get())
    # dark magic incoming
    # flatten the list
    # make it a list of tuples of id,index,domainlist
    data = [(exon['transcript_id'],exon['index'],json.dumps((exon['domains_states'])),json.dumps(exon['domains'])) for exons in data if exons != None for exon in exons if exon != None]
    #ids = [tup[0] for tup in data]
    #indexes = [tup[1] for tup in data]
    #domains = [tup[2] for tup in data]
    #data = zip(ids,indexes,names)
    write_to_db(data,specie)
    print()
if __name__ == '__main__':
    for specie in conf.species:
        user_input = input("Create the {} domains database? (Y/n): ".format(specie))
        if user_input.lower() == 'n':
            continue
        main(specie)


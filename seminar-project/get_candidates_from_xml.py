import os
import re
from xml.etree import ElementTree

import psycopg2
from dotenv import load_dotenv


def get_candidates_from_db():
    conn = psycopg2.connect(host='127.0.0.1', port=os.getenv('DB_SERVICE_PORT'), dbname=os.getenv('POSTGRES_DB'),
                            user=os.getenv('POSTGRES_USER'), password=os.getenv('POSTGRES_PASSWORD'))
    cur = conn.cursor()

    str_contents = open('tezaurs_2022_04_tei.xml', 'r').read()
    str_contents = re.sub('(</?mentioned/?>)|(</?True/?>)', '', str_contents)
    new_file = open('processed.xml', 'w')
    new_file.write(str_contents)

    tezaurs = ElementTree.parse('processed.xml')
    body = tezaurs.getroot()[1]
    with open('possible_entries.txt', 'w') as output_file:
        for entry in body:
            with open('input.txt', 'r+') as input_file:
                definition = entry[1][0].text
                input_file.write(definition + '\n')
                os.system('./LVTagger/morphotagger.sh < ./input.txt > output.txt')
                output = open('output.txt', 'r')
                for line in output:
                    if not (lemma := line.split()):
                        continue
                    lemma = lemma[2]

                    # Checking if there is a corresponding entry to a lemmatized word.
                    cur.execute(f"select id from dict.entries where heading='{lemma}' limit 1")
                    res = cur.fetchone()

                    if res is None:
                        output_file.write(f'{lemma}\n')
                input_file.truncate()


if __name__ == '__main__':
    load_dotenv()
    get_candidates_from_db()
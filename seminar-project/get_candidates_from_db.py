import os

from dotenv import load_dotenv
import psycopg2


def get_candidates_from_db():
    conn = psycopg2.connect(host='127.0.0.1', port=os.getenv('DB_SERVICE_PORT'), dbname=os.getenv('POSTGRES_DB'),
                            user=os.getenv('POSTGRES_USER'), password=os.getenv('POSTGRES_PASSWORD'))
    cur = conn.cursor()

    cur.execute('select gloss from dict.senses')
    definitions = cur.fetchall()

    counter = 1

    with open('possible_entries.txt', 'w') as output_file:
        for definition in definitions:
            gloss = definition[0]
            print(f'Definition {counter}', gloss)
            counter += 1

            with open('input.txt', 'r+') as input_file:
                input_file.write(gloss + '\n')
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
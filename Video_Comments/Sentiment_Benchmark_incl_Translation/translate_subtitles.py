# filter the comments csv for only English comments
import pandas as pd
from DatabaseConnection import DatabaseConnection
import sqlite3
from DetectLanguage import DetectLanguage
from CsvAction import CsvAction
from datetime import datetime, timedelta

comments_file = "full_comments_dataframe.csv"

rows = 108000
# skipe one more than i value
skip = range(1, 266116)
counter = "counter.txt"
#bis 50000 in Datenbank
#bis 119645 in Datenbank
#bis 155245 in Datenbank

def save_to_database(db_file, csv):
    conn = sqlite3.connect(db_file)
    # i value to start with
    i = 266115
    for row in csv.itertuples():

        comment_id = row[1]
        comment_content = row[2]
        comment_date = row[3]
        comment_original = row[4]
        last_edit_date = row[5]
        like_count = row[6]
        video_id = row[7]

        if pd.isnull(comment_content):
            translation = None
            language = None
        else:
            translation, language = DetectLanguage.detect_language(comment_content)

        data = [[i, comment_id, comment_date, comment_content, comment_original, last_edit_date, like_count, video_id,
                 translation, language]]

        column_names = ["index", "comment_id", "comment_date", "comment_content", "comment_original", "last_edit_date",
                        "like_count", "video_id", "translation", "language"]
        sql_dataframe = pd.DataFrame(data, columns=column_names)
        i += 1
        if i == 0:
            sql_create_comments_table = """ CREATE TABLE IF NOT EXISTS comments (
                                                                    index INT PRIMARY KEY, 
                                                                   comment_id text,
                                                                   comment_content text ,
                                                                   comment_date DATE ,
                                                                   comment_original text ,
                                                                    last_edit_date DATE ,
                                                                    like_count FLOAT ,
                                                                    video_id text, 
                                                                    language text,
                                                                    translation text                                  
                                                               ); """
            DatabaseConnection.create_table(conn, sql_create_comments_table)
            sql_dataframe.to_sql('comments', conn, if_exists='append', index=False)
        else:
            sql_dataframe.to_sql('comments', conn, if_exists='append', index=False)
        str_i = str(i)
        file = open(counter, 'w')
        file.write(str_i)
        file.close()


def read_csv(comments):
    csv_data = CsvAction.read_csv(comments, skip, rows)
    return csv_data


def main():
    db_connection = DatabaseConnection.create_connection(
        r"C:\Users\ba051652\OneDrive - Otto-Friedrich-Universität Bamberg\SS 20\Seminar\Shared folder\sentiwordnet\Database\languages.db")
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print("Start Time =", current_time)
    csv_file = read_csv(comments_file)
    save_to_database(db_connection, csv_file)
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print("End Time =", current_time)


if __name__ == "__main__":
    main()

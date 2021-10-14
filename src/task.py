import pandas as pd
from pathlib import Path
import os
import ast
project_dir = str(Path(os.path.abspath(__file__)).parent.parent)
publications_dir = project_dir + '\data\publications_min.csv'


def get_unique_affiliations(df):
    affilitions = df['affiliations'].unique()

    # Here the large upgrade would be cleansing it and making the comparison between affiliations to merge the same ones
    # with tiny differences, for example Levenstein distance. Then the same affiliations should be normalised into the
    # exact same names.

    return affilitions


def get_unique_authors(df):
    # Splitting the author by surnames to facilitate and speed up extraction of distinct authors
    surnames = df['Surname'].unique()
    unique_authors = []
    for surname in surnames:
        _df = df[df['Surname'] == surname]
        if len(_df) == 1:  # This covers single surname appearances
            unique_authors.append(_df)

        else:
            lists_of_names = []
            for author in _df['Name']:
                author = ' '.join(author)
                if author not in lists_of_names:
                    lists_of_names.append(author)

            if len(lists_of_names) == 1:  # this covers reappearing single identical name
                # I should be checking affiliations here too to figure out if these are not separate people with the
                # same name.
                unique_authors.append(_df.iloc[0])

            else:
                """
                Here starts the part with comparing names between each other and initials.
                There are such possibilities:
                1. There are separate people with different names
                2. There is one person with name given in different format/way
                3. There are separate people with the same names

                and all the combinations of those.

                To record them as unique authors I would perform such steps:
                0. I create 'prerecord'.
                1. Check names and affiliations to 'prerecord' and separate people who are not doubled.
                2. Of remaining, if names are doubled, but affiliations don't match at all, I consider them different 
                   people with the same name and 'prerecord' them.
                3. If the names are doubled with intersecting affiliation I consider it one person and 'prerecord' them.

                4. I create record
                5. Now I'm verifying 'prerecorded' names with each other - same affiliations with matching initials or 
                   first element of name lists are considered the same person and recorded as the longest name list. 
                   Same affiliations with not matching initials/names are recorded as different people in the same 
                   affiliation (or intersecting affiliation).
                6. After checking results I would decide if further measures are needed. Probable options would be the
                   levenstein distance.

                """
                print(1)
    return unique_authors


def load_data():
    # Tn case the data would be very large, it should be done with generator, but if the memory is not a problem, this
    # is faster. In normal situation this method would be way larger, probably basing o multiple csvs, dbs or different
    # formats.
    return pd.read_csv(publications_dir)[['authors', 'affiliations']].dropna()


def normalise_data(data):
    """ Here the formats, encodings, unnecessary signs, different ways of writing same names and other issues should
    be brought to uniform format allowing easy comparison. """
    return data


def task():
    data = load_data()
    data = normalise_data(data)

    global all_auths
    all_auths = []

    def reformat_data_apply(row):
        authors = ast.literal_eval(row['authors'])  # reformats list-like string into list
        authors = pd.DataFrame(authors, columns=['authors'])

        # filters out empty strings and most of the cities and splits affiliations
        affiliations = [x for x in row['affiliations'].split(',') if x != '' and len(x.split()) > 1]
        authors['affiliations'] = [affiliations for i in authors.index]
        all_auths.append(authors)

    data.apply(reformat_data_apply, axis=1)
    all_auth_df = pd.concat(all_auths)

    unique_affiliations = get_unique_affiliations(data)

    # Cleaning the df and reformatting it
    all_auth_df.rename(columns={'authors': 'Name'}, inplace=True)
    all_auth_df['Surname'] = all_auth_df['Name'].apply(lambda x: x.split(" ")[-1])
    all_auth_df['Name'] = all_auth_df['Name'].apply(lambda x: x.split(" ")[:-1])
    all_auth_df.sort_values(by=['Surname'], inplace=True)
    all_auth_df = all_auth_df[~all_auth_df.astype(str).duplicated()]

    unique_authors = get_unique_authors(all_auth_df)

    return unique_affiliations, unique_authors


if __name__ == "__main__":
    task()


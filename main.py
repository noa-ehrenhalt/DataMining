import os
import argparse
import pandas as pd
import Web_Scraper
import update_animal_db

def parse():
#    OPERATION_MAP = dict(intake_date_range=intake_date_range, search_animal=search_animal)
    LOCATIONS = list(update_animal_db.location_table['location_name'])
    BREEDS = list(update_animal_db.breed_table['breed_name'])

    parser = argparse.ArgumentParser(description='')
#    parser.add_argument('operation', metavar='', choices=OPERATION_MAP.keys(), help='operation')
#    parser.add_argument('arg1')
    parser.add_argument('-l', dest='location', choices=LOCATIONS, nargs=1,
                        help='filter result by specific location')
    parser.add_argument('-b', dest='breed', choices=BREEDS, nargs=1,
                        help='filter result by specific breed')

    args = parser.parse_args()

    if args.location and args.breed:
        loc_df = update_animal_db.location_table[update_animal_db.location_table['location_name'].isin(args.location)]
        loc_id = loc_df.iloc[0][0]
        breed_df = update_animal_db.breed_table[update_animal_db.breed_table['breed_name'].isin(args.breed)]
        breed_id = breed_df.iloc[0][0]
        results_df = update_animal_db.animal_table[(update_animal_db.animal_table['breed_id'] == breed_id) &
                                                   (update_animal_db.animal_table['location_id'] == loc_id)]
        print(results_df)
    elif args.location:
        loc_df = update_animal_db.location_table[update_animal_db.location_table['location_name'].isin(args.location)]
        loc_id = loc_df.iloc[0][0]
        loc_df = update_animal_db.animal_table[update_animal_db.animal_table['location_id'] == loc_id]
        print(loc_df)
    elif args.breed:
        breed_df = update_animal_db.breed_table[update_animal_db.breed_table['breed_name'].isin(args.breed)]
        breed_id = breed_df.iloc[0][0]
        breed_df = update_animal_db.animal_table[update_animal_db.animal_table['breed_id'] == breed_id]
        print(breed_df)

#os.system('python Web_Scraper.py')
#os.system('python update_animal_db.py')


def main():
    parse()

if __name__ == '__main__':
    main()
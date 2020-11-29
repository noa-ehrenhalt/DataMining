from datetime import timedelta, datetime
import argparse
import update_animal_db
import Web_Scraper
import os


def parse():
    locations = list(update_animal_db.location_table['location_name'])
    breeds = list(update_animal_db.breed_table['breed_name'])

    parser = argparse.ArgumentParser(description='Shows animals available at Los Angeles County animal shelters')
    parser.add_argument('-d', dest='days', type=int, nargs=1, help='filter result by animal availability in the last d '
                                                                   'number of days')
    parser.add_argument('-l', dest='location', choices=locations, nargs=1,
                        help='filter result by specific location')
    parser.add_argument('-b', dest='breed', choices=breeds, nargs=1,
                        help='filter result by specific breed')
    parser.add_argument('-a', dest='animal', nargs=1, help='filter result by animal ID - this is recommended to be used'
                                                           ' without other parameters')

    args = parser.parse_args()

    if args.animal:
        results_df = update_animal_db.master_df[update_animal_db.master_df['animal_id'].isin(args.animal)]
        if results_df.empty:
            print('Animal not found. Please verify the animal ID was entered correctly.')
        else:
            print(results_df)
    elif args.days or args.breed or args.location:
        results_df = update_animal_db.master_df
        if args.days:
            today = datetime.now()
            delta = timedelta(days=args.days[0])
            result = today - delta
            results_df = results_df[results_df['available_date'] >= result.date()]
        if args.breed:
            results_df = results_df[results_df['breed_name'].isin(args.breed)]
        if args.location:
            results_df = results_df[results_df['location_name'].isin(args.location)]
        print(results_df)
    else:
        print(update_animal_db.master_df)


def main():
    os.system('python Web_Scraper.py')
    parse()
    os.remove('animal_data.csv')


if __name__ == '__main__':
    main()

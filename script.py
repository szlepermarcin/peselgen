from datetime import date, timedelta
import argparse
#
# pesel generator
#
# generuje numery PESEL w zadanym zakresie lat



start_year = 2014
end_year = 2014
gender = None
limit_for_date = None

parser = argparse.ArgumentParser(
    description='Generuje pesel dla zadanych lat'
    )
parser.add_argument('-s', '--start', help='rok poczatkowy', required=True, type=int)
parser.add_argument('-e', '--end', help='rok koncowy', required=True, type=int)
parser.add_argument('-g', '--gender', help='plec', choices=['M', 'F'])
parser.add_argument('-l', '--limit', help='limit dla jednego roku', type=int)
args = parser.parse_args()
start_year = args.start
end_year = args.end
if args.gender:
    gender = args.gender
if args.limit:
    limit_for_date = args.limit


def date_segment_range():
    def month_offset(year):
        offset = 0
        if (year >= 1800 and year <= 1899):
            offset = 80
        elif (year >= 2000 and year <= 2099):
            offset = 20
        elif (year >= 2100 and year <= 2199):
            offset = 40
        elif (year >= 2200 and year <= 2299):
            offset = 60
        return offset

    def create_date_segment(date_in):
        result = date_in.strftime("%y")
        result = result + str(
            (int(date_in.strftime("%m")) +
                month_offset(int(date_in.strftime("%Y"))))
            ).zfill(2)
        return result + date_in.strftime("%d")

    start_date = date(start_year, 1, 1)
    end_date = date(end_year + 1, 1, 1)

    for n in range(int((end_date - start_date).days)):
        yield create_date_segment(start_date + timedelta(n))

def middle_segment_range():
    end = 9999
    if (limit_for_date is not None):
        end = limit_for_date

    def filter(fn):
        return {
                "M": (fn % 2) == 1,
                "F": (fn % 2) == 0
                }.get(gender, True)

    for n in [i for i in range(0, end + 1) if filter(i)]:
        yield str(n).zfill(4)

def control_sum_segment(p):
    return str(
            ((9 * int(p[0])) +
                (7 * int(p[1])) +
                (3 * int(p[2])) +
                (1 * int(p[3])) +
                (9 * int(p[4])) +
                (7 * int(p[5])) +
                (3 * int(p[6])) +
                (1 * int(p[7])) +
                (9 * int(p[8])) +
                (7 * int(p[9]))) % 10
            )

def create_pesel(date_segment, middle_segment):
    return (date_segment +
            middle_segment +
            control_sum_segment(date_segment + middle_segment))

def generator():
    for pesel in (create_pesel(date_segment, middle_segment)
            for date_segment in date_segment_range()
            for middle_segment in middle_segment_range()):
        yield pesel


for pesel in generator():
    print(pesel)

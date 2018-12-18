import pandas as pd
from multiprocessing import Pool


class Mapper:
    """Custom multiprocessing map reduce. 
    
    The use of this class for dataframe processing and manipulation greatly
    speeds up the run time."""

    @staticmethod
    def list_to_df(list_object):
        """Read text file for each path in list item (map function)"""

        df = pd.read_csv(list_object, index_col=None, header=None,
                         names=['taxi_id', 'date_time', 'longitude', 'latitude'])

        df['date_time'] = pd.to_datetime(df['date_time'])

        return df

    @staticmethod
    def mult_map(func, list_object):
        """Process a map function in parallel"""

        pool = Pool()
        mapped_list = list(pool.map(func, list_object))

        pool.close()
        pool.join()

        return mapped_list


def vincenty_distance(df):
    """Calculate vincenty distance"""

    from vincenty import vincenty

    df["longitude_shift"] = df.longitude.shift()
    df["latitude_shift"] = df.latitude.shift()

    df['vincenty_distance'] = df.apply(lambda row: vincenty(point1=(row['latitude'], row['longitude']),
                                                            point2=(row['latitude_shift'], row['longitude_shift'])),
                                       axis=1)

    df = df.drop(['longitude_shift', 'latitude_shift'], axis=1)

    return df

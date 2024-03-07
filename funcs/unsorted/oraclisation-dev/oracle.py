import time

import numpy as np

import math

# Degrees of longitude and latitude in 1 chunk
CHUNK_DEC = 2
CHUNK_RES = 1/(math.pow(10,CHUNK_DEC))

class query:
    """
    
    """

    def coord_boundaries(self, lon, lat):
        """
        Check input longitude and latitude are within margins/boundaries
        Boundaries are (0 <= lon <= 360) and (0 <= lat <= 180)
        """
        bool_lon = False
        bool_lat = False
        if 0 <= lon and lon <= 360:
            bool_lon = True
        if 0 < lat and lat <= 180:
            bool_lat = True
        return (bool_lon and bool_lat)
    
    def get_chunks(self, chunk_coords):
        """
        Takes chunk_coords and gets chunk id's
        """
        self.chunks = []
        for coords in chunk_coords:
            chunk_id = ((180/CHUNK_RES))*(coords[0]/CHUNK_RES) + coords[1]/CHUNK_RES
            self.chunks.append(round(chunk_id))

    def __init__(self, input_coords):
        """
        Initial query setup
        """
        chunk_coords = []
        # Checks if input coords are valid
        if isinstance(input_coords, (list, tuple, np.ndarray)):
            for coords in input_coords:
                if len(coords) == 2:
                    coords_r = (round(coords[0],CHUNK_DEC), round(coords[1],CHUNK_DEC))
                    if self.coord_boundaries(coords_r[0], coords_r[1]):
                        chunk_coords.append(coords_r)
        # If any coordinates have passed validity test timestamp saved
        if len(chunk_coords) > 0:
            self.get_chunks(chunk_coords)
            self.timestamp = time.time()
        # If no valid coordinates selected error raised and no new query created
        else:
            raise Exception("Input coords must be of form [(lon1, lat1), (lon2, lat2), ...]")
        
    


new_query = query([(359.99,179.99), (9,9)])
print(new_query.chunks)






# def get_location():
#     """
#     Get location from sender of what location is required
#         Coordinates, Radius
#     """

#     return

# def input_data_current():
#     """
#     Get location related data from sources available (Sources can be paid for being data provider)
#         Vector and Raster Maps (Vector would be more useful as smaller data size)
#     """
#     return

# def input_data_historic():
#     """
#     Get location related data from IPFS storage
#     """
#     return

# def combine():
#     """
    
#     """
#     return

# def output_data():
#     """
#     Save data onto IPFS
#     Send IPFS link to blockchain oracle is built on
#     """
#     return
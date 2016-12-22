import os
import records

home_dir = os.path.expanduser('~')
base_photo_stream_dir = os.path.join(home_dir,'Library', 'Containers', 'com.apple.cloudphotosd', 'Data', 'Library',
                                     'Application Support', 'com.apple.cloudphotosd', 'services',
                                     'com.apple.photo.icloud.sharedstreams')


def initialize(destination, streams=None, verbose=False):
    if not os.path.exists(destination):
        # TODO: make a real error statement
        print "Unable to read destination directory"
    if streams is None:
        streams_list = os.listdir(destination)
        # TODO: make a real output statement
        print "No streams selected, defaulting to all: " + ' ,'.join(map(str, streams_list))


def get_sqllite_db_path(photostream_dir):
    """
    This module is basically just to find the sqllite database from the base photostream directory.
    It is kinda lazy and probably brittle, but if this breaks then a lot of other stuff will probably also break.
    :param photostream_dir:
    :return: sqllite file path
    """
    share_dir = os.path.join(photostream_dir, 'coremediastream-state')
    # now look for the directory in the share dir, and grab the first one
    # based on this answer:
    # http://stackoverflow.com/questions/973473/getting-a-list-of-all-subdirectories-in-the-current-directory
    # this folder name can probably be figured out programmatically
    model_dir = next(os.walk(share_dir))[1][0]
    sqlite_path = os.path.join(share_dir, model_dir, "Model.sqlite")
    return sqlite_path


def get_ps_img_uuids(stream_name, photostream_dir):
    sqlite_path = get_sqllite_db_path(photostream_dir)
    db = records.Database('sqlite+pysqlite:///'+sqlite_path)
    sql = "SELECT ac.GUID AS 'uuid', ac.photoDate AS 'date' FROM AssetCollections AS ac JOIN Albums AS a ON a.GUID = " \
          "ac.albumGUID WHERE a.name = :stream;"
    rows = db.query(sql, stream=stream_name).as_dict()
    return rows


def get_ps_album_uuids(stream_name, photostream_dir):
    sqlite_path = get_sqllite_db_path(photostream_dir)
    db = records.Database('sqlite+pysqlite:///'+sqlite_path)
    sql = "SELECT a.GUID AS 'uuid' FROM Albums AS a WHERE a.name = :stream;"
    rows = db.query(sql, stream=stream_name).as_dict()
    return rows

def get_all_photostream_names(photostream_dir):
    sqlite_path = get_sqllite_db_path(photostream_dir)
    db = records.Database('sqlite+pysqlite:///' + sqlite_path)
    sql = "SELECT name FROM Albums;"
    rows = db.query(sql).as_dict()
    print rows
    return rows

photo_folders = get_ps_img_uuids("Sylvia", base_photo_stream_dir)
print photo_folders
stream_folder = get_ps_album_uuids("Sylvia", base_photo_stream_dir)
print('stream(s)')
print stream_folder

get_all_photostream_names(base_photo_stream_dir)
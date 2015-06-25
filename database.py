import logging as log
import sqlite3

class Database():
    "Class to manage interactions with database"

    def __init__(self):
        self.connection = sqlite3.connect('book.db')
        self.connection.row_factory = sqlite3.Row
        try:
            self.sanity_checks()
        except Exception:
            self.create_schema()

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.connection.close()

    def sanity_checks(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='BOOKINGS'")
        if cursor.fetchone() == None:
            log.info('Missing database schema, creating it')
            raise RuntimeError('Missing schema')

    def create_schema(self):
        cursor = self.connection.cursor()
        cursor.executescript('''
            CREATE TABLE ROOMS (ROOM_ID INTEGER PRIMARY KEY,
                                NAME TEXT UNIQUE NOT NULL);
            CREATE UNIQUE INDEX IDX_ROOMS ON ROOMS(NAME);

            CREATE TABLE GUESTS (GUEST_ID INTEGER PRIMARY KEY,
                                 NICKNAME TEXT UNIQUE NOT NULL, 
                                 FIRST_NAME TEXT, 
                                 LAST_NAME TEXT);
            CREATE UNIQUE INDEX IDX_GUESTS ON GUESTS(NICKNAME);

            CREATE TABLE FEATURES (FEATURE_ID INTEGER PRIMARY KEY,
                                   NAME TEXT UNIQUE NOT NULL,
                                   DESC TEXT);
            CREATE UNIQUE INDEX IDX_FEATURES ON FEATURES(NAME);

            CREATE TABLE BEDS (BED_ID INTEGER PRIMARY KEY, 
                               NAME TEXT UNIQUE NOT NULL,
                               CAPACITY INTEGER NOT NULL,
                               FEATURE_ID INTEGER,
                               ROOM_ID INTEGER,
                               FOREIGN KEY(FEATURE_ID) REFERENCES FEATURES(FEATURE_ID),
                               FOREIGN KEY(ROOM_ID) REFERENCES ROOMS(ROOM_ID));
            CREATE UNIQUE INDEX IDX_BEDS ON BEDS(NAME);

            CREATE TABLE BOOKINGS (BOOKING_ID INTEGER PRIMARY KEY,
                                   GUEST_ID INTEGER NOT NULL,
                                   BED_ID INTEGER NOT NULL,
                                   DATE TEXT NOT NULL,
                                   FOREIGN KEY(GUEST_ID) REFERENCES GUESTS(GUEST_ID),
                                   FOREIGN KEY(BED_ID) REFERENCES BEDS(BED_ID));
            CREATE UNIQUE INDEX IDX_BOOKINGS ON BOOKINGS(GUEST_ID, BED_ID, DATE);
        ''')

    def add_room(self, name):
        log.info('Adding room [%s] to the database', name)
        cursor = self.connection.cursor()
        cursor.execute("INSERT INTO ROOMS (NAME) VALUES (:ROOM_NAME)", {"ROOM_NAME": name})
        self.connection.commit()

    def add_feature(self, name, desc = None):
        log.info('Adding feature [%s] to the database', name)
        cursor = self.connection.cursor()
        cursor.execute("INSERT INTO FEATURES (NAME, DESC) VALUES (:FEATURE_NAME,:FEATURE_DESC)",
                {"FEATURE_NAME": name, "FEATURE_DESC": desc})
        self.connection.commit()

    def add_guest(self, nick, first_name = None, last_name = None):
        log.info('Adding guest [%s] to the database', nick)
        cursor = self.connection.cursor()
        cursor.execute("INSERT INTO GUESTS (NICKNAME, FIRST_NAME, LAST_NAME) VALUES (:NICKNAME,:FIRST_NAME,:LAST_NAME)",
                {"NICKNAME": nick, "FIRST_NAME": first_name, "LAST_NAME": last_name})
        self.connection.commit()

    def add_bed(self, name, capacity, room = None, feature = None):
        log.info('Adding bed [%s] to the database', name)
        cursor = self.connection.cursor()
        # First check that the room and feature exists and fetch the corresponding ids
        room_id = None
        feature_id = None
        if room:
            cursor.execute("SELECT ROOM_ID FROM ROOMS WHERE NAME=:NAME",{"NAME": room})
            room_id = cursor.fetchone()
            if room_id == None:
                print "Room [%s] does not exist!" % room
                exit(1)
            room_id = room_id["ROOM_ID"]
        if feature:
            cursor.execute("SELECT * FROM FEATURES WHERE NAME=:NAME",{"NAME": feature})
            feature_id = cursor.fetchone()
            if feature_id == None:
                print "Feature [%s] does not exist!" % feature
                exit(1)
            feature_id = feature_id["FEATURE_ID"]
        cursor.execute("INSERT INTO BEDS (NAME,CAPACITY,FEATURE_ID,ROOM_ID) VALUES (:NAME,:CAPACITY,:FEATURE,:ROOM)",{"NAME":name,"CAPACITY":capacity,"FEATURE":feature_id,"ROOM":room_id})
        self.connection.commit()
        
    def remove_bed(self, name):
        log.info('Removing bed [%s] from the database', name)
        cursor = self.connection.cursor()

        # First check that the bed exists and fetch the corresponding id
        bed_id = None
        cursor.execute("SELECT BED_ID FROM BEDS WHERE NAME=:NAME",{"NAME": name})
        bed_id = cursor.fetchone()
        if bed_id == None:
            print "Bed [%s] does not exist!" % name
            log.warn('Bed [%s] does not exist!', name)
            exit(1)
        bed_id = bed_id["BED_ID"]

        # Now check if bookings exist for this bed, in which case they must be removed first
        cursor.execute("SELECT COUNT(*) AS NB_BOOKINGS FROM BOOKINGS WHERE BED_ID = :ID",{"ID":bed_id})
        resultset = cursor.fetchone()
        if resultset != None:
            nb_bookings = resultset["NB_BOOKINGS"]
            if nb_bookings != 0:
                print "Some bookings exist for this bed, please remove them first!"
                log.warn('Bookings registered for bed [%s], can\'t remove it', name)
                exit(1)

        cursor.execute("DELETE FROM BEDS WHERE BED_ID = :ID",{"ID":bed_id})
        self.connection.commit()

    def remove_feature(self, name):
        log.info('Removing feature [%s] from the database', name)
        cursor = self.connection.cursor()

        # First check that the feature exists and fetch the corresponding id
        feature_id = None
        cursor.execute("SELECT FEATURE_ID FROM FEATURES WHERE NAME=:NAME",{"NAME": name})
        feature_id = cursor.fetchone()
        if feature_id == None:
            print "Feature [%s] does not exist!" % name
            log.warn('Feature [%s] does not exist!', name)
            exit(1)
        feature_id = feature_id["FEATURE_ID"]

        # Now check if beds have this feature, in which case they must be removed first
        cursor.execute("SELECT COUNT(*) AS NB_BEDS FROM BEDS WHERE FEATURE_ID = :ID",{"ID":feature_id})
        resultset = cursor.fetchone()
        if resultset != None:
            nb_beds = resultset["NB_BEDS"]
            if nb_beds != 0:
                print "Some beds are registered with this feature, please remove them first!"
                log.warn('Beds registered with feature [%s], can\'t remove it', name)
                exit(1)

        cursor.execute("DELETE FROM FEATURES WHERE FEATURE_ID = :ID",{"ID":feature_id})
        self.connection.commit()

    def remove_guest(self, nickname):
        log.info('Removing guest [%s] from the database', nickname)
        cursor = self.connection.cursor()

        # First check that the guest exists and fetch the corresponding id
        guest_id = None
        cursor.execute("SELECT GUEST_ID FROM GUESTS WHERE NICKNAME=:NAME",{"NAME": nickname})
        guest_id = cursor.fetchone()
        if guest_id == None:
            print "Guest [%s] does not exist!" % nickname
            log.warn('Guest [%s] does not exist!', nickname)
            exit(1)
        guest_id = guest_id["GUEST_ID"]

        # Now check if bookings exist for this guest, in which case they must be removed first
        cursor.execute("SELECT COUNT(*) AS NB_BOOKINGS FROM BOOKINGS WHERE GUEST_ID = :ID",{"ID":guest_id})
        resultset = cursor.fetchone()
        if resultset != None:
            nb_bookings = resultset["NB_BOOKINGS"]
            if nb_bookings != 0:
                print "Some bookings exist for this guest, please remove them first!"
                log.warn('Bookings registered for guest [%s], can\'t remove it', nickname)
                exit(1)

        cursor.execute("DELETE FROM GUESTS WHERE GUEST_ID = :ID",{"ID":guest_id})
        self.connection.commit()

    def remove_room(self, name):
        log.info('Removing room [%s] from the database', name)
        cursor = self.connection.cursor()

        # First check that the room exists and fetch the corresponding id
        room_id = None
        cursor.execute("SELECT ROOM_ID FROM ROOMS WHERE NAME=:NAME",{"NAME": name})
        room_id = cursor.fetchone()
        if room_id == None:
            print "Room [%s] does not exist!" % name
            log.warn('Room [%s] does not exist!', name)
            exit(1)
        room_id = room_id["ROOM_ID"]

        # Now check if beds are found for this room, in which case they must be removed first
        cursor.execute("SELECT COUNT(*) AS NB_BEDS FROM BEDS WHERE ROOM_ID = :ID",{"ID":room_id})
        resultset = cursor.fetchone()
        if resultset != None:
            nb_beds = resultset["NB_BEDS"]
            if nb_beds != 0:
                print "Some beds are registered for this room, please remove them first!"
                log.warn('Beds registered for room [%s], can\'t remove it', name)
                exit(1)

        cursor.execute("DELETE FROM ROOMS WHERE ROOM_ID = :ID",{"ID":room_id})
        self.connection.commit()

    def list_room(self, name):
        log.info('Listing bookings for room [%s]', name)
        cursor = self.connection.cursor()
        query = '''
            select * from BOOKINGS where BED_ID in (
                select BED_ID from BEDS where ROOM_ID = (select ROOM_ID from ROOMS where NAME=:ROOM_NAME)
            )'''
        cursor.execute(query,{"ROOM_NAME": name})
        rows = cursor.fetchall()
        for row in rows:
            print "Room id: %d, Room name: %s" % (row["ROOM_ID"], row["NAME"])

    def show_entity(self, entity):
        print "%s:" % entity
        cursor = self.connection.cursor()
        query = "select * from '%s'" % entity
        cursor.execute(query)
        rows = cursor.fetchall()
        for row in rows:
            print "\t",
            print row
        print "\n"
        
    def stats_number(self):
        log.info('Gathering database statistics')
        cursor = self.connection.cursor()
        cursor.execute("select name from sqlite_master where type='table'")
        rows = cursor.fetchall()
        for row in rows:
            table = row["NAME"]
            query = "select count(*) as NUM from '%s'" % table
            cursor.execute(query)
            count = cursor.fetchone()
            print "%s | %d" % (table, count["NUM"])

        
    def dump(self):
        for line in self.connection.iterdump():
            print "%s\n" % line

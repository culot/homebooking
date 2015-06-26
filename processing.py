from storage import Database as Storage

class Processing():
    "Class that contains all processing-related methods"

    @staticmethod
    def command_help(options):
        pass

    @staticmethod
    def command_add(options):
        if options.room:
            room_name = options.room[0]
            with Storage() as store:
                store.add_room(room_name)

        if options.bed:
            if len(options.bed) < 3:
                print "At least 3 options are required to register a bed"
                print 'Try: book help'
                exit(1)
            bed_name = options.bed[0]
            bed_capacity = options.bed[1]
            bed_room = options.bed[2]
            bed_feature = options.bed[3] if len(options.bed) == 4 else None
            with Storage() as store:
                store.add_bed(bed_name, bed_capacity, bed_room, bed_feature)

        if options.feature:
            feature_name = options.feature[0]
            feature_desc = options.feature[1] if len(options.feature) == 2 else None
            with Storage() as store:
                store.add_feature(feature_name, feature_desc)

        if options.guest:
            guest_nick = options.guest[0]
            guest_firstname = None
            guest_lastname = None
            guest_firstname = options.guest[1] if len(options.guest) >= 2 else None
            guest_lastname = options.guest[2] if len(options.guest) == 3 else None
            with Storage() as store:
                store.add_guest(guest_nick, guest_firstname, guest_lastname)

    @staticmethod
    def command_register(options):
	guest_nick = options.guest[0]
	bed_name = options.bed[0]
	date = options.date[0]
	with Storage() as store:
	    store.register(guest_nick, bed_name, date)

    @staticmethod
    def command_unregister(options):
	guest_nick = options.guest[0]
	bed_name = options.bed[0]
	date = options.date[0]
	with Storage() as store:
	    store.unregister(guest_nick, bed_name, date)

    @staticmethod
    def command_remove(options):
        if options.bed:
            bed_name = options.bed[0]
            with Storage() as store:
                store.remove_bed(bed_name)

        if options.feature:
            feature_name = options.feature[0]
            with Storage() as store:
                store.remove_feature(feature_name)

        if options.guest:
            guest_name = options.guest[0]
            with Storage() as store:
                store.remove_guest(guest_name)

        if options.room:
            room_name = options.room[0]
            with Storage() as store:
                store.remove_room(room_name)

    @staticmethod
    def command_list(options):
        if options.room:
            room_name = options.room[0]
            with Storage() as store:
                store.list_room(room_name)
        if options.bed:
            bed_name = options.bed[0]
            with Storage() as store:
                store.list_bed(bed_name)
        if options.guest:
            guest_nick = options.guest[0]
            with Storage() as store:
                store.list_guest(guest_nick)
        if options.date:
            date = options.date[0]
            with Storage() as store:
                store.list_date(date)

    @staticmethod
    def command_search(options):
        date = options.date[0]
        with Storage() as store:
            store.search_date(date)

    @staticmethod
    def command_show(options):
        if options.bed:
            with Storage() as store:
                store.show_entity("BEDS")            
        if options.feature:
            with Storage() as store:
                store.show_entity("FEATURES")
        if options.guest:
            with Storage() as store:
                store.show_entity("GUESTS")
        if options.room:
            with Storage() as store:
                store.show_entity("ROOMS")
            
    @staticmethod
    def command_stats(options):
        if options.number:
            with Storage() as store:
                store.stats_number()
    
    @staticmethod
    def command_dump(options):
        with Storage() as store:
            store.dump()


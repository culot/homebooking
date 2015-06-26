import sys
import argparse

class CmdLine():
    "User input handling class"

    def __init__(self):

        self.command = None
        self.options = None

        parser = argparse.ArgumentParser(
                    description='Home booking system',
                    usage='''book <command> [<options>] (see: book help)''')
        parser.add_argument("command", help='Subcommand to run')
        args = parser.parse_args(sys.argv[1:2])
        self.command = args.command

        if not hasattr(self, args.command):
            print 'Unrecognized command\n'
            print 'Try: book help'
            exit(1)

        getattr(self, self.command)()


    def help(self):
        print '''\
usage: book <command> [<options>]

The available commands are (when marked with *, command is not yet implemented):
  help        Display help text

  add         Add an entity to the booking system
              The available options are:

              -b, --bed <name> <capacity> [room_name] [feature_name]
                  Add a bed, specifying a name for it, the name of
                  the room it resides, its capacity and an optional
                  feature name

              -f, --feature <name> [description]
                  Add a feature, specifying its name and adding an
                  optional description

              -g, --guest <nick> [first_name] [last_name]
                  Add a guest, specifying its nickname, and optional
                  first and last names

              -r, --room <name>
                  Add a room, specifying its name

  remove      Remove an entity from the booking system
              The available options are:

              -b, --bed <name>
                  Remove bed called <name>

              -f, --feature <name>
                  Remove feature called <name>

              -g, --guest <nick>
                  Remove guest whose nickname is <nick>

              -r, --room <name>
                  Remove room called <name>

  register    Register a guest
              The following options are mandatory to register a guest
              for the specified bed at the specified date:

              -g, --guest <nick>
              -b, --bed <name>
              -d, --date <date>

  unregister  Unregister a guest
              Mandatory options are the same as when registering a
              guest:

              -g, --guest <nick>
              -b, --bed <name>
              -d, --date <date>

  *list*      List bookings based on user-provided options
              The available options are: 

              -d, --date  <date>
                  Search for the specified date

              -g, --guest <nickname>
                  Search for the specified nickname

              -r, --room  <name>
                  Search for the specified room

  *search*    Search for availabilities

  show        Show entities stored in the booking system.
              If no options are specified then all entities are shown.
              The available options are: 

              -b, --bed
                  Show beds

              -f, --feature
                  Show features

              -g, --guest
                  Show guests

              -r, --room
                  Show rooms

  stats       Display statistics about objects stored in database
              The available options are:

              -n, --number
                  Display the number of objects stored in database

  dump        Dump database objects formatted as insert queries


'''

    def add(self):
        parser = argparse.ArgumentParser(description = 'Add an entity to the booking system')
        parser.add_argument("-b", "--bed", nargs = '+')
        parser.add_argument("-f", "--feature", nargs = '+')
        parser.add_argument("-g", "--guest", nargs = '+')
        parser.add_argument("-r", "--room", nargs = 1)
        args = parser.parse_args(sys.argv[2:])
        if not args.bed and not args.feature and not args.guest and not args.room:
            print "At least one option is required!"
            print 'Try: book --help'
            exit(1)
        self.options = args

    def remove(self):
        parser = argparse.ArgumentParser(description = 'Remove an entity from the booking system')
        parser.add_argument("-b", "--bed", nargs = 1)
        parser.add_argument("-f", "--feature", nargs = 1)
        parser.add_argument("-g", "--guest", nargs = 1)
        parser.add_argument("-r", "--room", nargs = 1)
        args = parser.parse_args(sys.argv[2:])
        if not args.bed and not args.feature and not args.guest and not args.room:
            print "At least one option is required!"
            print 'Try: book --help'
            exit(1)
        self.options = args

    def register(self):
        parser = argparse.ArgumentParser(description = 'Register a guest in the booking system')
        parser.add_argument("-g", "--guest", nargs = 1)
        parser.add_argument("-b", "--bed", nargs = 1)
        parser.add_argument("-d", "--date", nargs = 1)
        args = parser.parse_args(sys.argv[2:])
        if not args.guest or not args.bed or not args.date:
            print "A guest name, bed name, and a date must be provided!"
            print 'Try: book --help'
            exit(1)
        self.options = args

    def unregister(self):
        parser = argparse.ArgumentParser(description = 'Unregister a guest from the booking system')
        parser.add_argument("-g", "--guest", nargs = 1)
        parser.add_argument("-b", "--bed", nargs = 1)
        parser.add_argument("-d", "--date", nargs = 1)
        args = parser.parse_args(sys.argv[2:])
        if not args.guest or not args.bed or not args.date:
            print "A guest name, bed name, and a date must be provided!"
            print 'Try: book --help'
            exit(1)
        self.options = args

    def list(self):
        parser = argparse.ArgumentParser(description = 'List bookings based on given options')
        parser.add_argument("-g", "--guest", nargs = 1)
        parser.add_argument("-d", "--date", nargs = 1)
        parser.add_argument("-r", "--room", nargs = 1)
        args = parser.parse_args(sys.argv[2:])
        if not args.guest and not args.date and not args.room:
            print "At least one option is required!"
            print 'Try: book --help'
            exit(1)
        self.options = args

    def search(self):
        pass

    def show(self):
        parser = argparse.ArgumentParser(description = 'Show objects found in the booking systems')
        parser.add_argument("-b", "--bed", action='store_true')
        parser.add_argument("-f", "--feature", action='store_true')
        parser.add_argument("-g", "--guest", action='store_true')
        parser.add_argument("-r", "--room", action='store_true')
        args = parser.parse_args(sys.argv[2:])
        if not args.bed and not args.feature and not args.guest and not args.room:
            args.bed = True
            args.feature = True
            args.guest = True
            args.room = True
        self.options = args
        
    def stats(self):
        parser = argparse.ArgumentParser(description = 'Display statistics about database')
        parser.add_argument("-n", "--number", action='store_true')
        args = parser.parse_args(sys.argv[2:])
        if not args.number:
            print "At least one option is required!"
            print 'Try: book --help'
            exit(1)
        self.options = args
        
    def dump(self):
        pass

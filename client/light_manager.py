import argparse
import commands.art
import commands.genconfig
import commands.reset
import commands.refresh
import commands.set_art
import commands.turn
import commands.toggle
import commands.upcoming_events
from datetime import datetime

def main():
    parser = argparse.ArgumentParser(description='Manage indoor lighting.')
    subparsers = parser.add_subparsers(dest='command')

    genconfig = subparsers.add_parser('genconfig',
                                      description='Interactively generate a new config file.')
    genconfig.add_argument('output_path', metavar='output-path', type=str, help='System path to write output file to.')

    upcoming_events = subparsers.add_parser('upcoming-events',
                                  description='Print upcoming events.')
    upcoming_events.add_argument('config', type=str, help='System path to config file')
    upcoming_events.add_argument('-d', '--date',
                                 default=datetime.now().strftime("%Y%m%d"),
                                 help='Date to use as start point, formatted as YYYYMMDD. Defaults to system date.')
    upcoming_events.add_argument('-t', '--time',
                                 default=datetime.now().strftime("%H%M"),
                                 help='Time to use as start point, formatted as HHMM. Defaults to system time.')
    upcoming_events.add_argument('-n',
                                 default=2**128,
                                 type=int,
                                 help='Number of events to display. Displays all events by default.')


    reset = subparsers.add_parser('reset',
                                  description='Set lights to default state.')
    reset.add_argument('config', type=str, help='System path to config file')
    reset.add_argument('-d', '--date',
                       default=datetime.now().strftime("%Y%m%d"),
                       help='Date to use when calculating state, formatted as YYYYMMDD. Defaults to system date.')
    reset.add_argument('-t', '--time',
                       default=datetime.now().strftime("%H%M"),
                       help='Time to use when calculating state, formatted as HHMM. Defaults to system time.')
    reset.add_argument('--dry-run',
                       dest='dry_run', action='store_true',
                       help='Do not send commands to toggle lights.')

    turn = subparsers.add_parser('turn',
                              description='Change the state of a specific light.')
    turn.add_argument('lightID', type=int, help='Light identifier, an integer >= 0.')
    turn.add_argument('state', type=str, help='State to change to: \'on\' or \'off\'.')
    turn.add_argument('config', type=str, help='System path to config file.')
    turn.add_argument('--dry-run',
                      dest='dry_run', action='store_true',
                      help='Do not send commands to toggle lights.')

    toggle = subparsers.add_parser('toggle',
                              description='Change the state of a specific light.')
    toggle.add_argument('lightID', type=int, help='Light identifier, an integer >= 0.')
    toggle.add_argument('config', type=str, help='System path to config file.')
    toggle.add_argument('--dry-run',
                      dest='dry_run', action='store_true',
                      help='Do not send commands to toggle lights.')

    refresh = subparsers.add_parser('refresh',
                              description='Send signals to apply the last state used to all lights. Lights that were turned off will be told to turn off, and vise versa.')
    refresh.add_argument('config', type=str, help='System path to config file.')
    refresh.add_argument('--dry-run',
                         dest='dry_run', action='store_true',
                         help='Do not send commands to toggle lights.')

    set_art = subparsers.add_parser('set-art',
                                    description='Set ASCII art of room layout. The art can contain light id\'s 0-9, that will be colorized to indicate state when the art command is used.')
    set_art.add_argument('art', type=str, help='System path to file containing ASCII art.')
    set_art.add_argument('config', type=str, help='System path to config file.')

    art = subparsers.add_parser('art',
                                description='Print room layout ASCII art')
    art.add_argument('config', type=str, help='System path to config file.')

    args = parser.parse_args()

    if args.command == 'genconfig':
        commands.genconfig.do(args.output_path)
    if args.command == 'upcoming-events':
        commands.upcoming_events.do(args.config, args.date, args.time, args.n)
    if args.command == 'reset':
        commands.reset.do(args.config, args.date, args.time, args.dry_run)
    if args.command == 'turn':
        commands.turn.do(args.config, args.lightID, args.state, args.dry_run)
    if args.command == 'toggle':
        commands.toggle.do(args.config, args.lightID, args.dry_run)
    if args.command == 'set-art':
        commands.set_art.do(args.config, args.art)
    if args.command == 'art':
        commands.art.do(args.config)
    if args.command == 'refresh':
        commands.refresh.do(args.config, args.dry_run)

if __name__ == '__main__':
    main()

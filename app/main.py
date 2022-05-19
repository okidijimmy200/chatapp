from handlers import (
    parse_args,
    publisher,
    subscriber
)

args = parse_args()
arg_command = args.command
    
if arg_command == 'send':
    publisher(channel=args.channel, server=args.server, group=args.group)

elif arg_command == 'receive':
    subscriber(channel=args.channel, start_from=args.start_from, server=args.server, group=args.group)



import sys
import argparse
from confluent_kafka import Producer, Consumer


'''input to user'''
def write_message():
    print('Please enter a message')
    try:
        user_input = ''          
        for line in sys.stdin:   
            if line == '\n':     
                break           
            user_input += line  
        return user_input
    except:
        sys.stderr.write('Exception Occurred in the system input!\n')

'''delivery report'''
def delivery_report(err, msg):
    try:
        if err is not None:
            x = 'Message delivery failed: {}'.format(err)
            return x
        else:
            y = 'Message delivered to {} [{}]'.format(msg.topic(), msg.partition())
            return y
    except NameError:
        return "NameError occurred. err or msg isn't defined."

'''parse arguments'''
def parse_args():
    try:
        parser = argparse.ArgumentParser()
        subparser = parser.add_subparsers(dest='command')
        send = subparser.add_parser('send')
        receive = subparser.add_parser('receive')

        send.add_argument('--channel', type=str, required=True)
        send.add_argument('--server', type=str, required=True)
        send.add_argument('--group', type=str, required=False)

        receive.add_argument('--channel', type=str, required=True)
        receive.add_argument('--start_from', type=str, required=True)
        receive.add_argument('--server', type=str, required=True)
        receive.add_argument('--group', type=str, required=True)

        args = parser.parse_args()
        return args  
    except SystemExit:
        print("System exit error.")

'''producer'''
def publisher(channel, server, group=None):
    p = Producer({'bootstrap.servers': server})
    x = write_message()
    p.poll(0)
    p.produce(channel, x, callback=delivery_report)
        
    result = p.flush()
    return result

'''consumer'''
def subscriber(channel, start_from, server, group):
    c = Consumer({
    'bootstrap.servers': server,
    'group.id': group,
    'auto.offset.reset': start_from
    })

    c.subscribe([channel])

    while True:
        msg = c.poll(1.0)

        if msg is None:
            continue
        if msg.error():
            print("Consumer error: {}".format(msg.error()))
            continue
        print('Received message: {}'.format(msg.value().decode('utf-8')))
    x = c.close()
    return x


import io
import sys
from unittest import mock

from app.handlers import  (
    write_message,
    parse_args,
    delivery_report,
    publisher
) 

'''test input from user'''
def test_user_input(monkeypatch):
    monkeypatch.setattr('sys.stdin', io.StringIO('my test data input'))
    i = write_message()
    assert i == 'my test data input'

'''test system args'''
def test_parse_args():
    cmd = 'main.py send --channel mytopic --server localhost:9092 --group mygroup'
    
    sys.argv = cmd.split(' ')
    result = parse_args()
    assert result.channel == 'mytopic'
    assert result.server == 'localhost:9092'
    assert result.group == 'mygroup'

'''test systen receive'''
def test_parse_args_recieve():
    # test coverage highlighter
    cmd = 'main.py receive --channel mytopic --start_from beginning --server localhost:9092 --group mygroup'
    
    sys.argv = cmd.split(' ')
    result = parse_args()
    assert result.channel == 'mytopic'
    assert result.server == 'localhost:9092'
    assert result.group == 'mygroup'


'''test delivery report'''
def test_delivery_report():
    response = delivery_report(err='error', msg='message')
    assert type(response) is str

'''test producer'''
@mock.patch('app.handlers.Producer')
def test_publisher(mock_producer, monkeypatch):
    monkeypatch.setattr('sys.stdin', io.StringIO('my test data input'))
    i = write_message()

    p = mock_producer({'bootstrap.servers':'localhost:9092'})
    p.producer('mychannel', i, callback=delivery_report)

    p.flush.return_value= 'Test value'

    # call publisher here
    result = publisher(channel='mychannel', server='localhost:9092')

    mock_producer.assert_called_with({'bootstrap.servers':'localhost:9092'})
    p.poll.assert_called_with(0)
    p.flush.assert_called
    p.producer.assert_called_with('mychannel', i, callback=delivery_report)
    assert result == 'Test value'
    

@mock.patch('app.handlers.Consumer')
def test_consumer(mock_consumer):
    test = {
    'bootstrap.servers': 'localhost:9092',
    'group.id': 'mygroup',
    'auto.offset.reset': 'beginning'
    }
    channel = ['test', 'work', 1]

    mock_consumer(test)
    mock_consumer.subscribe([channel])
    mock_consumer.poll(1.0)

    consumer = mock_consumer.call_args.args
    subscribe = mock_consumer.subscribe.call_args.args
    poll = mock_consumer.poll.call_args.args

    assert type(*consumer) == dict
    assert type(*subscribe) == list
    assert type(*poll) == float



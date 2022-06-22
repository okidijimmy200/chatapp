import time
import threading
import io
import sys
from unittest import mock
import pytest

from handlers import  (
    write_message,
    parse_args,
    delivery_report,
    publisher,
    subscriber
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
@mock.patch('handlers.Producer')
def test_publisher(mock_producer, monkeypatch):
    monkeypatch.setattr('sys.stdin', io.StringIO('my test data input'))
    i = write_message()

    mock_producer.producer('mychannel', 'my test data input', callback=delivery_report)
    mock_producer({'bootstrap.servers':'localhost:9092'})
    mock_producer.poll(0)
    mock_producer().flush.return_value = 'Test value'
    result = publisher(channel='mychannel', server='localhost:9092')

  
    assert result == 'Test value'
    mock_producer.assert_called_with({'bootstrap.servers':'localhost:9092'})
    mock_producer.poll.assert_called_with(0)
    mock_producer.producer.assert_called_with('mychannel', i, callback=delivery_report)
 
'''test consumer'''
@mock.patch('handlers.Consumer')
def test_consumer_error(mock_consumer, capsys):
    
    # mock_consumer().poll().error.return_value = 'test error'
    # mock_consumer().poll().value.return_value = 'test message'
    mock_consumer().poll().side_effect = [
        'test error',
        'test message'
    ]
    def switch(running):
        time.sleep(.001)
        running['running'] = False

    running = {
        'running': True
    }
    t = threading.Thread(
        target=switch,
        args=(running,)
    )
    t.start()
    subscriber('mychannel', 'beginning', 'localhost:9092', 'mygroup', running)
    captured = capsys.readouterr()

    x = list(captured.out)
    output = []
    for i in x:
        if i == '\n':
            break
        output.append(i)
    assert ''.join(output) == 'Consumer error: test error'
    assert ''.join(output) == 'Receivied message: test message'
    








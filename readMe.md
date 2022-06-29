
![Tests](https://github.com/okidijimmy200/chatapp/actions/workflows/build.yaml/badge.svg)
A command line chat application that uses message broker services of confluent kafka to send
messages.

to send messages:
>python main.py send --channel mychannel --server localhost:9092 --group mygroup

type a message to send

to receive the message
>python main.py receive --channel mychannel --start_from beginning --server localhost:9092 --group mygroup
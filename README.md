# Framework

A Attack and Defence framework used in ctf AWD game.

*When building the docker container, do not use the 163 apt mirror.*

Usage:
You should edit configuration file in folder `config` first and then run:
```
# ./run-docker.sh
root@626d325b64af:/app#
root@626d325b64af:/app# ./main.py
➜  
```
Use `help` instruction to see what we support.

### Basic usage:
To build docker, run:
```
docker build -t n0b0dy:framework .
```
To run docker, run:
```
./run-docker.sh
```


Run command `service all start` first to init all services.
The single command `attack` will attack all gameboxes of all teams of all exps.
To stop auto attack, use `attack stop`;
If new exploit is added, use `service exploit reload` and just type all after the prompt to reload all exploits.
To see currrent exploits, use `service exploit show`.
To see current gameboxes, use `service gamebox show`.

To add exploit, put your *python* script in folder `exploit`.

## CHANGE LOG 2018.6.16
To support auto completion to each command and customize each command's parameters, I decided to migrate the main framework from python native lib 'cmd' to 'python prompt toolkit'.
We keep two central parts, one is command and another is server. The command unit is used for implementation for all commands. Server unit is used for background tasks such as submitting flag.

## CHANGE LOG 2018.6.25
Migrate the framework from `cmd` to `python prompt toolkit`.


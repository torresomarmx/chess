A complete 2 player chess game on the command line.

![demo image](https://raw.githubusercontent.com/torresomarmx/chess/master/image.png)

Features:
- Board flipping after every move
- En passant move
- Pawn promotion
- Castling
- Stalemate
- Checkmate
- Position highlighting
- Save game to yaml file
- Create board from yaml file

Dockerhub: https://hub.docker.com/r/omartorres/cli-chess

To run on docker engine, simply clone the image on dockerhub and then run:

docker container run -it omartorres/cli-chess

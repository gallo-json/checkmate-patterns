from CheckmatePattern import CheckmatePattern
import chess, chess.pgn
import io
import berserk

client = berserk.Client()
games = list(client.games.export_by_player('buenos_dias'))

checkmate_counter = 0
checkmate_moves = []

for i in range(len(games)):
    if games[i]['status'] == 'mate' and games[i]['variant'] == 'standard':
        checkmate_counter += 1
        checkmate_moves.append(games[i]['moves'])

print(checkmate_counter)

fens = []

for i in checkmate_moves:
    fens.append(chess.pgn.read_game(io.StringIO(i)).end().board().fen())

for i in fens:
    CheckmatePattern(i).find_checkmate_pattern()

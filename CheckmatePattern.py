import chess

class CheckmatePattern:

    def __init__(self, board):
        self.board = chess.Board(board)

    def get_full_name(self, letter):
        full_piece_names = {
            'Q': 'Queen',
            'R': 'Rook',
            'B': 'Bishop',
            'N': 'Knight',
            'P': 'Pawn'
        }
        return full_piece_names[letter.upper()]

    # Check if a square around the king is blocked by his own piece
    def is_blocked(self, square):
        if self.board.color_at(square) == (not self.winner()):
            return True
        else:
            return False

    def surrounding_squares(self, king):

        #012
        #3 4
        #567

        return [king + 7, king + 8, king + 9,
                king - 1,           king + 1,
                king - 9, king - 8, king - 7]
    
    def king_on_side(self, king):

        #01     34      123     4 0     
        # 2     2       0 4     321
        #43     10

        # If the king is on the left side
        if chess.square_file(king) == 0:
            return [king + 8, king + 9, king + 1, king - 7, king - 8]
        # If king is on right
        elif chess.square_file(king) == 7:
            return [king - 8, king - 9, king - 1, king + 7, king + 8]
        # Bottom
        elif chess.square_rank(king) == 0:
            return [king - 1, king + 7, king + 8, king + 9, king + 1]
        # Top
        elif chess.square_rank(king) == 7:
            return [king + 1, king - 7, king - 8, king - 9, king - 1]

    def king_on_corner(self, king):

        #21     12      0       0
        # 0     0      21       12

        if chess.square_rank(king) == 0:
            # Bottom left
            if chess.square_file(king) == 0:
                return [1, 9, 8]
            
            # Bottom right
            if chess.square_file(king) == 7:
                return [6, 14, 15]

        if chess.square_rank(king) == 7:
            # Top left
            if chess.square_file(king) == 0:
                return [57, 49, 48]

            # Top right
            if chess.square_file(king) == 7:
                return [62, 54, 55]

    def winner(self):
        if str(self.board.result()) == "1-0":
            return True
        else:
            return False

    ### Checkmate patterns

    def smothered(self, available_squares):
        # If all the squares around the king are blocked by its friendly pieces
        if all(self.is_blocked(i) for i in available_squares):
            print('Smothered mate')
    
    def suffocation_and_pillsburys(self, available_squares, square):
        # If there is 2 squares that is not blocked by the king's own pieces and those 2 squares are attacked by the same piece
        # This algorithm checks the suffocation mate (with knight) and Pillsbury's mate (with rook)
        squares_free = []
        pillsburys = False
        for i in available_squares:
            if not self.is_blocked(i):
                if len(squares_free) > 2:
                # found too many free squares
                    continue
                else:
                # found the first free square
                    squares_free.append(i)
        if str(self.board.piece_at(square)).upper() == 'N':
            if len(squares_free) == 1:
                print('Suffocation mate')
            elif len(squares_free) == 2 and (self.board.attackers(self.winner(), squares_free[0]) == self.board.attackers(self.winner(), squares_free[1])):
                print('Suffocation mate')
        elif str(self.board.piece_at(square)).upper() == 'R':
            if len(squares_free) <= 2:
                for i in squares_free:
                    for attacker in self.board.attackers(self.winner(), i):
                        if str(self.board.piece_at(attacker)) == 'B' and (i in self.board.attacks(attacker)):
                            # Prints multiple times
                            pillsburys = True

                if pillsburys:
                    print("Pillsbury's mate")
    
    def suffocation_corner(self, available_squares):
        # If there is only 1 square that is not blocked by the king's own pieces
        one_square_free = False
        for i in available_squares:
            if not self.is_blocked(i):
                if one_square_free:
                # found too many free squares
                    one_square_free = False
                else:
                # found the first free square
                    one_square_free = True
    # found zero or one True value
        if one_square_free:
            print('Suffocation mate')
        

    def back_rank(self, available_squares, square):
        # On a board, there are 2 realistic ways back ranks can happen (white checkmated on his side, and vice versa)
        if all(self.is_blocked(i) for i in available_squares[1:4]) and (available_squares[0] and available_squares[4] in self.board.attacks(square)):
            print('Back-rank mate')
        
    def back_rank_corner(self, available_squares, square):
        # Thre are 4 realistic ways back ranks with losing king on corner can happen
        if all(self.is_blocked(i) for i in available_squares[1:]) and (available_squares[0] in self.board.attacks(square)):
            print('Back-rank mate')

    def scholars(self, available_squares, queen_pos):
        # If the queen is on f7 or f2 and a bishop on c4 or c5 (white and black, respectively) is defending it
        if self.winner():
            if queen_pos == chess.F7 and str(self.board.piece_at(chess.C4)) == 'B':
                print("Scholar's mate")
        else:
            if queen_pos == chess.F2 and str(self.board.piece_at(chess.C5)) == 'B':
                print("Scholar's mate")

    def anastasias(self, available_squares):
        # If the king is blocked by one of his own pieces and the remaining squares are control by the knight and a rook in a particular manner
        squares_free = [available_squares[1], available_squares[3]]
        anastasias = False
        if self.board.attackers(self.winner(), squares_free[0]) == self.board.attackers(self.winner(), squares_free[0]):
            for i in squares_free:
                for attacker in self.board.attackers(self.winner(), i):
                    if str(self.board.piece_at(attacker)).upper() == 'N' and (squares_free[0] and squares_free[1] in self.board.attacks(attacker)):
                        print("Anastasia's mate")

    def anastasias_corner(self, available_squares):
        for attacker in self.board.attackers(self.winner(), available_squares[0]):
            if self.is_blocked(available_squares[1]) and str(self.board.piece_at(attacker)).upper() == 'N':
                print("Anastasia's mate")

    def arabian(self, available_squares, rook_pos):
        for attacker in self.board.attackers(self.winner(), rook_pos):
            if str(self.board.piece_at(attacker)).upper() == 'N' and chess.square_distance(self.board.king(not self.winner()), attacker) == 2:
                print('Arabian mate')

    def epaulette(self, available_squares, queen_pos):
        # If the losing king is blocked by 2 pieces each on each side and the queen is 2 squares away from him
        distance_king_queen = chess.square_distance(self.board.king(not self.winner()), queen_pos)
        
        if self.is_blocked(available_squares[0]) and self.is_blocked(available_squares[4]) and distance_king_queen == 2:
            print('Epaulette mate')
    
    def blind_swine(self, available_squares, square):
        only_one_square_blocked = False
        for i in available_squares:
            if self.is_blocked(i):
                if only_one_square_blocked:
                    only_one_square_blocked = False
                else:
                    only_one_square_blocked = True
    
        if self.is_blocked(available_squares[4]) and only_one_square_blocked:
            if (str(self.board.piece_at(available_squares[1])).upper() == 'R' and 
            (chess.square_file(square) == chess.square_file(available_squares[1])) or (chess.square_rank(square) == chess.square_rank(available_squares[1]))):
                print('Blind swine mate')

        elif self.is_blocked(available_squares[0]) and only_one_square_blocked:
            if (str(self.board.piece_at(available_squares[3])).upper() == 'R' and 
            (chess.square_file(square) == chess.square_file(available_squares[3])) or (chess.square_rank(square) == chess.square_rank(available_squares[3]))):
                print('Blind swine mate')

    def swallows_tail(self, available_squares, square):
        if ((self.is_blocked(available_squares[0]) and self.is_blocked(available_squares[2]) and square == available_squares[6]) or 
        (self.is_blocked(available_squares[2]) and self.is_blocked(available_squares[7]) and square == available_squares[3]) or 
        (self.is_blocked(available_squares[7]) and self.is_blocked(available_squares[5]) and square == available_squares[1]) or 
        (self.is_blocked(available_squares[5]) and self.is_blocked(available_squares[0]) and square == available_squares[4]) and 
        chess.square_distance(self.board.king(not self.winner()), square) == 1):
            print("Swallow's tail mate")

    def corner_and_morphys(self, available_squares, square):
        # This pattern takes care of the corner mate (given with knight) and Murphy's mate (given with bishop)
        if (self.is_blocked(available_squares[2])):
            for i in available_squares[1:]:
                for attacker in self.board.attackers(self.winner(), i):
                    if str(self.board.piece_at(attacker)).upper() == 'R' or str(self.board.piece_at(attacker)).upper() == 'Q':
                        if str(self.board.piece_at(square)).upper() == 'B':
                            print("Morphy's mate")
                        elif str(self.board.piece_at(square)).upper() == 'N':
                            print('Corner mate')

    def opera(self, available_squares, square):
        if square == available_squares[0] and self.is_blocked(available_squares[3]):
            for defender in self.board.attackers(self.winner(), available_squares[0]):
                if str(self.board.piece_at(defender)) == 'B':
                    print('Opera mate')
        elif square == available_squares[4] and self.is_blocked(available_squares[1]):
            for defender in self.board.attackers(self.winner(), available_squares[4]):
                if str(self.board.piece_at(defender)) == 'B':
                    print('Opera mate')

    def mayets(self, available_squares, square):
        if square == available_squares[0] and (self.is_blocked(available_squares[1]) or self.is_blocked(available_squares[2])):
            for defender in self.board.attackers(self.winner(), available_squares[0]):
                if str(self.board.piece_at(defender)) == 'B':
                    print("Mayet's mate")
        elif square == available_squares[4] and (self.is_blocked(available_squares[2]) or self.is_blocked(available_squares[3])):
            for defender in self.board.attackers(self.winner(), available_squares[0]):
                if str(self.board.piece_at(defender)) == 'B':
                    print("Mayet's mate")

    def mayets_corner(self, available_squares, square):
        if square == available_squares[0] and (self.is_blocked(available_squares[2]) or self.is_blocked(available_squares[1])):
            for defender in self.board.attackers(self.winner(), available_squares[0]):
                if str(self.board.piece_at(defender)) == 'B':
                    print("Mayet's mate")

    def damianos_and_max_langes(self, available_squares, square):
        if square == available_squares[1] or square == available_squares[3]:
            for defender in self.board.attackers(self.winner(), square):
                if (available_squares[1] or available_squares[3] in self.board.attacks(defender)):
                    if str(self.board.piece_at(defender)) == 'P':
                        print("Damiano's mate")
                    elif str(self.board.piece_at(defender)) == 'B':
                        print("Max Lange's mate")

    def damianos_bishop_and_lollis(self, available_squares, square):
        if square == available_squares[2]:
            for defender in self.board.attackers(self.winner(), available_squares[2]):
                if chess.square_distance(self.board.king(not self.winner), defender) == 2:
                    if str(self.board.piece_at(defender)).upper() == 'B':
                        print("Damiano's bishop mate")
                    elif str(self.board.piece_at(defender)).upper() == 'P':
                        print("Lolli's mate")

    def damianos_bishop_corner_and_lollis_corner(self, available_squares, square):
        possible_squares = [available_squares[0], available_squares[2]]

        for i in possible_squares:
            if square == i:
                for defender in self.board.attackers(self.winner(), i):
                    if chess.square_distance(self.board.king(not self.winner), defender) == 2:
                        if str(self.board.piece_at(defender)).upper() == 'B':
                            print("Damiano's bishop mate")
                        elif str(self.board.piece_at(defender)).upper() == 'P':
                            if ((chess.square_rank(square) == 6 and chess.square_rank(self.board.king(not self.winner())) == 7) or 
                            (chess.square_rank(square) == 1 and chess.square_rank(self.board.king(not self.winner())) == 0)):
                                print("Lolli's mate")
    
    def box(self, available_squares):
        if (available_squares[1] and available_squares[2] and available_squares[3]) in self.board.attacks(self.board.king(self.winner())):
            print('Box mate')
    
    def box_corner(self, available_squares, square):
        if chess.square_file(square) == 0 or chess.square_file(square) == 7:
            if (available_squares[1] and available_squares[2]) in self.board.attacks(self.board.king(self.winner())):
                print('Box mate')
        elif chess.square_rank(square) == 0 or chess.square_rank(square) == 7:
            if (available_squares[0] and available_squares[1]) in self.board.attacks(self.board.king(self.winner())):
                print('Box mate')


    def queen_and_king(self, available_squares, square):
        if (square in self.surrounding_squares(self.board.king(self.winner()))) and (square in available_squares[1:3]):
            print('Queen and king mate')

    def queen_and_king_corner(self, square):
        if (square in self.surrounding_squares(self.board.king(self.winner()))):
            print('Queen and king mate')

    def grecos(self, available_squares, square):
        if self.is_blocked(available_squares[1]):
            if chess.square_file(square) == 0 or chess.square_file(square) == 7:
                for attacker in self.board.attackers(self.winner(), available_squares[0]):
                    if str(self.board.piece_at(attacker)) == 'B':
                        print("Greco's mate")
            elif chess.square_rank(square) == 0 or chess.square_rank(square) == 7:
                for attacker in self.board.attackers(self.winner(), available_squares[2]):
                    if str(self.board.piece_at(attacker)) == 'B':
                        print("Greco's mate")

    def dovetail(self, available_squares, square):
        if ((self.is_blocked(available_squares[1]) and self.is_blocked(available_squares[3]) and square == available_squares[7]) or
        (self.is_blocked(available_squares[1]) and self.is_blocked(available_squares[4]) and square == available_squares[5]) or
        (self.is_blocked(available_squares[4]) and self.is_blocked(available_squares[6]) and square == available_squares[0]) or
        (self.is_blocked(available_squares[6]) and self.is_blocked(available_squares[3]) and square == available_squares[2])):
            print('Dovetail mate')

    def dovetail_bishop(self, available_squares, square):
        if square == available_squares[7]:
            for attacker in self.board.attackers(self.winner(), available_squares[1]):
                if available_squares[3] in self.board.attacks(attacker) and str(self.board.piece_at(attacker)) == 'B':
                    print('Dovetail bishop mate')
        elif square == available_squares[5]:
            for attacker in self.board.attackers(self.winner(), available_squares[1]):
                if available_squares[4] in self.board.attacks(attacker) and str(self.board.piece_at(attacker)) == 'B':
                    print('Dovetail bishop mate')
        elif square == available_squares[0]:
            for attacker in self.board.attackers(self.winner(), available_squares[4]):
                if available_squares[6] in self.board.attacks(attacker) and str(self.board.piece_at(attacker)) == 'B':
                    print('Dovetail bishop mate')
        elif square == available_squares[2]:
            for attacker in self.board.attackers(self.winner(), available_squares[6]):
                if available_squares[3] in self.board.attacks(attacker) and str(self.board.piece_at(attacker)) == 'B':
                    print('Dovetail bishop mate')

    def kill_box(self, available_squares, square):
        if square == available_squares[0]:  
            for defender in self.board.attackers(self.winner(), square):
                if (str(self.board.piece_at(defender)).upper() == 'Q' and chess.square_distance(square, defender) == 2 and 
                (available_squares[3] and available_squares[4] in self.board.attacks(defender))):
                    print('Kill box mate')

        elif square == available_squares[4]:
            for defender in self.board.attackers(self.winner(), square):
                if (str(self.board.piece_at(defender)).upper() == 'Q' and chess.square_distance(square, defender) == 2 and 
                (available_squares[0] and available_squares[1] in self.board.attacks(defender))):
                    print('Kill box mate')
    
    def triangle(self, available_squares, square):
        if square == available_squares[1]:
            for defender in self.board.attackers(self.winner(), square):
                if (str(self.board.piece_at(defender)).upper() == 'R' and chess.square_distance(square, defender) == 2 and 
                (available_squares[2] and available_squares[4] in self.board.attacks(defender))):
                    print('Triangle mate')

        elif square == available_squares[3]:
            for defender in self.board.attackers(self.winner(), square):
                if (str(self.board.piece_at(defender)).upper() == 'R' and chess.square_distance(square, defender) == 2 and 
                (available_squares[2] and available_squares[0] in self.board.attacks(defender))):
                    print('Triangle mate')
    
    def triangle_center(self, available_squares, square):
        for defender in self.board.attackers(self.winner(), square):
                if str(self.board.piece_at(defender)).upper() == 'R' and chess.square_distance(square, defender) == 2 and (defender in available_squares):
                    if self.is_blocked(available_squares[1]) or self.is_blocked(available_squares[3]) or self.is_blocked(available_squares[4]) or self.is_blocked(available_squares[6]):
                        print('Triangle mate')

    def balestra(self, available_squares, square):
        for attacker in self.board.attackers(self.winner(), available_squares[2]):
            if (chess.square_distance(square, self.board.king(not self.winner)) == 2 and 
            chess.square_distance(attacker, self.board.king(not self.winner)) == 2 and chess.square_distance(square, attacker) == 3):
                print('Balestra mate')

    def hook(self, available_squares, square):
        for defender in self.board.attackers(self.winner(), square):
            if str(self.board.piece_at(defender)).upper() == 'N':
                if ((square == available_squares[1] and (defender == available_squares[5] or defender == available_squares[7])) or
                (square == available_squares[3] and (defender == available_squares[2] or defender == available_squares[7])) or 
                (square == available_squares[6] and (defender == available_squares[0] or defender == available_squares[2])) or
                (square == available_squares[4] and (defender == available_squares[0] or defender == available_squares[5]))):
                    print('Hook mate')

    def hook_side(self, available_squares, square):
        if square == available_squares[0]:
            for defender in self.board.attackers(self.winner(), square):
                if str(self.board.piece_at(defender)).upper() == 'N' and defender == available_squares[3]:
                    print('Hook mate')
        elif square == available_squares[4]:
            for defender in self.board.attackers(self.winner(), square):
                if str(self.board.piece_at(defender)).upper() == 'N' and defender == available_squares[1]:
                    print('Hook mate')

    def anderssens(self, available_squares, square):
        if (str(self.board.piece_at(available_squares[2])).upper() == 'P' and self.board.color_at(available_squares[2]) == self.winner() and 
        (chess.square_rank(square) == 0 or chess.square_rank(square) == 7) and (square == available_squares[0] or square == available_squares[4])):
            print("Anderssen's mate")

    def double_bishop(self, available_squares, square):
        pass
    
    def blackburnes_1(self, available_squares, square):
        if square == available_squares[1] and self.is_blocked(available_squares[4]):
            pass
        elif square == available_squares[3] and self.is_blocked(available_squares[0]):
            pass
    
    def blackburnes_2(self, available_squares, square):
        pass

    def king_and_two_bishops(self, available_squares, square):
        pass


    def ladder(self, available_squares, square):
        # If all the remaining squares are attacked by a queen or a rook
        ladder = False

        checkmater_file = 0
        checkmater_rank = 0
        attacker_file = 0
        attacker_rank = 0

        for i in available_squares[1:4]:
            for attacker in self.board.attackers(self.winner(), i):       
                if square != i and (str(self.board.piece_at(attacker)).upper() == 'Q' or str(self.board.piece_at(attacker)).upper() == 'R'):
                    # For some reason, it would print 'Ladder mate' 3 times. This just bypasses it.
                    attacker_file = chess.square_file(attacker)
                    attacker_rank = chess.square_rank(attacker)
                    ladder = True

        if (available_squares[0] and available_squares[4]) in self.board.attacks(square):
            checkmater_file = chess.square_file(square)
            checkmater_rank = chess.square_rank(square)
            ladder = True
        else:
            ladder = False

        
        if (((checkmater_file == 0 and attacker_file == 1) or (checkmater_file == 7 and attacker_file == 6)) or 
        ((checkmater_rank == 0 and attacker_rank == 1) or (checkmater_rank == 7 and attacker_rank == 6))):
            if ladder:
                print('Ladder mate')
    
    def ladder_corner(self, available_squares, square):
        # 8 plausible ways to get ladder mated on a corner
        ladder = False

        if chess.square_file(square) == 0 or chess.square_file(square) == 7:
            for i in available_squares[:2]:
                for attacker in self.board.attackers(self.winner(), i):
                    if (square != i and (str(self.board.piece_at(attacker)).upper() == 'Q' or str(self.board.piece_at(attacker)).upper() == 'R') and 
                    (chess.square_file(attacker) == 1 or chess.square_file(attacker) == 6)):
                        ladder = True

        elif chess.square_rank(square) == 0 or chess.square_rank(square) == 7:
            for i in available_squares[1:]:
                for attacker in self.board.attackers(self.winner(), i):
                    if (square != i and (str(self.board.piece_at(attacker)).upper() == 'Q' or str(self.board.piece_at(attacker)).upper() == 'R') and 
                    (chess.square_rank(attacker) == 1 or chess.square_rank(attacker) == 6)):
                        ladder = True

        # Prevents from printing it out multiple times
        if ladder:
            print('Ladder mate')

    def bishop_and_knight(self, available_squares, square):
        if all(not self.is_blocked(i) for i in available_squares):
            pass
    
    def bishop_and_knight_corner(self, available_squares, squares):
        if all(not self.is_blocked(i) for i in available_squares):
            pass
    
    def find_checkmate_pattern(self):
        losing_side = not self.winner()
        opponent_king = self.board.king(losing_side)

        if self.board.is_checkmate:
            print(self.board)
            for square in self.board.checkers():
                if len(self.board.checkers()) > 1:
                    print('Double checkmate')
                    break
                try:
                    if ((chess.square_file(opponent_king) == 0 or chess.square_file(opponent_king) == 7) and 
                    (chess.square_rank(opponent_king) == 0 or chess.square_rank(opponent_king) == 7)): # Corner

                        available_squares = self.king_on_corner(opponent_king)
                        
                        if str(self.board.piece_at(square)).upper() == 'Q':
                            print(self.get_full_name('Q'), 'gave checkmate')

                            self.back_rank_corner(available_squares, square)
                            self.damianos_bishop_corner_and_lollis_corner(available_squares, square)
                            self.queen_and_king_corner(square)
                            self.box_corner(available_squares)
                            self.grecos(available_squares, square)
                            self.ladder_corner(available_squares, square)

                        elif str(self.board.piece_at(square)).upper() == 'R':
                            print(self.get_full_name('R'), 'gave checkmate')

                            self.back_rank_corner(available_squares, square)
                            self.anderssens(available_squares, square)
                            self.anastasias_corner(available_squares)
                            self.arabian(available_squares, square)
                            self.mayets_corner(available_squares, square)
                            self.box_corner(available_squares)
                            self.grecos(available_squares, square)
                            self.ladder_corner(available_squares, square)
            
                        elif str(self.board.piece_at(square)).upper() == 'B':
                            print(self.get_full_name('B'), 'gave checkmate')

                            self.corner_and_morphys(available_squares, square)

                        elif str(self.board.piece_at(square)).upper() == 'N':
                            print(self.get_full_name('N'), 'gave checkmate')

                            self.smothered(available_squares)
                            self.suffocation_corner(available_squares)
                            self.corner_and_morphys(available_squares, square)
                            
                        elif str(self.board.piece_at(square)).upper() == 'P':
                            print(self.get_full_name('P'), 'checkmate!')

                    elif (chess.square_file(opponent_king) != 0 and chess.square_file(opponent_king) != 7 and 
                    chess.square_rank(opponent_king) != 0 and chess.square_rank(opponent_king) != 7): # Center
                        available_squares = self.surrounding_squares(opponent_king)

                        if str(self.board.piece_at(square)).upper() == 'Q':
                            print(self.get_full_name('Q'), 'gave checkmate')

                            self.swallows_tail(available_squares, square)
                            self.dovetail(available_squares, square)
                            self.dovetail_bishop(available_squares, square)
                            self.triangle_center(available_squares, square)

                        elif str(self.board.piece_at(square)).upper() == 'R':
                            print(self.get_full_name('R'), 'gave checkmate')

                            self.hook(available_squares, square)
                            self.blind_swine(available_squares)
                            
            
                        elif str(self.board.piece_at(square)).upper() == 'B':
                            print(self.get_full_name('B'), 'gave checkmate')

                        elif str(self.board.piece_at(square)).upper() == 'N':
                            print(self.get_full_name('N'), 'gave checkmate')

                        elif str(self.board.piece_at(square)).upper() == 'P':
                            print(self.get_full_name('P'), 'checkmate!')
                    
                    else: # Side
                        available_squares = self.king_on_side(opponent_king)

                        if str(self.board.piece_at(square)).upper() == 'Q':
                            print(self.get_full_name('Q'), 'gave checkmate')

                            self.scholars(available_squares, square)
                            self.back_rank(available_squares, square)
                            self.epaulette(available_squares, square)
                            self.damianos_bishop_and_lollis(available_squares, square)
                            self.damianos_and_max_langes(available_squares, square)
                            self.queen_and_king(available_squares, square)
                            self.box(available_squares)
                            self.ladder(available_squares, square)

                        elif str(self.board.piece_at(square)).upper() == 'R':
                            print(self.get_full_name('R'), 'gave checkmate')

                            self.ladder(available_squares, square)
                            
                            self.suffocation_and_pillsburys(available_squares, square)
                            self.blind_swine(available_squares, square)
                            self.back_rank(available_squares, square)
                            self.anastasias(available_squares)
                            self.opera(available_squares, square)
                            self.kill_box(available_squares, square)   
                            self.box(available_squares)
                            self.anderssens(available_squares, square)
                            self.hook_side(available_squares, square)
            
                        elif str(self.board.piece_at(square)).upper() == 'B':
                            print(self.get_full_name('B'), 'gave checkmate')

                            self.balestra(available_squares, square)

                        elif str(self.board.piece_at(square)).upper() == 'N':
                            print(self.get_full_name('N'), 'gave checkmate')

                            self.smothered(available_squares)
                            self.suffocation_and_pillsburys(available_squares)

                        elif str(self.board.piece_at(square)).upper() == 'P':
                            print(self.get_full_name('P'), 'checkmate!')

                except TypeError:
                    # 100% error proof
                    pass
'''
# Confirmed list of extra jumps available
def confirm_extra_jump(currState, x1, y1, x2, y2):
    self.board.show()
    print 'You can jump again! Choose a space to jump to or choose the space of your own piece to stay still:'
    destination = raw_input('')
    
    # parses player input
    x2 = letter_number_parse(destination)[0]
    y2 = letter_number_parse(destination)[1]
    
    piece = self.board.get_space(x1, y1)
    
    if isinstance(piece, p1_piece):
        player = self.p1
    else:
        player = self.p2
    
    # if the player chooses the same spot, we interpret that as instruction to stay still
    if x2 == x1 and y2 == y1:
        return
    # otherwise we check if the move is a legal jump and make the move if it is
    elif piece.is_legal_diagonal_jump(x2, y2) and player.is_legal_move(self.board, x1, y1, x2, y2)[0]:
        self.make_move([x1, y1, x2, y2])
    # if the move isn't legal, we tell the player and let them make another input
    else:
        print 'Illegal move: You must select either a legal tile to jump to or the tile of your own piece'
        time.sleep(1.75)
        self.confirm_extra_jump(x1, y1)
'''


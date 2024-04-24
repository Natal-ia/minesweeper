## =========================================================================
## @author Leonardo Florez-Valencia (florez-l@javeriana.edu.co)
## =========================================================================

import heapq, random, sys
from MineSweeperBoard import *

'''
'''
class Player_H1:

  '''
  '''
  def __init__( self, w, h, m ):
    self.m_Width = w
    self.m_Height = h
    self.m_NumberOfMines = m
    self.m_Mines = [ [ False for j in range( h ) ] for i in range( w ) ]
    self.m_Count = [ [ 9 for j in range( h ) ] for i in range( w ) ]
    self.m_Probabilities = []
    p = float( m ) / float( w * h )
    for i in range( w ):
      for j in range( h ):
        self.m_Probabilities += [ ( p, ( i, j ) ) ]
      # end for
    # end for
    random.shuffle( self.m_Probabilities )
  # end def

  '''
  '''
  def next_play( self ):
    p, ( i, j ) = heapq.heappop( self.m_Probabilities )
    while self.m_Mines[ i ][ j ] or self.m_Count[ i ][ j ] < 9:
      p, ( i, j ) = heapq.heappop( self.m_Probabilities )
    # end while
    self.m_Play = ( i, j )
    return self.m_Play
  # end def

  '''
  '''
  def update_cell( self, i, j ):
    m = 9
    n = 8
    for x in range( -1, 2 ):
      for y in range( -1, 2 ):
        if x != 0 or y != 0:
          nx = i + x
          ny = j + y
          if nx >= 0 and nx < self.m_Width and ny >= 0 and ny < self.m_Height:
            if self.m_Count[ nx ][ ny ] < m:
              m = self.m_Count[ nx ][ ny ]
            # end if
            if self.m_Count[ nx ][ ny ] < 9:
              n -= 1
            # end if
          # end if
        else:
          n -= 1
        # end if
      # end for
    # end for

    if n > 0:
      p = float( m ) / float( n )
    else:
      p = float( 0 )
    # end if

    if p < 1:
      heapq.heappush( self.m_Probabilities, ( p, ( i, j ) ) )
    else:
      self.m_Mines[ i ][ j ] = True
      self.m_NumberOfMines -= 1
    # end if
  # end def

  '''
  '''
  def update( self, n ):
    if n < 9:
      ( i, j ) = self.m_Play
      self.m_Count[ i ][ j ] = n
      for x in range( -1, 2 ):
        for y in range( -1, 2 ):
          if x != 0 or y != 0:
            nx = i + x
            ny = j + y
            if nx >= 0 and nx < self.m_Width and ny >= 0 and ny < self.m_Height:
              self.update_cell( nx, ny )
            # end if
          # end if
        # end for
      # end for
    # end if
  # end def

# end class

# --------------------------------------------------------------------------
if len( sys.argv ) < 4:
  print( "Usage: python3", sys.argv[ 0 ], "width height mines" )
  sys.exit( 1 )
# end if
w = int( sys.argv[ 1 ] )
h = int( sys.argv[ 2 ] )
m = int( sys.argv[ 3 ] )
board = MineSweeperBoard( w, h, m )

# Prepare H1 player
player = Player_H1( w, h, m )

# Play!
while not board.have_won( ) and not board.have_lose( ):

  # Click best cell
  ( i, j ) = player.next_play( )
  print( board )
  input(
    'Next click on ('
    +
    chr( i + ord( 'A' ) )
    +
    ','
    +
    chr( j + ord( 'A' ) ) + ')'
    )

  # Update decisions
  player.update( board.click( i, j ) )

# end while

print( board )
if board.have_won( ):
  print( "You won!" )
elif board.have_lose( ):
  print( "You lose :-(" )
# end if

## eof - Player_H1.py

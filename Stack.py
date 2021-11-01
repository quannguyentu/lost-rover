class Stack :
  def __init__( self ):
    self._top = None
    self._size = 0

  def is_empty( self ):
    return self._top is None

  def __len__( self ):
    return self._size

  def peek( self ):
    assert not self.is_empty(), "Cannot peek at an empty stack"
    return self._top.item

  def pop( self ):
      assert not self.is_empty(), "Cannot pop from an empty stack"
      node = self._top
      self._top = self._top.next
      self._size -= 1
      return node.item

  def push( self, item ):
      self._top = _StackNode( item, self._top )
      self._size += 1



# The private storage class for creating stack nodes.
class _StackNode :
  def __init__( self, item, link=None ) :
    self.item = item
    self.next = link

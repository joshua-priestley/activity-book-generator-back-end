from math import sqrt, floor, log2, pow
from random import shuffle, randint
import string

MAX_GRID_LENGTH = 15
MAX_ATTEMPTS = 100

directions = [(-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1)]

def compute_grid_length(min_length, total):
  # Setup the array for the binary search
  squares = []
  for i in range(min_length, MAX_GRID_LENGTH + 1):
    squares.append(i * i)
  
  # Binary search the length that fits all the words
  step = int(pow(2, floor(log2(MAX_GRID_LENGTH - min_length + 1))))
  index = 0

  while step > 0:
    temp = index + step
    if temp < len(squares) and squares[temp] < total:
      index = temp
    step //= 2

  return int(sqrt(squares[index + 1]))

def compute_constraints(words, hidden_message):
  lengths = list(map(len, words))
  total_cells = sum(lengths)
  
  if hidden_message != None:
    total_cells += len(hidden_message)

  return (max(lengths), total_cells)


def generate(words, hidden_message = None):
  # We are expecting a list of words
  assert(isinstance(words, list))

  print("The words you have to find are: ", end='')
  print(*words, sep=", ")

  if hidden_message != None:
    hidden_words = hidden_message.split()
    hangman_text = ""
    for i in range(len(hidden_words)):
      for _ in range(len(hidden_words[i])):
        hangman_text += '_ '
      hangman_text += '  '
    hangman_text = hangman_text.strip()
    hidden_message = hidden_message.lower().translate({ord(c): None for c in string.whitespace})

  min_length, total_cells = compute_constraints(words, hidden_message)

  global l, grid_size
  l = compute_grid_length(min_length, total_cells)
  grid_size = l * l
  place_words(words)
  place_hidden_message(hidden_message)
  add_random_letters()
  print_board()
  print("Complete the secret message in the space below:")
  print(hangman_text + '\n')

ALPHABET_SIZE = 26

def add_random_letters():
  global cells
  for i in range(l):
    for j in range(l):
      if cells[i][j] == '':
        cells[i][j] = chr(ord('a') + randint(0, ALPHABET_SIZE - 1))


def print_board():
  print("\n    ", end='')
  for i in range(l):
    print(" %c " % str(i), end='')
  print("\n")

  for i in range(l):
    print("{0}   ".format(i), end='')
    for j in range(l):
      print(" %c " % cells[i][j], end='')

    print()
  print()


def place_hidden_message(msg):
  if msg == None:
    return

  global cells

  msg_len = len(msg)
  cnt = 0
  for i in range(l):
    for j in range(l):
      if cells[i][j] == '':
        cells[i][j] = msg[cnt]
        cnt += 1
        if cnt == msg_len:
          return

def place_words(words):
  global l, grid_size
  while True:
    attempts = 0
    while attempts < MAX_ATTEMPTS:
      attempts += 1
      global cells
      cells = [['' for _ in range(l)] for _ in range(l)]
      shuffle(words)
      success = True

      for word in words:
        if not try_place_word(word):
          # We failed to place the current word on the grid, start fresh
          success = False
          break

      # If we managed to find a solution we return it
      if success:
        return cells
      # Otherwise we try again
    
    # If we could not fill this grid, we try a bigger one
    l += 1
    grid_size = l * l

def try_place_word(word):
  rand_pos = randint(0, grid_size - 1)
  rand_dir = randint(0, len(directions) - 1)

  for i in range(len(directions)):
    dir = directions[(i + rand_dir) % len(directions)]

    for j in range(grid_size):
      pos = (j + rand_pos) % grid_size
      if try_position(word, pos, dir):
        return True

  return False


def try_position(word, pos, dir):
  r = pos // l
  c = pos % l
  
  # Check bounds
  endr = r + dir[0] * len(word)
  endc = c + dir[1] * len(word)
  if endr < 0 or endr >= l or endc < 0 or endc >= l:
    return False

  rr = r
  cc = c
  # Check we can add the word without changing any letter already written
  for i in range(len(word)):
    if cells[rr][cc] != '' and cells[rr][cc] != word[i]:
      return False
    rr += dir[0]
    cc += dir[1]
  
  for i in range(len(word)):
    cells[r][c] = word[i]
    r += dir[0]
    c += dir[1]
  
  return True


if __name__ == "__main__":
  generate(["squirrel", "wolf", "bear", "lion", "tiger", "tortoise"], "We love animals")

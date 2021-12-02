from math import sqrt, floor, log2, pow
from random import shuffle, randint
import string

import sys

from flask import Blueprint, jsonify, render_template, request

MAX_GRID_LENGTH = 20
MAX_ATTEMPTS = 100

directions = [(-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1)]

bp = Blueprint("word-search", __name__, url_prefix="/activities/word-search")

@bp.route("/state")
def get_state():
  """Returns internal word search state from provided options"""

  hidden_message = request.args.get("hidden-message")
  
  # Ignore hidden message if empty string
  hidden_message = hidden_message if hidden_message else None

  # Get the words to be included in the word search
  words = request.args.get("words").split(",")

  # Assert that the list of words is non empty
  assert(words != [])

  # Concatenate terms made of multiple words
  copy_words = list(map(lambda w: w.replace(" ", ""), words))

  # Make sure no word is longer than the maximum size of the square grid
  # TODO: Extend the grid to rectangular shapes
  assert(list(filter(lambda w: len(w) > MAX_GRID_LENGTH, copy_words)) == [])

  cells, hangman_words, word_positions = generate(copy_words, hidden_message)
  description = [
    "Some words have been hidden in this square board. You can find them written in a row, column "
    "or diagonally, from left to right or viceversa. ",
    f"The words you are looking for are: {', '.join(words)}.",
  ]
  if hidden_message:
    description.append(
      "Find all these words and circle them on the board. Once you're done, look at the unused letters "
      "and find the hidden message. In order to do this, keep in mind that each 2 consecutive letters composing the hidden "
      "message have the same number of unused letters between them."
    )
  return {
    "description": description,
    "cells": cells,
    "words": words,
    "hangman_words": hangman_words,
    "word_positions": word_positions
  }

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

  assert(words != [])

  lengths = list(map(len, words))
  
  # There should be no empty words
  assert(0 not in lengths)

  total_cells = sum(lengths)
  
  if hidden_message != None:
    total_cells += len(hidden_message)

  return (max(lengths), total_cells)


def generate(words, hidden_message = None):
  # We are expecting a list of words
  assert(isinstance(words, list))

  print("The words you have to find are: ", end='')
  print(*words, sep=", ")
  print()

  global hidden_msg_length

  if hidden_message != None:
    hidden_words = hidden_message.split()
    hangman_words = ["" for _ in hidden_words]
    for i in range(len(hidden_words)):
      for _ in range(len(hidden_words[i])):
        hangman_words[i] += '_ '
      hangman_words[i] = hangman_words[i].strip()
    hidden_message = hidden_message.lower().translate({ord(c): None for c in string.whitespace})
    hidden_msg_length = len(hidden_message)
  else:
    hidden_msg_length = 0
    hidden_words = hangman_words = []

  hangman_text = '   '.join(hangman_words)

  min_length, total_cells = compute_constraints(words, hidden_message)

  global l, grid_size
  l = compute_grid_length(min_length, total_cells)
  grid_size = l * l
  place_words(words)
  place_hidden_message(hidden_message)
  add_random_letters()
  # print_board()
  if hidden_message != None:
    print("Complete the secret message in the space below:")
    print(hangman_text + '\n')

  print("\n The word positions are:")
  for word in words:
    print(word + ": " + str(word_positions[word]))
  print()

  return (cells, hangman_words, word_positions)

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

  letter_gap = remaining // hidden_msg_length - 1
  msg_len = len(msg)
  cnt = crt_gap = 0
  for i in range(l):
    for j in range(l):
      if cells[i][j] == '':
        if crt_gap == letter_gap:
          cells[i][j] = msg[cnt]
          cnt += 1
          crt_gap = 0
          if cnt == msg_len:
            return
        else:
          crt_gap += 1

def place_words(words):
  global l, grid_size
  while True:
    attempts = 0
    while attempts < MAX_ATTEMPTS:
      global cells, remaining, word_positions
      cells = [['' for _ in range(l)] for _ in range(l)]
      remaining = grid_size
      word_positions = {}
      attempts += 1
      shuffle(words)
      success = True

      for word in words:
        if not try_place_word(word):
          # We failed to place the current word on the grid, start fresh
          success = False
          break

      # If we managed to find a solution we return it
      if success and remaining >= hidden_msg_length:
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

  global remaining, word_positions
  word_positions[word] = ((r, c), (rr - dir[0], cc-dir[1]))

  for i in range(len(word)):
    if cells[r][c] == '':
      cells[r][c] = word[i]
      remaining -= 1
    r += dir[0]
    c += dir[1]
  
  return True

def generate_html(data):
  return render_template("word-search.html", words=data["words"], cells=data["cells"], 
    hangman_words=data["hangman_words"])


if __name__ == "__main__":
  # generate_html(None, None)
  generate(["squirrel", "wolf", "bear", "lion", "tiger", "tortoise"], "We love animals")
  
# minesweeper_bot
An automatic minesweeper solver, for the classic version of minesweeper (included in the repository)
Solves the advanced mode.

Uses template matching to build the current game map.
Only uses the two basic rules of solving minesweeper 

  => if number of flags = square's numer : 
      all others tiles are not bombs
  => if the amount of empty squares + flags = square's number : 
      all other tiles are bombs

Has a few more functions, such as clicking the most probable square when no other move is found, check finish, save the end game screen after each match.

Uses pyautogui to control the mouse, numpy to model the field, cv2 to make the template matching, plus some standart python libraries.

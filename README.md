Chess AI Code

This was written as a final project for the Oxford class, Artificial Intelligence.
It is an implementation of fail-safe alpha-beta pruning (ABP) as seen in the Oxford notes,
and incorporates opening book compatibility, an endgame Syzygy tablebase, and quiescence search
so that only quiet (non-quiescent) positions are evaluated. There is a novel heuristic incorporated.

Note that the ABP implementation inside AlphaBeta.py is not chess-specific and only requires an implementation
of the methods in State.py and a compatible heuristic for any given two-player game. The default search depth is 3 (because this is Python and I have a MacBook) not counting the depth of the quiescence. 

The files 3-4-5 and Prodeo.bin contain the endgame tablebase and the opening book, respectively. 

To play a game, install the amazing python-chess package and simply run PlayGame.py; there will be a text-based interface. Here is an example of a game played:

1. d4 c6 2. c4 d5 3. Nc3 dxc4 4. e4 b5 5. a4 b4 6. Na2 Nf6 7. e5 Nd5 8. Bxc4 e6 9. Nf3 Be7 10. Bd2 a5 11. Nc1 Nd7
12. Nb3 Bb7 13. O-O h6 14. Qc2 Rc8 15. Qe4 c5 16. Rfc1 Kf8 17. Qe2 g5 18. Nxc5 Nxc5 19. dxc5 Bxc5 20. Ba6 Bxa6 
21. Qxa6 g4 22. Nd4 Nb6 23. Nb3 Nd7 24. Qxa5 Qxa5 25. Nxa5 Nb6 26. Rxc5 Rxc5 27. Bxb4 Nd7 28. Bxc5+ Nxc5 29. b4 Nd3 
30. Nc6 Ke8 31. b5 f6 32. exf6 e5 33. Rd1 e4 34. f7+ Kxf7 35. Nd4 Kf6 36. b6 Rd8 37. Rxd3 exd3 38. Nb5 d2 39. h3 d1=Q+ 
40. Kh2 Qxa4 41. Nc3 Qc6 42. Ne2 Qxb6 43. hxg4 Qxf2 44. Ng3 Qf4 45. Kh3 Rd3 46. g5+ Ke7 47. Kh2 Qxg3+ 48. Kh1 Kf8 
49. Kg1 Re3 50. Kh1 Kg8 51. Kg1 Kh8 52. Kh1 Kg8 53. Kg1 Qe1+ 54. Kh2 Qh4+ 55. Kg1 Qg3 56. Kh1 Kh8 57. Kg1 Kg8 
58. Kh1 Qe1+ 59. Kh2 Re4 60. g3 Re2+ 61. Kh3 Rh2+ 62. Kxh2 hxg5 63. Kh3 Qf2 64. Kg4 Kh8 65. Kh5 Kg8 66. Kg4 Kh8 
67. Kh5 Qf5 68. Kh6 Kg8 69. Kh5 Kh7 70. g4 Qg6# 0-1

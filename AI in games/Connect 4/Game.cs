using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Connect_4
{
    internal class Game
    {
        public
        Board Board;
        RandomPlayer Player1;
        RandomPlayer Player2;

        public Game()
        {
            Board = new();
            Player1 = new();
            Player2 = new();
        }

        public void Play()
        {
            int move;

            while (MoveIsPossible())
            {
                move = Player1.MakeMove(Board.Fields);
                Board.UpdateBoard(move, 'X');
                Board.PrintBoard();
                Console.ReadKey();
                Console.Clear();    

                move = Player2.MakeMove(Board.Fields);
                Board.UpdateBoard(move, 'O');
                Board.PrintBoard();
                Console.ReadKey();
                Console.Clear();
            }
        }

        private bool MoveIsPossible()
        {
            for (int x = 0; x <= 6; x++)
            {
                if (Board.Fields[x, 5] == '|')
                {
                    return true;
                }
            }
            return false;
        }
    }
}

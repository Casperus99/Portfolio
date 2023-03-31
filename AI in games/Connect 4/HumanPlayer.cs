using System;
using System.Collections.Generic;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Connect_4
{
    internal class HumanPlayer : Player
    {
        int colour;

        public HumanPlayer(int Incolour)
        {
            colour = Incolour;
        }

        override public int MakeMove(Board board)
        {
            int Move;
            while (true)
            {
                board.PrintBoard();
                Move = Int32.Parse(Console.ReadLine());
                Console.Clear();
                if (board.Fields[Move-1, 5] == 0)
                {
                    board.UpdateBoard(Move-1, colour);
                    return Move-1;
                }
                else
                {
                    Console.WriteLine("This column is unavailable");
                }
            }
        }
    }
}

using System;
using System.Collections.Generic;
using System.ComponentModel.DataAnnotations.Schema;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Connect_4
{
    internal class RandomPlayer : Player
    {
        Random rnd = new();
        int colour;

        public RandomPlayer(int Incolour)
        {
            colour = Incolour;
        }

        override public int MakeMove(Board board)
        {
            int Move;
            while (true)
            {
                Move = rnd.Next(0, 7);
                if (board.Fields[Move, 5] == 0)
                {
                    board.UpdateBoard(Move, colour);
                    return Move;
                }
            }
        }
    }
}

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

        override public int MakeMove(char[,] fields)
        {
            int Move;
            while (true)
            {
                Move = rnd.Next(0, 7);
                if (fields[Move, 5] == '|')
                {
                    return Move;
                }
            }
        }
    }
}

using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Connect_4
{
    internal class HumanPlayer : Player
    {
        override public int MakeMove(char[,] fields)
        {
            int Move;
            while (true)
            {
                PrintFields(fields);
                Move = Int32.Parse(Console.ReadLine());
                Console.Clear();
                if (fields[Move-1, 5] == '|')
                {
                    return Move-1;
                }
                else
                {
                    Console.WriteLine("This column is unavailable");
                }
            }
        }

        public void PrintFields(char[,]  fields)
        {
            for (int y = 5; y >= 0; y--)
            {
                string row = " ";
                for (int x = 0; x <= 6; x++)
                {
                    row += fields[x, y] + " ";
                }
                Console.WriteLine(row);
            }
            Console.WriteLine(" 1 2 3 4 5 6 7");
        }
    }
}

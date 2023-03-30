using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Connect_4
{
    internal class Board
    {
        public char[,] Fields { get; set; }

        public Board()
        {
            Fields = new char[7, 6];
            ResetBoard();
        }

        public void ResetBoard()
        {
            for (int x = 0; x <= 6; x++)
            {
                for (int y = 0; y <= 5; y++)
                {
                    Fields[x, y] = '|';
                }
            }
        }

        public void PrintBoard()
        {
            for (int y = 5; y >= 0; y--)
            {
                string row = " ";
                for (int x = 0; x <= 6; x++)
                {
                    row += Fields[x, y] + " ";
                }
                Console.WriteLine(row);
            }
        }

        public void UpdateBoard(int column, char colour)
        {
            for (int y = 0; y <= 5; y++)
            {
                if (Fields[column, y] == '|')
                {
                    Fields[column, y] = colour;
                    break;
                }
            }
        }
    }
}

using System;
using System.Collections;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Connect_4
{
    internal class Board
    {
        public
        int[,] Fields { get; set; }
        int Evaluation { get; set; }
        IDictionary<string, int>[] OpenTerminals { get; set; }

        public Board()
            {
            Fields = new int[7, 6];
            OpenTerminals = new Dictionary<string, int>[2];
            OpenTerminals[0] = new Dictionary<string, int>();
            OpenTerminals[1] = new Dictionary<string, int>();
            Evaluation = 0;
            ResetBoard();
            }

        public void ResetBoard()
        {
            for (int x = 0; x <= 6; x++)
            {
                for (int y = 0; y <= 5; y++)
                {
                    Fields[x, y] = 0;
                }
            }
        }

        public void UpdateBoard(int column, int colour)
        {
            for (int y = 0; y <= 5; y++)
            {
                if (Fields[column, y] == 0)
                {
                    Fields[column, y] = colour;
                    Evaluate(column, y);
                    break;
                }
            }
        }

        public void Evaluate(int x_new, int y_new)
        {
            int[] Hrange = { 0, 0 };
            int colour = Fields[x_new, y_new];
            int terminalSum = 0;


            for (int i = -1; i <= 1; i+=2)
            {
                for (int x = 1; x <= 3; x++)
                {
                    if (x_new + x*i >= 0 && x_new + x*i <= 6)
                    {
                        if (Fields[x_new + x*i, y_new] != colour*(-1))
                        {
                            Hrange[SymmetryToTable(i)] += 1;
                        }
                        else { break; }
                    }
                    else { break; }
                }
            }
            if (Hrange[0] + Hrange[1] >= 3)
            {
                for (int x_left = Hrange[0]; -x_left <= Hrange[1] - 3; x_left--)
                {
                    int[] left = { x_new - x_left, y_new };
                    int[] right= { x_new - x_left + 3 , y_new };
                    try
                    {
                        OpenTerminals[SymmetryToTable(colour)].Add(EncodeTerminalState(left, right), 1);
                    }
                    catch
                    {
                        OpenTerminals[SymmetryToTable(colour)][EncodeTerminalState(left, right)] += 1;
                    }
                }
            }
        }

        public static string EncodeTerminalState(int[] begin, int[] end)
        {
            string code = begin[0].ToString() + begin[1].ToString() + end[0].ToString() + end[1].ToString();
            return code;
        }

        public static int SymmetryToTable(int i)
        {
            if (i == -1) { return 0; }
            else { return 1; }
        }

        public void PrintBoard()
        {
            for (int y = 5; y >= 0; y--)
            {
                string row = " ";
                for (int x = 0; x <= 6; x++)
                {
                    row += Decode(Fields[x, y]) + " ";
                }
                Console.WriteLine(row);
            }
            Console.WriteLine(" 1 2 3 4 5 6 7");
        }

        public char Decode(int code)
        {
            if (code == 0)
            {
                return '|';
            }
            else if (code == 1)
            {
                return 'X';
            }
            else
            {
                return 'O';
            }
        }
    }
}

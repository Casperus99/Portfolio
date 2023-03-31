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
        HumanPlayer Player2;

        public Game()
        {
            Board = new();
            Player1 = new(1);
            Player2 = new(-1);
        }

        public void Play()
        {
            while (true)
            {
                Player1.MakeMove(Board);
                if (Win(1))
                {
                    Console.WriteLine("Player 1 wins!");
                    break;
                }

                Player2.MakeMove(Board);
                if (Win(-1))
                {
                    Console.WriteLine("Player 2 wins!");
                    break;
                }

                if (MoveIsPossible() != true)
                {
                    Console.WriteLine("Tie!");
                    break;
                }
            }
        }

        private bool MoveIsPossible()
        {
            for (int x = 0; x <= 6; x++)
            {
                if (Board.Fields[x, 5] == 0)
                {
                    return true;
                }
            }
            return false;
        }

        private bool Win(int colour)
        {
            if (VertCheck(colour) || HorizCheck(colour) || SlashCheck(colour) || BackslashCheck(colour))
            {
                return true;
            }
            return false;
        }

        private bool VertCheck(int colour)
        {
            bool possibleWin;
            for (int x = 0; x <= 6; x++)
            {
                for (int start = 0; start <= 2; start++)
                {
                    possibleWin = true;
                    for (int y = 0; y <= 3; y++)
                    {
                        if (Board.Fields[x, start + y] != colour)
                        {
                            possibleWin = false;
                            break;
                        }
                    }
                    if (possibleWin == true)
                    {
                        return true;
                    }
                }
            }
            return false;
        }

        private bool HorizCheck(int colour)
        {
            bool possibleWin;
            for (int y = 0; y <= 5; y++)
            {
                for (int start = 0; start <= 3; start++)
                {
                    possibleWin = true;
                    for (int x = 0; x <= 3; x++)
                    {
                        if (Board.Fields[start + x, y] != colour)
                        {
                            possibleWin = false;
                            break;
                        }
                    }
                    if (possibleWin == true)
                    {
                        return true;
                    }
                }
            }
            return false;
        }

        private bool SlashCheck(int colour)
        {
            bool possibleWin;
            for (int x = 0; x <= 3; x++)
            {
                for (int start = 0; start <= 2; start++)
                {
                    possibleWin = true;
                    for (int y = 0; y <= 3; y++)
                    {
                        if (Board.Fields[x + y, start + y] != colour)
                        {
                            possibleWin = false;
                            break;
                        }
                    }
                    if (possibleWin == true)
                    {
                        return true;
                    }
                }
            }
            return false;
        }

        private bool BackslashCheck(int colour)
        {
            bool possibleWin;
            for (int x = 3; x <= 6; x++)
            {
                for (int start = 0; start <= 2; start++)
                {
                    possibleWin = true;
                    for (int y = 0; y <= 3; y++)
                    {
                        if (Board.Fields[x - y, start + y] != colour)
                        {
                            possibleWin = false;
                            break;
                        }
                    }
                    if (possibleWin == true)
                    {
                        return true;
                    }
                }
            }
            return false;
        }
    }
}

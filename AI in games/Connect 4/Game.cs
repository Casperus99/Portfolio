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

            while (true)
            {
                move = Player1.MakeMove(Board.Fields);
                Board.UpdateBoard(move, 'X');
                Board.PrintBoard();
                Console.ReadKey();
                Console.Clear();
                if (Win('X'))
                {
                    Console.WriteLine("Player 1 wins!");
                    break;
                }

                move = Player2.MakeMove(Board.Fields);
                Board.UpdateBoard(move, 'O');
                Board.PrintBoard();
                Console.ReadKey();
                Console.Clear();
                if (Win('O'))
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
                if (Board.Fields[x, 5] == '|')
                {
                    return true;
                }
            }
            return false;
        }

        private bool Win(char colour)
        {
            if (VertCheck(colour) || HorizCheck(colour) || SlashCheck(colour) || BackslashCheck(colour))
            {
                return true;
            }
            return false;
        }

        private bool VertCheck(char colour)
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

        private bool HorizCheck(char colour)
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

        private bool SlashCheck(char colour)
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

        private bool BackslashCheck(char colour)
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

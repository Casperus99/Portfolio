using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Connect_4
{
    abstract internal class Player
    {
        abstract public int MakeMove(Board board);
    }
}

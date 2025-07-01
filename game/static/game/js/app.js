import { Card } from "./card.js";
import { Deck } from "./deck.js";
import { Cards } from "./cards.js";
import { Player } from "./player.js";
import { Board } from "./board.js";

// const thisCard = {
//   rank: "2",
//   suite: "clubs",
//   set: "black-cards",
//   isHidden: false,
// };
//
export const App = () => {
  return {
    view: () => {
      return m(Board, { numPlayers: 3 });
    },
  };
};

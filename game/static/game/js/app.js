import { Card } from "./card.js";
import { Deck } from "./deck.js";
import { Player } from "./player.js";

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
      // bad code for debugging
      let thisDeck = new Deck();

      let player = { cards: [thisDeck.draw(), thisDeck.draw()] };

      return m(Player, player);
    },
  };
};

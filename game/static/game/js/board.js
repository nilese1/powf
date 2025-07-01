import { Player } from "./player.js";
import { Cards } from "./cards.js";
import { Deck } from "./deck.js";

export const Board = {
  oninit: (vnode) => {},
  view: (vnode) => {
    const numPlayers = vnode.attrs.numPlayers;

    // bad code for debugging
    let thisDeck = new Deck();

    let players = [];

    for (let i = 0; i < numPlayers; i++) {
      let cards = {
        cards: [thisDeck.draw(), thisDeck.draw()],
      };

      let daCards = m(Cards, cards);

      let player = {
        cards: daCards,
      };

      players.push(player);
    }

    return m(
      ".board",
      {},
      players.map((player) => {
        return m(Player, player);
      }),
    );
  },
};

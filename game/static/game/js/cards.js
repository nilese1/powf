import { Card } from "./card.js";

// The distance in angle for the card fan when viewing it by default
// and when the user is hovering over the fan
const viewAngleMagnitude = 15;
const hoverAngleMagnitude = 25;

// Calculates the angle needed to fan the cards in a pretty way
function calculateCardViewAngle(index, maxCards, viewAngleMagnitude) {
  console.assert(index >= 0, `Card view index (${index}) must be at least 0`);
  console.assert(
    index <= maxCards,
    `Card view index ${index} must be less than ${maxCards}`,
  );

  // amount of rotation for the "fan" to be centered
  // negative so the rotation is left
  const centerOffset = -1 * ((viewAngleMagnitude * maxCards) / 4);

  return centerOffset + index * viewAngleMagnitude;
}

export const Cards = {
  oninit: (vnode) => {
    let attributes = vnode.attrs;

    vnode.state.cards = attributes.cards;
    vnode.state.angleBetweenCards = viewAngleMagnitude;
  },
  // card fanning not working :(
  fanCards: (vnode) => {
    vnode.state.angleBetweenCards = hoverAngleMagnitude;
  },
  collapseCards: (vnode) => {
    vnode.state.angleBetweenCards = viewAngleMagnitude;
  },
  view: (vnode) => {
    return m(
      ".cards",
      {
        onmouseover: () => {
          Cards.fanCards(vnode);
        },
        onmouseout: () => {
          Cards.collapseCards(vnode);
        },
      },
      vnode.state.cards.map((card, index) => {
        let maxCards = vnode.state.cards.length;

        card.attrs.rotation = calculateCardViewAngle(
          index,
          maxCards,
          vnode.state.angleBetweenCards,
        );

        return m(Card, card.attrs);
      }),
    );
  },
};

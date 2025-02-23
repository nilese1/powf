import { Card } from "./card.js";

// Calculates the angle needed to fan the cards in a pretty way
function calculateCardViewAngle(index, maxCards) {
  console.assert(index >= 0, `Card view index (${index}) must be at least 0`);
  console.assert(
    index <= maxCards,
    `Card view index ${index} must be less than ${maxCards}`,
  );

  // The angle between each card
  const viewAngleOffset = 30;
  // amount of rotation for the "fan" to be centered
  // negative so the rotation is left
  const centerOffset = -1 * (viewAngleMagnitude * (maxCards / 2));

  return centerOffset + index * viewAngleOffset;
}

export const Player = {
  oninit: (vnode) => {
    let attributes = vnode.attrs;

    vnode.state.cards = attributes.cards;
  },
  view: (vnode) => {
    return m(
      ".player",
      vnode.state.cards.map((card) => {
        return m(Card, card);
      }),
    );
  },
};

import { Card } from "./card.js";

const thisCard = {
  rank: "2",
  suite: "clubs",
  set: "black-cards",
  isHidden: false,
};

export const App = () => {
  return {
    view: () => {
      return m(Card, thisCard);
    },
  };
};

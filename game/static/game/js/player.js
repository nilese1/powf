import { Cards } from "./cards.js";

export const Player = {
  oninit: (vnode) => {
    let attributes = vnode.attrs;

    vnode.state.cards = attributes.cards;

    // optional attributes
    vnode.state.rotation = attributes.rotation ? attributes.rotation : 0;
  },
  view: (vnode) => {
    return m(".player", {}, [m(Cards, vnode.state.cards.attrs)]);
  },
};

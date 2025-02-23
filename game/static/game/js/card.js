export const validCardRanks = [
  "ace",
  "2",
  "3",
  "4",
  "5",
  "6",
  "7",
  "8",
  "9",
  "10",
  "jack",
  "queen",
  "king",
];

export const validCardSuites = ["hearts", "diamonds", "clubs", "spades"];

export const validCardSets = ["black-cards"];

function assertAttributes(attributes) {
  console.assert(
    validCardSuites.includes(attributes.suite),
    `${attributes.suite} is not a valid suite`,
  );
  console.assert(
    validCardRanks.includes(attributes.rank),
    `${attributes.rank} is not a valid rank`,
  );
  console.assert(
    validCardSets.includes(attributes.set),
    `${attributes.set} is not a valid card set`,
  );
}

export const Card = {
  oninit: (vnode) => {
    let attributes = vnode.attrs;
    assertAttributes(attributes);

    vnode.state.rank = attributes.rank;
    vnode.state.suite = attributes.suite;
    vnode.state.set = attributes.set;
    vnode.state.isHidden = attributes.isHidden;
  },
  flipCard: (vnode) => {
    vnode.state.isHidden = !vnode.state.isHidden;
  },
  view: (vnode) => {
    let imagePath;
    let altText;

    if (vnode.state.isHidden) {
      // shows backside when hidden
      imagePath = `/static/game/images/${vnode.state.set}/card-backside.svg`;
      altText = `The backside of a playing card`;
    } else {
      imagePath = `/static/game/images/${vnode.state.set}/card-${vnode.state.rank}-${vnode.state.suite}.svg`;
      altText = `A ${vnode.state.rank} of ${vnode.state.suite} playing card`;
    }

    return m(
      ".card",
      {
        // Debug
        onclick: () => {
          Card.flipCard(vnode);
        },
      },
      [
        m("img", {
          src: imagePath,
          alt: altText,
          style: "width: 100%; height: 100%;",
        }),
      ],
    );
  },
};

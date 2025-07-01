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

export const validCardSuites = ["heart", "diamond", "club", "spade"];

export const validCardSets = ["standard"];

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

// gets image path given a valid rank suite and set
// will probably need refactoring if all sets don't have the same naming rules
function getCardImagePath(rank, suite, set) {
  const specialRanks = {
    king: 13,
    queen: 12,
    jack: 11,
  };

  // holy shit I should just rename the cards this is getting ridiculous
  if (rank == "ace") rank = "1";

  const cardsPath = `/static/game/images/${set}`;

  // clean data to fit standard set naming convention (just check the damn files)
  let cleanedSuite = suite.toUpperCase();
  let cleanedRank = rank.toUpperCase();

  if (rank in specialRanks) {
    const faceNumber = specialRanks[rank];
    return cardsPath + `/${cleanedSuite}-${faceNumber}-${cleanedRank}.svg`;
  }

  return cardsPath + `/${cleanedSuite}-${cleanedRank}.svg`;
}

export const Card = {
  oninit: (vnode) => {
    let attributes = vnode.attrs;
    assertAttributes(attributes);

    vnode.state.rank = attributes.rank;
    vnode.state.suite = attributes.suite;
    vnode.state.set = attributes.set;
    vnode.state.isHidden = attributes.isHidden;

    // optional attributes
    vnode.state.rotation = attributes.rotation ? attributes.rotation : 0;
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
      imagePath = getCardImagePath(
        vnode.state.rank,
        vnode.state.suite,
        vnode.state.set,
      );

      altText = `A ${vnode.state.rank} of ${vnode.state.suite} playing card`;
    }

    console.log(vnode);

    return m(
      ".card",
      {
        // Debug
        onclick: () => {
          Card.flipCard(vnode);
        },
        style: `rotate: ${vnode.state.rotation}deg; transform-origin: center 120%`,
      },
      [
        m("img", {
          src: imagePath,
          alt: altText,
          style: `width: 100%; height: 100%;`,
        }),
      ],
    );
  },
};

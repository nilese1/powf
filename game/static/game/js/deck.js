import { Card, validCardRanks, validCardSuites } from "./card.js";

export class Deck {
  constructor(numberOfDecks = 1, set = "black-cards") {
    this.cards = [];
    this.set = set;

    for (let i = 0; i < numberOfDecks; i++) {
      this.createDeck();
    }

    this.shuffle();
  }

  createDeck() {
    for (let rank of validCardRanks) {
      for (let suite of validCardSuites) {
        this.addCard(rank, suite, this.set, false);
      }
    }
  }

  shuffle() {
    for (let i = this.cards.length - 1; i >= 0; i--) {
      let randomIndex = Math.floor(Math.random() * i);

      let temp = this.cards[i];
      this.cards[i] = this.cards[randomIndex];
      this.cards[randomIndex] = temp;
    }
  }

  // For the purposes of add and draw, the deck functions like a stack
  // using FIFO
  addCard(rank, suite, set, isHidden) {
    let cardToAdd = {
      rank: rank,
      suite: suite,
      set: set,
      isHidden: isHidden,
    };

    this.cards.push(m(Card, cardToAdd));
  }

  draw() {
    return this.cards.pop();
  }
}

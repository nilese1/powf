import { App } from "./app.js";
import { Deck } from "./deck.js";

console.log(new Deck());

const mountNode = document.querySelector("#app");
m.mount(mountNode, App);

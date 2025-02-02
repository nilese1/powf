const lobbyID = JSON.parse(document.getElementById("lobby-id").textContent);
const socket = new WebSocket(
  `ws://${window.location.host}/ws/lobby/${lobbyID}/`,
);

socket.onmessage = function (event) {
  const data = JSON.parse(event.data);

  console.log(data);

  // gotta reload the table each time because tables are static
  // I'm assuming I'll get sick of this later and use a framework making all of this shit redundant
  let innerHTML = `<table>
                <tr>
                    <th>Username</th>
                    <th>Chips</th>
                    <th>Is Host</th>
                </tr>`;

  data.forEach((player) => {
    innerHTML += `<tr>
                    <td>${player.username}</td>
                    <td>${player.chips}</td>
                    <td>${player.is_host}</td>
                  </tr>`;
  });
  innerHTML += `</table>`;

  let div = document.getElementById("user-table");
  console.log(div);
  div.innerHTML = innerHTML;
};

socket.onclose = function () {
  console.log("WebSocket closed unexpectedly");
};

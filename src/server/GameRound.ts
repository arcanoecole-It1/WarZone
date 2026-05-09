import { Players, Workspace } from "@rbxts/services";
import { loadMap, unloadMap } from "./MapLoader";
import { spawnTeam } from "./SpawnManager";
import { sendKill, openMatch, closeMatch } from "./ApiService";

const ROUND_DURATION = 300; // 5 minutes

function onPlayerKill(
	player: Player,
	callback: (killer: Player, victim: Player) => void,
): RBXScriptConnection {
	return player.CharacterAdded.Connect((char) => {
		const humanoid = char.WaitForChild("Humanoid") as Humanoid;
		humanoid.Died.Connect(() => {
			const tag = humanoid.FindFirstChild("creator") as ObjectValue | undefined;
			if (tag && tag.Value) {
				const killer = tag.Value as Player;
				callback(killer, player);
			}
		});
	});
}

export function startRound(redTeam: Player[], blueTeam: Player[]): void {
	// 1. Ouvre la partie dans l'API
  print("1. openMatch...");
	const matchId = openMatch("Map_Labyrinth");

	// 2. Charge la map
  print("2. loadMap...");
	loadMap("Map_Labyrinth");
  print("3. waiting...")
	task.wait(1);

	// 3. Spawn les équipes
  print("4. spawnTeam...");
	spawnTeam(redTeam, "Red");
	spawnTeam(blueTeam, "Blue");

	// 4. Compteur de kills par équipe
	const scores = { Red: 0, Blue: 0 };

	// 5. Connecte la détection des kills pour chaque joueur
	const killConnections: RBXScriptConnection[] = [];

	const allPlayers = [...redTeam, ...blueTeam];
	allPlayers.forEach((player) => {
		const conn = onPlayerKill(player, (killer, victim) => {
			const killerTeam = redTeam.includes(killer) ? "Red" : "Blue";
			scores[killerTeam] += 1;

			// Détermine l'arme utilisée
			const tool = killer.Character?.FindFirstChildOfClass("Tool");
			const weaponName = tool ? tool.Name : "Unknown";

			// Envoie le kill à l'API
			sendKill(matchId, killer, victim, weaponName);
		});
		killConnections.push(conn);
	});

	// 6. Timer du round
	let timeLeft = ROUND_DURATION;
	while (timeLeft > 0) {
		task.wait(1);
		timeLeft -= 1;
	}

	// 7. Déconnecte tous les événements de kill
	killConnections.forEach((c) => c.Disconnect());

	// 8. Détermine le gagnant
	const winner = scores.Red >= scores.Blue ? "Red" : "Blue";

	// 9. Ferme la partie dans l'API et décharge la map
	closeMatch(matchId, winner);
	unloadMap();

	print(`Round terminé ! Gagnant : ${winner}`);
}
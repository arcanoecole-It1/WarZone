import { HttpService } from "@rbxts/services";

// URL de ton backend FastAPI
// En local pour les tests Studio, en production remplace par ton URL publique
const BASE_URL = "http://127.0.0.1:8000";

// pcall = "protected call" en Lua/roblox-ts
// Si le code à l'intérieur plante, pcall attrape l'erreur
// et le reste du jeu continue de tourner
// Retourne [true, résultat] si succès, [false, erreur] si échec

// ─────────────────────────────────────────
// Ouvre une partie dans la BDD
// Appelé au début de chaque round par GameRound.ts
// Retourne l'UUID de la partie créée
// ─────────────────────────────────────────
export function openMatch(mapName: string): string {
	let matchId = "offline-match"; // valeur par défaut si l'API est inaccessible

	const [success] = pcall(() => {
		const response = HttpService.RequestAsync({
			Url: `${BASE_URL}/matches/`,
			Method: "POST",
			Headers: { "Content-Type": "application/json" },
			Body: HttpService.JSONEncode({
				map_name: mapName,
				started_at: os.time(),
			}),
		});

		if (response.Success) {
			const data = HttpService.JSONDecode(response.Body) as { id: string };
			matchId = data.id;
			print(`Match créé : ${matchId}`);
		} else {
			warn(`Erreur HTTP openMatch : ${response.StatusCode}`);
		}
	});

	if (!success) {
		print("API non disponible, mode offline - openMatch");
	}

	return matchId;
}

// ─────────────────────────────────────────
// Ferme la partie avec le gagnant
// Appelé à la fin du round par GameRound.ts
// ─────────────────────────────────────────
export function closeMatch(matchId: string, winner: string): void {
	// Si on est en mode offline, pas la peine d'appeler l'API
	if (matchId === "offline-match") {
		print("Mode offline - closeMatch ignoré");
		return;
	}

	const [success] = pcall(() => {
		const response = HttpService.RequestAsync({
			Url: `${BASE_URL}/matches/${matchId}/close`,
			Method: "PATCH",
			Headers: { "Content-Type": "application/json" },
			Body: HttpService.JSONEncode({
				winner_team: winner,
				ended_at: os.time(),
			}),
		});

		if (response.Success) {
			print(`Match fermé, gagnant : ${winner}`);
		} else {
			warn(`Erreur HTTP closeMatch : ${response.StatusCode}`);
		}
	});

	if (!success) {
		print("API non disponible, mode offline - closeMatch");
	}
}

// ─────────────────────────────────────────
// Enregistre un kill en BDD
// Appelé à chaque kill pendant le round
// Met à jour les stats KD et le grade automatiquement côté FastAPI
// ─────────────────────────────────────────
export function sendKill(
	matchId: string,
	killer: Player,
	victim: Player,
	weapon: string,
): void {
	if (matchId === "offline-match") {
		print(`Mode offline - kill ignoré : ${killer.Name} → ${victim.Name}`);
		return;
	}

	const [success] = pcall(() => {
		const response = HttpService.RequestAsync({
			Url: `${BASE_URL}/kills/`,
			Method: "POST",
			Headers: { "Content-Type": "application/json" },
			Body: HttpService.JSONEncode({
				killer_id: tostring(killer.UserId),
				victim_id: tostring(victim.UserId),
				match_id: matchId,
				weapon: weapon,
				timestamp: os.time(),
			}),
		});

		if (response.Success) {
			print(`Kill enregistré : ${killer.Name} → ${victim.Name} (${weapon})`);
		} else {
			warn(`Erreur HTTP sendKill : ${response.StatusCode}`);
		}
	});

	if (!success) {
		print("API non disponible, mode offline - sendKill");
	}
}

// ─────────────────────────────────────────
// Enregistre un joueur en BDD
// Appelé quand un joueur rejoint le jeu
// Si le joueur existe déjà, le backend retourne juste le joueur existant
// ─────────────────────────────────────────
export function registerPlayer(player: Player): void {
	const [success] = pcall(() => {
		const response = HttpService.RequestAsync({
			Url: `${BASE_URL}/players/`,
			Method: "POST",
			Headers: { "Content-Type": "application/json" },
			Body: HttpService.JSONEncode({
				roblox_id: tostring(player.UserId),
				username: player.Name,
			}),
		});

		if (response.Success) {
			print(`Joueur enregistré : ${player.Name}`);
		} else {
			warn(`Erreur HTTP registerPlayer : ${response.StatusCode}`);
		}
	});

	if (!success) {
		print(`API non disponible, mode offline - ${player.Name} non enregistré`);
	}
}
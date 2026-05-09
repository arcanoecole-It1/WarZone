import { Players, ReplicatedStorage } from "@rbxts/services";
import { startRound } from "./GameRound";
import { setupRifle } from "./Weapons/Rifle";
import { setupSword } from "./Weapons/Sword";
import { registerPlayer } from "./ApiService";

const MIN_PLAYERS = 1;

function divideTeams(players: Player[]): [Player[], Player[]] {
    const shuffled = [...players];
    for (let i = shuffled.size() - 1; i > 0; i--) {
        const j = math.floor(math.random() * (i + 1));
        const temp = shuffled[i];
        shuffled[i] = shuffled[j];
        shuffled[j] = temp;
    }

    const mid = math.floor(shuffled.size() / 2);
    const redTeam: Player[] = [];
    const blueTeam: Player[] = [];

    for (let i = 0; i < mid; i++) redTeam.push(shuffled[i]);
    for (let i = mid; i < shuffled.size(); i++) blueTeam.push(shuffled[i]);

    return [redTeam, blueTeam];
}

function giveWeapons(players: Player[]): void {
    const weapons = ReplicatedStorage.WaitForChild("Weapons");
    const rifleTemplate = weapons.WaitForChild("Rifle") as Tool;
    const swordTemplate = weapons.WaitForChild("Sword") as Tool;

    players.forEach((player) => {
        const backpack = player.FindFirstChildOfClass("Backpack");
        if (!backpack) return;

        const rifle = rifleTemplate.Clone();
        const sword = swordTemplate.Clone();
        rifle.Parent = backpack;
        sword.Parent = backpack;

        setupRifle(rifle, player);
        setupSword(sword, player);
    });
}

let roundStarted = false; // ← ajoute cette variable

function tryStartRound(): void {
    if (roundStarted) return; // ← bloque le deuxième appel
    
    const allPlayers = Players.GetPlayers();
    if (allPlayers.size() < MIN_PLAYERS) return;

    roundStarted = true; // ← marque comme démarré
    
    allPlayers.forEach((p) => registerPlayer(p));
    const [redTeam, blueTeam] = divideTeams(allPlayers);
    giveWeapons([...redTeam, ...blueTeam]);
    startRound(redTeam, blueTeam);
}

// Gère les joueurs déjà connectés au démarrage du script
// (cas fréquent en playtest Studio)
print("main.server chargé !");
task.delay(2, () => {    
    print("task.delay déclenché !");
    const allPlayers = Players.GetPlayers();
    print(`Nombre de joueurs : ${allPlayers.size()}`);
    print("Script serveur prêt !");
    tryStartRound();
});

// Gère les nouveaux joueurs qui rejoignent après
Players.PlayerAdded.Connect((player) => {
    print(`Joueur ajouté : ${player.Name}`);
    registerPlayer(player);
    task.delay(1, () => tryStartRound());
});
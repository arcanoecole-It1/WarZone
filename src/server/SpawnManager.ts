import { Workspace } from "@rbxts/services";

function getMap(): Model {
    for (let i = 0; i < 10; i++) {
        const map = Workspace.FindFirstChild("CurrentMap") as Model;
        if (map) {
            print("Map trouvée !");
            return map;
        }
        print(`Map pas encore là, essai ${i + 1}/10...`);
        task.wait(0.5);
    }
    throw "CurrentMap introuvable après 10 essais";
}

export function spawnTeam(players: Player[], team: "Red" | "Blue"): void {
    const currentMap = getMap();
    
    const spawns = currentMap.FindFirstChild("Spawns");
    if (!spawns) {
        print("Dossier Spawns introuvable !");
        return;
    }

    const spawnName = team === "Red" ? "SpawnRed" : "SpawnBlue";
    const spawnPart = spawns.FindFirstChild(spawnName) as Part;
    if (!spawnPart) {
        print(`${spawnName} introuvable !`);
        return;
    }

    print(`Spawn ${team} trouvé, téléportation...`);
    players.forEach((player, index) => {
        const char = player.Character;
        if (!char) return;

        const root = char.FindFirstChild("HumanoidRootPart") as Part;
        if (!root) return;

        root.CFrame = new CFrame(
            spawnPart.Position.X + index * 4,
            spawnPart.Position.Y + 3,
            spawnPart.Position.Z,
        );
    });
}
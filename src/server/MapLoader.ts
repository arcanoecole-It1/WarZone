import { ReplicatedStorage, Workspace } from "@rbxts/services";

print("MapLoader chargé !");
const mapsFolder = ReplicatedStorage.WaitForChild("Maps");
print("Dossier Maps trouvé !");

export function loadMap(mapName: string): Model {
    print(`loadMap appelé avec : ${mapName}`);

    const old = Workspace.FindFirstChild("CurrentMap");
    if (old) old.Destroy();

    print(`Contenu de Maps :`);
    mapsFolder.GetChildren().forEach((child) => {
        print(`  - ${child.Name}`);
    });

    const mapTemplate = mapsFolder.FindFirstChild(mapName) as Model;
    if (!mapTemplate) {
        print(`ERREUR : ${mapName} introuvable dans Maps !`);
        return undefined!;
    }

    print(`Template trouvé ! Clonage...`);
    const map = mapTemplate.Clone();
    map.Name = "CurrentMap";
    map.Parent = Workspace;
    print(`CurrentMap créé dans Workspace !`);

    return map;
}

export function unloadMap(): void {
    const map = Workspace.FindFirstChild("CurrentMap");
    if (map) map.Destroy();
}
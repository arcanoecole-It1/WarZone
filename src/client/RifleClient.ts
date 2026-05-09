// src/client/weapons/RifleClient.ts
import { Players, UserInputService, Workspace } from "@rbxts/services";

const player = Players.LocalPlayer;
const mouse = player.GetMouse();

player.CharacterAdded.Connect((char) => {
    char.ChildAdded.Connect((child) => {
        if (child.Name === "Rifle" && child.IsA("Tool")) {
            const tool = child as Tool;
            const fireEvent = tool.WaitForChild("FireEvent") as RemoteEvent;

            tool.Activated.Connect(() => {
                // Envoie la position visée au serveur
                fireEvent.FireServer(mouse.Hit.Position);
            });
        }
    });
});
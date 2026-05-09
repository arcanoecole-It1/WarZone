import { Players, Workspace } from "@rbxts/services";

const RIFLE_DAMAGE = 35;
const RIFLE_RANGE  = 500;

export function setupRifle(tool: Tool, player: Player): void {
  const fireEvent = tool.FindFirstChild("FireEvent") as RemoteEvent;

  fireEvent.OnServerEvent.Connect((shooter, targetPos) => {
    const char   = shooter.Character;
    const barrel = tool.FindFirstChild("Barrel") as Part;
    if (!char || !barrel) return;

    // Raycast depuis le canon vers la cible
    const direction = (targetPos as Vector3)
      .sub(barrel.Position).Unit.mul(RIFLE_RANGE);

    const result = Workspace.Raycast(
      barrel.Position,
      direction,
      new RaycastParams()
    );

    if (!result) return;

    // Vérifie si on a touché un joueur
    const hit = result.Instance;
    const victimChar = hit.Parent as Model;
    const humanoid = victimChar?.FindFirstChild("Humanoid") as Humanoid;
    if (!humanoid || humanoid === char.FindFirstChild("Humanoid")) return;

    // Tag le killer pour que GameRound puisse l'identifier
    const tag = new Instance("ObjectValue");
    tag.Name  = "creator";
    tag.Value = shooter;
    tag.Parent = humanoid;

    humanoid.TakeDamage(RIFLE_DAMAGE);
  });
}
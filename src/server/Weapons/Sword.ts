import { Workspace } from "@rbxts/services";
const SWORD_DAMAGE = 75;

export function setupSword(tool: Tool, player: Player): void {
  const handle = tool.FindFirstChild("Handle") as Part;

  tool.Activated.Connect(() => {
    const char = player.Character;
    if (!char) return;

    // Zone de touche autour du joueur (melee range)
    const root = char.FindFirstChild("HumanoidRootPart") as Part;
    const hits = Workspace.GetPartBoundsInBox(
      root.CFrame,
      new Vector3(6, 6, 6)
    );

    hits.forEach((part) => {
      const victimChar = part.Parent as Model;
      const humanoid = victimChar?.FindFirstChild("Humanoid") as Humanoid;
      if (!humanoid || victimChar === char) return;

      const tag = new Instance("ObjectValue");
      tag.Name  = "creator";
      tag.Value = player;
      tag.Parent = humanoid;
      humanoid.TakeDamage(SWORD_DAMAGE);
    });
  });
}
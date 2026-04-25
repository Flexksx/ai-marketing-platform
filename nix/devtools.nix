{
  pkgs,
}:
{
  packages = with pkgs; [
    oxker
  ];
  shellHook="";
}

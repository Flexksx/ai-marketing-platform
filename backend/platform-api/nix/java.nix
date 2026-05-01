{ pkgs }:
{
  packages = with pkgs; [
    java-language-server
    jdk25
    gradle
  ];

  shellHook = ''
    export JAVA_HOME="${pkgs.jdk25}"
  '';
}
